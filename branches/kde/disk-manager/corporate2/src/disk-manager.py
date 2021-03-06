#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

# Python Modules
import os
import sys
import dbus
import functools
import string
import parted

# KDE/QT Modules
from qt import *
from kdeui import *
from kfile import *
from khtml import *
from kdecore import *

# Widget
from diskform import mainForm

from plinklabel import PLinkLabel

# COMAR
import comar

# DBus event loop
from dbus.mainloop.qt3 import DBusQtMainLoop

version = '2.1.4'

"""
A util list for HAL. It is used for storing volume device changes.
Plugging and removing volumes effects it.
"""
deviceList = {}

# HAL related variables.
# These are used for configuring communication with 'hald'.
serviceName = 'org.freedesktop.Hal'
interfaceName =  '/org/freedesktop/Hal/Manager'
managerName = 'org.freedesktop.Hal.Manager'
deviceManagerName = 'org.freedesktop.Hal.Device'

"""
diskForm pointer. This is set in main function and used in
hal daemon communication functions (such as deviceAdded function).
"""
dmWidget = None 

def AboutData():
    about_data = KAboutData('disk-manager',
                            'Disk Manager',
                            version,
                            'Disk Manager Interface',
                            KAboutData.License_GPL,
                            '(C) 2006-2010 UEKAE/TÜBİTAK',
                            None, None,
                            'gokmen@pardus.org.tr')
    about_data.addAuthor('Gökmen GÖKSEL', None, 'gokmen@pardus.org.tr')
    return about_data

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def loadIconSet(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIconSet(name, group, size)

class MountDialog(QDialog):
    def __init__(self, parent = None, name = None, modal = 0, fl = 0, partition = None):
        QDialog.__init__(self, parent, name, modal, fl)
        self.setCaption(i18n('Mount'))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed, 0, 0, self.sizePolicy().hasHeightForWidth()))

        self.partition = partition

        layout = QGridLayout(self, 2, 3 ,8, 8)
        layout.setResizeMode(QLayout.Fixed)

        self.buttonGroup = QButtonGroup(self)
        bgLayout = QGridLayout(self.buttonGroup, 6, 6, 8, 2)
        layout.addMultiCellWidget(self.buttonGroup, 0, 0, 0, 2)
        #self.buttonGroup.setFrameShape(QFrame.NoFrame)

        self.savedOptions = QRadioButton(i18n("Mount to system saved point"), self.buttonGroup)
        bgLayout.addMultiCellWidget(self.savedOptions, 0, 0, 0, 5)

        self.savedLabel = QLabel(self.buttonGroup, "savedLabel")
        bgLayout.addMultiCellWidget(self.savedLabel, 1, 1, 1, 5)

        self.belowOptions = QRadioButton(i18n("Mount to chosen point"), self.buttonGroup)
        bgLayout.addMultiCellWidget(self.belowOptions, 2, 2, 0, 5)

        self.mountPointInfoLabel = QLabel(i18n("Mount Point:"), self.buttonGroup)
        bgLayout.addMultiCellWidget(self.mountPointInfoLabel, 3, 3, 0, 5)

        self.mountPointEdit = QLineEdit(self.buttonGroup, "mountPointEdit")
        bgLayout.addMultiCellWidget(self.mountPointEdit, 4, 4, 0, 4)

        self.mountBrowseButton = QPushButton(self.buttonGroup, "mountBrowseButton")
        self.mountBrowseButton.setText("...")
        bgLayout.addMultiCellWidget(self.mountBrowseButton, 4, 4, 5, 5)

        self.cancelButton = QPushButton(self, "cancelButton")
        self.cancelButton.setText(i18n("Cancel"))
        layout.addWidget(self.cancelButton, 1, 1)

        self.mountButton = QPushButton(self,"mountButton")
        self.mountButton.setText(i18n("Mount"))
        layout.addWidget(self.mountButton, 1, 2)

        spacer = QSpacerItem(10, 2, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer, 1, 0)

        self.connect(self.cancelButton, SIGNAL('clicked()'), self, SLOT('reject()'))
        self.connect(self.mountButton, SIGNAL('clicked()'), SLOT('accept()'))
        self.connect(self.mountBrowseButton, SIGNAL('clicked()'), self.browseMountPoint)
        self.connect(self.savedOptions, SIGNAL("toggled(bool)"), self.slotToggle)
        self.connect(self.belowOptions, SIGNAL("toggled(bool)"), self.slotToggle)

        if partition.isInEntries:
            self.savedOptions.setOn(True)
            self.savedLabel.setText(i18n("Partition is going to mount %s" % partition.mountPoint))
            self.savedOptions.show()
            self.savedLabel.show()
            self.belowOptions.show()
        else:
            self.belowOptions.setOn(True)
            self.savedLabel.setText(i18n("There is no saved data for %s" % partition.name))
            self.savedOptions.hide()
            self.savedLabel.hide()
            self.belowOptions.show()

    def browseMountPoint(self):
        mountPoint = QFileDialog.getExistingDirectory(
            "/media",
            self,
            "browse mount point",
            i18n("Browse mount point"),
            True )
        self.mountPointEdit.setText(mountPoint)

    def accept(self):
        if self.savedOptions.isOn():
            QDialog.accept(self)
            return

        if not os.path.ismount(str(self.mountPointEdit.text())):
            if os.path.exists(str(self.mountPointEdit.text())):
                QDialog.accept(self)
            else:
                KMessageBox.sorry(self, i18n("Path is not valid. Select a valid one."), i18n('Error'))
        else:
            KMessageBox.sorry(self, i18n("Another filesystem has been mounted this path. Select a different one."), i18n('Error'))


    def exec_loop(self):
        if QDialog.exec_loop(self):
            if self.savedOptions.isOn():
                return self.partition.mountPoint
            else:
                return str(self.mountPointEdit.text())
        else:
            return False

    def slotToggle(self):
        if self.savedOptions.isOn():
            self.savedLabel.setEnabled(True)
            self.mountBrowseButton.setEnabled(False)
            self.mountPointEdit.setEnabled(False)
        else:
            self.savedLabel.setEnabled(False)
            self.mountBrowseButton.setEnabled(True)
            self.mountPointEdit.setEnabled(True)

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(i18n('Disk Manager'))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 300)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)
        self.lang_code = os.environ['LANG'][:5].split('_')[0].lower()
        if os.path.isdir(locate('data', 'disk-manager/help/%s/'%self.lang_code)):
            self.htmlPart.openURL(KURL(locate('data', 'disk-manager/help/%s/main_help.html'%self.lang_code)))
        else:
            self.htmlPart.openURL(KURL(locate('data', 'disk-manager/help/en/main_help.html')))

