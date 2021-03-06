#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors:  İsmail Dönmez <ismail@uludag.org.tr>
# Resistence is futile, turn on god damn Unicode!

# System
import sys
import math
import posix

# PyQt/PyKDE
from qt import *
from kdecore import *
from kdeui import *
from kio import *
import kdedesigner

# Local imports
from Enums import *
from Formatter import *
import HelpDialog
import MainWindow
import Progress
import Preferences
import ThreadRunner
import PisiUi
import Success
import UpdateWizardDialog
import FastUpdatesDialog
import CustomUpdatesDialog

# Pisi Imports
import pisi.ui
import pisi.config
import pisi.packagedb
import pisi.installdb
import pisi.repodb
import pisi.context

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

description = I18N_NOOP("GUI for PiSi package manager")
version = "1.0.3"

def AboutData():
    global version,description
    
    about_data = KAboutData("pisi_kga", "PiSi KGA", version, \
                            description, KAboutData.License_GPL,
                            "(C) 2005,2006 UEKAE/TÜBİTAK", None, None, "ismail@uludag.org.tr")
    
    about_data.addAuthor("İsmail Dönmez", I18N_NOOP("Author"), "ismail@uludag.org.tr")
    about_data.addAuthor("Görkem Çetin",I18N_NOOP("GUI Design & Usability"), "gorkem@uludag.org.tr")
    about_data.addAuthor("Eray Özkural", I18N_NOOP("Search, Component/Category"), "eray@uludag.org.tr")
    about_data.addCredit("Gürer Özen", I18N_NOOP("Python coding help"), None)
    about_data.addCredit("Barış Metin",  I18N_NOOP("Helping with PiSi API"), None)
    about_data.addCredit("PiSi Authors", I18N_NOOP("Authors of PiSi API"), "pisi@uludag.org.tr")
    about_data.addCredit("Simon Edwards", I18N_NOOP("Author of PyKDEeXtensions"),"simon@simonzone.com")
    return about_data

