"""
MetadataToLens - Automatic Camera & Lens Metadata Pipeline for Nuke

Nuke initialization script. This file is automatically loaded when Nuke starts.
It sets up the plugin and registers the menu.

Author: MetadataToLens Contributors
License: MIT
"""

import sys
import os
from pathlib import Path

# Get the .nuke directory
NUKE_DIR = Path(__file__).parent

# Add metadata_to_lens to Python path
if str(NUKE_DIR) not in sys.path:
    sys.path.insert(0, str(NUKE_DIR))

print(f"[MetadataToLens] Initialized from: {NUKE_DIR}")
print(f"[MetadataToLens] Python path updated")

# Try to import and verify the package
try:
    import metadata_to_lens
    print(f"[MetadataToLens] Package imported successfully (v{metadata_to_lens.__version__})")
except ImportError as e:
    print(f"[MetadataToLens] Warning: Could not import metadata_to_lens: {e}")
