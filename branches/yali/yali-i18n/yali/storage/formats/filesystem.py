#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import math
import parted

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali
import yali.util
from . import Format, register_device_format
from pardus.sysutils import get_kernel_option

class FilesystemError(yali.Error):
    pass

class FilesystemFormatError(FilesystemError):
    pass

class FilesystemResizeError(FilesystemError):
    pass

class FilesystemCheckError(FilesystemError):
    pass

global kernel_filesystems

def get_kernel_filesystems():
    fs_list = []
    for line in open("/proc/filesystems").readlines():
        fs_list.append(line.split()[-1])
    return fs_list

kernel_filesystems = get_kernel_filesystems()

class Filesystem(Format):
    _type = "filesystem"  # fs type name
    _mountType = None                    # like _type but for passing to mount
    _name = None
    _mkfs = ""                           # mkfs utility
    _resizefs = ""                       # resize utility
    _labelfs = ""                        # labeling utility
    _fsck = ""                           # fs check utility
    _fsckErrors = {}                     # fs check command error codes & msgs
    _infofs = ""                         # fs info utility
    _formatOptions = []                  # default options passed to mkfs
    _mountOptions = ["defaults"]         # default options passed to mount
    _labelOptions = []
    _checkOptions = []
    _infoOptions = []
    _existingSizeFields = []
    _fsProfileSpecifier = None           # mkfs option specifying fsprofile

    def __init__(self, *args, **kwargs):
        """ Create a FileSystem instance.

            Keyword Args:

                device -- path to the device containing the filesystem
                mountpoint -- the filesystem's mountpoint
                label -- the filesystem label
                uuid -- the filesystem UUID
                mountopts -- mount options for the filesystem
                size -- the filesystem's size in MiB
                exists -- indicates whether this is an existing filesystem

        """
        if self.__class__ is FileSystem:
            raise TypeError("FileSystem is an abstract class.")

        Format.__init__(self, *args, **kwargs)
        self.label = kwargs.get("label")
        self._minInstanceSize = None    # min size of this FS instance
        self._size = kwargs.get("size", 0)
        self._mountpoint = kwargs.get("mountpoint")
        self.mountopts = kwargs.get("mountopts")

        # filesystem size does not necessarily equal device size
        if self.exists and self.supported:
            self._size = self._getExistingSize()
            calculated = self.minSize      # force calculation of minimum size

        self._targetSize = self._size

    def __str__(self):
        s = Format.__str__(self)
        s += ("  mountpoint = %(mountpoint)s  mountopts = %(mountopts)s\n"
              "  label = %(label)s  size = %(size)s\n" %
              {"mountpoint": self.mountpoint, "mountopts": self.mountopts,
               "label": self.label, "size": self._size})
        return s

    def _setTargetSize(self, newsize):
        """ Set a target size for this filesystem. """
        if not self.exists:
            raise FilesystemError("filesystem has not been created")

        if newsize is None:
            # unset any outstanding resize request
            self._targetSize = self._size
            return

        if not self.minSize <= newsize < self.maxSize:
            raise ValueError("invalid target size request")

        self._targetSize = newsize

    def _getTargetSize(self):
        """ Get this filesystem's target size. """
        return self._targetSize

    targetSize = property(_getTargetSize, _setTargetSize,
                          doc="Target size for this filesystem")

    def _getSize(self):
        """ Get this filesystem's size. """
        size = self._size
        if self.resizable and self.targetSize != size:
            size = self.targetSize
        return size

    size = property(_getSize, doc="This filesystem's size, accounting "
                                  "for pending changes")

    def _getExistingSize(self):
        """ Determine the size of this filesystem.  Filesystem must
            exist.  Each filesystem varies, but the general procedure
            is to run the filesystem dump or info utility and read
            the block size and number of blocks for the filesystem
            and compute megabytes from that.
        """
        size = self._size

        if self.infofs and self.mountable and self.exists and not size:
            try:
                values = []
                argv = self._defaultInfoOptions + [ self.device ]

                buf = yali.util.run_batch(self.infofs, argv)[1]

                for line in buf.splitlines():
                    found = False

                    line = line.strip()
                    tmp = line.split(' ')
                    tmp.reverse()

                    for field in self._existingSizeFields:
                        if line.startswith(field):
                            for subfield in tmp:
                                try:
                                    values.append(long(subfield))
                                    found = True
                                    break
                                except ValueError:
                                    continue

                        if found:
                            break

                    if len(values) == len(self._existingSizeFields):
                        break

                if len(values) != len(self._existingSizeFields):
                    return 0

                size = 1
                for value in values:
                    size *= value

                # report current size as megabytes
                size = math.floor(size / 1024.0 / 1024.0)
            except Exception as e:
                ctx.logger.error("failed to obtain size of filesystem on %s: %s"
                          % (self.device, e))

        return size

    @property
    def currentSize(self):
        """ The filesystem's current actual size. """
        size = 0
        if self.exists:
            size = self._size
        return float(size)

    def _getFormatOptions(self, options=None):
        argv = []
        if options and isinstance(options, list):
            argv.extend(options)
        argv.extend(self.formatOptions)
        if self._fsProfileSpecifier and self.fsprofile:
            argv.extend([self._fsProfileSpecifier, self.fsprofile])
        argv.append(self.device)
        return argv

    @property
    def resizeArgs(self):
        argv = [self.device, "%d" % (self.targetSize,)]
        return argv

    def _getCheckArgs(self):
        argv = []
        argv.extend(self.checkOptions)
        argv.append(self.device)
        return argv

    def _fsckFailed(self, rc):
        return False

    def _fsckErrorMessage(self, rc):
        return _("Unknown return code: %d.") % (rc,)

    def doFormat(self, *args, **kwargs):
        """ Create the filesystem.

            Arguments:

                None

            Keyword Arguments:

                options -- list of options to pass to mkfs

        """
        options = kwargs.get("options")

        if self.exists:
            raise FilesystemFormatError("filesystem already exists", self.device)

        if not self.formattable:
            return

        if not self.mkfs:
            return

        if self.exists:
            return

        if not os.path.exists(self.device):
            raise FilesystemFormatError("device does not exist", self.device)

        argv = self._getFormatOptions(options=options)

        try:
            rc = yali.util.run_batch(self.mkfs,argv)

        except Exception as e:
            raise FilesystemFormatError(e, self.device)

        if rc:
            raise FilesystemFormatError("format failed: %s" % rc, self.device)

        self.exists = True
        self.notifyKernel()

        if self.label:
            self.writeLabel(self.label)


    def doResize(self, *args, **kwargs):
        """ Resize this filesystem to new size @newsize.

            Arguments:

        """

        if not self.exists:
            raise FileSystemResizeError("filesystem does not exist", self.device)

        if not self.resizable:
            raise FileSystemResizeError("filesystem not resizable", self.device)

        if not self.resizefs:
            return

        if not os.path.exists(self.device):
            raise FileSystemResizeError("device does not exist", self.device)

        self.doCheck()

        self._minInstanceSize = None
        if self.targetSize < self.minSize:
            self.targetSize = self.minSize
            ctx.logger.info("Minimum size changed, setting targetSize on %s to %s" \
                     % (self.device, self.targetSize))

        try:
            rc = yali.util.run_batch(self.resizefs, self.resizeArgs)
        except Exception as e:
            raise FileSystemResizeError(e, self.device)

        if rc:
            raise FileSystemResizeError("resize failed: %s" % rc, self.device)

        self.doCheck()
        self.notifyKernel()


    def doCheck(self):
        if not self.exists:
            raise FileSystemError("filesystem has not been created")

        if not self.fsck:
            return

        if not os.path.exists(self.device):
            raise FileSystemError("device does not exist")

        w = None

        try:
            rc = yali.util.run_batch(self.fsck, self._getCheckArgs())
        except Exception as e:
            raise FileSystemError("filesystem check failed: %s" % e)

        if self._fsckFailed(rc):
            hdr = _("%(type)s filesystem check failure on %(device)s: ") % \
                   (self.type, self.device,)
            msg = self._fsckErrorMessage(rc)

            raise FileSystemError(hdr + msg)

    def mount(self, *args, **kwargs):
        """ Mount this filesystem.

            Arguments:

                None

            Keyword Arguments:

                options -- mount options (overrides all other option strings)
                chroot -- prefix to apply to mountpoint
                mountpoint -- mountpoint (overrides self.mountpoint)
        """
        options = kwargs.get("options", "")
        chroot = kwargs.get("chroot", "/")
        mountpoint = kwargs.get("mountpoint")

        if not self.exists:
            raise FileSystemError("filesystem has not been created")

        if not mountpoint:
            mountpoint = self.mountpoint

        if not mountpoint:
            raise FileSystemError("no mountpoint given")

        if self.status:
            return

        # XXX os.path.join is FUBAR:
        #
        #         os.path.join("/mnt/foo", "/") -> "/"
        #
        #mountpoint = os.path.join(chroot, mountpoint)
        chrootedMountpoint = os.path.normpath("%s/%s" % (chroot, mountpoint))
        iutil.mkdirChain(chrootedMountpoint)

        # passed in options override default options
        if not options or not isinstance(options, str):
            options = self.options

        try:
            rc = isys.mount(self.device, chrootedMountpoint, 
                            fstype=self.mountType,
                            options=options,
                            bindMount=isinstance(self, BindFileSystem))
        except Exception as e:
            raise FileSystemError("mount failed: %s" % e)

        if rc:
            raise FileSystemError("mount failed: %s" % rc)

        self._mountpoint = chrootedMountpoint

    def unmount(self):
        """ Unmount this filesystem. """
        if not self.exists:
            raise FileSystemError("filesystem has not been created")

        if not self._mountpoint:
            # not mounted
            return

        if not os.path.exists(self._mountpoint):
            raise FileSystemError("mountpoint does not exist")

        rc = isys.umount(self._mountpoint, removeDir = False)
        if rc:
            raise FileSystemError("umount failed")

        self._mountpoint = None

    def _getLabelArgs(self, label):
        argv = []
        argv.extend(self.labelOptions)
        argv.extend([self.device, label])
        return argv 

    def writeLabel(self, label):
        """ Create a label for this filesystem. """
        if not self.exists:
            raise FileSystemError("filesystem has not been created")

        if not self.labelfs:
            return

        if not os.path.exists(self.device):
            raise FileSystemError("device does not exist")

        argv = self._getLabelArgs(label)
        rc = sysutils.run(self.labelfs,argv)

        if rc:
            raise FileSystemError("label failed")

        self.label = label
        self.notifyKernel()

    @property
    def isDirty(self):
        return False

    @property
    def mkfs(self):
        """ Program used to create filesystems of this type. """
        return self._mkfs

    @property
    def fsck(self):
        """ Program used to check filesystems of this type. """
        return self._fsck

    @property
    def resizefs(self):
        """ Program used to resize filesystems of this type. """
        return self._resizefs

    @property
    def labelfs(self):
        """ Program used to manage labels for this filesystem type. """
        return self._labelfs

    @property
    def infofs(self):
        """ Program used to get information for this filesystem type. """
        return self._infofs

    @property
    def utilsAvailable(self):
        for prog in [self.mkfs, self.resizefs, self.labelfs, self.infofs]:
            if not prog:
                continue

            if not filter(lambda d: os.access("%s/%s" % (d, prog), os.X_OK),
                          os.environ["PATH"].split(":")):
                return False

        return True

    @property
    def supported(self):
        return self._supported and self.utilsAvailable

    @property
    def mountable(self):
        return (self.mountType in kernel_filesystems) or \
               (os.access("/sbin/mount.%s" % (self.mountType,), os.X_OK))

    @property
    def formatOptions(self):
        """ Default options passed to mkfs for this filesystem type. """
        # return a copy to prevent modification
        return self._formatOptions[:]

    @property
    def mountOptions(self):
        """ Default options passed to mount for this filesystem type. """
        # return a copy to prevent modification
        return self._mountOptions[:]

    @property
    def labelOptions(self):
        """ Default options passed to labeler for this filesystem type. """
        # return a copy to prevent modification
        return self._labelOptions[:]

    @property
    def checkOptions(self):
        """ Default options passed to checker for this filesystem type. """
        # return a copy to prevent modification
        return self._checkOptions[:]

    def _getOptions(self):
        options = ",".join(self.mountOptions)
        if self.mountopts:
            options = self.mountopts
        return options

    def _setOptions(self, options):
        self.mountopts = options

    options = property(_getOptions, _setOptions)

    @property
    def type(self):
        return self._type

    @property
    def mountType(self):
        if not self._mountType:
            self._mountType = self._type

        return self._mountType

    def create(self, *args, **kwargs):
        if self.exists:
            raise FilesystemError("filesystem already exists")

        Format.create(self, *args, **kwargs)

        return self.doFormat(*args, **kwargs)

    def setup(self, *args, **kwargs):
        """ Mount the filesystem.

            The filesystem will be mounted at the directory indicated by
            self.mountpoint.
        """
        return self.mount(**kwargs)

    def teardown(self, *args, **kwargs):
        return self.unmount(*args, **kwargs)

    @property
    def status(self):
        # FIXME check /proc/mounts or similar
        if not self.exists:
            return False
        return self._mountpoint is not None

