#!/usr/bin/env python3

import os
import sys
import unittest

from test.util import engine

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

if __name__ == '__main__':
    unittest.main()

class TestExcalidraw(engine.ComposeIntegrationTestCase):
    service = 'excalidraw'
