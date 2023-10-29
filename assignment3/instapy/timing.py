"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
import instapy
from instapy import io
from typing import Callable
import numpy as np


def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    # run the filter function `calls` times
    # return the _average_ time of one call
    ...


def make_reports(filename: str = "rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """
    rfile = open('timing-report.txt', "w")
    # load the image
    image = io.read_image(filename)
    #io.display(image) #show the image

    # print the image name, width, height
    print("Time perfomance using file %s: %sx%s" % (filename, len(image), len(image[0])), file=rfile)

    # iterate through the filters
    filter_names = ["color2gray"]
    for filter_name in filter_names:
        # get the reference filter function
        start = time.time()
        reference_filter = instapy.get_filter(filter_name) #auto python
        reference_filter(image)
        # time the reference implementation
        reference_time = time.time() - start
        print(
            f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})", file=rfile
        )
        # iterate through the implementations
        implementations = ["numpy", "numba"]
        for implementation in implementations:
            start2 = time.time()
            filter = instapy.get_filter(filter_name, implementation)
            filter(image)
            # time the filter
            filter_time = time.time() - start2
            # compare the reference time to the optimized time
            speedup = reference_time / filter_time
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)", file=rfile
            )


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
