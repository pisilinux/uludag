# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import copy
import parted
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext


from PyQt4 import QtGui
from PyQt4.QtCore import *

import yali.util
import yali.context as ctx
from yali.gui.YaliDialog import Dialog, QuestionDialog
from yali.gui.ScreenWidget import ScreenWidget

from yali.gui.partition_gui import PartitionEditor
from yali.gui.lvm_gui import LVMEditor
from yali.gui.raid_gui import RaidEditor
from yali.gui.Ui.manualpartwidget import Ui_ManualPartWidget
from yali.storage.library import lvm
from yali.storage import formats
from yali.storage.devices.device import devicePathToName, Device
from yali.storage.devices.partition import Partition
from yali.storage.partitioning import doPartitioning, hasFreeDiskSpace, PartitioningError, PartitioningWarning
from yali.storage.storageBackendHelpers import doDeleteDevice, doClearPartitionedDevice, checkForSwapNoMatch, getPreExistFormatWarnings, confirmResetPartitionState

class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Manual Partitioning')
    desc = _('You can easily configure your partitions...')
    icon = "iconPartition"
    helpSummary = _("Partition manual summary")
    help = _('''
<p>
In this screen, you can manually partition your disk. You can select 
existing partitions and resize or delete them. You can create new 
partition(s) in the empty parts, make Pardus use them for system files, 
users' home directories, swap space or general use. The changes that you 
make will not be applied until you go on with the installation, 
which means you can revert if you make any unwanted changes or change your configuration.
</p>
<p>
Please refer to Pardus Installing and Using Guide for more information
about disk partitioning.
</font>
''')


    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_ManualPartWidget()
        self.ui.setupUi(self)
        self.storage = ctx.storage
        self.intf = ctx.interface

        # New Device Popup Menu
        self.setupMenu()

        #self.connect(self.ui.newButton, SIGNAL("clicked()"),self.createDevice)
        self.connect(self.ui.editButton, SIGNAL("clicked()"),self.editDevice)
        self.connect(self.ui.deleteButton, SIGNAL("clicked()"),self.deleteDevice)
        self.connect(self.ui.resetButton, SIGNAL("clicked()"),self.reset)
        self.connect(self.ui.deviceTree, SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self.activateButtons)
        self.connect(self.menu, SIGNAL("triggered(QAction*)"), self.createDevice)

        # self.ui.deviceTree.hide()
        self._active_device = None

        self.ui.GGdeviceTree = BlockGroup(self, _("Hard Drives"))
        self.ui.verticalLayout.addWidget(self.ui.GGdeviceTree)

        self.ui.GGVdeviceTree = BlockGroup(self, _("Volume Groups"))
        self.ui.verticalLayout.addWidget(self.ui.GGVdeviceTree)

        self.ui.GGRdeviceTree = BlockGroup(self, _("Raid Arrays"))
        self.ui.verticalLayout.addWidget(self.ui.GGRdeviceTree)

    def shown(self):
        checkForSwapNoMatch(self.intf, self.storage)
        self.populate()
        (errors, warnings) =  self.storage.sanityCheck()
        if errors or warnings:
            ctx.mainScreen.disableNext()
        else:
            ctx.mainScreen.enableNext()

    def execute(self):
        ctx.logger.info("Manual Partitioning selected...")
        ctx.mainScreen.processEvents()
        check = self.nextCheck()
        if not check:
            ctx.mainScreen.enableBack()
        elif check is None:
            ctx.mainScreen.enableNext()
        return check

    def update(self):
        if self.storage.storageset.rootDevice:
            ctx.mainScreen.enableNext()
        else:
            ctx.mainScreen.disableNext()
        self.updateMenus()

    def activateButtons(self, item, index):
        if item:
            if isinstance(item.device, Device) and not isinstance(item.device, parted.partition.Partition):
                self.ui.editButton.setEnabled(True)
                self.ui.deleteButton.setEnabled(True)
            else:
                self.ui.editButton.setEnabled(False)
                self.ui.deleteButton.setEnabled(False)

    def nextCheck(self):
        (errors, warnings) = self.storage.sanityCheck()
        if errors:
            detailed =  _("The partitioning scheme you requested\n"
                          "caused the following critical errors.\n"
                          "You must correct these errors before\n"
                          "you continue your installation of %s." %
                          yali.util.product_name())

            comments = "\n\n".join(errors)
            self.intf.detailedMessageWindow(_("Partitioning Errors"),
                                             detailed, comments, type="ok")
            return False

        if warnings:
            detailed = _("The partitioning scheme you requested generated the \n"
                         "following warnings. Would you like to continue with \n"
                         "your requested partitioning "
                         "scheme?")

            comments = "\n\n".join(warnings)
            rc = self.intf.detailedMessageWindow(_("Partitioning Warnings"),
                                                  detailed, comments, type="custom",
                                                  customButtons=[_("Ok"), _("Cancel")], default=1)
            if rc == 1:
                return False

        formatWarnings = getPreExistFormatWarnings(self.storage)
        if formatWarnings:
            detailed = _("The following pre-existing devices have\n"
                         "been selected to be formatted, destroying\n"
                         "all data.")

            comments = ""
            for (device, type, mountpoint) in formatWarnings:
                comments = comments + "%s         %s         %s\n" % (device, type, mountpoint)

            rc = self.intf.detailedMessageWindow(_("Format Warnings"),
                                                  detailed, comments, type="custom",
                                                  customButtons=[_("Format"), _("Cancel")], default=1)
            if rc:
                return False

        return True


    def backCheck(self):
        rc = self.intf.messageWindow(_("Warning"), _("All Changes that you made will be removed"),
                                      type="custom", customIcon="question",
                                      customButtons=[_("Ok"), _("Cancel")], default=1)
        if not rc:
            self.storage.reset()
            return True
        return False

    def setupMenu(self):
        self.menu = QtGui.QMenu("New")
        self.standardDevices = self.menu.addMenu(_("Standard"))
        self.lvmDevices = self.menu.addMenu(_("LVM"))
        self.raidDevices = self.menu.addMenu(_("RAID"))

        self.createPartition = self.standardDevices.addAction(_("Partition"))
        self.createPartition.setWhatsThis(_("General purpose of partition creation"))
        self.createPartition.setVisible(False)
        self.createPhysicalVolume = self.lvmDevices.addAction(_("Physical Volume"))
        self.createPhysicalVolume.setWhatsThis(_("Create LVM formatted partition"))
        self.createPhysicalVolume.setVisible(False)
        self.createVolumeGroup = self.lvmDevices.addAction(_("Volume Group"))
        self.createVolumeGroup.setWhatsThis(_("Requires at least 1 free LVM formatted partition"))
        self.createVolumeGroup.setVisible(False)
        self.createLogicalVolume = self.lvmDevices.addAction(_("Logical Volume"))
        self.createLogicalVolume.setWhatsThis(_("Create Logical Volume on selected Volume Group"))
        self.createLogicalVolume.setVisible(False)
        self.createRaidMember = self.raidDevices.addAction(_("Member"))
        self.createRaidMember.setWhatsThis(_("Create Raid formatted partition"))
        self.createRaidMember.setVisible(False)
        self.createRaidArray= self.raidDevices.addAction(_("Array"))
        self.createRaidArray.setWhatsThis(_("Requires at least 2 free Raid formatted partition"))
        self.createRaidArray.setVisible(False)

        self.ui.newButton.setMenu(self.menu)

    def addDevice(self, device, item, GGitem = None):
        if device.format.hidden:
            return

        format = device.format

        if not format.exists:
            formatIcon = QtGui.QIcon(":/images/tick.png")
        else:
            formatIcon = QtGui.QIcon(":/images/dialog-error.png")

        # mount point string
        if format.type == "lvmpv":
            vg = None
            for _vg in self.storage.vgs:
                if _vg.dependsOn(device):
                    vg = _vg
                    break
            mountpoint = getattr(vg, "name", "")
        elif format.type == "mdmember":
            array = None
            for _array in self.storage.raidArrays:
                if _array.dependsOn(device):
                    array = _array
                    break

            mountpoint = getattr(array, "name", "")
        else:
            mountpoint = getattr(format, "mountpoint", "")
            if mountpoint is None:
                mountpoint = ""

        # device name
        name = getattr(device, "lvname", device.name)

        # label
        label = getattr(format, "label", "")
        if label is None:
            label = ""

        if GGitem:
            GGitem.setName(name)
            if isinstance(GGitem, Partition):
                GGitem.setDetails('%s - %s (%s)' % (label, mountpoint,
                    format.name))
                GGitem.setSize(int(device.size))
                GGitem.setFSType(format.name)
                GGitem.setDevice(device)
                print ">>> Added, ", name, int(device.size), format.name

        item.setDevice(device)
        item.setName(name)
        item.setMountpoint(mountpoint)
        item.setLabel(label)
        item.setType(format.name)
        item.setSize("%Ld" % device.size)
        item.setFormat(formatIcon)

    def populate(self):
        # Clear device tree
        self.ui.deviceTree.clear()
        self.ui.GGdeviceTree.clear()
        self.ui.GGVdeviceTree.clear()
        self.ui.GGRdeviceTree.clear()

        # first do LVM
        vgs = self.storage.vgs
        if vgs:
            volumeGroupsItem = DeviceTreeItem(self.ui.deviceTree)
            volumeGroupsItem.setName(_("Volume Groups"))
            for vg in vgs:
                volumeGroupItem = DeviceTreeItem(volumeGroupsItem)
                GGvolumeGroupItem = self.ui.GGVdeviceTree.addBlock("VV")
                self.addDevice(vg, volumeGroupItem, GGvolumeGroupItem)
                volumeGroupItem.setType("")
                for lv in vg.lvs:
                    logicalVolumeItem = DeviceTreeItem(volumeGroupItem)
                    GGlogicalVolumeItem = GGvolumeGroupItem.addPartition()#Partition(GGvolumeGroupItem))
                    self.addDevice(lv, logicalVolumeItem, GGlogicalVolumeItem)

                # We add a row for the VG free space.
                if vg.freeSpace > 0:
                    freeLogicalVolumeItem = DeviceTreeItem(volumeGroupItem)
                    GGfreeLogicalVolumeItem = GGvolumeGroupItem.addPartition()#Partition(GGvolumeGroupItem))

                    freeLogicalVolumeItem.setName(_("Free"))
                    GGfreeLogicalVolumeItem.setName(_("Free"))

                    freeLogicalVolumeItem.setSize("%Ld" % vg.freeSpace)
                    GGfreeLogicalVolumeItem.setSize(int(vg.freeSpace))
                    freeLogicalVolumeItem.setDevice(None)
                    freeLogicalVolumeItem.setMountpoint("")

        # handle RAID next
        raidarrays = self.storage.raidArrays
        if raidarrays:
            raidArraysItem = DeviceTreeItem(self.ui.deviceTree)
            raidArraysItem.setName(_("Raid Arrays"))
            for array in raidarrays:
                GGraidArrayItem = self.ui.GGRdeviceTree.addBlock("XX")
                raidArrayItem = DeviceTreeItem(raidArraysItem)
                self.addDevice(array, raidArrayItem, GGraidArrayItem)

        # now normal partitions
        disks = self.storage.partitioned
        # also include unpartitioned disks that aren't mpath or biosraid
        whole = filter(lambda d: not d.partitioned and not d.format.hidden,
                       self.storage.disks)
        disks.extend(whole)
        disks.sort(key=lambda d: d.name)
        # Disk&Partitions
        drivesItem = DeviceTreeItem(self.ui.deviceTree)
        drivesItem.setName(_("Hard Drives"))
        for disk in disks:
            diskItem = DeviceTreeItem(drivesItem)
            GGdiskItem = self.ui.GGdeviceTree.addBlock("%s - %s" % (disk.model, disk.name))
            diskItem.setName("%s - %s" % (disk.model, disk.name))
            #self.ui.deviceTree.expandItem(diskItem)
            if disk.partitioned:
                partition = disk.format.firstPartition
                extendedItem = None
                while partition:
                    if partition.type & parted.PARTITION_METADATA:
                        partition = partition.nextPartition()
                        continue

                    partName = devicePathToName(partition.getDeviceNodeName())
                    device = self.storage.devicetree.getDeviceByName(partName)

                    if not device and not partition.type & parted.PARTITION_FREESPACE:
                        ctx.logger.debug("can't find partition %s in device tree" % partName)

                    # Force partitions tree item not to be less than 12 MB
                    if partition.getSize(unit="MB") <= 12.0:
                        if not partition.active or not partition.getFlag(parted.PARTITION_BOOT):
                            partition = partition.nextPartition()
                            continue

                    if device and device.isExtended:
                        if extendedItem:
                            raise RuntimeError, _("Can't handle more than "
                                                 "one extended partition per disk")
                        extendedItem = partItem = DeviceTreeItem(diskItem)
                        partitionItem = extendedItem

                        GGextendedItem = GGpartItem = GGdiskItem.addPartition(Block(GGdiskItem, root = self))#Partition(GGdiskItem))
                        GGpartitionItem = GGextendedItem

                    elif device and device.isLogical:
                        if not extendedItem:
                            raise RuntimeError, _("Crossed logical partition before extended")
                        partitionItem = DeviceTreeItem(extendedItem)
                        GGpartitionItem = GGextendedItem.addPartition()#Partition(GGdiskItem))

                    else:
                        # Free space item
                        if partition.type & parted.PARTITION_LOGICAL:
                            partitionItem = DeviceTreeItem(extendedItem)
                            GGpartitionItem = GGextendedItem.addPartition()#Partition(GGdiskItem))
                        else:
                            partitionItem = DeviceTreeItem(diskItem)
                            GGpartitionItem = GGdiskItem.addPartition()#Partition(GGdiskItem))

                    if device and not device.isExtended:
                        self.addDevice(device, partitionItem, GGpartitionItem)
                    else:
                        # either extended or freespace
                        if partition.type & parted.PARTITION_FREESPACE:
                            deviceName = _("Free")
                            device = partition
                            deviceType = ""
                            GGpartitionItem.setFSType("free")
                            GGpartitionItem.setDevice(device)
                        else:
                            deviceName = device.name
                            deviceType = _("Extended")

                        GGpartitionItem.setName(deviceName)

                        partitionItem.setName(deviceName)
                        partitionItem.setType(deviceType)
                        size = partition.getSize(unit="MB")
                        if size < 1.0:
                            size = "< 1"
                        else:
                            size = "%Ld" % (size)
                        partitionItem.setSize(size)
                        GGpartitionItem.setSize(int(size))
                        partitionItem.setDevice(device)

                    partition = partition.nextPartition()
            else:
                self.addDevice(disk, diskItem)

        #Expands all item in selected device tree item
        for index in range(self.ui.deviceTree.topLevelItemCount()):
            self.ui.deviceTree.topLevelItem(index).setExpanded(True)
            childItem = self.ui.deviceTree.topLevelItem(index)
            for childIndex in range(childItem.childCount()):
                childItem.child(childIndex).setExpanded(True)

    def refresh(self, justRedraw=None):
        ctx.logger.debug("refresh: justRedraw=%s" % justRedraw)
        self.ui.deviceTree.clear()
        self.ui.GGdeviceTree.clear()
        self.ui.GGVdeviceTree.clear()
        self.ui.GGRdeviceTree.clear()
        if justRedraw:
            rc = 0
        else:
            try:
                doPartitioning(self.storage)
                rc = 0
            except PartitioningError, msg:
                self.intf.messageWindow(_("Error Partitioning"), 
                                        _("Could not allocate requested partitions: %s." % msg),
                                        customIcon="error")
                rc = -1
            except PartitioningWarning, msg:
                rc = self.intf.messageWindow(_("Warning Partitioning"),
                                             _("Warning: %s." % msg),
                                             customButtons=[_("Modify Partition"), _("Continue")],
                                             customIcon="warning")
                if rc == 1:
                    rc = -1
                else:
                    rc = 0
                    all_devices = self.storage.devicetree.devices
                    bootDevs = [d for d in all_devices if d.bootable]

        if not rc == -1:
            self.populate()

        self.update()
        return rc


    def getCurrentDevice(self):
        if self.ui.deviceTree.currentItem():
            return self.ui.deviceTree.currentItem().device

    def getCurrentDeviceParent(self):
        """ Return the parent of the selected row.  Returns an item.
            None if there is no parent.
        """
        pass

    def updateMenus(self):
        self.createPartition.setVisible(True)
        activatePartition = False
        freePartition = hasFreeDiskSpace(self.storage)
        if freePartition:
            activatePartition = True

        activateVolumeGroup = False
        availablePVS = len(self.storage.unusedPVS())
        if (lvm.has_lvm() and
                formats.getFormat("lvmpv").supported and
                availablePVS > 0):
            activateVolumeGroup = True

        activateRaidArray = False
        availableRaidMembers = len(self.storage.unusedRaidMembers())
        availableMinors = len(self.storage.unusedRaidMinors)
        if (availableMinors > 0
                and formats.getFormat("software RAID").supported
                and availableRaidMembers > 1):
            activateRaidArray = True


        """if (not activatePartition and not activateVolumeGroup):
            self.intf.messageWindow(_("Cannot perform any creation operation"),
                                    _("Note that the creation operation requires one of the\nfollowing:"
                                      " * Free space in one of the Hard Drives.\n"
                                      " * At least one free physical volume (LVM) partition.\n"
                                      " * At least one Volume Group with free space."),
                                    customIcon="warning")
            return"""

        freeVolumeGroupSpace = []
        for vg in self.storage.vgs:
            if vg.freeSpace > 0:
                freeVolumeGroupSpace.append(vg)

        activateLogicalVolume = False
        if len(freeVolumeGroupSpace) > 0:
            activateLogicalVolume = True

        if activatePartition:
            self.createPartition.setVisible(True)
            self.createPhysicalVolume.setVisible(True)
            self.createRaidMember.setVisible(True)

        if activateVolumeGroup:
            self.createVolumeGroup.setVisible(True)
            self.createLogicalVolume.setVisible(True)

        if activateLogicalVolume:
            #FIXME: find way to show only logical volume editor
            pass

        if activateRaidArray:
            self.createRaidArray.setVisible(True)

    def createDevice(self, action):

        if self._active_device:
            device = self._active_device
            self._active_device = None
        else:
            device = self.getCurrentDevice()

        if isinstance(device, parted.partition.Partition):
            if action == self.createRaidMember:
                raidmember = self.storage.newPartition(fmt_type="mdmember")
                self.editPartition(raidmember, isNew=True, partedPartition=device, restricts=["mdmember"])
                return
            elif action == self.createPhysicalVolume:
                physicalvolume = self.storage.newPartition(fmt_type="lvmpv")
                self.editPartition(physicalvolume, isNew=True, partedPartition=device, restricts=["lvmpv"])
                return
            elif action == self.createPartition:
                format = self.storage.defaultFSType
                partition = self.storage.newPartition(fmt_type=format)
                self.editPartition(partition, isNew=True, partedPartition=device)
                return

        elif action == self.createRaidArray:
            raidarray = self.storage.newRaidArray(fmt_type=self.storage.defaultFSType)
            self.editRaidArray(raidarray, isNew=True)
            return


        elif action == self.createVolumeGroup:
            vg = self.storage.newVolumeGroup()
            self.editVolumeGroup(vg, isNew=True)
            return


    def editDevice(self, *args):
        if self.sender() == self.ui.editButton:
            device = self.getCurrentDevice()
        else:
            device = self.sender().device

        if device and not isinstance(device, parted.partition.Partition):
            reason = self.storage.deviceImmutable(device, ignoreProtected=True)

            if reason:
                self.intf.messageWindow(_("Unable To Edit"),
                                       _("You cannot edit this device:\n\n%s")
                                        % reason,
                                        customIcon="error")
                return

            if device.type == "mdarray":
                self.editRaidArray(device)
            elif device.type == "lvmvg":
                self.editVolumeGroup(device)
            elif device.type == "lvmlv":
                self.editLogicalVolume(lv=device)
            elif isinstance(device, Partition):
                self.editPartition(device)



    def editVolumeGroup(self, device, isNew=False):
        volumegroupEditor =  LVMEditor(self, device, isNew=isNew)

        while True:
            origDevice = copy.copy(device)
            operations = volumegroupEditor.run()

            for operation in operations:
                self.storage.devicetree.addOperation(operation)

            if self.refresh(justRedraw=not operations):
                operations.reverse()

                for operation in operations:
                    self.storage.devicetree.removeOperation(operation)

                if not isNew:
                    device = origDevice

                if self.refresh():
                    raise RuntimeError, ("Returning partitions to state "
                                         "prior to edit failed")
            else:
                break

        volumegroupEditor.destroy()

    def editLogicalVolume(self, lv=None, vg=None):
        """Will be consistent with the state of things and use this funciton
        for creating and editing LVs.

        lv -- the logical volume to edit.  If this is set there is no need
              for the other two arguments.
        vg -- the volume group where the new lv is going to be created. This
              will only be relevant when we are createing an LV.
        """
        if lv != None:
            volumegroupEditor = LVMEditor(self, lv.vg, isNew = False)
            lv = volumegroupEditor.lvs[lv.lvname]
            isNew = False

        elif vg != None:
            volumegroupEditor = LVMEditor(self, vg, isNew = False)
            tempvg = volumegroupEditor.tmpVolumeGroup
            name = self.storage.createSuggestedLogicalVolumeName(tempvg)
            format = fornmats.getFormat(self.storage.defaultFSType)
            volumegroupEditor.lvs[name] = {'name': name,
                                           'size': vg.freeSpace,
                                           'format': format,
                                           'originalFormat': format,
                                           'stripes': 1,
                                           'logSize': 0,
                                           'snapshotSpace': 0,
                                           'exists': False}
            lv = volumegroupEditor.lvs[name]
            isNew = True

        else:
            return

        while True:
            #volumegroupEditor.editLogicalVolume(lv, isNew = isNew)
            operations = volumegroupEditor.run()

            for operation in operations:
                self.storage.devicetree.addOperation(operation)

            if self.refresh(justRedraw=True):
                operations.reverse()
                for operation in operations:
                    self.storage.devicetree.removeOperation(operation)

                if self.refresh():
                    raise RuntimeError, ("Returning partitions to state "
                                         "prior to edit failed")
                continue
            else:
                break

        volumegroupEditor.destroy()

    def editRaidArray(self, device, isNew=False):
        raideditor = RaidEditor(self, device, isNew)

        while True:
            operations = raideditor.run()

            for operation in operations:
                self.storage.devicetree.addOperation(operation)

            if self.refresh(justRedraw=True):
                operation.reverse()
                for operation in operation:
                    self.storage.devicetree.removeOperation(operation)
                    if self.refresh():
                        raise RuntimeError, ("Returning partitions to state "
                                             "prior to RAID edit failed")
                continue
            else:
                break

        raideditor.destroy()

    def editPartition(self, device, isNew=False, partedPartition=None, restricts=None):
        partitionEditor = PartitionEditor(self, device, isNew=isNew, partedPartition=partedPartition, restricts=restricts)

        while True:
            origDevice = copy.copy(device)
            operations = partitionEditor.run()
            for operation in operations:
                self.storage.devicetree.addOperation(operation)

            if self.refresh(justRedraw=not operations):
                operations.reverse()
                for operation in operations:
                    self.storage.devicetree.removeOperation(operation)

                if not isNew:
                    device.req_size = origDevice.req_size
                    device.req_base_size = origDevice.req_base_size
                    device.req_grow = origDevice.req_grow
                    device.req_max_size = origDevice.req_max_size
                    device.req_primary = origDevice.req_primary
                    device.req_disks = origDevice.req_disks

                if self.refresh():
                    raise RuntimeError, ("Returning partitions to state "
                                         "prior to edit failed")
            else:
                break

        partitionEditor.destroy()

    def deleteDevice(self):
        if self.sender() == self.ui.deleteButton:
            device = self.getCurrentDevice()
        else:
            device = self.sender().device

        if device:
            if device.partitioned:
                if doClearPartitionedDevice(self.intf, self.storage, device):
                    self.refresh()
            elif doDeleteDevice(self.intf, self.storage, device):
                if isinstance(device, Partition):
                    justRedraw = False
                else:
                    justRedraw = True
                    if device.type == "lvmlv" and device in device.vg.lvs:
                        device.vg._removeLogicalVolume(device)

                self.refresh(justRedraw=justRedraw)

    def reset(self):
        if confirmResetPartitionState(self.intf):
            return
        self.storage.reset()
        self.ui.deviceTree.clear()
        self.ui.GGdeviceTree.clear()
        self.ui.GGVdeviceTree.clear()
        self.ui.GGRdeviceTree.clear()
        self.refresh(justRedraw=True)


class DeviceTreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent, device=None):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.device = device

    def setDevice(self, device):
        self.device = device

    def setName(self, device):
        self.setText(0, device)

    def setMountpoint(self, mountpoint):
        self.setText(1, mountpoint)

    def setLabel(self, label):
        self.setText(2, label)

    def setType(self, type):
        self.setText(3, type)

    def setFormat(self, format):
        self.setIcon(4, format)

    def setSize(self, size):
        self.setText(5, size)


### NEW PARTITION WIDGET ###

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QRect
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QMimeData
from PyQt4.QtCore import SIGNAL

from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QDrag
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QHBoxLayout, QVBoxLayout

from yali.gui.Ui.partitionitem import Ui_PartitionItem

VERTICAL, HORIZONTAL = range(2)
SHARED = '#Partition{ border:1px solid #585858;border-radius:4px;}'
BUTTON = 'border:1px solid rgba(0,0,0,120);border-radius:4px;'

STYLES = {"free":'background-color:rgba(0,0,0,80);',
          "ext4":'background-color:#008080;',
          "swap":'background-color:#008000;color:white;',
          "hfs+":'background-color:pink;color:black;'}

UNKNOWN_STYLE = 'background-color:lightyellow;color:black;'

class Partition(QWidget, Ui_PartitionItem):
    def __init__(self, parent, title = 'Free Space', fs_type = "free", size = 0, root = None):
        QWidget.__init__(self, parent)
        self.ui = Ui_PartitionItem()
        self.ui.setupUi(self)
        self.parent = parent
        self.root = root
        self.device = None

        self.setFSType(fs_type)
        self.setName(title)
        self.setSize(size)

        self.ui.useButton.setStyleSheet(BUTTON)
        self.ui.editButton.setStyleSheet(BUTTON)
        self.ui.deleteButton.setStyleSheet(BUTTON)

        # Shame on me.
        self.ui.deleteButton.clicked.connect(lambda: self.emit(SIGNAL("deleteButtonClicked"), True))
        self.ui.editButton.clicked.connect(lambda: self.emit(SIGNAL("editButtonClicked"), True))

        self.connect(self, SIGNAL("deleteButtonClicked"), self.root.deleteDevice)
        self.connect(self, SIGNAL("editButtonClicked"), self.root.editDevice)

        QTimer.singleShot(0, self.leaveEvent)

    def setDevice(self, device):
        self.device = device

    def setName(self, text):
        self.ui.title.setText(text)

    def setDetails(self, details):
        self.ui.comment.setText(details)

    def name(self):
        return self.ui.title.text()

    def setFSType(self, fs_type):
        self._fs_type = fs_type
        self.ui.Partition.setStyleSheet(STYLES.get(fs_type, UNKNOWN_STYLE))

    def setSize(self, size):
        self._size = size
        self.setToolTip('Size: %s MB' % size)
        self.parent._updateSize()

    def enterEvent(self, event):
        if not self._fs_type == 'free':
            self.ui.editButton.show()
            self.ui.deleteButton.show()
            self.setMinimumWidth(200)
        elif self._fs_type == 'free':
            self.ui.useButton.show()
            self.ui.useButton.setMenu(self.root.menu)
            self.root._active_device = self.device

    def leaveEvent(self, event=None):
        if self._fs_type == 'free':
            self.ui.useButton.setMenu(QMenu())
        self.ui.useButton.hide()
        self.ui.editButton.hide()
        self.ui.deleteButton.hide()
        self.setMinimumWidth(60)

