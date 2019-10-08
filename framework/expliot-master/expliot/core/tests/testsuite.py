"""Test suite handler."""
import importlib
import inspect
import pkgutil
import sys

from expliot.core.tests.test import Test

sys.path.append("..")


class TestSuite(dict):
    """
    Test Suite class inherits from dict and stores all the test cases
    from plugins package name specified in __init__().
    """

    testcls = [Test]

    def __init__(self, pkgname="expliot.plugins"):
        """
        Initialize the test suite with the plugins in the package.

        :param pkgname: The package to load test case plugins from or
                        'expliot.plugins' if None specified
        """
        self.import_plugins(pkgname)

    def import_plugins(self, pkgname):
        """
        Import all tests from the specified package into a dict.

        :param pkgname: The package to load all test case plugins from
        :return:
        """
        packages = [pkgname]
        # Import from all subpackages recursively
        while len(packages) > 0:
            pkg = packages.pop()
            pmod = importlib.import_module(pkg)
            prefix = "{}.".format(pmod.__name__)
            for finder, name, is_pkg in pkgutil.iter_modules(pmod.__path__, prefix):
                if is_pkg:
                    packages.append(name)
                else:
                    mod = importlib.import_module(name)
                    for test_name, test_class in inspect.getmembers(mod):
                        if (
                            inspect.isclass(test_class)
                            and issubclass(test_class, Test)
                            and test_class not in TestSuite.testcls
                        ):
                            test = test_class()
                            self[test.id] = {
                                "class": test_class,
                                "summary": test.summary,
                            }
