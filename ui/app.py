#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "FileCompare"))

from file_compare_gui import FileCompareGUI

if __name__ == "__main__":
    app = FileCompareGUI()
    app.run()
