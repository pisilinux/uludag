#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys
import os
import locale
import comar
import time

# i18n

import gettext
__trans = gettext.translation('mudur', fallback=True)
_ = __trans.ugettext

# Utilities

def comlink():
    com = comar.Link()
    com.localize()
    return com

def report_error(reply):
    if reply.command == "denied":
        print _("You dont have permission to do this operation.")
    elif reply.command == "none":
        if reply.data == "noapp":
            print _("There is no such service.")
        else:
            print _("Service doesn't provide this operation.")
    else:
        print _("%s error: %s") % (reply.script, reply.data)

def collect(c):
    reply = c.read_cmd()
    if reply.command == "start":
        replies = []
        while True:
            reply = c.read_cmd()
            if reply.command == "end":
                return replies
            replies.append(reply)
    else:
        return [reply]

# Operations

class Service:
    types = {
        "local": _("local"),
        "script": _("script"),
        "server": _("server"),
    }
    
    def __init__(self, name, info=None):
        self.name = name
        self.running = ""
        self.autostart = ""
        if info:
            type, state, self.description = info.split("\n")
            self.state = state
            self.type = self.types[type]
            if state in ("on", "started"):
                self.running = _("running")
            if state in ("on", "stopped"):
                self.autostart = _("yes")


def format_service_list(services, use_color=True):
    if os.environ.get("TERM", "") == "xterm":
        colors = {
            "on": '[0;32m',
            "started": '[1;32m',
            "stopped": '[0;31m',
            "off": '[0m'
        }
    else:
        colors = {
            "on": '[1;32m',
            "started": '[0;32m',
            "stopped": '[1;31m',
            "off": '[0m'
        }
    name_title = _("Service")
    run_title = _("Status")
    auto_title = _("Autostart")
    desc_title = _("Description")
    
    name_size = max(max(map(lambda x: len(x.name), services)), len(name_title))
    run_size = max(max(map(lambda x: len(x.running), services)), len(run_title))
    auto_size = max(max(map(lambda x: len(x.autostart), services)), len(auto_title))
    desc_size = len(desc_title)
    
    line = "%s | %s | %s | %s" % (
        name_title.center(name_size),
        run_title.center(run_size),
        auto_title.center(auto_size),
        desc_title.center(desc_size)
    )
    print line
    print "-" * (len(line))
    
    cstart = ""
    cend = ""
    if use_color:
        cend = "\x1b[0m"
    for service in services:
        if use_color:
            cstart = "\x1b%s" % colors[service.state]
        line = "%s%s%s | %s%s%s | %s%s%s | %s%s%s" % (
            cstart,
            service.name.ljust(name_size),
            cend, cstart,
            service.running.center(run_size),
            cend, cstart,
            service.autostart.center(auto_size),
            cend, cstart,
            service.description,
            cend
        )
        print line

def list(use_color=True):
    c = comlink()
    c.call("System.Service.info")
    data = collect(c)
    services = filter(lambda x: x.command == "result", data)
    errors = filter(lambda x: x.command != "result", data)
    
    if len(services) > 0:
        services.sort(key=lambda x: x.script)
        lala = []
        for item in services:
            lala.append(Service(item.script, item.data))
        format_service_list(lala, use_color)
    
    if len(errors) > 0:
        print
        map(report_error, errors)

def checkDaemon(pidfile):
    if not os.path.exists(pidfile):
        return False
    pid = file(pidfile).read().rstrip("\n")
    if not os.path.exists("/proc/%s" % pid):
        return False
    return True

def manage_comar(op):
    if os.getuid() != 0:
        print _("You should be the root user in order to control the comar service.")
        sys.exit(1)
    
    comar_pid = "/var/run/comar.pid"
    
    if op == "stop" or op == "restart":
        os.system("/sbin/start-stop-daemon --stop --pidfile %s" % comar_pid)
    
    timeout = 5
    while checkDaemon(comar_pid) and timeout > 0:
        time.sleep(0.2)
        timeout -= 0.2
    
    if op == "start" or op == "restart":
        os.system("/sbin/start-stop-daemon -b --start --pidfile %s --make-pidfile --exec /usr/bin/comar" % comar_pid)

def manage_service(service, op, use_color=True):
    c = comlink()
    
    if op == "start":
        c.System.Service[service].start()
    elif op == "stop":
        c.System.Service[service].stop()
    elif op == "reload":
        c.System.Service[service].reload()
    elif op == "on":
        c.System.Service[service].setState(state="on")
    elif op == "off":
        c.System.Service[service].setState(state="off")
    elif op in ["info", "status", "list"]:
        c.System.Service[service].info()
    elif op == "restart":
        manage_service(service, "stop")
        manage_service(service, "start")
        return
    
    reply = c.read_cmd()
    if reply.command != "result":
        report_error(reply)
        # LSB compliant exit codes
        if op == "status":
            sys.exit(4)
        sys.exit(1)
    
    if op == "start":
        print _("Service '%s' started.") % service
    elif op == "stop":
        print _("Service '%s' stopped.") % service
    elif op in ["info", "status", "list"]:
        s = Service(reply.script, reply.data)
        format_service_list([s], use_color)
        if op in ["info", "status"]:
            # LSB compliant status codes
            if s.state in ["on", "started"]:
                sys.exit(0)
            else:
                sys.exit(3)
    elif op == "reload":
        print _("Service '%s' reloaded.") % service
    elif op == "on":
        print _("Service '%s' will be auto started.") % service
    elif op == "off":
        print _("Service '%s' won't be auto started.") % service

# Usage

def usage():
    print _("""usage: service [<options>] [<service>] <command>
where command is:
 list     Display service list
 status   Display service status
 info     Display service status
 on       Auto start the service
 off      Don't auto start the service
 start    Start the service
 stop     Stop the service
 restart  Stop the service, then start again
 reload   Reload the configuration (if service supports this)
and option is:
 -N, --no-color  Don't use color in output""")

# Main

def main(args):
    operations = ("start", "stop", "info", "list", "restart", "reload", "status", "on", "off")
    use_color = True
    
    # Parameters
    if "--no-color" in args:
        args.remove("--no-color")
        use_color = False
    if "-N" in args:
        args.remove("-N")
        use_color = False
    
    # Operations
    if args == []:
        list(use_color)
    
    elif args[0] == "list" and len(args) == 1:
        list(use_color)
    
    elif args[0] == "help":
        usage()
    
    elif len(args) < 2:
        usage()
    
    elif args[0] == "comar":
        manage_comar(args[1])
    
    elif args[1] in operations:
        manage_service(args[0], args[1], use_color)
    
    else:
        usage()

#

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    main(sys.argv[1:])
