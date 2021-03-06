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
import parser
import piksemel


#
# PSPEC Validator
#

class Pspec:
    once, one_or_more, optional, optional_once = range(4)
    
    def __init__(self):
        self.errors = []
    
    def error(self, node, msg):
        self.errors.append("%s: %s" % (node.name(), msg))
    
    def check(self, node, childs):
        counts = {}
        for tag in node.tags():
            name = tag.name()
            if childs.has_key(name):
                counts[name] = counts.get(name, 0) + 1
            else:
                self.error(node, "unknown tag <%s>" % name)
        for name in childs:
            mode = childs[name]
            if isinstance(mode, tuple):
                mode = mode[0]
            count = counts.get(name, 0)
            if mode == self.once:
                if count == 0:
                    self.error(node, "missing tag <%s>" % name)
                elif count > 1:
                    self.error(node, "tag <%s> should not appear more than once" % name)
            elif mode == self.one_or_more:
                if count == 0:
                    self.error(node, "tag <%s> should appear at least once" % name)
            elif mode == self.optional_once:
                if count > 1:
                    self.error(node, "optional tag <%s> should not appear more than once" % name)
        # recurse for child funcs
        for name in childs:
            arg = childs[name]
            if isinstance(arg, tuple):
                mode = arg[0]
                func = arg[1]
                if mode == self.once or mode == self.optional_once:
                    tag = node.getTag(name)
                    if tag:
                        func(tag)
                else:
                    for tag in node.tags(name):
                        func(tag)
    
    def check_attr(self, node, attrs):
        for attr in node.attributes():
            if not attrs.has_key(attr):
                self.error(node, "unknown attribute '%s'" % attr)
        for attr in attrs:
            mode = attrs[attr]
            vals = None
            if isinstance(mode, tuple):
                mode, vals = mode
            val = node.getAttribute(attr)
            if mode == self.once and val == None:
                self.error(node, "missing attribute '%s'" % attr)
            if val and vals and not val in vals:
                self.error(node, "keyword '%s' is not accepted for attribute '%s'" % (val, attr))
    
    def validate_dependency(self, node):
        self.check_attr(
            node, {
                "versionFrom": self.optional_once,
                "versionTo": self.optional_once,
                "version": self.optional_once,
                "releaseFrom": self.optional_once,
                "releaseTo": self.optional_once,
                "release": self.optional_once,
            }
        )
    
    def validate_source_archive(self, node):
        self.check_attr(
            node, {
                "sha1sum": self.once,
                "type": self.once,
            }
        )
    
    def validate_source_patch(self, node):
        self.check_attr(
            node, {
                "compressionType": self.optional_once,
                "level": self.optional_once,
                "target": self.optional_once,
            }
        )
    
    def validate_source_patches(self, node):
        self.check(
            node, {
                "Patch": (self.optional, self.validate_source_patch),
            }
        )
    
    def validate_source_build_deps(self, node):
        self.check(
            node, {
                "Dependency": (self.optional, self.validate_dependency),
            }
        )
    
    def validate_source(self, node):
        self.check(
            node, {
                "Name": self.once,
                "Homepage": self.once,
                "Icon": self.optional_once,
                "Packager": self.once,
                "License": self.one_or_more,
                "IsA": self.optional,
                "PartOf": self.optional,
                "Summary": self.one_or_more,
                "Description": self.one_or_more,
                "Archive": (self.once, self.validate_source_archive),
                "Patches": (self.optional_once, self.validate_source_patches),
                "BuildDependencies": (self.optional_once, self.validate_source_build_deps),
            }
        )
    
    def validate_package_files_path(self, node):
        self.check_attr(
            node, {
                "fileType": (self.once, (
                    "executable",
                    "library",
                    "data",
                    "config",
                    "doc",
                    "man",
                    "info",
                    "localedata",
                    "header",
                )),
                "permanent": (self.optional_once, ( "true", "false" ))
            }
        )
    
    def validate_package_runtime_deps(self, node):
        self.check(
            node, {
                "Dependency": (self.optional, self.validate_dependency),
            }
        )
    
    def validate_package_files(self, node):
        self.check(
            node, {
                "Path": (self.one_or_more, self.validate_package_files_path),
            }
        )
    
    def validate_additional_file(self, node):
        self.check_attr(
            node, {
                "owner": self.optional_once,
                "permission": self.optional_once,
                "target": self.once,
            }
        )
    
    def validate_additional_files(self, node):
        self.check(
            node, {
                "AdditionalFile": (self.optional, self.validate_additional_file),
            }
        )
    
    def validate_package_conflicts(self, node):
        self.check(
            node, {
                "Package": self.optional,
            }
        )
    
    def validate_package_provides_comar(self, node):
        self.check_attr(
            node, {
                "script": self.once,
            }
        )
    
    def validate_package_provides(self, node):
        self.check(
            node, {
                "COMAR": (self.optional, self.validate_package_provides_comar),
            }
        )
    
    def validate_package(self, node):
        self.check(
            node, {
                "Name": self.once,
                "License": self.optional,
                "IsA": self.optional,
                "PartOf": self.optional_once,
                "Summary": self.optional,
                "Description": self.optional,
                "RuntimeDependencies": (self.optional_once, self.validate_package_runtime_deps),
                "Files": (self.once, self.validate_package_files),
                "Conflicts": (self.optional_once, self.validate_package_conflicts),
                "AdditionalFiles": (self.optional_once, self.validate_additional_files),
                "Provides": (self.optional_once, self.validate_package_provides),
            }
        )
    
    def validate_history_update(self, node):
        self.check_attr(
            node, {
                "release": self.once,
                "type": (self.optional_once, ( "security", "enhancement", "bug" )),
            }
        )
        
        self.check(
            node, {
                "Date": self.once,
                "Version": self.once,
                "Comment": self.once,
                "Name": self.once,
                "Email": self.once,
            }
        )
    
    def validate_history(self, node):
        self.check(
            node, {
                "Update": (self.one_or_more, self.validate_history_update)
            }
        )
        
        prev = None
        for tag in node.tags("Update"):
            rel = tag.getAttribute("release")
            if rel:
                try:
                    rel = int(rel)
                except:
                    self.error(node, "bad release number '%s'" % rel)
                    rel = None
                if rel:
                    if prev:
                        prev -= 1
                        if rel != prev:
                            self.error(node, "unsorted release numbers")
                    prev = rel
        if prev != 1:
            self.error(node, "bad release numbers")
    
    def validate(self, path):
        try:
            doc = piksemel.parse(path)
        except piksemel.ParseError:
            self.errors.append("Invalid XML")
            return
        
        if doc.name() != "PISI":
            self.error(node, "wrong top level tag")
        
        self.check(
            doc, {
                "Source": (self.once, self.validate_source),
                "Package": (self.one_or_more, self.validate_package),
                "History": (self.once, self.validate_history),
            }
        )


#
# Source Repo Validator
#

class SourceRepo:
    def validate(self, path):
        nr = 0
        nr_errors = 0
        for root, dirs, files in os.walk(path):
            if "pspec.xml" in files:
                pspec_path = os.path.join(root, "pspec.xml")
                spec = Pspec()
                spec.validate(pspec_path)
                if len(spec.errors) > 0:
                    nr_errors += 1
                    print "----- %s -----" % pspec_path
                    for err in spec.errors:
                        print "  %s" % err
                else:
                    nr += 1
            # dont walk into the versioned stuff
            if ".svn" in dirs:
                dirs.remove(".svn")
        if nr_errors:
            print "-----"
            print "%d packages failed to validate" % nr_errors
            sys.exit(1)
        print "%d source packages validated" % nr


#
# Command line driver
#

def main(args):
    if os.path.isdir(args[0]):
        repo = SourceRepo()
        repo.validate(args[0])
    else:
        spec = Pspec()
        spec.validate(args[0])
        if len(spec.errors) > 0:
            for err in spec.errors:
                print err
            sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
