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

import glob
import os
from os.path import join
from qt import *

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext


import pisi.ui

import yali.pisiiface
import yali.fstab
import yali.postinstall
import yali.sysutils
import yali.localedata
import yali.partitionrequest as request
from yali.gui.installwidget import InstallWidget
from yali.gui.ScreenWidget import ScreenWidget
import yali.gui.context as ctx


def iter_slide_pics():
    # load all pics
    pics = []
    g = glob.glob(ctx.consts.slidepics_dir + "/*.png")
    g.sort()
    for p in g:
        pics.append(QPixmap(p))

    while True:
        for pic in pics:
            yield pic



##
# Partitioning screen.
class Widget(InstallWidget, ScreenWidget):

    help = _('''
<font size="+2">Installation started</font>

<font size="+1">

<p>
Pardus is now being installed on your hard disk. 
</p>

<p>
The duration of this operation depends on the 
capability and power of your system. Meanwhile,
you can enjoy some visual elements showing 
the distinctive properties of Pardus, your 
new operating system.
</p>

<p>
Have fun!
</p>
</font>
''')

    def __init__(self, *args):
        apply(InstallWidget.__init__, (self,) + args)

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"),
                     self.slotChangePix)

        self.iter_pics = iter_slide_pics()

        # show first pic
        self.slotChangePix()

        self.total = 0
        self.cur = 0

    def shown(self):
        # initialize pisi

        # start installer thread
        self.pkg_installer = PkgInstaller(self)
        self.pkg_installer.start()

        ctx.screens.disableNext()
        ctx.screens.disablePrev()

        # start 30 seconds
        self.timer.start(1000 * 30)

        
    def slotNotify(self, parent, event, p):
        # FIXME: use logging
        if event == pisi.ui.installing:
            self.info.setText(_("Installing: %s<br>%s") % (
                    p.name, p.summary))
            
            self.cur += 1
            self.progress.setProgress(self.cur)
        elif event == pisi.ui.configuring:
#            print "lolo configure", p.name
            self.info.setText(_("Configuring package: %s") % p.name)
            
            self.cur += 1
            self.progress.setProgress(self.cur)
            ctx.screens.processEvents()



    def customEvent(self, qevent):

#        print "qevent", qevent, qevent.type()

        # User+1: pisi events
        if qevent.type() == QEvent.User+1:

            p, event = qevent.data()
        
            # FIXME: use logging
            if event == pisi.ui.installing:
                self.info.setText(_("Installing: %s<br>%s") % (
                        p.name, p.summary))

                self.cur += 1
                self.progress.setProgress(self.cur)
            elif event == pisi.ui.configuring:
                self.info.setText(_("Configuring package: %s") % p.name)
            
                self.cur += 1
                self.progress.setProgress(self.cur)

        # User+2: set progress
        elif qevent.type() == QEvent.User+2:
            total = qevent.data()
            self.progress.setTotalSteps(total)


        # User+3: finished
        elif qevent.type() == QEvent.User+3:
            self.finished()


        # User+10: error
        elif qevent.type() == QEvent.User+10:
            err = qevent.data()
            self.installError(err)



    def slotChangePix(self):
        self.pix.setPixmap(self.iter_pics.next())


    def execute(self):
        
        # fill fstab
        fstab = yali.fstab.Fstab()
        for req in ctx.partrequests:
            req_type = req.requestType()
            if req_type == request.mountRequestType:
                p = req.partition()
                pt = req.partitionType()

                path = p.getPath()
                fs = pt.filesystem.name()
                mountpoint = pt.mountpoint
                opts = pt.mountoptions

                e = yali.fstab.FstabEntry(path, mountpoint, fs, opts)
                fstab.insert(e)
            elif req_type == request.swapFileRequestType:
                path = "/" + ctx.consts.swap_file_name
                mountpoint = "none"
                fs = "swap"
                opts = "sw"
                e = yali.fstab.FstabEntry(path, mountpoint, fs, opts)
                fstab.insert(e)

        fstab.close()

        # Configure Pending...       
        # run baselayout's postinstall first
        yali.postinstall.initbaselayout()
        yali.sysutils.chroot_comar() # run comar in chroot
        self.info.setText(_("Configuring packages for your system!"))
        # re-initialize pisi with comar this time.
        ui = PisiUI_NoThread(notify_widget = self)
        yali.pisiiface.initialize(ui=ui, with_comar=True)
        # show progress
        self.cur = 0
        self.progress.setProgress(self.cur)
        self.total = yali.pisiiface.get_pending_len()
        self.progress.setTotalSteps(self.total)
        # run all pending...
        yali.pisiiface.configure_pending()
        yali.pisiiface.finalize()

        # stop slide show
        self.timer.stop()


        # FIXME: I don't know if this is the right way to do
        # this. maybe postinstall can be used too.
        yali.localedata.write_locale_from_cmdline()
