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
# User management module for YALI.

import random
import crypt
import os

from yali.constants import consts


class User:

    def __init__(self, username = ''):
        self.username = username
        self.group = ''
        self.realname = ''
        self.home_dir = ''
        self.passwd = ''

        self.shadow_path = os.path.join(consts.target_dir, "etc/shadow")
        self.passwd_path = os.path.join(consts.target_dir, "etc/passwd")


    def changePasswd(self, passwd):
        shadowed_passwd = crypt.crypt(passwd, str(random.random())[-2:])

        shadow_content = open(self.shadow_path, 'r').readlines()
        shadow_file = open(self.shadow_path, 'w')

        for line in shadow_content:
            parts = line.split(':')
            if parts[0] == self.username:
                parts[1] = shadowed_passwd
            shadow_file.write(":".join(parts))
        shadow_file.close()

    def addUser(self):
        pass

    def delUser(self):
        pass

    def getAvailableUid(self):
        j = map(lambda x: int(x[2]), [line.split(':') for line in open(self.passwd_path, 'r').readlines()])
        j.sort()

        for i in range(1000 + len(j), 1000, -1):
            if [int(x)+1 for x in j if i != int(x) if i == int(x) + 1]:
                return i
        return i-1


if __name__ == '__main__':
    pass