class Ext2FileSystem(FileSystem):
    """ ext2 filesystem. """
    _type = "ext2"
    _mkfs = "mke2fs"
    _resizefs = "resize2fs"
    _labelfs = "e2label"
    _fsck = "e2fsck"
    _fsckErrors = {4: _("File system errors left uncorrected."),
                   8: _("Operational error."),
                   16: _("Usage or syntax error."),
                   32: _("e2fsck cancelled by user request."),
                   128: _("Shared library error.")}
    _formattable = True
    _supported = True
    _resizable = True
    _bootable = True
    _linuxNative = True
    _formatOptions = []
    _mountOptions = ["defaults"]
    _checkOptions = ["-f", "-p", "-C", "0"]
    _dump = True
    _check = True
    _infofs = "dumpe2fs"
    _infoOptions = ["-h"]
    _existingSizeFields = ["Block count:", "Block size:"]
    _fsProfileSpecifier = "-T"
    _maxSize = 8 * 1024 * 1024
    _minSize = 0
    partedSystem = fileSystemType["ext2"]

    def _fsckFailed(self, rc):
        for errorCode in self._fsckErrors.keys():
            if rc & errorCode:
                return True
        return False

    def _fsckErrorMessage(self, rc):
        msg = ''

        for errorCode in self._fsckErrors.keys():
            if rc & errorCode:
                msg += "\n" + self._fsckErrors[errorCode]

        return msg.strip()

    def tuneFileSystem(self):
        if not isys.ext2HasJournal(self.device):
            # only do this if there's a journal
            return

        try:
            rc = sysutils.run("tune2fs",["-c0", "-i0","-ouser_xattr,acl", self.device])

        except Exception as e:
            pass

    @property
    def minSize(self):
        """ Minimum size for this filesystem in MB. """
        if self._minInstanceSize is None:
            # try once in the beginning to get the minimum size for an
            # existing filesystem.
            size = self._minSize
            blockSize = None

            if self.exists and os.path.exists(self.device):
                # get block size
                rc, out, err = yali.util.run_batch(self.infofs, ["-h", self.device])
                for line in out.splitlines():
                    if line.startswith("Block size:"):
                        blockSize = int(line.split(" ")[-1])
                        break

                if blockSize is None:
                    raise FilesystemError("failed to get block size for %s filesystem "
                                  "on %s" % (self.mountType, self.device))

                # get minimum size according to resize2fs
                rc, out, err = yali.util.run_batch(self.resizefs, ["-P", self.device])
                for line in out.splitlines():
                    if "minimum size of the filesystem:" not in line:
                        continue

                    # line will look like:
                    # Estimated minimum size of the filesystem: 1148649
                    #
                    # NOTE: The minimum size reported is in blocks.  Convert
                    # to bytes, then megabytes, and finally round up.
                    (text, sep, minSize) = line.partition(": ")
                    size = long(minSize) * blockSize
                    size = math.ceil(size / 1024.0 / 1024.0)
                    break

                if size is None:
                    ctx.logger.warning("failed to get minimum size for %s filesystem "
                                "on %s" % (self.mountType, self.device))

            self._minInstanceSize = size

        return self._minInstanceSize

    @property
    def isDirty(self):
        return isys.ext2IsDirty(self.device)

    @property
    def resizeArgs(self):
        argv = ["-p", self.device, "%dM" % (self.targetSize,)]
        return argv