def loadIcon(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIcon(name, group)

class MainApplicationWidget(MainWindow.MainWindow):
    def __init__(self, parent=None):
        MainWindow.MainWindow.__init__(self, parent, "PiSi KGA")

        self.progressDialog = Progress.Progress(self)
        self.packagesOrder = []
        self.selectedItems = []
        self.currentOperation = None
        self.currentFile = None
        self.currentRepo = None
        self.totalAppCount = 1
        self.currentAppIndex = 1
        self.totalSelectedSize = 0
        
        # Create a ThreadRunner and init the database
        self.command = ThreadRunner.PisiThread(self)
        self.command.initDatabase()

        # Check for empty repo.
        self.initialCheck()

    def initialCheck(self):
        if not nonPrivMode:
            try:
                repo = pisi.context.repodb.list()[0]
                pkg_db = pisi.packagedb.get_db(repo)
                self.packageList = pkg_db.list_packages()
            except:
                confirm = KMessageBox.questionYesNo(self,i18n("Looks like PiSi repository database is empty\nDo you want to update repository now?"),i18n("PiSi Question"))
                if confirm == KMessageBox.Yes:
                    self.command.addRepo('pardus', 'http://paketler.uludag.org.tr/pardus-1.0/pisi-index.xml')
                    self.command.updateRepo('pardus')
                else:
                    KMessageBox.information(self,i18n("You will not be able to install new programs or update old ones until you update repository."))

    def customEvent(self, event):
        
        eventType = event.type()
        eventData = event.data()

        print 'Event Type:',eventType,'Event Data:',eventData
        if eventType == CustomEvent.InitError:
            KMessageBox.information(self,i18n("Pisi could not be started! Please make sure no other pisi process is running."),i18n("Pisi Error"))
            sys.exit(1)
        elif eventType == CustomEvent.Finished:
            self.finished()
        elif eventType == CustomEvent.PisiWarning:
            pass
        elif eventType == CustomEvent.PisiError:
            self.showErrorMessage(eventData)
        elif eventType == CustomEvent.AskConfirmation:
            self.showConfirmationMessage(eventData)
        elif eventType == CustomEvent.UpdateProgress:
            self.currentFile = eventData["filename"]
            percent = eventData["percent"]
            rate = round(eventData["rate"],1)
            symbol = eventData["symbol"]
            downloaded = eventData["downloaded_size"]
            totalsize = eventData["total_size"]
            self.updateProgressBar(self.currentFile, percent, rate, symbol, downloaded, totalsize)
        elif eventType == CustomEvent.UpdateListing:
            self.updateListing()
        elif eventType == CustomEvent.PisiNotify:
            if isinstance(eventData,QString):
                if eventData == i18n("removing"):
                    self.currentFile = self.packagesOrder[self.currentAppIndex-1]
                    self.progressDialog.progressBar.setProgress((float(self.currentAppIndex)/float(self.totalApps))*100)
                elif eventData == i18n("installing"):
                    if not self.progressDialog.progressBar.progress():
                        self.progressDialog.progressBar.setProgress((float(self.currentAppIndex)/float(self.totalApps))*100)
                self.currentOperation = eventData
                self.updateProgressText()
            elif eventData in ["installed","removed","upgraded"]:
                self.currentAppIndex += 1
            elif isinstance(eventData,list):
                self.packagesOrder = eventData
                self.totalApps = len(self.packagesOrder)
        elif eventType == CustomEvent.RepositoryUpdate:
            self.currentRepo = eventData
            self.progressDialog.show()
        else:
            print 'Unhandled event:',eventType,'with data',eventData
    
    def showConfirmationMessage(self, question):
        answer = KMessageBox.questionYesNo(self,question,i18n("PiSi Question"))
        event = QCustomEvent(CustomEvent.UserConfirmed)
        if answer == KMessageBox.Yes:
            event.setData(True)
        else:
            event.setData(False)
        QThread.postEvent(self.command.ui,event)

    def showErrorMessage(self, message):
        KMessageBox.error(self,message,i18n("PiSi Error"))
        self.finished()
            
    def finished(self):
        self.selectedItems = []
        self.currentAppIndex = 1
        self.updateListing()
        self.progressDialog.closeForced()
        self.resetProgressBar()
        
    def resetProgressBar(self):
        self.progressDialog.progressBar.setProgress(0)
        self.progressDialog.setLabelText(i18n("<b>Preparing PiSi...</b>"))
        self.progressDialog.speedLabel.setText(i18n('<b>Speed:</b> Unknown'))
        self.progressDialog.sizeLabel.setText(i18n('<b>Downloaded/Total:</b> Unknown'))

    def updateProgressBar(self, filename, length, rate, symbol,downloaded_size,total_size):
        self.updateProgressText()
        self.progressDialog.speedLabel.setText(i18n('<b>Speed:</b> %1 %2').arg(rate).arg(symbol))
        
        downloadedText = FormatNumber(downloaded_size)
        totalText = FormatNumber(total_size)

        self.progressDialog.sizeLabel.setText(i18n('<b>Downloaded/Total:</b> %1/%2').arg(downloadedText).arg(totalText))
        self.progressDialog.progressBar.setProgress((float(downloaded_size)/float(total_size))*100)

    def updateProgressText(self):
        if self.currentFile:
            if self.currentFile.endswith(".xml"):
                self.currentOperation = i18n("updating repository")
                self.currentFile = self.currentRepo
            self.progressDialog.setLabelText(i18n('Now %1 <b>%2</b> (%3 of %4)')
                                             .arg(self.currentOperation).arg(self.currentFile).arg(self.currentAppIndex).arg(self.totalAppCount))
        
    def updateDetails(self,selection):

        icon =  pisi.packagedb.get_package(selection.text(0)).icon
        if icon:
            self.iconLabel.setPixmap(loadIcon(icon))
        else:
            self.iconLabel.setPixmap(loadIcon("package"))
                  
        installed = pisi.packagedb.inst_packagedb.has_package(selection.text(0))
        if installed:
            self.package = pisi.packagedb.inst_packagedb.get_package(selection.text(0))
        else:
            self.package = pisi.packagedb.get_package(selection.text(0))
            
        self.progNameLabel.setText(QString("<qt><h1>"+self.package.name+"</h1></qt>"))

        if self.package.summary != self.package.description:
            self.infoLabel.setText(u"%s<br><br>%s" % (self.package.summary, self.package.description) )
        else:
            self.infoLabel.setText(u"%s" % self.package.summary)
        
        size = self.package.installedSize
        size_string = FormatNumber(size)

        self.moreInfoLabelDetails.setText(i18n("Program Version :")+QString(" <b>")+QString(self.package.version)+QString("</b><br>")+i18n("Program Size :")+QString("<b> ")+QString(size_string)+QString("</b>"))
            
    def updateButtons(self, listViewItem=None):

        if nonPrivMode:
            self.installOrRemoveButton.setEnabled(False)
            return
        elif not listViewItem:
            return

        if listViewItem.type() == QCheckListItem.CheckBoxController:
            item = listViewItem.firstChild()
            while item:
                self.updateButtons(item)
                item = item.nextSibling()
            
        try:
            text = str(listViewItem.text(0))

            if pisi.packagedb.inst_packagedb.has_package(text):
                self.package = pisi.packagedb.inst_packagedb.get_package(text)
            else:
                self.package = pisi.packagedb.get_package(text)
            
            if text in self.selectedItems:
                if not listViewItem.isOn():
                    self.selectedItems.remove(text)
                    self.totalSelectedSize -= self.package.installedSize
                else:
                    pass
            elif listViewItem.isOn():
                self.selectedItems.append(text)
                self.totalSelectedSize += self.package.installedSize
                
            if len(self.selectedItems):
                self.installOrRemoveButton.setEnabled(True)
            else:
                self.installOrRemoveButton.setEnabled(False)
            
            self.updateSelectionInfo()
        except:
            pass

    def updateSelectionInfo(self):
        if len(self.selectedItems):
            self.selectionInfo.setText(i18n('Selected %1 packages, total size %2').arg(len(self.selectedItems)).arg(FormatNumber(self.totalSelectedSize)))
        else:
            self.selectionInfo.setText(i18n("No package selected"))
        
    
    def updatePackages(self, list):
   
        self.listView.clear()
        self.listView.setUpdatesEnabled(False)
    
        list = filter(lambda x: x in self.shownPackages, list)
    
        self.packageList = list

        self.updateButtons()
        self.updateSelectionInfo()

        # list components
        componentNames = pisi.context.componentdb.list_components()
        componentNames.sort() # necessary
        components = [pisi.context.componentdb.get_component(x) for x in componentNames]
        componentDict = {}
        for component in components:
            if not nonPrivMode:
                componentItem = QCheckListItem(self.listView,"",QCheckListItem.CheckBoxController)
            else:
                componentItem = QListViewItem(self.listView,None)
            componentItem.setOpen(True)
            name = u'%s' % component.localName
            componentItem.setText(0, name)
            componentItem.setPixmap(0,loadIcon('package_system', KIcon.Small))
            componentItem.setSelectable(False)
            componentDict[component.name] = (component, componentItem)

        def isApp(package):
            return ('app:gui' in package.isA or 
                    'app:console' in package.isA or
                    'plugin' in package.isA)
            
        list.sort()
        self.packages = [] #FIXME: caching the entire package database somehow does not look right :)
        packageItems = []
        for pack in list:
            parent = self.listView
            # find component
            for compname, (component, componentItem) in componentDict.items():
                if pack in component.packages:
                    parent = componentItem
                    break
            package = pisi.packagedb.get_package(pack)
            self.packages.append(package)

            if self.getShowOnlyPrograms():
                if not isApp(package):
                    continue   # do not show if not an app

            if not nonPrivMode:
                item = QCheckListItem(parent,pack,QCheckListItem.CheckBox)
                if item.text(0) in self.selectedItems:
                    item.setOn(True)
            else:
                item = QListViewItem(parent,pack)
            item.setText(1,package.version)
            packageItems.append(item)
            
        del componentDict    # not used any more
        
        # erase empty components
            
        # Select first item in the list
        try:
            compIt = self.listView.firstChild()
            while compIt:
                if compIt.firstChild():
                    self.listView.setSelected(compIt.firstChild(),True)
                    break
                compIt = compIt.nextSibling()
        except:
            pass

        compIt = self.listView.firstChild()
        while compIt:
            compItNext = compIt.nextSibling()
            if not compIt.firstChild():
                compIt.setVisible(False)
            compIt = compItNext

        self.listView.setUpdatesEnabled(True)

            
    def updateListing(self):
    
        # Check if updateSystemButton should be enabled
        if len(self.command.listUpgradable()) > 0:
            self.updateSystemButton.setEnabled(not nonPrivMode)
        else:
            self.updateSystemButton.setEnabled(False)
    
        index = self.selectionGroup.selectedId()
    
        if index == 2 :
            # Show only installed apps
            shownPackages = self.command.listPackages()
            self.installOrRemoveButton.setText(i18n("Remove package(s)"))

        elif index == 1:
            # Only upgrades
            shownPackages = self.command.listUpgradable()
            self.installOrRemoveButton.setText(i18n("Update package(s)"))
        
        elif index == 0 :
            # Show only not-installed apps
            available = self.command.listAvailable()
            installed = self.command.listPackages()
            shownPackages = list(available - set(installed))
            self.installOrRemoveButton.setText(i18n("Install package(s)"))
        
        if not len(shownPackages):
            mainwidget.infoWidgetStack.raiseWidget(1)
        else:
            mainwidget.infoWidgetStack.raiseWidget(0)

        self.shownPackages = set(shownPackages)
        self.updatePackages(shownPackages)

    def installRemoveFinished(self):
        pass
        # RETHINK
        
    def installSinglePackage(self,package):
        pass
        # RETHINK
                    
    def installRemove(self):

        try: # Dependencies might bite us here, http://bugs.uludag.org.tr/show_bug.cgi?id=1170
            dependencies = self.command.packageGraph(self.selectedItems).vertices()
            self.totalAppCount = len(dependencies)
            self.selectedItems = list(set.union(set(self.selectedItems),set(dependencies)))
        except Exception,e:
            KMessageBox.error(self,unicode(e),i18n("PiSi Error"))
            return
                                                
        index = mainwidget.selectionGroup.selectedId()
        self.installOrRemoveButton.setEnabled(False)
        self.progressDialog.setCaption(i18n("Add or Remove Programs"))
        self.progressDialog.show()

        if index == 0: # Install baby
            self.operation = "install"
            self.command.install(self.selectedItems)

        elif index == 1: # Upgrade baby
            self.operation = "upgrade"
            self.command.upgrade(self.selectedItems)
                                    
        elif index == 2: # Remove baby
            self.operation = "remove"
            self.command.remove(self.selectedItems)
                      
    def updateSystemSelection(self):
        self.installOrRemoveButton.setEnabled(False)
        
        self.progressDialog.setCaption(i18n("Add or Remove Programs"))
        self.progressDialog.show()
        
        list = self.command.listUpgradable()
        self.totalAppCount = len(list)
        self.operation = "upgrade"
        self.command.upgrade(list)

    if False: # Disabled for rc1, will enable later
        self.installOrRemoveButton.setEnabled(False)
        self.updateWizard = UpdateWizardDialog.UpdateWizardDialog()
        self.fastUpdatesDialog = FastUpdatesDialog.FastUpdatesDialog()
        self.customUpdatesDialog = CustomUpdatesDialog.CustomUpdatesDialog()
    
        self.updateWizard.addPage(self.fastUpdatesDialog, i18n("Fast Updates (only security)"))
        self.updateWizard.addPage(self.customUpdatesDialog, i18n("Custom Updates"))
                    
        self.connect(self.updateWizard.nextButton(),SIGNAL("clicked()"),self.updateSystem)
        
        self.updateWizard.setModal(True)
        self.updateWizard.show()
                

    def updateSystem(self):
        self.updateList = self.command.listUpgradable()
        self.installSize = 0
        
        if self.updateWizard.fastUpdateButton.isOn():
            self.updateWizard.setAppropriate(self.customUpdatesDialog, False)
            self.updateWizard.showPage(self.fastUpdatesDialog)
            self.fastUpdatesDialog.listView.clear()
            self.securityUpdates = []
            for app in self.updateList:
                packageHistory = pisi.packagedb.get_package(app).history[0]
                if packageHistory.type == "security":
                    self.securityUpdates.append(app)
                    self.installSize += pisi.packagedb.inst_packagedb.get_package(app).installedSize
                    item = QListViewItem(self.fastUpdatesDialog.listView,app)
                    item.setText(1,packageHistory.version)
                    item.setText(2,pisi.packagedb.inst_packagedb.get_package(app).history[0].version)
            self.fastUpdatesDialog.installSizeLabel.setText(i18n('Total size: %s').arg(FormatNumber(self.installSize)))
        else:
            self.updateWizard.setAppropriate(self.fastUpdatesDialog, False)
            self.updateWizard.showPage(self.customUpdatesDialog)
            self.customUpdatesDialog.listView.clear()
            for app in self.updateList:
                packageHistory = pisi.packagedb.get_package(app).history[0]
                self.installSize += pisi.packagedb.inst_packagedb.get_package(app).installedSize
                item = QListViewItem(self.customUpdatesDialog.listView,app)
                item.setText(1,packageHistory.version)
                item.setText(2,pisi.packagedb.inst_packagedb.get_package(app).history[0].version)
            self.customUpdatesDialog.installSizeLabel.setText(i18n('Total size: %s').arg(FormatNumber(self.installSize)))
                   
    def installSingle(self):
        app = []
        app.append(str(self.listView.currentItem().text(0)))
        self.command.install(app)
        
    def searchPackage(self):
    
        # search summary / description
        query = unicode(self.queryEdit.text())
        
        # search names
        query.strip()
        if query:
            result = self.command.searchPackage(query)
            result = result.union( self.command.searchPackage(query, 'en' ) )

            for pkg in self.packageList:
                if pkg.find(query) != -1:
                    result.add(pkg)
       
            if not len(result):
                mainwidget.infoWidgetStack.raiseWidget(1)
            else:
                mainwidget.infoWidgetStack.raiseWidget(0)
            
            self.updatePackages(list(result))
        else:
            self.updateListing() # get the whole list if blank query            
    
    def clearSearch(self):
        self.queryEdit.clear()    
        self.updateListing()

    def showPreferences(self):
        self.pref = Preferences.Preferences(self)
        self.pref.show()

    def setShowOnlyPrograms(self,hideLibraries=False):
        global kapp
        self.config = kapp.config()
        self.config.setGroup("General")
        self.config.writeEntry("HideLibraries",hideLibraries)
        self.config.sync()

    def getShowOnlyPrograms(self):
        global kapp
        self.config = kapp.config()
        self.config.setGroup("General")
        return self.config.readBoolEntry("HideLibraries")                                    

# Are we running as a separate standalone application or in KControl?
standalone = __name__=='__main__'

if standalone:
    programbase = QDialog
else:
    programbase = KCModule
    
class MainApplication(programbase):
    def __init__(self,parent=None,name=None):
        global standalone
        global mainwidget

        if standalone:
            QDialog.__init__(self,parent,name)
            self.setCaption("PiSi KGA")
        else:
            KCModule.__init__(self,parent,name)
            KGlobal.locale().insertCatalogue("pisi_kga")
            # Create a configuration object.
            self.config = KConfig("pisi_kga")
            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("pisi_kga")

        self.aboutus = KAboutApplication(self)
        self.helpWidget = None

        mainwidget = MainApplicationWidget(self)
        toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
        toplayout.addWidget(mainwidget)
        mainwidget.listView.setResizeMode(KListView.LastColumn)
        mainwidget.iconLabel.setPixmap(loadIcon('package', KIcon.Desktop))
        
        self.connect(mainwidget.selectionGroup,SIGNAL("clicked(int)"),mainwidget.updateListing)
        self.connect(mainwidget.clearButton,SIGNAL("clicked()"),mainwidget.clearSearch)
        self.connect(mainwidget.closeButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(mainwidget.helpButton,SIGNAL("clicked()"),self.showHelp)
        self.connect(mainwidget.listView,SIGNAL("selectionChanged(QListViewItem *)"),mainwidget.updateDetails)
        self.connect(mainwidget.listView,SIGNAL("clicked(QListViewItem *)"),mainwidget.updateButtons)
        self.connect(mainwidget.listView,SIGNAL("spacePressed(QListViewItem *)"),mainwidget.updateButtons)
        self.connect(mainwidget.installOrRemoveButton,SIGNAL("clicked()"),mainwidget.installRemove)
        self.connect(mainwidget.updateSystemButton,SIGNAL("clicked()"),mainwidget.updateSystemSelection)
        self.connect(mainwidget.preferencesButton,SIGNAL("clicked()"),mainwidget.showPreferences)
        self.connect(mainwidget.searchButton,SIGNAL("clicked()"),mainwidget.searchPackage)
        
        # Read only settings
        mainwidget.preferencesButton.setEnabled(not nonPrivMode)
        if nonPrivMode:
            mainwidget.selectionInfo.hide()

        if programbase == KCModule:
            mainwidget.closeButton.hide()

        mainwidget.selectionGroup.setButton(0);
        mainwidget.updateListing();

        if not nonPrivMode and packageToInstall:
            mainwidget.installSinglePackage(packageToInstall)

    def showHelp(self):
        global mainwidget
        if not self.helpWidget:
            self.helpWidget = HelpDialog.HelpDialog(mainwidget)
            # FIXME make non modal
            self.helpWidget.setModal(True)
        self.helpWidget.show()

    def exec_loop(self):
        global programbase
        
        # Load configuration here
        self.__loadOptions()
        
        programbase.exec_loop(self)
        
        # Save configuration here
        self.__saveOptions()

    def __loadOptions(self):
        global kapp
        config = kapp.config()
        config.setGroup("General")
        size = config.readSizeEntry("Geometry")
        if size.isEmpty():
            self.resize(700,600)
        else:
            self.resize(size)

    def __saveOptions(self):
        global kapp
        config = kapp.config()
        config.setGroup("General")
        config.writeEntry("Geometry", self.size())
        config.sync()
        
    # KControl virtual void methods
    def load(self):
        pass
    def save(self):
        pass
    def defaults(self):
        pass        
    def sysdefaults(self):
        pass
    
    def aboutData(self):
        # Return the KAboutData object which we created during initialisation.
        return self.aboutdata
    
    def buttons(self):
        # Only supply a Help button. Other choices are Default and Apply.
        return KCModule.Help

# This is the entry point used when running this module outside of kcontrol.
def main():
    global kapp
    global nonPrivMode
    global packageToInstall

    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)
    KCmdLineArgs.addCmdLineOptions ([("install <package>", I18N_NOOP("Package to install"))])

    if not KUniqueApplication.start():
        print i18n("Pisi KGA is already running!")
        return

    nonPrivMode = posix.getuid()
    kapp = KUniqueApplication(True, True, True)

    args = KCmdLineArgs.parsedArgs()
    if args.isSet("install"):
        packageToInstall = str(KIO.NetAccess.mostLocalURL(KURL(args.getOption("install")), None).path())
    else:
        packageToInstall = None

    myapp = MainApplication()
    kapp.setMainWidget(myapp)
        
    sys.exit(myapp.exec_loop())
    
# Factory function for KControl
def create_pisi_kga(parent,name):
    global kapp
    global nonPrivMode
    global packageToInstall
   
    packageToInstall = None
    nonPrivMode = posix.getuid()
    kapp = KApplication.kApplication()
    return MainApplication(parent, name)

if standalone:
    main()
