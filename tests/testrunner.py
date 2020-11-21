import os
import sys
import unittest

from dragonfly import get_engine

from castervoice.lib.ctrl.mgr.errors import GuidanceRejectionException
from castervoice.lib.util import guidance
from tests.test_util import settings_mocking, utilities_mocking


def reject_file_writing():
    raise GuidanceRejectionException()


def get_master_suite():
    return unittest.defaultTestLoader.discover(os.path.dirname(__file__))


def run_tests():
    get_engine("text")
    settings_mocking.prevent_initialize()
    utilities_mocking.mock_toml_files()
    return unittest.TextTestRunner(verbosity=2).run(get_master_suite())


if __name__ == '__main__':
    guidance.offer = reject_file_writing
    result = run_tests()
    sys.exit(len(result.failures) + len(result.errors) + len(result.unexpectedSuccesses))
