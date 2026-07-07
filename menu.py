"""
MetadataToLens - Nuke Menu Integration

This file registers the MetadataToLens menu in Nuke.
It is automatically loaded by Nuke during startup.

Author: MetadataToLens Contributors
License: MIT
"""

import nuke

try:
    # Get the Nodes menu
    toolbar = nuke.menu("Nodes")
    
    # Create Metadata submenu
    metadata_menu = toolbar.addMenu("Metadata")
    
    # Add MetadataToLens command
    metadata_menu.addCommand(
        "MetadataToLens",
        lambda: nuke.createNode("MetadataToLens"),
        icon="MetadataToLens.png"
    )
    
    print("[MetadataToLens] Menu registered successfully!")
    
except Exception as e:
    print(f"[MetadataToLens] Error registering menu: {e}")
    import traceback
    traceback.print_exc()
