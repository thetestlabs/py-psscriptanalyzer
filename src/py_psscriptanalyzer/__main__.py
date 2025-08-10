#!/usr/bin/env python3
"""
Command-line interface for py-psscriptanalyzer.
"""

import sys

from .core import main

if __name__ == "__main__":
    sys.exit(main())
