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

import os
import glob
import shutil

from yali.constants import consts

grub_conf_tmp = """
default 0
timeout 5
splashimage = (%(grub_root)s)/boot/grub/splash.xpm.gz

title=2.6.12-2 [ %(pardus_version)s ]
root (%(grub_root)s)
kernel (%(grub_root)s)/boot/pardus-kernel-2.6.12-2 ro root=/dev/%(root)s

"""

grub_shell_tmp = """
root (%(grub_root)s)
setup (%(grub_dev)s)
"""

device_map = os.path.join(consts.target_dir, "boot/grub/device.map")

def _find_grub_dev(dev):
    global device_map

    for l in open(device_map).readlines():
        if l.find(dev) >= 0:
            l = l.split()
            d = l[0]
            # remove paranthesis
            return d[1:-1]


def write_grub_conf(root, dev):
    global device_map

    grub_conf = os.path.join(consts.target_dir, "boot/grub/grub.conf")

    d = os.path.join(consts.target_dir, "boot/grub")
    if not os.path.exists(d):
        os.makedirs(d)

    #write an empty grub.conf, for grub to create a device map.
    open(grub_conf, "w").close()
    # create device map
    cmd = "/sbin/grub --batch --no-floppy --device-map=%s < %s" %(
        device_map, grub_conf)
    os.system(cmd)


# TODO: support installing grub to diffrent devices's MBR.
#    grub_dev = _find_grub_dev(dev)
    minor = str(int(root[-1]) - 1)
    grub_root = ",".join(["hd0", minor])

    s = grub_conf_tmp % {"root": root,
                         "grub_root": grub_root,
                         "pardus_version": consts.pardus_version}
    open(grub_conf, "w").write(s)


def install_files():
    src = os.path.join(consts.target_dir, "lib/grub")
    src2 = os.path.join(consts.target_dir, "usr/lib/grub")
    fnlist = glob.glob(src + "/*/*")
    fnlist2 = glob.glob(src2 + "/*/*")
    for x in fnlist2: fnlist.append(x)

    for x in fnlist:
        if os.path.isfile(x):
            print x
            fname = os.path.basename(x)
            newpath = os.path.join(consts.target_dir, "boot/grub", fname)
            shutil.copyfile(x, newpath)

    m = os.path.join(consts.target_dir, "boot/grub/menu.lst")
    os.symlink("grub.conf", m)


def install_grub(root, dev):

    grub_dev = _find_grub_dev(dev)
    minor = str(int(root[-1]) - 1)
    grub_root = ",".join([grub_dev, minor])

    grub_shell = grub_shell_tmp % {"grub_root": grub_root,
                                   "grub_dev": grub_dev}

    open("/tmp/grub-shell", "w").write(grub_shell)

    # FIXME: check command...
    cmd = "/sbin/grub --batch < /tmp/grub-shell"
    print cmd
    os.system(cmd)
