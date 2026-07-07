"""
MetadataToLens - Automatic Camera & Lens Metadata Pipeline for Nuke

A production-ready plugin for Nuke 17.0+ that automatically reads camera metadata
from EXR files (ARRI, RED, Sony, Canon, Blackmagic) and synchronizes parameters
to Camera and LensCore nodes.

Author: MetadataToLens Contributors
License: MIT
Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "MetadataToLens Contributors"
__license__ = "MIT"

import sys
import logging
from pathlib import Path

# Setup logging
logger = logging.getLogger("MetadataToLens")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Add package to path
PACKAGE_ROOT = Path(__file__).parent.parent

__all__ = [
    "metadata_reader",
    "camera_sync",
    "constants",
    "logger",
]
