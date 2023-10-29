"""pure Python implementation of image filters"""

import numpy as np
from instapy.io import *


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    N,M,_ = image.shape
    for row in range(N):
        for col in range(M):
            rgb = image[row][col]
            gray_image[row][col] = rgb[0]*.21 + rgb[1]*.72 + rgb[2]*.07
    
    # iterate through the pixels, and apply the grayscale transform
    gray_image = gray_image.astype("uint8")
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],
    ]
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix
    N,M,_ = image.shape
    for row in range(N):
        for col in range(M):
            rgb = image[row][col]
            pixelvalues = [min(255, np.sum(np.multiply(rgb, sepia_matrix[i]))) for i in range(3)]
            sepia_image[row][col] = pixelvalues
    # Return image
    # don't forget to make sure it's the right type!
    sepia_image = sepia_image.astype("uint8")
    return sepia_image
