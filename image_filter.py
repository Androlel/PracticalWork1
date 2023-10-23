import array
import numpy as np


def image_filter(image,
                 filter_mask,
                 numprocessors,
                 filtered_image):
    #Filter comes in as 2d matrix (filter_mask)
    print(filter_mask)

    #Will do this through a for loop with each row
    (rows,cols,depth) = image.shape

    frows = len(filter_mask)    
    try:
        fcols = len(filter_mask[0])
    except:
        fcols = 1  # Treat it as a 1D array
    
    #Doing integer division to find the midpoint of the filter, this will be how many values we have to offset in each direction
    midrow = frows//2
    midcol = fcols//2

    print(rows, cols)
    
    for r in range(rows):
        for c in range(cols):
            #Apply filter here
            filtered_value = 0

            #We start at the midpoint then go forward or backwards depending on the size of the filter
            #filtered_image[r,c] = image[r,c]
            if(midcol == 0):
                for i in range(-midrow, midrow + 1):
                    if (r + i >= 0 and r + i < rows):
                        # Multiply the filter value with the corresponding pixel value
                        filtered_value += image[r + i, c] * filter_mask[i + midrow]

            else:
                for i in range(-midrow, midrow + 1):
                    for j in range(-midcol, midcol + 1):
                        # Check if the current indices are within bounds
                        if (r + i >= 0 and r + i < rows) and (c + j >= 0 and c + j < cols):
                            # Multiply the filter value with the corresponding pixel value
                            ri = r+i
                            cj = c+j
                            imid = i+midrow
                            jmid = j +midcol
                            filtered_value += image[ri, cj] * filter_mask[imid][jmid]


            # Assign the filtered value to the corresponding pixel in the filtered image
            filtered_image[r, c] = filtered_value


    return filtered_image
