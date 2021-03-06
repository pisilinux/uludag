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

from qt import *

from yali.steps import Steps

##
# Screens...
class Screens(QObject, Steps):

    def __init__(self, *args):
        Steps.__init__(self)
        apply(QObject.__init__, (self,) + args)

    ##
    # add new a screen
    # @param stage(int): stage number that the screen belongs to.
    # @param index(int): index number.
    # @param widget(QWidget): screen data. Can be a QWidget for GUI implementation.
    def addScreen(self, index, stage, widget):
        data = ScreenData(stage, widget)
        self.addStep(index, data)
        self.emit(PYSIGNAL("signalAddScreen"), (self, widget))


    def next(self):

        # we are finished with the current screen. Call the widget's
        # execute() function to do it's work.
        self.getCurrent().getWidget().execute()

        nxt = self.getCurrentIndex() + 1
        if self.hasIndex(nxt):
            self.__setCurrent(nxt)

    def previous(self):
        prev = self.getCurrentIndex() - 1
        if self.hasIndex(prev):
            self.__setCurrent(prev)
        

    def nextDisabled(self):
        self.emit(PYSIGNAL("nextButtonDisabled"), ())

    def prevDisabled(self):
        self.emit(PYSIGNAL("prevButtonDisabled"), ())

    def nextEnabled(self):
        self.emit(PYSIGNAL("nextButtonEnabled"), ())

    def prevEnabled(self):
        self.emit(PYSIGNAL("prevButtonEnabled"), ())


    ##
    # process events
    def processEvents(self):
        self.emit(PYSIGNAL("signalProcessEvents"), ())

    ##
    # Sets the current screen and logs.
    # @param index(int): screen index to be the current.
    def __setCurrent(self, index):
        Steps.setCurrent(self, index)
        self.emit(PYSIGNAL("signalCurrent"), (self, index))

        # trigger screen
        self.getCurrent().getWidget().shown()

        # FIXME: is it feasible to write the widget object in GUI mode???
        #yali.logger.log("Changed screen to %s." % self._steps.getCurrent())


        

class ScreenData:
    _stage = None
    _widget = None
    #_text = None

    def __init__(self, stage, widget):
        self._stage = stage
        self._widget = widget

    def getWidget(self):
        return self._widget

    def getStage(self):
        return self._stage
