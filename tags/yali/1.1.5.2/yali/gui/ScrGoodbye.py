# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
from qt import *

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.sysutils
import yali.users
import yali.localeutils
import yali.postinstall
from yali.gui.ScreenWidget import ScreenWidget
from yali.gui.YaliDialog import WarningDialog
import yali.gui.context as ctx

##
# Goodbye screen
class Widget(QWidget, ScreenWidget):

    help = _('''
<font size="+2">Congratulations</font>


<font size="+1">
<p>
You have successfully installed Pardus, a very easy to use desktop system on
your machine. Now you can start playing with your system and stay productive
all the time.
</p>
<P>
Click on the Next button to proceed. One note: You remember your password,
don't you?
</p>
</font>
''')

    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
        
        img = QLabel(self)
        img.setPixmap(ctx.iconfactory.newPixmap("goodbye"))

        self.info = QLabel(self)
        self.info.setText(
            _('<b><font size="+2" color="#FF6D19">Rebooting system. Please wait!</font></b>'))
        self.info.hide()
        self.info.setAlignment(QLabel.AlignCenter|QLabel.AlignTop)
        self.info.setMinimumSize(QSize(0,50))

        vbox = QVBoxLayout(self)
        vbox.addStretch(1)

        hbox = QHBoxLayout(vbox)
        hbox.addStretch(1)
        hbox.addWidget(img)
        hbox.addStretch(1)

        vbox.addStretch(1)
        vbox.addWidget(self.info)

    def shown(self):
        from os.path import basename
        ctx.debugger.log("%s loaded" % basename(__file__))
        ctx.screens.disablePrev()
        self.processPendingActions()

    def execute(self):

        ctx.screens.disableNext()

        self.info.show()
        self.info.setAlignment(QLabel.AlignCenter)

        #open(ctx.consts.log_file,"w").write(ctx.debugger.traceback.plainLogs)

        try:
            ctx.debugger.log("Trying to umount %s" % (ctx.consts.target_dir + "/home"))
            yali.sysutils.umount(ctx.consts.target_dir + "/home")
            ctx.debugger.log("Trying to umount %s" % (ctx.consts.target_dir))
            yali.sysutils.umount(ctx.consts.target_dir)
        except:
            ctx.debugger.log("Umount Failed.")
            pass
        
        ctx.debugger.log("Trying to eject the CD.")
        # remove cd...
        w = RebootWidget(self)
        ctx.debugger.log("Show reboot dialog.")
        self.dialog = WarningDialog(w, self)
        self.dialog.exec_loop()

        ctx.debugger.log("Yali, fastreboot calling..")
        yali.sysutils.fastreboot()

    # process pending actions defined in other screens.
    def processPendingActions(self):
        # add users
        for u in yali.users.pending_users:
            ctx.debugger.log("User %s adding to system" % u.username)
            u.addUser()
            ctx.debugger.log("User %s added to system" % u.username)

        # write console keyboard data
        yali.localeutils.write_keymap(ctx.keydata.console)
        ctx.debugger.log("Keymap stored.")

        # migrate xorg.conf
        yali.postinstall.migrate_xorg_conf(ctx.keydata.X)
        ctx.debugger.log("xorg.conf merged.")

class RebootWidget(QWidget):

    def __init__(self, *args):
        QWidget.__init__(self, *args)

        l = QVBoxLayout(self)
        l.setSpacing(20)
        l.setMargin(10)

        warning = QLabel(self)
        warning.setText(_('''<b>
<p>Please remove Pardus CD from your drive and pres Reboot button.</p>
</b>
'''))

        self.reboot = QPushButton(self)
        self.reboot.setText(_("Reboot"))

        buttons = QHBoxLayout(self)
        buttons.setSpacing(10)
        buttons.addStretch(1)
        buttons.addWidget(self.reboot)

        l.addWidget(warning)
        l.addLayout(buttons)

        yali.sysutils.eject_cdrom()

        self.connect(self.reboot, SIGNAL("clicked()"),
                     self.slotReboot)

    def slotReboot(self):
        self.emit(PYSIGNAL("signalOK"), ())
