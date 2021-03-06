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
import ldap
import ldap.modlist

import ajan.config


class LdapClass:
	
    """ Designed for Ldap format for entries of modules of ajan """
    	
    def __init__(self, attr={}):
        self.fromEntry(attr)
    
    def fromEntry(self, attr):
	    
	""" 'entries' is a tuple of tuples in format varname, attrname, valuetype and  default values respectively
	    fromEntry  reads attribute names , makes necessary format casts and stores in LDapClass' 'varname' attribute 
	"""
        for varname, attrname, valuetype, default in self.entries:
            value = attr.get(attrname, None)
            if value:
                if valuetype == int:
                    val = int(value[0])
                elif valuetype == str:
                    val = unicode(value[0])
                elif valuetype == set:
                    val = set(value)
                else:
                    val = value
            else:
                val = default
		
	    # self.varname=val :
            setattr(self, varname, val)
    
    def toEntry(self):
	    
	"""  Reads attributes from entries to a list'attr' 
	     If the attribute type is int type conversion is made to str    
	"""
        attr = {}
        for item in self.entries:
            val = getattr(self, item[0])
            if item[2] == int:
                val = [str(val)]
            elif item[2] == str:
                val = [val]
            elif item[2] == set:
                val = list(val)
            attr[item[1]] = val
        return attr
    
    def __str__(self):
	
	""" overrides method -str() cast- for 'entries's tuples to become a string in wanted format"""
        text = []
        for varname, attrname, valuetype, default in self.entries:
            value = getattr(self, varname, "")
            text.append("%s: %s" % (attrname, value))
        return "\n".join(text)


class Connection:
	
    def __init__(self):
	
	""" opens ldap connection, connection attribute : 'conn' 
	    'ldap' is the LdapDomain object defined in config.py
	"""
        conf = ajan.config.ldap
        conn = ldap.open(conf.uri)
        if conf.bind_dn:
            conn.simple_bind_s(conf.bind_dn, conf.bind_password)
        self.conn = conn
    
    def close(self):
	""" Closes connection"""
        self.conn.unbind_s()
        self.conn = None
    
    def search_computer(self):
	"""Searcehs computer by computer_dn or withhostname"""    
        name= ajan.config.computer_dn
        if name:
            return self.conn.search_s(
                name,
                ldap.SCOPE_BASE,
                "objectClass=pardusComputer"
            )
        else:
            # If computer DN is not specified, search with hostname
            name = os.uname()[1]
            return self.conn.search_s(
                ajan.config.ldap.base_dn,
                ldap.SCOPE_SUBTREE,
                "(&(objectClass=pardusComputer)(cn=%s))" % name
            )
    
    def search_ou(self, unit):
	    
	""" Searches for 'organizational unit' members """
        if unit.startswith("ou="):
            ret = self.conn.search_s(
                unit,
                ldap.SCOPE_BASE,
                "objectClass=organizationalUnit"
            )
        else:
            ret = self.conn.search_s(
                ajan.config.ldap.base_dn,
                ldap.SCOPE_SUBTREE,
                "(&(objectClass=organizationalUnit)(ou=%s))" % unit
            )
        return ret
