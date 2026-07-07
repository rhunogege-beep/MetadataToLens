"""
MetadataToLens - Constants and Database

Defines constants for camera models, sensors, lenses, and metadata fields.

Author: MetadataToLens Contributors
License: MIT
"""

from enum import Enum
from typing import Dict, Tuple

# ============================================================================
# CAMERA MODELS & MANUFACTURERS
# ============================================================================

class CameraManufacturer(Enum):
    """Supported camera manufacturers"""
    ARRI = "ARRI"
    RED = "RED"
    SONY = "SONY"
    CANON = "CANON"
    BLACKMAGIC = "BLACKMAGIC"


# ============================================================================
# ARRI CAMERAS
# ============================================================================

ARRI_CAMERAS = {
    "ALEXA 35": {
        "manufacturer": "ARRI",
        "sensor_width_mm": 28.0,
        "sensor_height_mm": 15.77,
        "iso_native": 800,
        "supports_lut": True,
    },
    "ALEXA Mini LF": {
        "manufacturer": "ARRI",
        "sensor_width_mm": 36.70,
        "sensor_height_mm": 25.54,
        "iso_native": 800,
        "supports_lut": True,
    },
    "ALEXA XT Plus": {
        "manufacturer": "ARRI",
        "sensor_width_mm": 27.65,
        "sensor_height_mm": 15.52,
        "iso_native": 800,
        "supports_lut": True,
    },
    "ALEXA SXT": {
        "manufacturer": "ARRI",
        "sensor_width_mm": 27.65,
        "sensor_height_mm": 15.52,
        "iso_native": 800,
        "supports_lut": False,
    },
}

# ============================================================================
# RED CAMERAS
# ============================================================================

RED_CAMERAS = {
    "V-RAPTOR": {
        "manufacturer": "RED",
        "sensor_width_mm": 40.64,
        "sensor_height_mm": 22.86,
        "iso_native": 2000,
        "supports_lut": True,
    },
    "KOMODO": {
        "manufacturer": "RED",
        "sensor_width_mm": 26.70,
        "sensor_height_mm": 14.24,
        "iso_native": 2000,
        "supports_lut": True,
    },
    "GEMINI": {
        "manufacturer": "RED",
        "sensor_width_mm": 40.64,
        "sensor_height_mm": 22.86,
        "iso_native": 2000,
        "supports_lut": True,
    },
}

# ============================================================================
# SONY CAMERAS
# ============================================================================

SONY_CAMERAS = {
    "BURANO": {
        "manufacturer": "SONY",
        "sensor_width_mm": 36.0,
        "sensor_height_mm": 20.25,
        "iso_native": 1000,
        "supports_lut": True,
    },
    "FX9": {
        "manufacturer": "SONY",
        "sensor_width_mm": 35.80,
        "sensor_height_mm": 20.14,
        "iso_native": 2000,
        "supports_lut": True,
    },
    "VENICE": {
        "manufacturer": "SONY",
        "sensor_width_mm": 40.96,
        "sensor_height_mm": 23.04,
        "iso_native": 2000,
        "supports_lut": True,
    },
}

# ============================================================================
# LENS DATABASE
# ============================================================================

LENS_DATABASE = {
    "Zeiss Supreme Prime 18/T1.5": {
        "manufacturer": "ZEISS",
        "series": "Supreme Prime",
        "focal_length": 18,
        "max_tstop": 1.5,
        "transmission": 0.917,
        "sensor_type": "FF",
    },
    "Zeiss Supreme Prime 50/T1.5": {
        "manufacturer": "ZEISS",
        "series": "Supreme Prime",
        "focal_length": 50,
        "max_tstop": 1.5,
        "transmission": 0.917,
        "sensor_type": "FF",
    },
    "Zeiss Supreme Prime 85/T1.5": {
        "manufacturer": "ZEISS",
        "series": "Supreme Prime",
        "focal_length": 85,
        "max_tstop": 1.5,
        "transmission": 0.917,
        "sensor_type": "FF",
    },
    "Cooke Anamorphic/i SF 32": {
        "manufacturer": "COOKE",
        "series": "Anamorphic/i SF",
        "focal_length": 32,
        "max_tstop": 1.8,
        "transmission": 0.85,
        "sensor_type": "FF",
    },
    "ARRI Signature Prime 35": {
        "manufacturer": "ARRI",
        "series": "Signature Prime",
        "focal_length": 35,
        "max_tstop": 1.8,
        "transmission": 0.90,
        "sensor_type": "FF",
    },
}

# ============================================================================
# METADATA FIELD MAPPINGS
# ============================================================================

# ARRI EXR metadata fields
ARRI_METADATA_FIELDS = {
    "focal_length": "exr/nominalFocalLength",
    "focus_distance": "exr/focusDistance",
    "t_stop": "exr/tStop",
    "f_stop": "exr/fStop",
    "lens_model": "exr/lensModel",
    "camera_model": "exr/cameraModel",
    "shutter_angle": "exr/shutterAngle",
    "iso_speed": "exr/isoSpeed",
    "exposure_index": "exr/exposureIndex",
}

# RED metadata fields
RED_METADATA_FIELDS = {
    "focal_length": "red:focalLength",
    "focus_distance": "red:focusDistance",
    "t_stop": "red:tStop",
    "f_stop": "red:fStop",
    "lens_model": "red:lensModel",
    "sensor_width": "red:sensorWidth",
    "sensor_height": "red:sensorHeight",
}

# SONY metadata fields
SONY_METADATA_FIELDS = {
    "focal_length": "sony:focalLength",
    "focus_distance": "sony:focusDistance",
    "t_stop": "sony:tstop",
    "f_stop": "sony:fstop",
    "lens_model": "sony:lensModel",
    "camera_model": "sony:cameraModel",
}

# ============================================================================
# UNIT CONVERSION CONSTANTS
# ============================================================================

MM_TO_INCH = 0.0393701
INCH_TO_MM = 25.4
MM_TO_FEET = 0.00328084
FEET_TO_MM = 304.8

# ============================================================================
# NUKE CAMERA CONSTANTS
# ============================================================================

NUKE_CAMERA_DEFAULTS = {
    "focal_length": 50.0,
    "aperture": 0.5,
    "haperture": 1.0,
    "vaperture": 0.75,
    "near": 0.1,
    "far": 10000.0,
}

# ============================================================================
# T-STOP TO F-STOP CONVERSION
# ============================================================================

def tstop_to_fstop(t_stop: float, transmission: float = 1.0) -> float:
    """
    Convert T-stop to F-stop using transmission factor.
    
    Formula: F-stop = T-stop / sqrt(transmission)
    
    Args:
        t_stop: T-stop value
        transmission: Lens transmission (0-1)
    
    Returns:
        F-stop value
    """
    if transmission <= 0:
        transmission = 1.0
    return t_stop / (transmission ** 0.5)


def fstop_to_tstop(f_stop: float, transmission: float = 1.0) -> float:
    """
    Convert F-stop to T-stop using transmission factor.
    
    Formula: T-stop = F-stop * sqrt(transmission)
    
    Args:
        f_stop: F-stop value
        transmission: Lens transmission (0-1)
    
    Returns:
        T-stop value
    """
    if transmission <= 0:
        transmission = 1.0
    return f_stop * (transmission ** 0.5)
