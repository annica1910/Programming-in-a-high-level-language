from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia

import numpy.testing as nt
from instapy.io import *

def test_color2gray(image, reference_gray):
    res = numpy_color2gray(image)
    res2 = write_image(res, 'rain_grayscale_numpy.jpg')
    display(res)

    #nt.assert_allclose(res, reference_gray)
 
def test_color2sepia(image, reference_sepia):
    res = numpy_color2sepia(image, 0.5)
    res2 = write_image(res, 'rain_sepia_numpy.jpg')
    display(res)

    #nt.assert_allclose(res, reference_sepia)
