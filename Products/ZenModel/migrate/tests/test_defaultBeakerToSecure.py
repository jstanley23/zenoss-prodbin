#!/usr/bin/env python

import os
import unittest

import Globals
import common


class Test_UseBeakerInZope(unittest.TestCase, common.ServiceMigrationTestCase):
    """
    Test that beaker is added to zope's config file.
    """
    initial_servicedef = 'zenoss-resmgr-5.0.6_1-useBeakerInZope.json'
    expected_servicedef = 'zenoss-resmgr-5.0.6_1-defaultBeakerToSecure.json'
    migration_module_name = 'defaultBeakerToSecure'
    migration_class_name = 'DefaultBeakerToSecure'
       

if __name__ == '__main__':
    unittest.main()