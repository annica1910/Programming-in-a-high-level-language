"""numpy implementation of image filters"""

from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
import time

def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    w = [.21, .72, .07]
    rgb = [image[:, :, 0],image[:, :, 1], image[:, :, 2]]
    gray_image = rgb[0] * w[0] + rgb[1] * w[1] + rgb[2] * w[2]

    # Return image (make sure it's the right type!)
    grayscale_image = gray_image.astype("uint8")

    return grayscale_image


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    sepia_image = np.empty_like(image)

    # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)
    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],
    ]
    sepia_matrix = np.multiply(k,sepia_matrix)

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix
    # Apply the matrix filter

    sepia_image = np.einsum('ijk,lk->ijl', image, sepia_matrix)

    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    sepia_image[sepia_image[:,:,:] > 255] = 255

    # Return image (make sure it's the right type!)
    sepia_image = sepia_image.astype("uint8")
    return sepia_image
