# Case Conductor is a Test Case Management system.
# Copyright (C) 2011 uTest Inc.
#
# This file is part of Case Conductor.
#
# Case Conductor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Case Conductor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.
"""
Tests for Product model.

"""
from django.test import TestCase

from ... import factories as F



class ProductTest(TestCase):
    def test_unicode(self):
        """Unicode representation is name of Product"""
        p = F.ProductFactory.build(name="Firefox")

        self.assertEqual(unicode(p), u"Firefox")


    def test_clone_no_cases(self):
        """
        Cloning a Product does not clone test cases.

        """
        c = F.CaseFactory()

        new = c.product.clone()

        self.assertEqual(len(new.cases.all()), 0)


    def test_clone_no_suites(self):
        """
        Cloning a Product does not clone test suites.

        """
        s = F.SuiteFactory()

        new = s.product.clone()

        self.assertEqual(len(new.cases.all()), 0)