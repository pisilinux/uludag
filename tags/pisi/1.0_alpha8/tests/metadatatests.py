# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import unittest
import os

from pisi import metadata
from pisi import util
import pisi.context as ctx

import testcase
class MetaDataTestCase(testcase.TestCase):

    def testRead(self):
        md = metadata.MetaData()
        md.read('tests/popt/metadata.xml')

        self.assertEqual(md.package.license, ["As-Is"])

        self.assertEqual(md.package.version, "1.7")

        self.assertEqual(md.package.installedSize, 149691)
        return md
    
    def testWrite(self):
        md = self.testRead()
        md.write(os.path.join(ctx.config.tmp_dir(),'metadata-test.xml' ))

    def testVerify(self):
        md = self.testRead()
        if md.has_errors():
            self.fail("Couldn't verify!")


suite = unittest.makeSuite(MetaDataTestCase)
