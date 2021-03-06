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


from qt import *

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext


import yali.users
from yali.gui.ScreenWidget import ScreenWidget
from yali.gui.Ui.setupuserswidget import SetupUsersWidget
import yali.gui.context as ctx
import xcapslock

##
# Partitioning screen.
class Widget(SetupUsersWidget, ScreenWidget):

    help = _('''
<font size="+2">User setup</font>

<font size="+1">
<p>
Other than the system administrator user,
you can create a user account for your 
daily needs, i.e reading your e-mail, surfing
on the web and searching for daily recipe
offerings. Usual password assignment
rules also apply here: This password should 
be unique and private. Choose a password 
difficult to guess, but easy to remember. 
</p>
<p>
Click Next button to proceed.
</p>
</font>
''')

    def __init__(self, *args):
        apply(SetupUsersWidget.__init__, (self,) + args)

        self.pix.setPixmap(ctx.iconfactory.newPixmap("users"))
        self.pass_error.setText("")
        self.createButton.setEnabled(False)

        self.connect(self.pass1, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.pass2, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.username, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)

        self.connect(self.createButton, SIGNAL("clicked()"),
                     self.slotCreateUser)

        self.connect(self.deleteButton, SIGNAL("clicked()"),
                     self.slotDeleteUser)


        self.connect(self.userList, SIGNAL("doubleClicked(QListBoxItem*)"),
                     self.slotEditUser)

        self.connect(self.pass2, SIGNAL("returnPressed()"),
                     self.slotReturnPressed)

    def shown(self):
        self.checkUsers()
        self.checkCapsLock()
        self.username.setFocus()

    def execute(self):
        # reset and fill pending_users
        yali.users.reset_pending_users()

        for i in range(self.userList.count()):
            u = self.userList.item(i).getUser()
            yali.users.pending_users.add(u)

        return True

    def checkCapsLock(self):
        if xcapslock.isOn():
            self.caps_error.setText(
                _('<font color="#FF6D19">Caps Lock is on!</font>'))
        else:
            self.caps_error.setText("")

    def keyReleaseEvent(self, e):
        self.checkCapsLock()

    def slotTextChanged(self):

        p1 = self.pass1.text()
        p2 = self.pass2.text()

        if p2 != p1 and p2:
            self.pass_error.setText(
                _('<font color="#FF6D19">Passwords do not match!</font>'))
            self.pass_error.setAlignment(QLabel.AlignCenter)
            return self.createButton.setEnabled(False)
        else:
            self.pass_error.setText("")


        if self.username.text() and p1 and p2:
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)

    def slotCreateUser(self):
        u = yali.users.User()
        u.username = self.username.text().ascii()
        # ignore last character. see bug #887
        u.realname = unicode(self.realname.text().utf8().data())[:-1]
        u.passwd = self.pass1.text().ascii()
        u.groups = ["users", "pnp", "pnpadmin", "removable", "disk", "audio", "video", "power", "wheel", "dialout"]


        existsInList = [i for i in range(self.userList.count())
                        if self.userList.item(i).getUser().username == u.username]
        # check user validity
        if u.exists() or existsInList:
            self.pass_error.setText(
                _('<font color="#FF6D19">Username exists, choose another one!</font>'))
            return
        elif not u.usernameIsValid():
            self.pass_error.setText(
                _('<font color="#FF6D19">Username contains invalid characters!</font>'))
            return
        elif not u.realnameIsValid():
            self.pass_error.setText(
                _('<font color="#FF6D19">Realname contains invalid characters!</font>'))
            return

        try:
            self.userList.removeItem(self.edititemindex)
            del self.edititemindex
        except:
            # nothing wrong. just adding a new user...
            pass
        i = UserItem(self.userList, user = u)

        # clear all
        self.username.clear()
        self.realname.clear()
        self.pass1.clear()
        self.pass2.clear()

        # give focus to username widget for a new user. #3280
        self.username.setFocus()

        self.checkUsers()


    def slotDeleteUser(self):
        self.userList.removeItem(self.userList.currentItem())
        self.checkUsers()

    def slotEditUser(self, item):
        u = item.getUser()

        self.username.setText(u.username)
        self.realname.setText(u.realname)
        self.pass1.setText(u.passwd)
        self.pass2.setText(u.passwd)

        self.edititemindex = self.userList.currentItem()

    def checkUsers(self):
        if self.userList.count():
            ctx.screens.enableNext()
        else:
            ctx.screens.disableNext()

    def slotReturnPressed(self):
        self.slotCreateUser()


class UserItem(QListBoxText):

    ##
    # @param user (yali.users.User)
    def __init__(self, parent, user):
        apply(QListBoxText.__init__, (self,parent,user.username))
        self._user = user
    
    def getUser(self):
        return self._user

