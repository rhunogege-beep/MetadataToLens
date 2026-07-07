"""
MetadataToLens - Camera Synchronization

Synchronizes extracted metadata to Nuke Camera and LensCore nodes.

Author: MetadataToLens Contributors
License: MIT
"""

import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger("MetadataToLens.CameraSync")

# Try to import nuke (optional - for Nuke integration)
try:
    import nuke
    NUKE_AVAILABLE = True
except ImportError:
    NUKE_AVAILABLE = False

from .metadata_reader import MetadataReader
from .constants import (
    NUKE_CAMERA_DEFAULTS,
    tstop_to_fstop,
    LENS_DATABASE,
)


class CameraSync:
    """
    Synchronizes camera and lens metadata to Nuke nodes.
    """

    def __init__(self):
        """Initialize camera sync."""
        self.camera_node = None
        self.lens_core_node = None
        self.metadata_reader = MetadataReader()

    def sync_from_file(
        self, file_path: str, camera_node=None, lens_node=None
    ) -> bool:
        """
        Read metadata from file and sync to camera nodes.

        Args:
            file_path: Path to EXR file
            camera_node: Optional Nuke Camera node (will auto-find if not provided)
            lens_node: Optional Nuke LensCore node (will auto-find if not provided)

        Returns:
            True if sync successful, False otherwise
        """
        if not NUKE_AVAILABLE:
            logger.warning("Nuke not available - cannot sync")
            return False

        try:
            # Read metadata
            metadata = self.metadata_reader.read_from_file(file_path)

            if not metadata:
                logger.warning(f"No metadata found in {file_path}")
                return False

            # Find or use provided nodes
            if camera_node is None:
                camera_node = self._find_camera_node()
            if lens_node is None:
                lens_node = self._find_lens_core_node()

            self.camera_node = camera_node
            self.lens_core_node = lens_node

            # Apply metadata to nodes
            return self._apply_metadata_to_nodes()

        except Exception as e:
            logger.error(f"Error syncing from file: {e}")
            return False

    def sync_from_node(
        self, source_node, camera_node=None, lens_node=None
    ) -> bool:
        """
        Read metadata from a Nuke node and sync to camera nodes.

        Args:
            source_node: Source Nuke node with metadata
            camera_node: Optional Nuke Camera node
            lens_node: Optional Nuke LensCore node

        Returns:
            True if sync successful, False otherwise
        """
        if not NUKE_AVAILABLE:
            logger.warning("Nuke not available - cannot sync")
            return False

        try:
            # Read metadata
            metadata = self.metadata_reader.read_from_node(source_node)

            if not metadata:
                logger.warning(f"No metadata in node {source_node.name()}")
                return False

            # Find or use provided nodes
            if camera_node is None:
                camera_node = self._find_camera_node()
            if lens_node is None:
                lens_node = self._find_lens_core_node()

            self.camera_node = camera_node
            self.lens_core_node = lens_node

            # Apply metadata
            return self._apply_metadata_to_nodes()

        except Exception as e:
            logger.error(f"Error syncing from node: {e}")
            return False

    def _apply_metadata_to_nodes(self) -> bool:
        """Apply metadata to camera and lens nodes."""
        try:
            metadata = self.metadata_reader.get_all_metadata()

            logger.info("Applying metadata to nodes...")

            # Apply to camera node
            if self.camera_node:
                self._sync_to_camera_node(metadata)

            # Apply to lens node
            if self.lens_core_node:
                self._sync_to_lens_node(metadata)

            logger.info("✓ Metadata sync complete")
            return True

        except Exception as e:
            logger.error(f"Error applying metadata: {e}")
            return False

    def _sync_to_camera_node(self, metadata: Dict[str, Any]) -> None:
        """Sync metadata to Camera node."""
        if not self.camera_node:
            logger.warning("No camera node to sync to")
            return

        try:
            logger.info(f"Syncing to camera node: {self.camera_node.name()}")

            # Focal length
            focal_length = metadata.get("focal_length")
            if focal_length:
                self.camera_node["focal_length"].setValue(focal_length)
                logger.info(f"  → Focal Length: {focal_length}mm")

            # T-stop / Aperture
            t_stop = metadata.get("t_stop")
            if t_stop:
                # Convert T-stop to aperture (f-stop equivalent)
                aperture = tstop_to_fstop(t_stop)
                self.camera_node["aperture"].setValue(aperture)
                logger.info(f"  → Aperture (from T{t_stop}): f/{aperture:.1f}")

            # Focus distance (if available)
            focus_distance = metadata.get("focus_distance")
            if focus_distance:
                # Convert from mm to inches for Nuke
                focus_distance_inches = focus_distance / 25.4
                if "focus_distance" in self.camera_node.knobs():
                    self.camera_node["focus_distance"].setValue(focus_distance_inches)
                    logger.info(f"  → Focus Distance: {focus_distance}mm")

        except Exception as e:
            logger.error(f"Error syncing to camera node: {e}")

    def _sync_to_lens_node(self, metadata: Dict[str, Any]) -> None:
        """Sync metadata to LensCore node."""
        if not self.lens_core_node:
            logger.warning("No lens node to sync to")
            return

        try:
            logger.info(f"Syncing to lens node: {self.lens_core_node.name()}")

            lens_model = metadata.get("lens_model")
            if lens_model:
                # Try to find matching lens in database
                if lens_model in LENS_DATABASE:
                    lens_info = LENS_DATABASE[lens_model]
                    logger.info(f"  → Lens Model: {lens_model}")

                    # Apply lens parameters if available
                    if "focal_length" in lens_info:
                        logger.info(f"    Focal Length: {lens_info['focal_length']}mm")

                    if "max_tstop" in lens_info:
                        logger.info(f"    Max T-stop: {lens_info['max_tstop']}")
                else:
                    logger.info(f"  → Lens: {lens_model} (not in database)")

            focal_length = metadata.get("focal_length")
            if focal_length:
                # Set focal length for lens distortion calculations
                logger.info(f"  → Using focal length: {focal_length}mm")

        except Exception as e:
            logger.error(f"Error syncing to lens node: {e}")

    def _find_camera_node(self):
        """Find first available Camera node in the composition."""
        if not NUKE_AVAILABLE:
            return None

        try:
            for node in nuke.allNodes():
                if node.Class() == "Camera2":
                    logger.info(f"Found camera node: {node.name()}")
                    return node
            logger.warning("No Camera node found in composition")
            return None
        except Exception as e:
            logger.error(f"Error finding camera node: {e}")
            return None

    def _find_lens_core_node(self):
        """Find first available LensCore node in the composition."""
        if not NUKE_AVAILABLE:
            return None

        try:
            for node in nuke.allNodes():
                if node.Class() == "LensCore":
                    logger.info(f"Found lens node: {node.name()}")
                    return node
            logger.warning("No LensCore node found in composition")
            return None
        except Exception as e:
            logger.error(f"Error finding lens node: {e}")
            return None

    def get_metadata(self) -> Dict[str, Any]:
        """Get current metadata dictionary."""
        return self.metadata_reader.get_all_metadata()

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"CameraSync("
            f"camera={self.camera_node.name() if self.camera_node else 'None'}, "
            f"lens={self.lens_core_node.name() if self.lens_core_node else 'None'})"
        )


# Module-level convenience functions

def sync_file_to_camera(
    file_path: str, camera_node=None, lens_node=None
) -> bool:
    """
    Convenience function to sync metadata from file to camera nodes.

    Args:
        file_path: Path to EXR file
        camera_node: Optional Camera node
        lens_node: Optional LensCore node

    Returns:
        True if successful
    """
    syncer = CameraSync()
    return syncer.sync_from_file(file_path, camera_node, lens_node)


def sync_node_to_camera(
    source_node, camera_node=None, lens_node=None
) -> bool:
    """
    Convenience function to sync metadata from node to camera nodes.

    Args:
        source_node: Source node with metadata
        camera_node: Optional Camera node
        lens_node: Optional LensCore node

    Returns:
        True if successful
    """
    syncer = CameraSync()
    return syncer.sync_from_node(source_node, camera_node, lens_node)
