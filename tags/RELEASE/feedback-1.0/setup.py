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
# Authors:  Bahadır Kandemir <bahadir@haftalik.net>

import kdedistutils

kdedistutils.setup(
    name="feedback",
    version="1.0",
    author="Bahadır Kandemir",
    author_email="bahadir@haftalik.net",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = ['src/feedback.py', 'src/usagedlg.py', 'src/experiencedlg.py', 'src/welcomedlg.py',
                        'src/purposedlg.py', 'src/questiondlg.py', 'src/personalinfodlg.py', 'src/opiniondlg.py',
                        'src/hardwareinfodlg.py', 'src/upload.py', 'src/goodbyedlg.py',
                        'src/usagedlg.ui', 'src/purposedlg.ui', 'src/hardwareinfodlg.ui', 'src/experiencedlg.ui',
                        'src/questiondlg.ui', 'src/goodbyedlg.ui', 'src/opiniondlg.ui', 'src/welcomedlg.ui',
                        'src/personalinfodlg.ui', 'src/upload.ui', 'src/feedback.png', 'src/feedback.png',
                        ("/usr/kde/3.5/share/applications/kde/",["src/feedback.desktop"])],
    executable_links = [('feedback','feedback.py')],
    i18n = ('po',['src'])
    )