register_device_format(Ext2FileSystem)

class Ext3FileSystem(Ext2FileSystem):
    """ ext3 filesystem. """
    _type = "ext3"
    _formatOptions = ["-t", "ext3"]
    partedSystem = fileSystemType["ext3"]


register_device_format(Ext3FileSystem)

class Ext4FileSystem(Ext3FileSystem):
    """ ext4 filesystem. """
    _type = "ext4"
    _formatOptions = ["-t", "ext4"]
    partedSystem = fileSystemType["ext4"]

register_device_format(Ext4FileSystem)

class FATFileSystem(FileSystem):
    """ FAT filesystem. """
    _type = "vfat"
    _mkfs = "mkdosfs"
    _labelfs = "dosfslabel"
    _fsck = "dosfsck"
    _fsckErrors = {1: _("Recoverable errors have been detected or dosfsck has "
                        "discovered an internal inconsistency."),
                   2: _("Usage error.")}
    _supported = True
    _formattable = True
    _mountOptions = ["umask=0077", "shortname=winnt"]
    # FIXME this should be fat32 in some cases
    _maxSize = 1024 * 1024
    partedSystem = fileSystemType["fat16"]

    def _fsckFailed(self, rc):
        if rc >= 1:
            return True
        return False

    def _fsckErrorMessage(self, rc):
        return self._fsckErrors[rc]

