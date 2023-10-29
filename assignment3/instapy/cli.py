"""Command-line (script) interface to instapy"""

import argparse
import sys

import numpy as np
from PIL import Image

import instapy
from . import get_filter, io


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
) -> None:
    """Run the selected filter"""
    # load the image from a file
    image = io.read_image('rain.jpg')
    if scale != 1:
        # Resize image, if needed
        w, h, _ = image.shape
        image = np.resize(image, (int(w*scale), int(h*scale), 3))

    # Apply the filter
    filter = get_filter(filter, implementation)
    filtered = filter(image)
    if out_file:
        # save the file
        io.write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", help="The output filename")

    # Add required arguments
    parser.add_argument("implementation", help="The implementation to use for filtering")
    parser.add_argument("-h", "--help", help="show this help message and exit")
    parser.add_argument("-g", "--gray", help="Select gray filter")
    parser.add_argument("-se", "--sepia", help="Select sepia filter")
    parser.add_argument("-sc", "--scale", help="Scale factor to resize image")
    parser.add_argument("-i", "--implementation" , help="The implementation")


    # parse arguments and call run_filter
    args = parser.parse_args()
    args.func(args)

