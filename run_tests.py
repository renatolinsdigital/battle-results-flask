#!/usr/bin/env python

import os
import sys
import unittest
import coverage

# Set up coverage
COV = coverage.coverage(
    branch=True,
    include='*.py',
    omit=[
        'tests/*',
        'venv/*',
        '*/site-packages/*'
    ]
)
COV.start()

# Set test directory
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, TEST_DIR + '/../')

# Find and run tests


def run_tests():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

# Run tests with coverage


def run_tests_with_coverage():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--coverage':
        exit_code = run_tests_with_coverage()
    else:
        exit_code = run_tests()
    sys.exit(exit_code)
