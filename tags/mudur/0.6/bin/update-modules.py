#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys
import os
import stat
import subprocess

header = "### This file is automatically generated by update-modules"

header_note = """
#
# Please do not edit this file directly. If you want to change
# anything, please take a look at the files in /etc/modules.d
# and read the Pardus initialization system documentation.
#
# Bu otomatik olarak oluşturulmuş bir dosyadır.
# Lütfen bu dosyayı elle değiştirmeyin. Değiştirmek istediğiniz
# şeyler varsa, /etc/modules.d dizinindeki dosyalara ve Pardus
# açılış sistemi belgesine bakın.
#
"""

#
# modules.d utilities
#

def read_modules_d():
    data = []
    for name in os.listdir("/etc/modules.d"):
        path = os.path.join("/etc/modules.d", name)
        # skip dirs (.svn, .cvs, etc)
        if stat.S_ISDIR(os.stat(path).st_mode):
            continue
        # skip backup and version control files
        if name.endswith("~") or name.endswith(".bak") or name.endswith(",v"):
            continue
        # skip pisi oldconfig files
        if name.endswith(".oldconfig"):
            continue
        
        f = file(path)
        data.append((path, f.read()))
        f.close()
    
    def key(x):
        return x[0]
    data.sort(key=key)
    
    return data

def join_modulesd(modulesd):
    lines = []
    for path, data in modulesd:
        for line in data.split("\n"):
            if line == "" or line.startswith("#"):
                continue
            lines.append(line)
    return lines

def parse_line(modulesd_line):
    line = modulesd_line.rstrip("\n")
    # skip spurios add
    if line.startswith("add "):
        line = line[4:]
    
    rest = None
    op, name = line.split(None, 1)
    if " " in name or "\t" in name:
        name, rest = name.split(None, 1)
        rest = rest.rstrip()
    
    return (op, name, rest)

#
# Old style modules.conf for modutils
#

def generate_modules_conf(out, modulesd):
    out.write(header)
    out.write(header_note)
    for path, data in modulesd:
        out.write("### modules-update: start processing %s\n" % path)
        out.write(data)
        out.write("\n### modules-update: end processing %s\n\n" % path)

#
# New style modprobe.conf for module-init-tools
#

class ModOp:
    def __init__(self, name):
        self.name = name
        self.pre = None
        self.op = None
        self.post = None
    
    def write(self, out, op):
        out.write("%s %s " % (op, self.name))
        if self.pre:
            out.write("{ %s; } ; " % self.pre)
        if self.op:
            out.write(self.op)
        else:
            if op == "install":
                tmp = "--first-time --ignore-install"
            else:
                tmp = "-r --first-time --ignore-remove"
            out.write("/sbin/modprobe %s %s" % (tmp, self.name))
        if self.post:
            out.write(" && { %s; }" % self.post)
        out.write("\n")


def find_alias_dest(dest, lines):
    for line in lines:
        op, name, rest = parse_line(line)
        if op == "alias" and name == dest:
            return find_alias_dest(rest, lines)
    return dest

def find_alias_name(name):
    tmp = name.split("-")
    if len(tmp) != 3 or (tmp[0] != "block" and tmp[0] != "char") or tmp[1] != "major":
        return name
    for x in tmp[2]:
        if not x in "0123456789":
            return name
    return name + "-*"

def generate_modprobe_conf(out, modulesd):
    lines = join_modulesd(modulesd)
    aliases = {}
    options = []
    install_ops = {}
    remove_ops = {}
    
    def set_op(name, op, rest):
        if op.endswith("install"):
            dict = install_ops
        else:
            dict = remove_ops
        
        if dict.has_key(name):
            mod = dict[name]
        else:
            mod = ModOp(name)
            dict[name] = mod
        
        if op.startswith("post"):
            mod.post = rest
        elif op.startswith("pre"):
            mod.pre = rest
        else:
            mod.op = rest
    
    for line in lines:
        op, name, rest = parse_line(line)
        
        if op == "alias":
            if rest == "off" or rest == "null":
                set_op(name, "install", "/bin/true");
            else:
                name = find_alias_name(name)
                dest = find_alias_dest(rest, lines)
                aliases[name] = dest
        
        elif op == "options":
            opts = []
            modopts = []
            next = False
            for opt in rest.split():
                if opt == "-o":
                    modopts.append("-o")
                    next = True
                else:
                    if next:
                        modopts.append(opt)
                    else:
                        opts.append(opt)
                    next = False
            if len(modopts) > 0:
                set_op(name, "install", "/sbin/modprobe %s --ignore-install %s" % (
                    " ".join(modopts), find_alias_dest(name, lines)))
            if len(opts) > 0:
                options.append("options %s %s" % (name, " ".join(opts)))
        
        elif op == "above":
            rest = rest.split()
            tmp = "; ".join(map(lambda x: "/sbin/modprobe %s" % x, rest))
            set_op(name, "post_install", tmp + "; /bin/true")
            tmp = "; ".join(map(lambda x: "/sbin/modprobe -r %s" % x, rest))
            set_op(name, "pre_remove", tmp)
        
        elif op == "below":
            rest = rest.split()
            tmp = "; ".join(map(lambda x: "/sbin/modprobe %s" % x, rest))
            set_op(name, "pre_install", tmp)
            tmp = "; ".join(map(lambda x: "/sbin/modprobe -r %s" % x, rest))
            set_op(name, "post_remove", tmp + "; /bin/true")
        
        elif op == "install":
            set_op(name, "install", rest)
        
        elif op == "pre-install":
            set_op(name, "pre_install", rest)
        
        elif op == "post-install":
            set_op(name, "post_install", rest)
        
        elif op == "remove":
            set_op(name, "remove", rest)
        
        elif op == "pre-remove":
            set_op(name, "pre_remove", rest)
        
        elif op == "post-remove":
            set_op(name, "post_remove", rest)
        
        elif op == "probe":
            rest = rest.split()
            tmp = " || ".join(map(lambda x: "/sbin/modprobe %s" % x, rest))
            set_op(name, "install", tmp)
        
        elif op == "probeall":
            rest = rest.split()
            tmp = "; ".join(map(lambda x: "/sbin/modprobe %s" % x, rest))
            set_op(name, "install", tmp + "; /bin/true")
        
        # prune, ifdef, othercrap not converted
    
    out.write(header)
    out.write(header_note)
    keys = aliases.keys()
    keys.sort()
    out.write("\n".join(map(lambda x: "alias %s %s" % (x, aliases[x]), keys)))
    out.write("\n\n")
    out.write("\n".join(options))
    out.write("\n\n")
    for item in install_ops:
        install_ops[item].write(out, "install")
    out.write("\n")
    for item in remove_ops:
        remove_ops[item].write(out, "remove")
    out.write("\n")

#
# modules.dep updater
#

def update_depmod():
    # Call depmod to stop insmod from complaining that modules.conf
    # is more recent than modules.dep
    if os.path.exists("/proc/modules"):
        subprocess.call(["/sbin/depmod", "-a"])

#
# Main
#

def update_modules():
    modulesd = read_modules_d()
    # No need to generate modules.conf (for 2.4 kernels) anymore
    #generate_modules_conf(sys.stdout, modulesd)
    generate_modprobe_conf(file("/etc/modprobe.conf", "w"), modulesd)
    update_depmod()

def main(args):
    # FIXME: check prefix,force,help arguments
    update_modules()

if __name__ == "__main__":
    main(sys.argv[1:])
