from instapy.numba_filters import numba_color2gray, numba_color2sepia

import numpy.testing as nt
from instapy.io import *


def test_color2gray(image, reference_gray):
    res = numba_color2gray(image)
    res2 = write_image(res, 'rain_grayscale_numba.jpg')
    display(res)
    
def test_color2sepia(image, reference_sepia):
    res = numba_color2sepia(image)
    res2 = write_image(res, 'rain_sepia_numba.jpg')
    display(res)

# if __name__ == "__main__":
#     test_color2gray('rain.jpg', 0)
#     test_color2sepia('rain.jpg', 0)
