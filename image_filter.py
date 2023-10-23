import numpy as np
import multiprocessing as mp

# Processes each individual segment
def process_segment(lock, start_row, end_row, image, filter_mask, midrow, midcol, filtered_image):
    rows, cols, _ = image.shape

    for row in range(start_row, end_row):
        filtered_row = np.zeros((cols, 3), dtype=np.uint8)

        for c in range(cols):
            filtered_value = 0

            if midrow == 0:
                for j in range(-midcol, midcol + 1):
                    if (c + j >= 0 and c + j < cols):
                        filtered_value += image[row, c + j] * filter_mask[j + midcol]
            elif midcol == 0:
                for i in range(-midrow, midrow + 1):
                    if (row + i >= 0 and row + i < rows):
                        filtered_value += image[row + i, c] * filter_mask[i + midrow]
            else:
                for i in range(-midrow, midrow + 1):
                    for j in range(-midcol, midcol + 1):
                        if (row + i >= 0 and row + i < rows) and (c + j >= 0 and c + j < cols):
                            filtered_value += np.uint8(image[row + i, c + j] * filter_mask[i + midrow][j + midcol])

            filtered_row[c] = filtered_value

        with lock:
            filtered_image[row, :] = filtered_row

def image_filter(image, filter_mask, numprocessors, filtered_image):
    # Filter comes in as a 2D matrix (filter_mask)
    print(filter_mask)

    # Will do this through a for loop with each row
    rows, cols, depth = image.shape

    frows = len(filter_mask)
    try:
        fcols = len(filter_mask[0])
    except TypeError:
        # Treat it as a 1D array
        fcols = len(filter_mask)
        frows = 1

    # Doing integer division to find the midpoint of the filter, this will be how many values we have to offset in each direction
    midrow = frows // 2
    midcol = fcols // 2

    print(frows, fcols)
    print(midrow, midcol)

    # Create a multiprocessing pool
    pool = mp.Pool(processes=numprocessors)
    lock = mp.Manager().Lock()

    # Divide the image into segments for parallel processing
    segment_size = rows // numprocessors
    segments = [(lock, i * segment_size, (i + 1) * segment_size, image, filter_mask, midrow, midcol, filtered_image)
                for i in range(numprocessors)]

    # Process segments in parallel
    pool.starmap(process_segment, segments)

    return filtered_image