register_device_format(FATFileSystem)

class EFIFileSystem(FATFileSystem):
    _type = "efi"
    _mountType = "vfat"
    _name = "EFI System Partition"
    _bootable = True
    _minSize = 50
    _maxSize = 256

    @property
    def supported(self):
        import platform
        p = platform.getPlatform(None)
        return (isinstance(p, platform.EFI) and
                p.isEfi and
                self.utilsAvailable)

register_device_format(EFIFileSystem)

class BTRFileSystem(FileSystem):
    """ btrfs filesystem """
    _type = "btrfs"
    _mkfs = "mkfs.btrfs"
    _resizefs = "btrfsctl"
    _formattable = True
    _linuxNative = True
    _bootable = False
    _maxLabelChars = 256
    _supported = False
    _dump = True
    _check = True
    _maxSize = 16 * 1024 * 1024
    # FIXME parted needs to be thaught about btrfs so that we can set the
    # partition table type correctly for btrfs partitions
    # partedSystem = fileSystemType["btrfs"]

    def _getFormatOptions(self, options=None):
        argv = []
        if options and isinstance(options, list):
            argv.extend(options)
        argv.extend(self.formatOptions)
        if self.label:
            argv.extend(["-L", self.label])
        argv.append(self.device)
        return argv

    @property
    def resizeArgs(self):
        argv = ["-r", "%dm" % (self.targetSize,), self.device]
        return argv

    @property
    def supported(self):
        """ Is this filesystem a supported type? """
        supported = self._supported
        if get_kernel_option.has_key("btrfs"):
            supported = self.utilsAvailable

        return supported

