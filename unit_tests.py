#!/usr/bin/env python3
import printer_tests
import unittest


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(loader.loadTestsFromModule(printer_tests))

    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)


if __name__ == "__main__":
    main()
