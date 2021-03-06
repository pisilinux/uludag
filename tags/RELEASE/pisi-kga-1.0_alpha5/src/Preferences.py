# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors: İsmail Dönmez <ismail@uludag.org.tr>

from kdeui import *
from qt import *
import PreferencesWidget
import RepoDialog
import ThreadRunner
import PisiKga # for loadIcon

# Pisi imports
import pisi.api
import pisi.repodb

class Preferences(PreferencesWidget.PrefsDialog):
    def __init__(self, parent=None):
        PreferencesWidget.PrefsDialog.__init__(self, parent)
        self.command = ThreadRunner.MyThread(parent)
        self.setCaption(u'PiSi KGA - Depo Ayarları')
        self.infoLabel.setPixmap(PisiKga.loadIcon('info'))
        self.networkLabel.setPixmap(PisiKga.loadIcon('network'))
        self.connect(self.addButton, SIGNAL("clicked()"), self.addNewRepo)
        self.connect(self.removeButton, SIGNAL("clicked()"), self.removeRepo)
        self.connect(self.repoListView, SIGNAL("selectionChanged()"), self.updateButtons)
        self.connect(self.moveupButton, SIGNAL("clicked()"), self.moveUp)
        self.connect(self.movedownButton, SIGNAL("clicked()"), self.moveDown)
        self.connect(self.updateRepoButton, SIGNAL("clicked()"), self.updateAllRepos)
        self.removeButton.setEnabled(False)
        self.repoListView.setSorting(-1)
        self.readConfig()
        self.updateListView()

    def updateButtons(self):
        if self.repoListView.childCount() > 1:
            moreThanOne = True
        else:
            moreThanOne = False
		
        if self.repoListView.currentItem().isSelected():
            self.removeButton.setEnabled(moreThanOne)
            self.moveupButton.setEnabled(moreThanOne)
            self.movedownButton.setEnabled(moreThanOne)
        else:
            self.removeButton.setEnabled(False)
            self.moveupButton.setEnabled(False)
            self.movedownButton.setEnabled(False)

    def moveUp(self):
        item = self.repoListView.currentItem()
        parent = item.itemAbove()
        
        if not parent:
            return
        
        if parent.itemAbove():
            item.moveItem(parent.itemAbove())
        else:
            self.repoListView.takeItem(item)
            self.repoListView.insertItem(item)
            self.repoListView.setSelected(item, True)

        pisi.api.ctx.repodb.swap(self.repoList.index(item.text(0)), self.repoList.index(parent.text(0)))

    def moveDown(self):
        item = self.repoListView.currentItem()
        sibling = item.itemBelow()

        if not sibling:
            return

        item.moveItem(sibling)

        pisi.api.ctx.repodb.swap(self.repoList.index(item.text(0)), self.repoList.index(sibling.text(0)))

    def updateAllRepos(self):
        self.updateRepoButton.setEnabled(False)
        
        for i in self.repoList:
            self.command.updateRepo(i)
        self.updateRepoButton.setEnabled(True)
    
    def addNewRepo(self):
        self.repo = RepoDialog.RepoDialog(self)
        self.repo.setCaption('PiSi KGA - Yeni Depo Ekle')
        self.repo.setModal(True)
        self.connect(self.repo.okButton, SIGNAL("clicked()"), self.processNewRepo)
        self.repo.show()

    def removeRepo(self):
        repoItem = self.repoListView.currentItem()
        self.repoListView.takeItem(repoItem)
        pisi.api.remove_repo(repoItem.text(0))
                    
    def processNewRepo(self):
        repoName = str(self.repo.repoNameLineEdit.text())
        repoAddress = str(self.repo.repoAddressLineEdit.text())
        try:
            pisi.api.add_repo(repoName,repoAddress)
        except pisi.repodb.Error:
            KMessageBox.error(self,u"<qt>Depo <b>%s</b> zaten var!</qt>"%(repoName), u"Pisi Hatası")
            return
        item = QListViewItem(self.repoListView,None)
        item.moveItem(self.repoListView.lastChild())
        item.setText(0, repoName)
        item.setText(1, repoAddress)
        self.repo.close()
    
    def updateListView(self):
        self.repoListView.clear()
        
        index = len(self.repoList)-1
        while index >= 0:
            repoName = self.repoList[index]
            item = QListViewItem(self.repoListView,None)
            item.setText(0, self.repoList[index])
            item.setText(1, pisi.api.ctx.repodb.get_repo(str(repoName)).indexuri.get_uri())
            index -= 1

    def customEvent(self,event):
        if event.type() == QEvent.User+3:
            self.repoList = pisi.api.ctx.repodb.list()
            self.updateListView()
            
    def readConfig(self):
        self.repoList = pisi.api.ctx.repodb.list()
        if not len(self.repoList):
            pisi.api.add_repo('uludag', 'http://paketler.uludag.org.tr/pardus-devel/pisi-index.xml')
            self.command.updateRepo('uludag')
