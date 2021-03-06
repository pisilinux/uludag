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

import sys
from optparse import OptionParser

import pisi
from pisi.uri import URI
from pisi.cli.commands import *

class ParserError(Exception):
    pass


class PreParser(OptionParser):
    """consumes any options, and finds arguments from command line"""

    def __init__(self, version):
        OptionParser.__init__(self, usage=usage_text, version=version)

    def error(self, msg):
        raise ParserError, msg
        
    def parse_args(self, args=None):
        self.rargs = self._get_args(args)
        self._process_args()
        return self.args

    def _process_args(self):
        args = []
        rargs = self.rargs
        if not self.allow_interspersed_args:
            first_arg = False
        while rargs:
            arg = rargs[0]
            def option():
                if not self.allow_interspersed_args and first_arg:
                    self.error('Options must precede non-option arguments')
                del rargs[0]
                return
            # We handle bare "--" explicitly, and bare "-" is handled by the
            # standard arg handler since the short arg case ensures that the
            # len of the opt string is greater than 1.
            if arg == "--":
                del rargs[0]
                break
            elif arg[0:2] == "--":
                # process a single long option (possibly with value(s))
                option()
            elif arg[:1] == "-" and len(arg) > 1:
                # process a cluster of short options (possibly with
                # value(s) for the last one only)
                option()
            else: # then it must be an argument
                args.append(arg)
                del rargs[0]
        self.args = args


class PisiCLI(object):

    def __init__(self):
        # first construct a parser for common options
        # this is really dummy
        self.parser = PreParser(version="%prog " + pisi.__version__)

        try:
            args = self.parser.parse_args()
            if len(args)==0: # more explicit than using IndexError
                print 'No command given'
                self.die()
            cmd_name = args[0]
        except ParserError:
            print 'Command line parsing error'
            self.die()

        self.command = Command.get_command(cmd_name)
        if not self.command:
            print "Unrecognized command: ", cmd
            self.die()

    def die(self):
        self.parser.print_help()
        sys.exit(1)

    def run_command(self):
        self.command.run()
