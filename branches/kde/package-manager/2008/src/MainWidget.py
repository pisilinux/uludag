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

# System
import sys

# PyQt/PyKDE
from qt import *
from kdecore import *
from kdeui import *
from kio import *
import kdedesigner

# Local imports
import Progress
import Basket
import BasketDialog
from Icons import *
import Preferences
import Commander
import Tray
import Settings
import LocaleData
import HelpDialog
from Component import *
from SpecialList import *
import Globals
from Notifier import *

# Pisi
import PisiIface

(install_state, remove_state, upgrade_state) = range(3)
nop = ["System.Manager.setCache", "System.Manager.clearCache"]

unremovable_packages = set(['qt','kdelibs','kdebase','sip','PyQt','PyKDE','pisi', 'package-manager'])

class MainApplicationWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent

        self.progressDialog = Progress.Progress(self)

        # Keys of this dict. are Components Listview's items, and values are component object about the item
        self.componentDict = {}

        self.lastSelectedComponent = None
        self.command = None
        self.state = install_state
        self.basket = Basket.Basket()
        self.command = Commander.Commander(self)
        self.settings = Settings.Settings(Globals.config())

        # set up timers
        self.delayTimer = QTimer(self)

        self.setupInterface()
        self.setupConnections()

        self.delayTimer.start(500, True)

        # inform user for the delay...
        item = KListViewItem(self.componentsList)
        item.setText(0,i18n("Loading Package List..."))
        self.componentsList.setSelected(self.componentsList.firstChild(),True)
        self.tipper = ComponentTipper(self)

        self.show()

    def updateAfterAPackageClicked(self):
        self.updateButtons()
        self.updateStatusBar()

    def packageClicked(self, itemName, checked):
        if checked:
            if itemName not in self.basket.packages:
                self.basket.add(itemName)
        else:
            self.basket.remove(itemName)

    def setupInterface(self):
        self.layout = QGridLayout(self)
        self.leftLayout = QVBox(self)
        self.rightLayout = QVBox(self)

        self.leftLayout.setSpacing(3)
        self.rightLayout.setSpacing(3)

        # KListViewSearchLineWidget can't be used here, so time to implement ours :P
        self.rightTopLayout = QHBox(self.rightLayout)
        self.rightTopLayout.setSpacing(3)
        self.clearButton = KPushButton(self.rightTopLayout)
        self.clearButton.setIconSet(loadIconSet("locationbar_erase"))
        self.searchLabel = QLabel(i18n("Search: "), self.rightTopLayout)
        self.searchLine = KLineEdit(self.rightTopLayout)

        self.searchAction = KPushButton(self.rightTopLayout)
        self.searchAction.setText(i18n("Search"))
        self.searchAction.setIconSet(loadIconSet("find"))

        self.basketAction = KPushButton(self.rightTopLayout)
        self.basketAction.setText(i18n("Show basket"))
        self.basketAction.setIconSet(loadIconSet("package"))
        self.basketAction.setEnabled(False)

        self.operateAction = KPushButton(self.rightTopLayout)
        self.operateAction.setText(i18n("Install Package(s)"))
        self.operateAction.setIconSet(loadIconSet("ok"))
        self.operateAction.setEnabled(False)

        # list of packages on the right side
        self.specialList = SpecialList(self.rightLayout)

        self.componentsList = KListView(self.leftLayout)
        self.componentsList.setFullWidth(True)
        self.componentsList.addColumn(i18n("Components"))

        self.leftLayout.setMargin(2)
        self.rightLayout.setMargin(2)
        self.leftLayout.setSpacing(5)
        self.rightLayout.setSpacing(5)

        self.layout.addWidget(self.leftLayout,1,1)
        self.layout.addWidget(self.rightLayout,1,2)
        self.layout.setColStretch(1,2)
        self.layout.setColStretch(2,6)

    def setupConnections(self):
        self.connect(self.componentsList,SIGNAL("selectionChanged(QListViewItem *)"),self.refreshComponentList)
        self.connect(self.clearButton, SIGNAL("clicked()"), self.searchClear)
        self.connect(self.searchAction, SIGNAL("clicked()"), self.searchPackage)
        self.connect(self.searchLine, SIGNAL("returnPressed()"), self.searchPackage)
        self.connect(self.basketAction, SIGNAL("clicked()"),self.showBasket)
        self.connect(self.operateAction, SIGNAL("clicked()"),self.takeAction)
        self.connect(self.specialList, PYSIGNAL("checkboxClicked"), self.packageClicked)
        self.connect(self.delayTimer, SIGNAL("timeout()"), self.lazyLoadComponentList)

    def searchClear(self):
        self.searchLine.clear()
        self.refreshState(False)

    def lazyLoadComponentList(self):

        try:
            self.parent.tray.updateTrayIcon()
        except PisiIface.RepoError:
            self.updateCheck()

        if self.componentsReady():
            self.installState()

            if Globals.packageToInstall:
                self.installPackage(unicode(Globals.packageToInstall))
                self.progressDialog.show()
                # KWin forces to raise it even though the parent is hidden, QWidget does not.
                KWin.raiseWindow(self.progressDialog.winId())
        else:
            self.updateCheck()

    def processEvents(self):
        Globals.processEvents()

    def componentsReady(self):
        if not PisiIface.get_components(): # Repo metadata empty
            return False

        return True

    def repoNotReady(self):
        KMessageBox.error(self, i18n("Package-manager needs to update package database. You need a network connection to update."),
                          i18n("Package database is empty"))

    # clear cache, basket, search line...
    def resetState(self):
        self.basket.empty()
        self.basketAction.setEnabled(False)
        self.operateAction.setEnabled(False)
        self.searchLine.clear()
        self.parent.showNewAction.setChecked(False)
        self.parent.showInstalledAction.setChecked(False)
        self.parent.showUpgradeAction.setEnabled(True)
        self.parent.showUpgradeAction.setChecked(False)

    # executed at start and when 'Show New Packages' is clicked
    def installState(self, reset=True):

        # set mouse to waiting icon
        Globals.setWaitCursor()

        try:
            # uncheck buttons, clear search line, empty cache
            if reset:
                self.resetState()

            # check the "Show New Packages" button
            self.parent.showNewAction.setChecked(True)
            self.processEvents()

            try:
                packages = self.command.listNewPackages()
            except PisiIface.RepoError:
                Globals.setNormalCursor()
                self.repoNotReady()
                return

            self.state = install_state

            # prepare components' listview on the left side
            self.createComponentList(packages)

            self.operateAction.setText(i18n("Install Package(s)"))
            self.operateAction.setIconSet(loadIconSet("ok"))
            self.basket.setState(self.state)

            # set last selected component and so, trigger SpecialList to create right side (packages)
            # (selects first component if it is the first time)
            self.setLastSelected()

            self.updateStatusBar()

        finally:
            Globals.setNormalCursor()

    # Executed when 'Show Installed Packages' is clicked
    def removeState(self, reset=True):
        Globals.setWaitCursor()

        try:
            if reset:
                self.resetState()
            self.parent.showInstalledAction.setChecked(True)
            self.processEvents()

            try:
                packages = self.command.listPackages()
            except PisiIface.RepoError:
                Globals.setNormalCursor()
                self.repoNotReady()
                return

            self.state = remove_state
            self.createComponentList(packages)
            self.operateAction.setText(i18n("Remove Package(s)"))
            self.operateAction.setIconSet(loadIconSet("no"))
            self.basket.setState(self.state)
            self.setLastSelected()
            self.updateStatusBar()

        finally:
            Globals.setNormalCursor()

    # Executed when 'Show Upgradable Packages' is clicked
    def updateCheck(self):
        self.resetState()
        self.state = upgrade_state
        self.parent.showUpgradeAction.setChecked(True)
        self.parent.showUpgradeAction.setEnabled(False)
        self.processEvents()
        self.progressDialog.hideStatus(True)
        self.progressDialog.setCurrentOperation(i18n("<b>Updating Repository</b>"))
        self.progressDialog.show()
        self.command.startUpdate()

    def upgradeState(self):
        Globals.setWaitCursor()

        try:
            # TODO:
            # If package-manager is opened while tray is updating-repo; progress dialog is
            # shown. And when it ends, pm switches to upgradeState but without checking
            # operation buttons. If pm is not opened while this is done, no change state happens
            # in pm, and when it is opened it will be seen in which state it was left.
            #
            # Later this background update may be done with a widget like kmail's small progress 
            # and any operation button will be disabled when tray is caught while updating. For 
            # now we show progress dialog and change pm state and button states manually.
            self.parent.showUpgradeAction.setChecked(True)
            self.parent.showNewAction.setChecked(False)
            self.parent.showInstalledAction.setChecked(False)
            ##

            try:
                upgradables = PisiIface.get_upgradable_packages()
            except PisiIface.RepoError:
                Globals.setNormalCursor()
                self.repoNotReady()
                return

            self.createComponentList(upgradables, True)
            self.operateAction.setText(i18n("Upgrade Package(s)"))
            self.operateAction.setIconSet(loadIconSet("reload"))
            self.lastSelectedComponent = i18n("All")
            self.setLastSelected()

            self.basket.setState(self.state)
            self.updateStatusBar()

        finally:
            Globals.setNormalCursor()

    def setLastSelected(self):
        item = self.componentsList.firstChild()

        # There may be no item in component list. No more new packages to install for example.
        if not item:
            self.clearPackageList()
            return

        # FIXME: a quick and ugly hack to see if we are in search state.
        if item.text(0) == i18n("Search Results"):
            return item

        for i in self.componentDict.keys():
            if self.componentDict[i].name == self.lastSelectedComponent:
                item = i
                break

        self.componentsList.setSelected(item, True)
        return item

    def refreshComponentList(self, item):
        Globals.setWaitCursor()
        try:
            # fetch packages including metadata from cache
            packagesWithMeta = [PisiIface.get_package(package, self.state == remove_state) for package in self.componentDict[item].packages]
            if self.state == remove_state:
                self.specialList.createList(packagesWithMeta, selected = self.basket.packages, disabled = unremovable_packages)
            else:
                self.specialList.createList(packagesWithMeta, selected = self.basket.packages)
                self.lastSelectedComponent = self.componentDict[item].name
        # initialization and search state listview items are not components
        except KeyError:
            pass
        finally:
            Globals.setNormalCursor()

    def updateStatusBar(self):
        Globals.setWaitCursor()
        try:
            self.basket.update()
        finally:
            Globals.setNormalCursor()

        if not self.basket.packages:
            text = i18n("Currently your basket is empty.")

        elif self.state == install_state or self.state == upgrade_state:
            text = i18n("Currently there are <b>%1</b> selected package(s) of total <b>%2</b> of size ").arg(len(self.basket.packages)).arg(Globals.humanReadableSize(self.basket.packagesSize))

            if self.basket.extraPackages:
                text += i18n("with <b>%3</b> extra dependencies of total <b>%4</b> of size ").arg(len(self.basket.extraPackages)).arg(Globals.humanReadableSize(self.basket.extraPackagesSize))

            text += i18n("in your basket.")

        elif self.state == remove_state:
            text = i18n("Currently there are <b>%1</b> selected package(s) of total <b>%2</b> of size ").arg(len(self.basket.packages)).arg(Globals.humanReadableSize(self.basket.packagesSize))

            if self.basket.extraPackages:
                text += i18n("with <b>%3</b> reverse dependencies of total <b>%4</b> of size ").arg(len(self.basket.extraPackages)).arg(Globals.humanReadableSize(self.basket.extraPackagesSize))

            text += i18n("in your basket.")

        self.parent.updateStatusBarText(text)

    def updateButtons(self):
        if self.basket.packages:
            self.operateAction.setEnabled(True)
            self.basketAction.setEnabled(True)
        else:
            self.operateAction.setEnabled(False)
            self.basketAction.setEnabled(False)

    def showBasket(self):
        basketDialog = BasketDialog.BasketDialog(self, self.basket)
        action = basketDialog.exec_loop()
        self.processEvents()

        if action == BasketDialog.APPLY_OPERATION:
            self.takeAction()

        self.updateButtons()
        self.refreshComponentList(self.setLastSelected())
        item = self.componentsList.firstChild()
        if item and item.text(0) == i18n("Search Results"):
            self.searchPackage()
        basketDialog.deleteLater()

    def conflictCheckPass(self):
        (C, D, pkg_conflicts) = self.command.checkConflicts(self.basket.packages + self.basket.extraPackages)

        conflicts_within = list(D)
        if conflicts_within:
            msg = i18n("Selected packages [%1] are in conflict with each other. These packages can not be installed together.").arg(", ".join(conflicts_within))
            self.showErrorMessage(msg, i18n("Conflict Error"))
            self.searchLine.clear()
            self.refreshState(False)
            return False

        if pkg_conflicts:
            msg = i18n("The following packages conflicts:\n")
            for pkg in pkg_conflicts.keys():
                msg += i18n("%1 conflicts with: [%2]\n").arg(pkg).arg(", ".join(pkg_conflicts[pkg]))
            msg += i18n("\nRemove the conflicting packages from the system?")
            if self.showConfirmMessage(msg, i18n("Conflict Error")) == KMessageBox.No:
                self.searchLine.clear()
                self.refreshState(False)
                return False

        return True

    def installPackage(self, package):
        self.progressDialog.hideStatus(True)
        self.progressDialog.updateProgressBar(100)

        if not self.command.inProgress():
            self.progressDialog.totalPackages = 1
            self.command.install([package])
            self.progressDialog.setCurrentOperation(i18n("<b>Installing Package(s)</b>"))
            self.progressDialog.show()
            # KWin forces to raise it even though the parent is hidden, QWidget does not.
            KWin.raiseWindow(self.progressDialog.winId())


    def confirmAction(self):
        message = None
        if self.state == install_state:
            message = QString(i18n("<qt>You have selected <b>%1</b> package(s) to be <b>installed</b>.")).arg(len(self.basket.packages))

            if self.basket.extraPackages:
                message += QString(i18n(" With the selected packages; <b>%1</b> extra dependencies are also going to be <b>installed</b>.")).arg(len(self.basket.extraPackages))
                message += QString(i18n("<br><br>Total of <b>%1</b> packages are going to be <b>installed</b>.")).arg(len(self.basket.packages) + len(self.basket.extraPackages))

        elif self.state == upgrade_state:
            message = i18n("<qt>You have selected <b>%1</b> package(s) to be <b>upgraded</b>.").arg(len(self.basket.packages))

            if self.basket.extraPackages:
                message += i18n(" With the selected packages; <b>%1</b> extra dependencies are also going to be <b>upgraded</b>.").arg(len(self.basket.extraPackages))
                message += i18n("<br><br>Total of <b>%1</b> packages are going to be <b>upgraded</b>.").arg(len(self.basket.packages) + len(self.basket.extraPackages))

        elif self.state == remove_state:
            message = i18n("<qt>You have selected <b>%1</b> package(s) to be <b>removed</b>.").arg(len(self.basket.packages))

            if self.basket.extraPackages:
                message += i18n(" Selected packages have reverse dependencies. Because the reverse dependencies of the selected packages needs those packages to work; by removing the selected packages; <b>%1</b> reverse dependencies are also going to be <b>removed</b>. Please check your basket and make sure those are the packages you want to remove. Accidentally removing some reverse dependencies may break the system stability.").arg(len(self.basket.extraPackages))

                message += i18n("<br><br>Total of <b>%1</b> packages are going to be <b>removed</b>.").arg(len(self.basket.packages) + len(self.basket.extraPackages))

        message += i18n("<br>Do you want to continue?</qt>")

        if KMessageBox.Yes == KMessageBox.warningYesNo(self, 
                                                       message,
                                                       i18n("Warning"),
                                                       KGuiItem(i18n("Continue"), "ok"),
                                                       KGuiItem(i18n("Cancel"), "no"),
                                                       ):
            return True

        return False

    def takeAction(self):
        if not self.confirmAction():
            return

        self.progressDialog.totalPackages = len(self.basket.packages + self.basket.extraPackages)

        # remove action
        if self.state == remove_state:
            self.command.remove(self.basket.packages)
            self.progressDialog.setCurrentOperation(i18n("<b>Removing Package(s)</b>"))
            self.progressDialog.hideStatus()

        # install action
        elif self.state == install_state:
            if not self.conflictCheckPass():
                return

            self.progressDialog.setCurrentOperation(i18n("<b>Installing Package(s)</b>"))
            self.progressDialog.showStatus()
            self.command.install(self.basket.packages)

        # upgrade action
        elif self.state == upgrade_state:
            if not self.conflictCheckPass():
                return

            self.progressDialog.setCurrentOperation(i18n("<b>Upgrading Package(s)</b>"))
            self.progressDialog.showStatus()
            self.command.updatePackage(self.basket.packages)

        if not self.parent.isHidden():
            self.progressDialog.show()

    def refreshState(self, reset=True):

        if self.settings.getBoolValue(Settings.general, "SystemTray"):
            self.parent.tray.show()
        elif not self.settings.getBoolValue(Settings.general, "SystemTray"):
            self.parent.tray.hide()

        if self.state == install_state:
            self.installState(reset)
        elif self.state == remove_state:
            self.removeState(reset)
        elif self.state == upgrade_state:
            self.upgradeState()

    def updateComponentList(self):
        item = self.componentsList.currentItem()
        component = self.componentDict[item]
        if component.packages:
            item.setText(0,u"%s (%s)" % (component.name, len(component.packages)))
        else:
            self.componentsList.takeItem(item)
            self.componentsList.setSelected(self.componentsList.firstChild(),True)

    #create a component list from given package list
    def createComponentList(self, packages, allComponent=False):
        # filter for selecting only apps with gui
        def appGuiFilter(pkg_name):
            if self.state == remove_state:
                package = PisiIface.get_installed_package(pkg_name)
                return "app:gui" in package.isA
            elif self.state == install_state:
                package = PisiIface.get_repo_package(pkg_name)
                return "app:gui" in package.isA

        self.componentsList.clear()
        self.componentDict.clear()

        # eliminate components that are not visible to users. This is achieved by a tag in component.xmls
        componentNames = [cname for cname in PisiIface.get_components() if PisiIface.is_component_visible(cname)]

        showOnlyGuiApp = self.settings.getBoolValue(Settings.general, "ShowOnlyGuiApp")

        # this list is required to find 'Others' group, that is group of packages not belong to any component
        componentPackages = []
        for componentName in componentNames:
            # just check the component existance
            try:
                component = PisiIface.get_union_component(componentName)
            except Exception:
                continue

            # get all packages of the component
            compPkgs = PisiIface.get_union_component_packages(componentName, walk=True)

            # find which packages belong to this component
            component_packages = list(set(packages).intersection(compPkgs))
            componentPackages += component_packages

            if self.state != upgrade_state and showOnlyGuiApp:
                    component_packages = filter(appGuiFilter, component_packages)

            if len(component_packages):
                # create ListView item for component
                item = KListViewItem(self.componentsList)
                if component.localName:
                    name = component.localName
                else:
                    name = component.name

                if component.icon:
                    icon = component.icon
                else:
                    icon = "package"

                item.setText(0,u"%s (%s)" % (name, len(component_packages)))
                item.setPixmap(0, KGlobal.iconLoader().loadIcon(icon, KIcon.Desktop,KIcon.SizeMedium))

                # create component object that has a list of its own packages and a summary
                self.componentDict[item] = Component(name, component_packages, component.summary)

        # Rest of the packages
        rest_packages = list(set(packages) - set(componentPackages))
        if self.state != upgrade_state and showOnlyGuiApp:
            rest_packages = filter(appGuiFilter, rest_packages)
        if rest_packages:
            item = KListViewItem(self.componentsList)
            name = i18n("Others")
            item.setText(0, u"%s (%s)" % (name, len(rest_packages)))
            item.setPixmap(0, KGlobal.iconLoader().loadIcon("package_applications",KIcon.Desktop,KIcon.SizeMedium))
            self.componentDict[item] = Component(name, rest_packages, name)

        # All of the component's packages
        if allComponent:
            item = KListViewItem(self.componentsList)
            name = i18n("All")
            item.setText(0, u"%s (%s)" % (name, len(packages)))
            item.setPixmap(0, KGlobal.iconLoader().loadIcon("package_network",KIcon.Desktop,KIcon.SizeMedium))
            self.componentDict[item] = Component(name, packages, name)

    def createSearchResults(self, packages):
        self.componentsList.clear()
        item = KListViewItem(self.componentsList)
        item.setText(0,i18n("Search Results"))
        item.setPixmap(0, KGlobal.iconLoader().loadIcon("find",KIcon.Desktop,KIcon.SizeMedium))
        packagesWithMeta = [PisiIface.get_package(package, self.state != install_state) for package in packages]
        if self.state == remove_state:
            self.specialList.createList(packagesWithMeta, selected = self.basket.packages, disabled = unremovable_packages)
        else:
            self.specialList.createList(packagesWithMeta, selected = self.basket.packages)
        self.componentsList.setSelected(self.componentsList.firstChild(),True)

    def displayProgress(self, data):
        operation = data[0]
        if operation in ["updatingrepo", "rebuilding-db"]:
            self.progressDialog.setOperationDescription(i18n(str(data[2])))
            percent = data[1]
            self.progressDialog.updateProgressBar(percent)

        elif operation == "fetching":
            if "pisi-index.xml" in data[1]:
                self.progressDialog.updateUpgradingInfo()
                self.progressDialog.updateProgressBar(progress=data[2])
                self.progressDialog.calculateTimeLeft(data[6], data[5], data[3], data[4])
                self.progressDialog.updateCompletedInfo()
            else:
                if self.state == install_state:
                    self.progressDialog.setCurrentOperation(i18n("<b>Installing Package(s)</b>"))
                elif self.state == upgrade_state:
                    self.progressDialog.setCurrentOperation(i18n("<b>Upgrading Package(s)</b>"))

                self.progressDialog.updateDownloadingInfo(i18n("downloading"), file=data[1])
                self.progressDialog.updateTotalDownloaded(pkgDownSize=data[5], pkgTotalSize=data[6], rate=data[3], symbol=data[4])
                self.progressDialog.updateCompletedInfo()
                self.progressDialog.updateTotalOperationPercent()

    def pisiNotify(self, operation, args):
        # operation is now cancellable
        if operation in ["started"]:
            self.progressDialog.enableCancel()

        elif operation in ["removing"]:
            self.progressDialog.updateOperationDescription(i18n(str(operation)), package=args[0])
            self.progressDialog.updateStatusInfo()

        elif operation in ["cached"]:
            # progressDialog.totalSize is the to be downloaded size by package-manager.
            # And that is (totalDownloadSize - alreadyCachedSize) 
            self.progressDialog.totalSize = int(args[0]) - int(args[1])
            self.progressDialog.updateTotalOperationPercent()
            self.progressDialog.updateCompletedInfo()

        elif operation in ["installing"]:
            self.progressDialog.updateOperationDescription(i18n(str(operation)), package=args[0])
            self.progressDialog.updateStatusInfo()

        elif operation in ["extracting", "configuring"]:
            self.progressDialog.disableCancel()
            self.progressDialog.updateOperationDescription(i18n(str(operation)), package=args[0])

        elif operation in ["removed", "installed", "upgraded"]:
            # Bug 4030
            if self.state != remove_state and operation == "removed":
                return

            self.progressDialog.packageNo += 1
            self.progressDialog.updateStatusInfo()
            self.progressDialog.updatePackageProgress()

        elif operation in ["savingrepos"]:
            self.progressDialog.setCurrentOperation(i18n("<b>Applying Repository Changes</b>"))

        elif operation in ["updatingrepo"]:
            self.progressDialog.setCurrentOperation(i18n("<b>Updating Repository</b>"))
            self.progressDialog.setOperationDescription(i18n('Downloading package list of %1').arg(args[0]))

    def showWarningMessage(self, message, warning=None):
        if not warning:
            warning=i18n("Warning")
        KMessageBox.sorry(self, message, warning)

    def showErrorMessage(self, message, error=None):
        #bug: 6479
        #if error=i18n("Error") is written above, it isn't translated
        if not error:
            error=i18n("Error")
        KMessageBox.error(self, message, error)

    def showConfirmMessage(self, message, error=None):
        if not error:
            error=i18n("Confirm")
        return KMessageBox.questionYesNo(self, message, error)

    def finished(self, command=None):
        # when pisi db version is upgraded, reload is needed before init
        packages = self.basket.packages + self.basket.extraPackages
        print "in finished(): command=%s" % command

        if command in nop:
            return

        #FIXME: Why do we need to reload pisi module every time. Added for not updating mem cached dbs of pisi
        PisiIface.reloadPisi()

        self.basket.empty()
        self.operateAction.setEnabled(False)
        self.basketAction.setEnabled(False)
        self.parent.showUpgradeAction.setEnabled(True)

        self.progressDialog.closeForced()
        self.progressDialog.reset()

        if command in ["System.Manager.updateAllRepositories",
                       "System.Manager.updateRepository"]:
            self.refreshState()

            if self.parent.isHidden():
                self.parent.tray.showPopup()

        elif command == "System.Manager.setRepositories":
            self.updateCheck()
            return

        elif command in ["System.Manager.updatePackage",
                         "System.Manager.installPackage",
                         "System.Manager.removePackage",
                         "System.Manager.cancelled"]:
            self.refreshState()

        self.parent.tray.updateTrayIcon()

    def searchPackage(self):
        Globals.setWaitCursor()
        query = unicode(self.searchLine.text())
        terms = query.split()
        if query:
            if self.state == remove_state:
                result = PisiIface.search_in_installed(terms)
            elif self.state == install_state:
                result = PisiIface.search_in_repos(terms)
            elif self.state == upgrade_state:
                result = PisiIface.search_in_upgradables(terms)
            self.createSearchResults(result)
        else:
            self.refreshState(reset=False)
        Globals.setNormalCursor()

    def showPreferences(self):
        self.pref = Preferences.Preferences(self)
        self.pref.show()

    def show(self):
        QWidget.show(self)
        if self.command and self.command.inProgress():
            self.progressDialog.show()

    def trayUpdateCheck(self, repo = None, forced = False):
        # timer interval check should not be run if package-manager is not hidden.
        if not forced and not self.parent.isHidden():
            return

        self.parent.showUpgradeAction.setEnabled(False)
        self.processEvents()
        self.progressDialog.hideStatus(True)

        self.command.startUpdate(repo, handleErrors=forced)

        # update repo command is given by the user
        if forced and not self.parent.isHidden():
            self.progressDialog.show()

    def trayUpgradeSwitch(self):
        self.resetState()
        self.state = upgrade_state
        self.upgradeState()
        self.processEvents()

