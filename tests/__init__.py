import unittest
from .ln_translator_tests import LNTranslatorTests
from .rpn_translator_tests import RPNTranslatorTests

test_cases = (
        LNTranslatorTests,
        RPNTranslatorTests
        )

def main():
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader

    for test_case in test_cases:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        suite.addTests(tests) 

    tests_runner = unittest.TextTestRunner()
    tests_runner.run(suite)
