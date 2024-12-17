#!/usr/bin/env python3
"""
Entry point script for the EQDKP Parser application.
"""
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == "__main__":
    main() 