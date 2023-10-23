import numpy as np
import multiprocessing as mp

#Processes each individual row
def process_row(lock, row, image, filter_mask, midrow, midcol, shared_dict):
    # Determine the size of the image and the depth
    rows, cols, depth = image.shape

    filtered_row = np.zeros((cols, 3), dtype=np.uint8)

    # Loop through each column within a row
    for c in range(cols):
        # Value of filter to be returned
        filtered_value = 0

        # If the array is 1x? dimension (aka one column)
        if midrow == 0:
            # Loop through each value in the column
            for j in range(-midcol, midcol + 1):
                # Check if in bounds of the image
                if (c + j >= 0 and c + j < cols):
                    # Add the original image pixel multiplied by the filter pixel, both adjusted for offset, to the filtered value
                    filtered_value += image[row, c + j] * filter_mask[j + midcol]
        # If there are no columns, aka a 1-Dimensional array
        elif midcol == 0:
            # Loop through each value of the array
            for i in range(-midrow, midrow + 1):
                # Check if in bounds of the image
                if (row + i >= 0 and row + i < rows):
                    # Add the original image pixel multiplied by the filter pixel, both adjusted for offset, to the filtered value
                    filtered_value += image[row + i, c] * filter_mask[i + midrow]
        # The filter has more than 1 row and column
        else:
            # Loop though both the rows and columns of the filter
            for i in range(-midrow, midrow + 1):
                for j in range(-midcol, midcol + 1):
                    # If the target pixel is in bounds of the image
                    if (row + i >= 0 and row + i < rows) and (c + j >= 0 and c + j < cols):
                        # Add the original image pixel multiplied by the filter pixel, both adjusted for offset, to the filtered value
                        filtered_value += np.uint8(image[row + i, c + j] * filter_mask[i + midrow][j + midcol])
        # With this fltered value we add it to a row at the column index we a working on
        filtered_row[c] = filtered_value

    # Lock access to the shared dictionary so that we can add the newly calculated row to it
    with lock:
        shared_dict[row] = filtered_row

def image_filter(image, filter_mask, numprocessors, filtered_image):

    # Determine the size of the image
    rows, cols, depth = image.shape

    # Find the size of the filter (5x5, 3x1, etc)
    frows = len(filter_mask)
    # Since it is possible for the filter to be a 1D array we have to implement a try-catch method in case of there being no mask[0] value
    try:
        fcols = len(filter_mask[0])
    except TypeError:
        # Treat it as a 1D array
        fcols = len(filter_mask)
        frows = 1

    # Doing integer division to find the midpoint of the filter, this will be how many values we have to offset in each direction
    midrow = frows // 2
    midcol = fcols // 2

    # Create a multiprocessing pool
    pool = mp.Pool(processes=numprocessors)
    
    # Create a pool manager
    manager = mp.Manager()

    # Create a dictionary from the pool manager to act as our shared memory space to read/write
    shared_dict = manager.dict()

    # Creating lock variables
    lock = mp.Manager().Lock()

    # Process rows in parallel, we do this via a seperate function that is passed in with additional variables needed. 
    # These variables are for multiporcessing (lock and shared_dict) as well as midrow and midcol for later use
    results = [pool.apply_async(process_row, args=(lock, r, image, filter_mask, midrow, midcol, shared_dict)) for r in range(rows)]
    
    # Wait for all processes to finish
    pool.close()
    pool.join()

    # Combine the processed rows into the filtered image
    for r in range(rows):
        filtered_image[r,:] = shared_dict[r]

    return filtered_image