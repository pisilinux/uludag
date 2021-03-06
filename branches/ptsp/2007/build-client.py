#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import shutil
import subprocess
import sys
import time
import socket
import getopt

default_exclude_list = """
lib/rcscripts/
usr/include/
usr/lib/cups/
usr/lib/python2.4/lib-tk/
usr/lib/python2.4/idlelib/
usr/lib/python2.4/distutils/
usr/lib/python2.4/bsddb/test/
usr/lib/python2.4/lib-old/
usr/lib/python2.4/test/
usr/lib/klibc/include/
usr/qt/3/include/
usr/qt/3/mkspecs/
usr/qt/3/bin/
usr/qt/3/templates/
usr/share/aclocal/
usr/share/cups/
usr/share/doc/
usr/share/info/
usr/share/sip/
usr/share/man/
var/db/pisi/
var/lib/pisi/
var/cache/pisi/packages/
var/cache/pisi/archives/
var/tmp/pisi/
tmp/pisi-root/
var/log/comar.log
var/log/pisi.log
root/.bash_history
"""

default_glob_excludes = (
    ( "usr/lib/python2.4/", "*.pyc" ),
    ( "usr/lib/python2.4/", "*.pyo" ),
    ( "usr/lib/", "*.a" ),
    ( "usr/lib/", "*.la" ),
    ( "lib/", "*.a" ),
    ( "lib/", "*.la" ),
    ( "var/db/comar/", "__db*" ),
    ( "var/db/comar/", "log.*" ),
)

# ptsp-client with dependencies lbuscd and ltspfs are needed.
# they are currently in playground. So we build and install them
# with --additional parameter.
PACKAGES = ["xorg-server"]
COMPONENTS = ["system.base"]

# start comar in chroot
def chroot_comar(image_dir):
    if os.fork() == 0:
        os.chroot(image_dir)
        subprocess.call(["/usr/bin/comar"])
        sys.exit(0)

    # wait comar to start
    timeout = 5
    wait = 0.1
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    while timeout > 0:
        try:
            sock.connect("%s/var/run/comar.socket" % image_dir)
            return True
        except:
            timeout -= wait
        time.sleep(wait)
    return False

# run command and terminate if something goes wrong
def run(cmd, ignore_error=False):
    print cmd
    ret = os.system(cmd)
    if ret and not ignore_error:
        print "%s returned %s" % (cmd, ret)
        sys.exit(1)

def get_exclude_list(output_dir):
    import fnmatch
       
    temp = default_exclude_list.split()
    for exc in default_glob_excludes:
        path = os.path.join(output_dir, exc[0])
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, exc[1]):
                    temp.append(os.path.join(root[len(output_dir)+1:], name))
    return temp

def shrink_rootfs(output_dir):
    excludes = get_exclude_list(output_dir)
    for x in excludes:
       os.system("rm -rf %s/%s" % (output_dir, x))

def create_ptsp_rootfs(output_dir, repository, add_pkgs):
    try:
        # Add repository of the packages
        run('pisi --yes-all --destdir="%s" add-repo pardus %s' % (output_dir, repository))

        # Install default components
        for component in COMPONENTS:
            run('pisi --yes-all --ignore-comar --ignore-file-conflicts -D"%s" it -c %s' % (output_dir, component))
    
        # Install default packages
        for package in PACKAGES:
            run('pisi --yes-all --ignore-comar --ignore-file-conflicts -D"%s" it %s' % (output_dir, package))

        # Install additional packages
        for package in add_pkgs:
            run('pisi --yes-all --ignore-comar --ignore-file-conflicts -D"%s" it %s' % (output_dir, package))

        # Create /etc from baselayout
        path = "%s/usr/share/baselayout/" % output_dir
        path2 = "%s/etc" % output_dir
        for name in os.listdir(path):
            run('cp -p "%s" "%s"' % (os.path.join(path, name), os.path.join(path2, name)))

        # Use proc and sys of the current system
        run('/bin/mount --bind /proc %s/proc' % output_dir)
        run('/bin/mount --bind /sys %s/sys' % output_dir)

        # run command in chroot
        def chrun(cmd):
            run('chroot "%s" %s' % (output_dir, cmd))
        
        chrun("/sbin/ldconfig")
        chrun("/sbin/update-environment")
        chroot_comar(output_dir)
        chrun("/usr/bin/hav call-package System.Package.postInstall baselayout")
        chrun("/usr/bin/pisi configure-pending")
        
        # create root
        chrun("hav call User.Manager.setUser uid 0 password pardus")

        chrun("/usr/bin/comar --stop")
        
        chrun("/sbin/update-modules")

        suffix = os.readlink("%s/boot/latestkernel" % output_dir).split("kernel-")[1]
        chrun("/sbin/depmod -a %s" % suffix)
        
        file(os.path.join(output_dir, "etc/pardus-release"), "w").write("Pardus 2007\n")

        shrink_rootfs(output_dir)

        # devices will be created in postinstall of ptsp-server
        os.unlink("%s/dev/null" % output_dir)
        shutil.rmtree("%s/lib/udev/devices" % output_dir)

        run('umount %s/proc' % output_dir)
        run('umount %s/sys' % output_dir)
    except KeyboardInterrupt:
        run('umount %s/proc' % output_dir, ignore_error=True)
        run('umount %s/sys' % output_dir, ignore_error=True)
        sys.exit(1)

def usage():
    print "\nUsage: build-client.py [option ...]\n"
    print "Following options are available:\n"
    print "    -h, --help            display this help and exit"
    print "    -o, --output          create the ptsp client rootfs into the given output path"
    print "    -r, --repository      ptsp client rootfs packages will be installed from this repository"
    print "    -a, --additional      install the given additional packages to ptsp client rootfs"

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:r:a:",
                                    [ "help", "output=", "repository=", "--additional"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    repository = "http://paketler.pardus.org.tr/pardus-2007/pisi-index.xml.bz2"
    output_dir = None
    add_pkgs   = []

    for opt in opts:
        if opt[0] in ( "-h", "--help" ):
            usage()
            sys.exit(0)

        if opt[0] in ( "-o", "--output" ):
            output_dir = opt[1]

        if opt[0] in ( "-r", "--repository" ):
            repository = opt[1]

        if opt[0] in ( "-a", "--additional" ):
            add_pkgs.append(opt[1])

    if not output_dir:
        usage()
        print "\nPtsp client rootfs output directory must be specified..."
        sys.exit(1)

    create_ptsp_rootfs(output_dir, repository, add_pkgs)
    
