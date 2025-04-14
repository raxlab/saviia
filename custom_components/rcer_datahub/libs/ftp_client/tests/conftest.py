"""
This is a configuration file for pytest. It sets up the test environment by modifying the Python path
to include the project's root directory, allowing for proper imports of project modules during testing.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))