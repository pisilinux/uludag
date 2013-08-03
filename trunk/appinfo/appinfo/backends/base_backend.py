#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

class Backend:

    def __init__(self):
        self.name = 'dummy'

    def getPackageList(self):
        pass

    def getPackageInfo(self, pkg_name):
        pass

    def getPackageFiles(self, pkg_name):
        pass

