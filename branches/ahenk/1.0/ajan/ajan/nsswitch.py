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

header = """#
# Auto generated by Ahenk
#

"""

class NSSDB:
    def __init__(self, line=None):
        self.name = ""
        self.sources = []
        if line:
            self.name, rest = line.split(":", 1)
            self.sources = rest.split()
    
    def __str__(self):
        return "%s:\t%s" % (self.name, " ".join(self.sources))


class NameServiceSwitch:
    conf_file = "/etc/nsswitch.conf"
    
    def __init__(self):
        """Reads valid entries from conf_file , appends them to 'db' attribute """
        self.db = []
        for line in file(self.conf_file):
            line = line.strip()
            if line and not line.startswith("#"):
                self.db.append(NSSDB(line))
    
    def __getitem__(self, key):
        """ __getitem__ is overwritten in ordeer to get db items by their name attribute """
        for db in self.db:
            if db.name == key:
                return db
        raise IndexError
    
    def save(self):
        """  Wite entries of 'db' attribute to the related configuration file  """
        
        f = file(self.conf_file, "w")
        f.write(header + "\n".join(map(str, self.db)) + "\n")
        f.close()
