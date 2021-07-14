#!/usr/bin/env python3
import utilities_tests
import unittest


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(loader.loadTestsFromModule(utilities_tests))

    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)

    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