class PartitionInfo():
    def __init__(self, name):
        self.name = name # /dev/sda1
        self.isInEntries = False
        self.mountPoint = None
        self.fsType = None
        self.isMounted = False
        self.uuid = None
        self.size = None

class diskForm(mainForm):
    def __init__(self, parent=None, name=None):
        mainForm.__init__(self, parent, name)
        self.link = comar.Link()
        # Connections
        self.connect(self.list_main, SIGNAL('selectionChanged()'), self.slotList)
        self.connect(self.combo_fs, SIGNAL('activated(const QString&)'), self.slotFS)
        self.connect(self.btn_reset, SIGNAL('clicked()'), self.slotReset)
        self.connect(self.btn_update, SIGNAL('clicked()'), self.slotUpdate)
        #self.connect(self.btn_mount, SIGNAL('clicked()'), self.slotMount)
        self.connect(self.frame_entry, SIGNAL('toggled(bool)'), self.slotToggle)

        self.list_main.header().hide()
        self.frame_detail.setEnabled(False)
        #self.frame_detail.hide()

        layout = QGridLayout(self.mountFrame, 1, 7, 0, 4)

        self.infoIconLabel = QLabel(self.mountFrame, "mountInfoIconLabel")
        self.infoIconLabel.setPixmap(loadIcon('info', size=16))
        layout.addWidget(self.infoIconLabel, 0, 0)

        self.infoLabel1 = QLabel(self.mountFrame, "mountInfoLabel1")
        self.infoLabel1.setAlignment(Qt.SingleLine)
        layout.addWidget(self.infoLabel1, 0, 1)

        self.clickLabel = PLinkLabel(self.mountFrame, "mountClickLabel")
        layout.addWidget(self.clickLabel, 0, 2)

        self.infoLabel2 = QLabel(self.mountFrame, "mountInfoLabel2")
        layout.addWidget(self.infoLabel2, 0, 3)

        self.clickLabel2 = PLinkLabel(self.mountFrame, "mountClickLabel2")
        layout.addWidget(self.clickLabel2, 0, 4)

        self.infoLabel3 = QLabel(self.mountFrame, "mountInfoLabel3")
        layout.addWidget(self.infoLabel3, 0, 5)

        layout.addItem(QSpacerItem(2, 2, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 6)

        self.mountFrame.layout = layout

        self.old = None
        self.pixBase = self.bindPixmaps(loadIcon("drive-harddisk.png", size=32), loadIcon("cancel", size=16), KGlobalSettings.baseColor())
        self.pixHighlight = self.bindPixmaps(loadIcon("drive-harddisk.png", size=32), loadIcon("cancel", size=16), KGlobalSettings.highlightColor())

        self.knownFS = [
            ('ext4', 'ext4'),
            ('ext3', 'ext3'),
            ('ext2', 'ext2'),
            ('reiserfs', 'Reiser FS'),
            ('xfs', 'XFS'),
            ('ntfs-3g', 'NTFS'),
            ('vfat', 'Fat 16/32'),
        ]

        self.fsOptions = {
            "vfat"      : "quiet,shortname=mixed,dmask=007,fmask=117,utf8,gid=6",
            "ext2"      : "noatime",
            "ext3"      : "noatime",
            "ext4"      : "noatime",
            "ntfs-3g"   : "dmask=007,fmask=117,locale=tr_TR.UTF-8,gid=6",
            "reiserfs"  : "noatime",
            "xfs"       : "noatime",
        }

        for name, label in self.knownFS:
            self.combo_fs.insertItem(label)

        self.initialize()

        # Listen signals
        self.link.listenSignals("Disk.Manager", self.signalHandler)

    def getFSName(self):
        for name, label in self.knownFS:
            if label == self.combo_fs.currentText():
                return name
        return None

    def setFSName(self, fsname):
        for name, label in self.knownFS:
            if fsname == name:
                self.combo_fs.setCurrentText(label)
                return
        # Unknown FS type, add to list
        self.knownFS.append((fsname, fsname))
        self.combo_fs.insertItem(fsname)
        self.combo_fs.setCurrentText(fsname)

    def handleOpenMediaEvents(self):
        item = self.list_main.selectedItem()
        if not item:
            return
        part = str(self.items[item])
        pi = self.partitions[part]
        os.system('/usr/bin/xdg-open '+pi.mountPoint)

    def handleMountLinkEvents(self):
        item = self.list_main.selectedItem()
        if not item:
            return
        part = str(self.items[item])
        pi = self.partitions[part]
        if pi.isMounted:
            if KMessageBox.Yes == KMessageBox.questionYesNo(
                    self,
                    i18n("Do you want to unmount '%s'?" % part),
                    i18n("Unmount"),
                    KStdGuiItem.yes(),
                    KStdGuiItem.no()
                ):
                self.mount(False, part)
        else:
            dialog = MountDialog(self, partition=pi)
            mountPoint = dialog.exec_loop()
            if mountPoint:
                self.mount(True, part, mountPoint)

    def initialize(self):

        self.frame_detail.setEnabled(False)
        self.resetMountInfoFrame()

        # Package
        self.package = None

        # Entries in the fstab. device name, file system type etc. all available
        # These entries are the only ones about disk devices
        self.entries = {}

        # Disk devices in the system. (/dev/sda, /dev/sdb...)
        self.devices = []

        # All partitions in the system and information about them. Stores PartitionInfo objects
        self.partitions = {}

        # Items
        self.items = {}

        # Get entries
        self.link.Disk.Manager.listEntries(async=self.asyncListEntries)

        # for setting icon background correctly
        self.old = None


    def signalHandler(self, package, signal, args):
        self.initialize()
        self.frame_detail.setEnabled(False)
        #self.frame_detail.hide()

    def asyncUmount(self, device, package, exception, result):
        """
        Asynchronous umount function displays if any error occurs.
        """
        if not exception:
            self.initialize()
            self.frame_detail.setEnabled(False)
            #self.frame_detail.hide()
        else:
            if unicode(exception.message).startswith("tr.org.pardus.comar"):
                #self.btn_mount.setEnabled(True)
                pass
            else:
                KMessageBox.sorry(self, unicode(exception.message))

    def asyncMount(self, device, path, package, exception, result):
        """
        Asynchronous mount function displays if any error occurs.
        """
        if not exception:
            self.initialize()
            self.frame_detail.setEnabled(False)
            #self.frame_detail.hide()
        else:
            if unicode(exception.message).startswith("tr.org.pardus.comar"):
                pass
                #self.btn_mount.setEnabled(True)
            else:
                KMessageBox.sorry(self, unicode(exception.message))

    def asyncListEntries(self, package, exception, result):
        """
        Entries that are in the fstab file
        """
        if not self.package:
            self.package = package
        else:
            return
        if not exception:
            for device in result[0]:
                self.entries[device] = self.link.Disk.Manager[self.package].getEntry(device)
            # Get devices
            self.link.Disk.Manager[self.package].getDevices(async=self.asyncGetDevices)

    def humanReadableSize(self, size, precision=".1"):
        symbols, depth = [' B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'], 0
        while size > 1000 and depth < 8:
            size = float(size / 1024)
            depth += 1
        if size == 0:
            return "0 B"
        fmt = "%%%sf %%s" % precision
        return fmt % (size, symbols[depth])

    def asyncGetDevices(self, package, exception, result):
        """
        Handles the disk devices in the system such as /dev/sda, /dev/sdb etc.
        """
        if not exception:
            self.list_main.clear()
            for device in result[0]:
                self.devices.append(device)
                try:
                    dsk = parted.Disk(parted.Device(device))
                except Exception, e:
                    continue
                model = dsk.device.model
                size = self.humanReadableSize(dsk.device.getSize(unit="B"))
                label = "%s  (%s)\n%s" % (device, size, model)
                disk = QListViewItem(self.list_main, label)
                disk.setMultiLinesEnabled(True)
                disk.setPixmap(0,loadIcon('drive-harddisk.png', size=32))
                disk.setOpen(True)
                disk.setVisible(False)
                # Get parts
                self.link.Disk.Manager[package].getDeviceParts(device, async=functools.partial(self.asyncGetPartitions, disk))

    def bindPixmaps(self, background, foreground, color):
        pix = QPixmap(36, 36)
        pix.fill(color)
        painter = QPainter(pix)
        #painter.begin(pix)
        painter.drawPixmap(0,0,background)
        painter.drawPixmap(20,20,foreground)
        painter.end()
        return pix


    def asyncGetPartitions(self, listItem, package, exception, result):
        """
        Handles partitions of a specific disk device.
        For example, /dev/sda1 and /dev/sda2 are partitions of disk device /dev/sda.
        """
        if not exception:
            for part in result[0]:
                pinfo = PartitionInfo(part)
                self.partitions[part] = pinfo
                if part in self.entries:
                    pinfo.isInEntries = True
                    entryMountPoint = self.entries[part][0]
                    pinfo.mountPoint = entryMountPoint
                    pinfo.fsType = self.entries[part][1]
                    dsk = parted.Disk(parted.Device(part.rstrip(string.digits)))
                    partition = dsk.getPartitionByPath(part)
                    size = self.humanReadableSize(partition.getSize(unit="B"))
                    pinfo.size = size
                    label = "%s (%s)\n%s" % (part, size, entryMountPoint)
                else:
                    dsk = parted.Disk(parted.Device(part.rstrip(string.digits)))
                    fstype = self.getFSType(part)
                    pinfo.fsType = fstype
                    label = "%s\n%s" % (part, fstype.upper())
                path = self.link.Disk.Manager[self.package].isMounted(part)
                if path:
                    pinfo.isMounted = True
                    pinfo.mountPoint = path
                    pixie = loadIcon('drive-harddisk.png', size=32)
                else:
                    pixie = self.pixBase
                listItem.setVisible(True)
                disk_part = QListViewItem(listItem, label)
                disk_part.setMultiLinesEnabled(True)
                disk_part.setPixmap(0, pixie)
                self.items[disk_part] = part

    def slotToggle(self, checked):
        if checked:
            self.slotFS()

    def slotFS(self, text=""):
        item = self.list_main.selectedItem()
        if not item:
            return
        device = str(self.items[item])
        part = self.partitions[device]
        fsType = part.fsType
        self.setFSName(fsType)
        options = self.fsOptions.get(fsType, "defaults")
        self.line_opts.setText(options)

    def getFSType(self, part):
        return self.link.Disk.Manager[self.package].getFSType(part)

    def mount(self, mount, part, mountPoint=""):
        """ buraları                                    düzenleeeeeeeeeeeeeeeeeeee         !!!!!!!!!!!
        Triggered when mount/umount button clicked. If the selected 
        partition is not mounted this function calls mount function 
        otherwise calls umount function.
        """
        #item = self.list_main.selectedItem()
        #device = str(self.items[item])
        try:
            if mount:
                self.link.Disk.Manager.mount(part, mountPoint, async=functools.partial(self.asyncMount, part, ''))
            else:
                self.link.Disk.Manager.umount(part, async=functools.partial(self.asyncUmount, part))
        except Exception, e:
            if e.message.startswith("tr.org.pardus.comar"):
                pass
            else:
                KMessageBox.sorry(self, unicode(e.message))
        # This is for preventing user to push repeatedly.
        #self.btn_mount.setEnabled(False)

    def isMounted(self, partition):
        return self.partitions[partition].isMounted

    def slotList(self):
        item = self.list_main.selectedItem()
        if self.old:
            self.old.setPixmap(0, self.pixBase)
        if item not in self.items:
            self.frame_detail.setEnabled(False)
            self.resetMountInfoFrame()
            #self.frame_detail.hide()
            return
        device = str(self.items[item])
        if not self.isMounted(device):
            item.setPixmap(0, self.pixHighlight)
            self.old = item
        if device not in self.entries:
            self.line_mountpoint.setText("")
            self.line_opts.setText("")
            self.combo_fs.setCurrentText(self.knownFS[0][1])
            self.frame_entry.setChecked(False)
        else:
            options = []
            for key, value in self.entries[device][2].iteritems():
                if value:
                    options.append("%s=%s" % (key, value))
                else:
                    options.append(key)
            self.line_mountpoint.setText(self.entries[device][0])
            self.line_opts.setText(",".join(options))
            self.setFSName(self.entries[device][1])
            self.frame_entry.setChecked(True)
        self.frame_detail.setEnabled(True)

        if self.isMounted(device):
            #self.btn_mount.setText(i18n('Unmount'))
            self.frame_entry.setEnabled(True)
            self.frame_detail.show()
            #self.btn_mount.setEnabled(True)
        else:
            # This partition is not mounted.
            fstype = self.partitions[device].fsType
            if fstype == 'swap' or fstype == 'LVM2_member':
                # If partition is a swap or LVM member there won't be mount option.
                self.frame_entry.setEnabled(False)
                #self.frame_detail.hide()
                #self.btn_mount.setEnabled(False)
            else:
                # Partition is not mounted and other than a swap.
                # Enable the mount button and set its text as 'mount'.
                #self.btn_mount.setText(i18n('Mount'))
                self.frame_entry.setEnabled(True)
                #self.btn_mount.setEnabled(True)
                self.frame_detail.show()
        self.updateMountFrame(device)

    def resetMountInfoFrame(self):
        self.infoLabel1.setText(i18n("Select a partition"))
        self.clickLabel.setLinkText("")
        self.infoLabel2.setText("")
        self.clickLabel2.setLinkText("")
        self.infoLabel3.setText("")

    def updateMountFrame(self, part):
        pi = self.partitions[part]
        if self.isMounted(part):
            msg = unicode(i18n("%s is mounted to <b>%s</b>. Click <b>here</b> to unmount" % (part, pi.mountPoint)))
            p1 = msg.split("<b>")
            p2 = p1[1].split("</b>")
            p3 = p1[2].split("</b>")
            self.infoLabel1.setText(p1[0])
            self.clickLabel.setLinkText(p2[0])
            self.infoLabel2.setText(p2[1])
            self.clickLabel2.setLinkText(p3[0])
            self.infoLabel3.setText(p3[1])
            self.clickLabel.method = self.handleOpenMediaEvents
            self.clickLabel2.method = self.handleMountLinkEvents
        else:
            msg = unicode(i18n("%s is not mounted. Click <b>here</b> to mount." % part))
            p1 = msg.split("<b>")
            p2 = p1[1].split("</b>")
            self.infoLabel1.setText(p1[0])
            self.clickLabel.setLinkText(p2[0])
            self.infoLabel2.setText(p2[1])
            self.clickLabel2.setLinkText("")
            self.infoLabel3.setText("")
            self.clickLabel.method = self.handleMountLinkEvents
        if pi.fsType == "swap":
            self.infoLabel1.setText(i18n("This is a swap partition."))
            self.clickLabel.setLinkText("")
            self.infoLabel2.setText("")
            self.clickLabel2.setLinkText("")
            self.infoLabel3.setText("")

    def slotUpdate(self):
        item = self.list_main.selectedItem()
        if item not in self.items:
            self.frame_detail.setEnabled(False)
            #self.frame_detail.hide()
            return
        device = str(self.items[item])
        if self.frame_entry.isChecked():
            # Path
            path = str(self.line_mountpoint.text())
            # FS type
            fsType = str(self.getFSName())
            # Options
            options = {}
            for opt in str(self.line_opts.text()).split(","):
                if "=" in opt:
                    key, value = opt.split("=", 1)
                    options[key] = value
                else:
                    options[opt] = ""
            try:
                # Get the mount path for related partition. This must be
                # stored before call of the addEntry function.
                mountPoint = self.partitions[device].mountPoint
                # Try to add an entry for this partition to fstab.
                # Add entry function also mounts a partition if it is
                # not mounted.
                self.link.Disk.Manager[self.package].addEntry(device, path, fsType, options)
                # Entry added. Before saving an entry if the partition
                # mounted a point which is different from entry's path,
                # say to user that it is saved but not mounted to entry's
                # path beacause it is mounted another point.
                if mountPoint and not mountPoint == path:
                    KMessageBox.sorry(self, i18n("Changes saved but system couldn't mount it because it has been already mounted another point"))
            except dbus.DBusException, e:
                if e.message.startswith("tr.org.pardus.comar"):
                    pass
                else:
                    KMessageBox.sorry(self, unicode(e.message))
        else:
            path = str(self.line_mountpoint.text())
            if path == '/boot':
                confirm = KMessageBox.questionYesNo(self, i18n("Removing this partition from auto mount list can cause some boot problems.\nDo you want to continue?"), i18n("Warning"))
                if confirm == KMessageBox.Yes:
                    pass
                else:
                    return
            try:
                self.link.Disk.Manager[self.package].removeEntry(device)
            except Exception, e:
                if e.message.startswith("tr.org.pardus.comar"):
                    pass
                else:
                    KMessageBox.sorry(self, unicode(e.message))

    def slotReset(self):
        name = self.getFSName()
        if name in self.fsOptions:
            self.line_opts.setText(self.fsOptions[name])
        else:
            self.line_opts.setText("")

    def slotHelp(self):
        self.helpwin = HelpDialog(self)
        self.helpwin.show()

    def slotQuit(self):
        self.combo_fs.clear()
        # self.frame_detail.hide()


class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue('disk-manager')
        KGlobal.iconLoader().addAppDir('disk-manager')
        self.config = KConfig('disk-manager')
        self.aboutdata = AboutData()
        widget = diskForm(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(widget)

    def aboutData(self):
        return self.aboutdata

def create_disk_manager(parent, name):
    global kapp
    kapp = KApplication.kApplication()
    if not dbus.get_default_main_loop():
        DBusQtMainLoop(set_as_default=True)
    return Module(parent, name)

def deviceAdded(udi):
    """
    Triggered when a device added to system by hal daemon. Adds device
    to the device list if it is a volume device and reinits disk form.
    """
    if not deviceList.has_key(udi):
        device = dbus.SystemBus().get_object(serviceName, udi)
        deviceInterface = dbus.Interface(device, deviceManagerName)
        try:
            if deviceInterface.GetProperty('info.category') == 'volume':
                deviceList[udi] = udi
                dmWidget.initialize()
                dmWidget.frame_detail.setEnabled(False)
                #self.frame_detail.hide()
        except Exception, e:
            pass

def deviceRemoved(udi):
    """
    Triggered when a device removed from system by hal daemon. Deletes
    related device if it is in our device list and reinits disk form.
    """
    if deviceList.has_key(udi):
        del deviceList[udi]
        dmWidget.initialize()
        dmWidget.frame_detail.setEnabled(False)
        #self.frame_detail.hide()

def main():
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    if not KUniqueApplication.start():
        print i18n('Disk Manager is already running!')
        return
    app = KUniqueApplication(True, True, True)


    DBusQtMainLoop(set_as_default=True)

    win = QDialog()
    win.setCaption(i18n('Disk Manager'))
    win.setIcon(loadIcon('disk_manager', size=128))
    widget = diskForm(win)
    toplayout = QVBoxLayout(win, 0, KDialog.spacingHint())
    toplayout.addWidget(widget)

    # Set global variable for further usages.
    global dmWidget
    dmWidget = widget

    # Connect to SystemBus
    systemBus = dbus.SystemBus()
    dbusService = systemBus.get_object(serviceName, interfaceName)
    halInterface = dbus.Interface(dbusService, managerName)

    # Connect to Device{Added/Removed} signals
    systemBus.add_signal_receiver(deviceAdded, 'DeviceAdded',  managerName, serviceName, interfaceName)
    systemBus.add_signal_receiver(deviceRemoved, 'DeviceRemoved',  managerName, serviceName, interfaceName)


    # Generate Global Device List
    for device in halInterface.GetAllDevices():
        deviceList[device] = device

    app.setMainWidget(win)
    app.connect(app, SIGNAL("lastWindowClosed()"), widget.slotQuit)

    sys.exit(win.exec_loop())

if __name__ == '__main__':
    main()
