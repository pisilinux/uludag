#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import sys
import time
import comar
from qt import *
from kdecore import *
from kdeui import *

import browser
import useredit
import groupedit
from utility import *


class UserManager(QWidgetStack):
    def __init__(self, parent):
        try:
            self.link = comar.Link()
        except comar.CannotConnect:
            KMessageBox.sorry(None, i18n("Cannot connect to the COMAR! If it is not running you should start it with the 'service comar start' command in a root console."))
            sys.exit(0)
        self.setupComar()
        
        QWidgetStack.__init__(self, parent)
        self.browse = browser.BrowseStack(self, self.link)
        self.user = useredit.UserStack(self, self.link)
        self.useredit = useredit.UserStack(self, self.link, edit=True)
        self.group = groupedit.GroupStack(self, self.link)
    
    def setupComar(self):
        self.link.localize()
        self.notifier = QSocketNotifier(self.link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        
        # Access control
        self.link.can_access("User.Manager.addUser", id=1000)
    
    def waitComar(self):
        dia = KProgressDialog(None, "lala", i18n("Waiting COMAR..."),
            i18n("Connection to the COMAR unexpectedly closed, trying to reconnect..."), True)
        dia.progressBar().setTotalSteps(50)
        dia.progressBar().setTextEnabled(False)
        dia.show()
        start = time.time()
        while time.time() < start + 5:
            try:
                self.link = comar.Link()
                dia.close()
                self.setupComar()
                return
            except comar.CannotConnect:
                pass
            if dia.wasCancelled():
                break
            percent = (time.time() - start) * 10
            dia.progressBar().setProgress(percent)
            qApp.processEvents(100)
        dia.close()
        KMessageBox.sorry(None, i18n("Cannot connect to the COMAR! If it is not running you should start it with the 'service comar start' command in a root console."))
        KApplication.kApplication().quit()
    
    def slotComar(self, sock):
        try:
            reply = self.link.read_cmd()
        except comar.LinkClosed:
            self.notifier = None
            self.waitComar()
            self.browse.link = self.link
            self.user.link = self.link
            self.useredit.link = self.link
            self.group.link = self.link
            return
        
        id = reply.id
        if id == 1:
            self.browse.comarUsers(reply)
        elif id == 2:
            self.browse.comarGroups(reply)
        elif id == 3:
            self.user.slotAddReply(reply)
        elif id == 4:
            self.group.slotAddReply(reply)
        elif id == 5:
            self.useredit.slotInfo(reply)
        elif id == 6:
            self.useredit.slotEditReply(reply)
        elif id == 1000:
            self.browse.slotAccessReply(reply)
    
    def slotCancel(self):
        self.raiseWidget(self.browse)
    
    def slotAdd(self):
        if self.browse.tab.currentPageIndex() == 0:
            names = []
            item = self.browse.users.firstChild()
            while item:
                names.append(item.nick)
                item = item.nextSibling()
            self.raiseWidget(self.user)
            self.user.startAdd(self.browse.groups, names)
        else:
            self.raiseWidget(self.group)
            self.group.startAdd()
    
    def slotEdit(self):
        self.raiseWidget(self.useredit)
        self.useredit.startEdit(self.browse.groups, self.browse.users.selectedItem().uid)
