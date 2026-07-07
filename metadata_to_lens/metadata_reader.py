"""
MetadataToLens - Metadata Reader

Extracts camera and lens metadata from EXR files and other sources.
Supports ARRI, RED, Sony, Canon, and Blackmagic formats.

Author: MetadataToLens Contributors
License: MIT
"""

import re
from typing import Dict, Optional, Tuple, Any
from pathlib import Path
import logging

logger = logging.getLogger("MetadataToLens.MetadataReader")

# Try to import nuke (optional - for Nuke integration)
try:
    import nuke
    NUKE_AVAILABLE = True
except ImportError:
    NUKE_AVAILABLE = False


class MetadataReader:
    """
    Reads and parses camera/lens metadata from EXR files.
    """

    def __init__(self):
        """Initialize the metadata reader."""
        self.metadata = {}
        self.camera_model = None
        self.lens_model = None
        self.focal_length = None
        self.t_stop = None
        self.focus_distance = None

    def read_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read metadata from an EXR file.

        Args:
            file_path: Path to EXR file

        Returns:
            Dictionary of metadata
        """
        if not NUKE_AVAILABLE:
            logger.warning("Nuke not available - cannot read EXR metadata")
            return {}

        try:
            # Read using Nuke's internal EXR reader
            read_node = nuke.nodes.Read(file=file_path)
            metadata = read_node.metadata()

            if metadata:
                self._parse_metadata(metadata)
                logger.info(f"Successfully read metadata from {file_path}")
            else:
                logger.warning(f"No metadata found in {file_path}")

            # Clean up temporary read node
            nuke.delete(read_node)

        except Exception as e:
            logger.error(f"Error reading metadata from {file_path}: {e}")

        return self.metadata

    def read_from_node(self, node) -> Dict[str, Any]:
        """
        Read metadata from a Nuke node.

        Args:
            node: Nuke node with metadata

        Returns:
            Dictionary of metadata
        """
        if not NUKE_AVAILABLE:
            logger.warning("Nuke not available")
            return {}

        try:
            metadata = node.metadata()

            if metadata:
                self._parse_metadata(metadata)
                logger.info(f"Successfully read metadata from node {node.name()}")
            else:
                logger.warning(f"No metadata in node {node.name()}")

        except Exception as e:
            logger.error(f"Error reading metadata from node: {e}")

        return self.metadata

    def _parse_metadata(self, metadata: Dict) -> None:
        """
        Parse metadata dictionary and extract relevant fields.

        Args:
            metadata: Raw metadata dictionary from Nuke
        """
        self.metadata = metadata

        # Detect camera manufacturer and parse accordingly
        if self._is_arri_metadata(metadata):
            self._parse_arri_metadata(metadata)
        elif self._is_red_metadata(metadata):
            self._parse_red_metadata(metadata)
        elif self._is_sony_metadata(metadata):
            self._parse_sony_metadata(metadata)
        else:
            self._parse_generic_metadata(metadata)

    def _is_arri_metadata(self, metadata: Dict) -> bool:
        """Check if metadata is from ARRI camera."""
        return any(
            key.startswith("exr/") or key.startswith("ARRI/")
            for key in metadata.keys()
        )

    def _is_red_metadata(self, metadata: Dict) -> bool:
        """Check if metadata is from RED camera."""
        return any(key.startswith("red:") for key in metadata.keys())

    def _is_sony_metadata(self, metadata: Dict) -> bool:
        """Check if metadata is from Sony camera."""
        return any(key.startswith("sony:") for key in metadata.keys())

    def _parse_arri_metadata(self, metadata: Dict) -> None:
        """Parse ARRI EXR metadata."""
        logger.info("Parsing ARRI metadata")

        # Camera model
        self.camera_model = metadata.get("exr/cameraModel", "")
        logger.info(f"  Camera: {self.camera_model}")

        # Focal length
        try:
            fl_str = metadata.get("exr/nominalFocalLength", "")
            if fl_str:
                # Extract numeric value (sometimes it's "50 mm")
                match = re.search(r"(\d+(?:\.\d+)?)", fl_str)
                if match:
                    self.focal_length = float(match.group(1))
                    logger.info(f"  Focal Length: {self.focal_length}mm")
        except (ValueError, TypeError) as e:
            logger.warning(f"Could not parse focal length: {e}")

        # T-stop (exposure)
        try:
            tstop_str = metadata.get("exr/tStop", "")
            if tstop_str:
                match = re.search(r"(\d+(?:\.\d+)?)", tstop_str)
                if match:
                    self.t_stop = float(match.group(1))
                    logger.info(f"  T-stop: {self.t_stop}")
        except (ValueError, TypeError) as e:
            logger.warning(f"Could not parse T-stop: {e}")

        # Lens model
        self.lens_model = metadata.get("exr/lensModel", "")
        if self.lens_model:
            logger.info(f"  Lens: {self.lens_model}")

        # Focus distance
        try:
            fd_str = metadata.get("exr/focusDistance", "")
            if fd_str:
                match = re.search(r"(\d+(?:\.\d+)?)", fd_str)
                if match:
                    self.focus_distance = float(match.group(1))
                    logger.info(f"  Focus Distance: {self.focus_distance}mm")
        except (ValueError, TypeError) as e:
            logger.warning(f"Could not parse focus distance: {e}")

    def _parse_red_metadata(self, metadata: Dict) -> None:
        """Parse RED EXR metadata."""
        logger.info("Parsing RED metadata")

        # Camera model
        self.camera_model = metadata.get("red:cameraModel", "")
        logger.info(f"  Camera: {self.camera_model}")

        # Focal length
        try:
            self.focal_length = float(metadata.get("red:focalLength", 0))
            if self.focal_length:
                logger.info(f"  Focal Length: {self.focal_length}mm")
        except (ValueError, TypeError):
            pass

        # T-stop
        try:
            self.t_stop = float(metadata.get("red:tStop", 0))
            if self.t_stop:
                logger.info(f"  T-stop: {self.t_stop}")
        except (ValueError, TypeError):
            pass

        # Lens model
        self.lens_model = metadata.get("red:lensModel", "")
        if self.lens_model:
            logger.info(f"  Lens: {self.lens_model}")

    def _parse_sony_metadata(self, metadata: Dict) -> None:
        """Parse Sony EXR metadata."""
        logger.info("Parsing SONY metadata")

        # Camera model
        self.camera_model = metadata.get("sony:cameraModel", "")
        logger.info(f"  Camera: {self.camera_model}")

        # Focal length
        try:
            self.focal_length = float(metadata.get("sony:focalLength", 0))
            if self.focal_length:
                logger.info(f"  Focal Length: {self.focal_length}mm")
        except (ValueError, TypeError):
            pass

        # T-stop
        try:
            self.t_stop = float(metadata.get("sony:tstop", 0))
            if self.t_stop:
                logger.info(f"  T-stop: {self.t_stop}")
        except (ValueError, TypeError):
            pass

        # Lens model
        self.lens_model = metadata.get("sony:lensModel", "")
        if self.lens_model:
            logger.info(f"  Lens: {self.lens_model}")

    def _parse_generic_metadata(self, metadata: Dict) -> None:
        """Parse generic/standard metadata."""
        logger.info("Parsing generic metadata")

        # Look for common metadata patterns
        for key, value in metadata.items():
            if "focal" in key.lower():
                try:
                    self.focal_length = float(str(value).split()[0])
                except (ValueError, IndexError):
                    pass
            elif "camera" in key.lower() or "model" in key.lower():
                self.camera_model = str(value)
            elif "lens" in key.lower():
                self.lens_model = str(value)
            elif "tstop" in key.lower() or "t-stop" in key.lower():
                try:
                    self.t_stop = float(str(value))
                except ValueError:
                    pass

    def get_camera_model(self) -> Optional[str]:
        """Get detected camera model."""
        return self.camera_model

    def get_lens_model(self) -> Optional[str]:
        """Get detected lens model."""
        return self.lens_model

    def get_focal_length(self) -> Optional[float]:
        """Get focal length in mm."""
        return self.focal_length

    def get_t_stop(self) -> Optional[float]:
        """Get T-stop value."""
        return self.t_stop

    def get_focus_distance(self) -> Optional[float]:
        """Get focus distance in mm."""
        return self.focus_distance

    def get_all_metadata(self) -> Dict[str, Any]:
        """Get all metadata as dictionary."""
        return {
            "camera_model": self.camera_model,
            "lens_model": self.lens_model,
            "focal_length": self.focal_length,
            "t_stop": self.t_stop,
            "focus_distance": self.focus_distance,
            "raw_metadata": self.metadata,
        }

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"MetadataReader("
            f"camera={self.camera_model}, "
            f"lens={self.lens_model}, "
            f"focal_length={self.focal_length}mm, "
            f"t_stop={self.t_stop})"
        )


# Module-level convenience functions

def read_metadata_from_file(file_path: str) -> Dict[str, Any]:
    """
    Convenience function to read metadata from a file.

    Args:
        file_path: Path to EXR file

    Returns:
        Dictionary of metadata
    """
    reader = MetadataReader()
    return reader.read_from_file(file_path)


def read_metadata_from_node(node) -> Dict[str, Any]:
    """
    Convenience function to read metadata from a Nuke node.

    Args:
        node: Nuke node

    Returns:
        Dictionary of metadata
    """
    reader = MetadataReader()
    return reader.read_from_node(node)
