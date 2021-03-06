#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

# CORE_PROF.py
# Event Subsystem (Draft).

class profileSubsystem:
	def __init__(self):
		pass
	def createEvent(self, prmlist = {}, callerInfo = None):
		"""Return a new event id.
	Parameters: None
	Returns a (COMARString) with new eventid or Null string for error (such as ACL error)"""
		pass
	def checkEventId(self, prmlist = {}, callerInfo = None):
		""" Check availability of event eventid
	Parameters:
		eventid, id (COMARString): id of checked event.."""
		pass
	def addEventQue(self, prmlist = {}, callerInfo = None):
		""" Register a new method to Event Process Queue
	callerInfo must contain valid call source information.
	Parameters:
		object		(COMARObject): Object for call.
		method		(COMARString): method of Object for call
		eventid, id	(COMARString): event_id for requested event.
		wait (optional, default "N") (COMARString) : If "Y", COMARd check for object is currently running and wait for end of object.
	return   : A key (COMARString) for use with delEventQue..
"""
		pass
	def delEventQue(self, prmlist = {}, callerInfo = None):
		""" Delete a previously registered method from event process Queue
	Parameters:
		event_id
		queue_key, key
"""
		pass
	def trigger(self, prmlist = {}, callerInfo = None):
		""" Start a event's processing
	Parameters:
		event_id, id, eventid (COMARString)
"""
