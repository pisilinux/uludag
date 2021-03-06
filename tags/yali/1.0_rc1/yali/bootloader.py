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

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext


from yali.constants import consts

grub_conf_tmp = """
default 0
timeout 5
splashimage = (%(grub_root)s)/boot/grub/splash.xpm.gz

title=  %(pardus_version)s
root (%(grub_root)s)
kernel (%(grub_root)s)/boot/%(boot_kernel)s %(boot_parameters)s
initrd=(%(grub_root)s)/boot/%(initrd)s 
"""

win_part_tmp = """
title= %(title)s (%(fs)s) - %(root)s
rootnoverify (%(grub_root)s)
makeactive
chainloader +1

"""

grub_shell_tmp = """
root (%(grub_root)s)
setup (%(grub_dev)s)
"""

device_map = os.path.join(consts.target_dir, "boot/grub/device.map")
grub_conf = os.path.join(consts.target_dir, "boot/grub/grub.conf")

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
    global grub_conf

    grub_dir = os.path.join(consts.target_dir, "boot/grub")
    if not os.path.exists(grub_dir):
        os.makedirs(grub_dir)

    #write an empty grub.conf, for grub to create a device map.
    open(grub_conf, "w").close()
    # create device map
    cmd = "/sbin/grub --batch --no-floppy --device-map=%s < %s" %(
        device_map, grub_conf)
    os.system(cmd)


# TODO: support installing grub to diffrent devices's MBR.
#    grub_dev = _find_grub_dev(dev)
    minor = str(int(filter(lambda u: u.isdigit(), root)) -1)
    grub_root = ",".join(["hd0", minor])


    def find_boot_kernel():
        d = os.path.join(consts.target_dir, "boot")
        k = glob.glob(d + "/kernel-*")
        return os.path.basename(k[0])
    
    def find_initrd_name(bk):
        ver = bk[len("kernel-"):]
        return "initrd-%s" % ver

    def boot_parameters_from_cmdline(root):
        s = ""
        for i in  open("/proc/cmdline", "r").read().split():
            if i.startswith("root="):
                i = "root=/dev/%s" % root
            elif i.startswith("cdroot") or i.startswith("init="):
                continue

            s = " ".join((s,i))

        return s

    boot_kernel = find_boot_kernel()
    initrd_name = find_initrd_name(boot_kernel)
    boot_parameters =  boot_parameters_from_cmdline(root)
    s = grub_conf_tmp % {"root": root,
                         "grub_root": grub_root,
                         "pardus_version": consts.pardus_version,
                         "boot_kernel": boot_kernel,
                         "boot_parameters": boot_parameters,
                         "initrd": initrd_name}
    open(grub_conf, "w").write(s)


def grub_conf_append_win(root, dev, fs):
    global grub_conf

    grub_dev = _find_grub_dev(dev)
    minor = str(int(filter(lambda u: u.isdigit(), root)) -1)
    grub_root = ",".join([grub_dev, minor])

    s = win_part_tmp % {"title": _("Windows"),
                        "grub_root": grub_root,
                        "root": root,
                        "fs": fs}
    open(grub_conf, "a").write(s)


def install_grub(root, dev):

    grub_dev = _find_grub_dev(dev)
    minor = str(int(filter(lambda u: u.isdigit(), root)) -1)
    grub_root = ",".join([grub_dev, minor])

    grub_shell = grub_shell_tmp % {"grub_root": grub_root,
                                   "grub_dev": grub_dev}

    open("/tmp/grub-shell", "w").write(grub_shell)

    # FIXME: check command...
    cmd = "/sbin/grub --batch < /tmp/grub-shell"
    print cmd
    os.system(cmd)