#        yali.localedata.write_font_from_cmdline(ctx.keydata)


        return True

    def finished(self):
        # Remove cd repository and install add real
        cd_repo_name = ctx.consts.cd_repo_name # install repo on CD
        pardus_repo_name = ctx.consts.pardus_repo_name
        pardus_repo_uri = ctx.consts.pardus_repo_uri

        yali.pisiiface.remove_repo(cd_repo_name)
        yali.pisiiface.add_repo(pardus_repo_name, pardus_repo_uri)

        yali.pisiiface.finalize()

        # trigger next screen
        ctx.screens.next()

    def installError(self, e):
        #self.info.setText(str(e))
        import yali
        import yali.gui.runner

        err_str = _('''An error during the installation of packages occured.

This is possibly a broken Pardus CD or CD-ROM drive.

Error:
%s
''') % str(e)


        yali.gui.runner.showException(yali.exception_fatal, err_str)
        


class PkgInstaller(QThread):

    def __init__(self, widget):
        QThread.__init__(self)
        self._widget = widget


    def run(self):
        ui = PisiUI(self._widget)

        yali.pisiiface.initialize(ui)

        cd_repo_name = ctx.consts.cd_repo_name
        cd_repo_uri = ctx.consts.cd_repo_uri
        yali.pisiiface.add_repo(cd_repo_name, cd_repo_uri)
        yali.pisiiface.update_repo(cd_repo_name)

        # show progress
        total = yali.pisiiface.get_available_len()
        # User+2: set total steps
        qevent = QCustomEvent(QEvent.User+2)
        qevent.setData(total)
        QThread.postEvent(self._widget, qevent)


        try:
            yali.pisiiface.install_all()
        except Exception, e:
            # User+10: error
            qevent = QCustomEvent(QEvent.User+10)
            qevent.setData(e)
            QThread.postEvent(self._widget, qevent)

        
        # User+3: finished
        qevent = QCustomEvent(QEvent.User+3)
        QThread.postEvent(self._widget, qevent)


class PisiUI(pisi.ui.UI):

    def __init__(self, notify_widget, *args):
        pisi.ui.UI.__init__(self)

        self._notify_widget = notify_widget


    def notify(self, event, **keywords):
        if event == pisi.ui.installing or event == pisi.ui.configuring:
            
            # User+1: pisi notify
            qevent = QCustomEvent(QEvent.User+1)
            data = [keywords['package'], event]
            qevent.setData(data)
#            print "qevent", keywords['package'].name
            QThread.postEvent(self._notify_widget, qevent)



class PisiUI_NoThread(QObject, pisi.ui.UI):

    def __init__(self, notify_widget, *args):
        pisi.ui.UI.__init__(self)
        apply(QObject.__init__, (self,) + args)

        self.connect(self, PYSIGNAL("signalNotify"),
                     notify_widget.slotNotify)

    def notify(self, event, **keywords):
        if event == pisi.ui.installing or event == pisi.ui.configuring:
            self.emit(PYSIGNAL("signalNotify"),
                      (self, event, keywords['package']))

