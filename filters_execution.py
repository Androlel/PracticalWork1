import numpy as np
import multiprocessing as mp
import image_filter as im


def apply_filter(image, filter_mask, numprocessors, filtered_image, conn):
    #applying the filter
    filtered_image = im.image_filter(image, filter_mask, numprocessors, filtered_image)
    #We now need to send out the results
    conn.send_bytes(filtered_image.tobytes())  #To do this we just send the bytes of the numpy array
    conn.close()

def filters_execution(image, filter_mask1, filter_mask2,numprocessors, filtered_image1, filtered_image2):
    #We are going to need to make a pipe for each process so we can get the results back
    parent_conn1, child_conn1 = mp.Pipe()
    parent_conn2, child_conn2 = mp.Pipe()

    #We are creating and starting two parallel processes to apply the filters
    process1 = mp.Process(target=apply_filter, args=(image, filter_mask1, numprocessors//2, filtered_image1.copy(), child_conn1))
    process2 = mp.Process(target=apply_filter, args=(image, filter_mask2, numprocessors//2, filtered_image2.copy(), child_conn2))
    process1.start()
    process2.start()

    #Getting the results out from the pipe
    filtered_image1[:] = np.frombuffer(parent_conn1.recv_bytes(), dtype=np.uint8).reshape(filtered_image1.shape)
    filtered_image2[:] = np.frombuffer(parent_conn2.recv_bytes(), dtype=np.uint8).reshape(filtered_image2.shape)
    #And done
    process1.join()
    process2.join()

    return filtered_image1, filtered_image2
