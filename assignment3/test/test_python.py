from instapy.python_filters import python_color2gray, python_color2sepia
from instapy.io import *
from PIL import Image

def test_color2gray(image):

    # run color2gray
    res = python_color2gray(image)
    res2 = write_image(res, 'rain_grayscale_python.jpg')
    display(res)
    # check that the result has the right shape, type
    assert image.shape == res.shape
    assert type(image)  == type(res)
    # assert uniform r,g,b(( values
    
    w, h, _ = image.shape
    im2 = np.resize(image, (int(w / 2), int(h / 2), 3))
    res = python_color2gray(im2)
    display(res)

def test_color2sepia(image):
    # run color2sepia
    res = python_color2sepia(image)
    res2 = write_image(res, 'rain_sepia_python.jpg')
    display(res)
    # check that the result has the right shape, type
    assert image.shape == res.shape
    assert type(image)  == type(res)
    # verify some individual pixel samples
    # according to the sepia matrix
    w = [ 0.393, 0.769, 0.189]
    assert res[0,0,0] == min(255, int(image[0,0,0]*w[0] + image[0,0,1]*w[1] + image[0,0,2]*w[2]))
    

