#!/usr/bin/env python3
"""
Entry point script for the EQDKP Parser application.
"""
import sys
import os
import argparse

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import main

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='EQDKP Parser Application')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(debug=args.debug) 