register_device_format(BTRFileSystem)

class ReiserFileSystem(FileSystem):
    """ reiserfs filesystem """
    _type = "reiserfs"
    _mkfs = "mkreiserfs"
    _resizefs = "resize_reiserfs"
    _labelfs = "reiserfstune"
    _formatOptions = ["-f", "-f"]
    _labelOptions = ["-l"]
    _maxLabelChars = 16
    _formattable = True
    _linuxNative = True
    _supported = False
    _dump = True
    _check = True
    _infofs = "debugreiserfs"
    _infoOptions = []
    _existingSizeFields = ["Count of blocks on the device:", "Blocksize:"]
    partedSystem = fileSystemType["reiserfs"]
    _maxSize = 16 * 1024 * 1024

    @property
    def supported(self):
        """ Is this filesystem a supported type? """
        supported = self._supported
        if get_kernel_option.has_key("reiserfs"):
            supported = self.utilsAvailable

        return supported

    @property
    def resizeArgs(self):
        argv = ["-s", "%dM" % (self.targetSize,), self.device]
        return argv


register_device_format(ReiserFileSystem)

class XFileSystem(FileSystem):
    """ XFileSystem filesystem """
    _type = "xfs"
    _mkfs = "mkfs.xfs"
    _labelfs = "xfs_admin"
    _formatOptions = ["-f"]
    _labelOptions = ["-L"]
    _maxLabelChars = 16
    _formattable = True
    _linuxNative = True
    _supported = True
    _dump = True
    _check = True
    _infofs = "xfs_db"
    _infoOptions = ["-c", "\"sb 0\"", "-c", "\"p dblocks\"",
                           "-c", "\"p blocksize\""]
    _existingSizeFields = ["dblocks =", "blocksize ="]
    partedSystem = fileSystemType["xfs"]
    _maxSize = 16 * 1024 * 1024

