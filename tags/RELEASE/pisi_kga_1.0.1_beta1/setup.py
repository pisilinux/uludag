#!/usr/bin/env python
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
#
# Authors:  İsmail Dönmez <ismail@uludag.org.tr>

import kdedistutils

kdedistutils.setup(
    name="pisi_kga",
    version="1.0.1_beta1",
    author="İsmail Dönmez",
    author_email="ismail@uludag.org.tr",
    url="http://www.uludag.org.tr/projeler/pisi/index.html",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = ['src/PisiKga.py', 'src/ThreadRunner.py','src/MainWindow.ui',
                        'src/Progress.ui','src/ProgressDialog.py','src/SuccessDialog.ui','src/Success.py',
                        'src/PisiUi.py','src/PreferencesDialog.ui','src/Preferences.py','src/pisianime.gif',
                        'src/RepoDialog.ui','src/HelpDialog.py','src/Enums.py','src/UpdateWizardDialog.ui',
                        'src/CustomUpdatesDialog.ui','src/FastUpdatesDialog.ui',
                        ("/usr/kde/3.5/share/apps/pisi_kga/help",["help"])],
    executable_links = [('pisi-kga','PisiKga.py')],
    i18n = ('po',['src']),
    kcontrol_modules = [ ('src/pisi_kga.desktop','PisiKga.py')],
    )