class Block(QGroupBox):

    def __init__(self, parent, name = '', size = 0, root = None):
        QGroupBox.__init__(self, name, parent)
        self.layout = QHBoxLayout(self)
        self.parent = parent
        self.root = root

        self._name = name
        self._size = size
        self._partitions = []

    def setName(self, name):
        self._name = name
        self.setTitle(self._name)

    def setSize(self, size):
        self._size = size

    def addPartition(self, partition = None, index = None):

        if not partition:
            partition = Partition(self, root = self.root)

        if index == None:
            index = len(self._partitions)

        self._partitions.insert(index, partition)
        self.layout.insertWidget(index, partition)
        self._updateSize()

        return partition

    def _updateSize(self):
        for i in range(len(self._partitions)):
            self.layout.setStretch(i, self._partitions[i]._size)

class BlockGroup(QGroupBox):

    def __init__(self, parent = None, name = 'Block Group'):
        QGroupBox.__init__(self, name, parent)

        self.parent = parent
        self.setStyleSheet(SHARED)
        self.layout = QVBoxLayout(self)
        self._disks = []
        self.hide()

    def clear(self):
        for disk in self._disks:
            disk.hide()
            self.layout.removeWidget(disk)
        self._disks = []
        self.hide()

    def addBlock(self, name, size = None):
        disk = Block(self, name, size, root = self.parent)
        self.layout.addWidget(disk)
        self._disks.append(disk)
        self.show()
        return disk

    def getBlock(self, index):
        return self._disks[index]

