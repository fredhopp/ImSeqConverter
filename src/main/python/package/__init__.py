"""
Image Sequence Converter Package
A professional tool for converting image sequences and video files
with advanced color space management for VFX workflows.
"""

__version__ = "1.2.0"
__author__ = "fredhopp"
__description__ = "Image Sequence Converter with batching, overlays, and colorspace conversion"

# Version info
VERSION = __version__
VERSION_INFO = tuple(map(int, __version__.split('.')))

def get_version():
    """Return the current version string."""
    return __version__

def get_version_info():
    """Return the current version as a tuple of integers."""
    return VERSION_INFO
