#!/usr/bin/env python

import unittest
import sys


def all_tests():
    from .test_pep8 import TestPep8
    from .test_arborapi import TestArborAPI

    suite = unittest.TestSuite()
    suite.addTest(TestPep8)
    suite.addTest(TestArborAPI)

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    status = runner.run(all_tests())

    if status.failures or status.errors:
        sys.exit(1)
    else:
        sys.exit(0)