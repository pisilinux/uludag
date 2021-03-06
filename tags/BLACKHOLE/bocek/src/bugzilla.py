#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

import httplib
import urllib
import consts
import sys

class bugzilla:
    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "text/plain"}
        self.logs=True

    def logger(self,msg):
        if self.logs:
            for line in msg.split("\n"):
                print "DEBUG : %s" % line

    def atomicSender(self,page,parameters):
        try:
            connection = httplib.HTTPConnection("%s:80" % consts.bugzilla["server"])
            connection.request("POST", consts.bugzilla[page], parameters, self.headers)
        except httplib.HTTPConnection:
            return False
        return connection.getresponse()

    def checkAuth(self,email,password):
        params = urllib.urlencode({'Bugzilla_login'     : email,
                                   'Bugzilla_password'  : password})

    def sendBug(self,email,password,summary,details):
        params = urllib.urlencode({'Bugzilla_login'     : email,
                                   'Bugzilla_password'  : password,
                                   'short_desc'         : summary,
                                   'comment'            : details,
                                   'bug_status'         : 'NEW',
                                   'product'            : consts.bugzilla['product'],
                                   'component'          : consts.bugzilla['component'],
                                   'version'            : consts.bugzilla['version'],
                                   'rep_platform'       : consts.bugzilla['platform'],
                                   'priority'           : consts.bugzilla['priority'],
                                   'op_sys'             : consts.bugzilla['op_sys'],
                                   'bug_severity'       : consts.bugzilla['severity'],
                                   'bug_file_loc'       : consts.bugzilla['bug_file_loc']})
        
        response = self.atomicSender("bugAdd",params)
        if response.reason=="OK":
            responseData = response.read()
            self.logger(responseData)
            if responseData.find(consts.bugzillaMsg["errorOnLogin"])==-1:
                return "Bug added successfully."
            return "Login failed. Check your e-mail and password."
        else:
            return "Connection error for server, please check your network configuration."