register_device_format(XFileSystem)

class NTFileSystem(FileSystem):
    """ ntfs filesystem. """
    _type = "ntfs"
    _resizefs = "ntfsresize"
    _fsck = "ntfsresize"
    _resizable = True
    _mountOptions = ["defaults", "ro"]
    _checkOptions = ["-c"]
    _infofs = "ntfsinfo"
    _infoOptions = ["-m"]
    _existingSizeFields = ["Cluster Size:", "Volume Size in Clusters:"]
    partedSystem = fileSystemType["ntfs"]
    _minSize = 1
    _maxSize = 16 * 1024 * 1024

    def _fsckFailed(self, rc):
        if rc != 0:
            return True
        return False

    @property
    def minSize(self):
        """ The minimum filesystem size in megabytes. """
        if self._minInstanceSize is None:
            # we try one time to determine the minimum size.
            size = self._minSize
            if self.exists and os.path.exists(self.device):
                minSize = None
                buf = iutil.execWithCapture(self.resizefsProg,
                                            ["-m", self.device],
                                            stderr = "/dev/tty5")
                for l in buf.split("\n"):
                    if not l.startswith("Minsize"):
                        continue
                    try:
                        min = l.split(":")[1].strip()
                        minSize = int(min) + 250
                    except Exception, e:
                        minSize = None
                        log.warning("Unable to parse output for minimum size on %s: %s" %(self.device, e))

                if minSize is None:
                    log.warning("Unable to discover minimum size of filesystem "
                                "on %s" %(self.device,))
                else:
                    size = minSize

            self._minInstanceSize = size

        return self._minInstanceSize

    @property
    def resizeArgs(self):
        # You must supply at least two '-f' options to ntfsresize or
        # the proceed question will be presented to you.
        argv = ["-ff", "-s", "%dM" % (self.targetSize,), self.device]
        return argv

register_device_format(NTFileSystem)
