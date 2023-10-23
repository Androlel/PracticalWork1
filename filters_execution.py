import numpy as np
import multiprocessing as mp
import image_filter as im
from multiprocessing import Process, Queue



def filters_execution(
    image,  
    filter_mask1, 
    filter_mask2,  
    numprocessors,
    filtered_image1, 
    filtered_image2):

    filtered_image1 = im.image_filter(image,filter_mask1,numprocessors//2,filtered_image1)
    filtered_image2 = im.image_filter(image,filter_mask2,numprocessors//2,filtered_image2)
    
    # # Create two Queues to store the filtered images
    # queue1 = Queue()
    # queue2 = Queue()

    # # Create two separate processes to filter the image
    # process1 = Process(target=im.image_filter, args=(image, filter_mask1, numprocessors // 2, queue1))
    # process2 = Process(target=im.image_filter, args=(image, filter_mask2, numprocessors // 2, queue2))

    # # Start the processes
    # process1.start()
    # process2.start()

    # # Wait for both processes to finish
    # process1.join()
    # process2.join()

    # # Get the filtered images from the Queues
    # filtered_image1 = queue1.get()
    # filtered_image2 = queue2.get()

    return filtered_image1, filtered_image2


    # results1 = [pool.apply_async(im.image_filter, args=(image, filter_mask1, numprocessors//2, filtered_image1))]
    # results2 = [pool.apply_async(im.image_filter, args=(image, filter_mask2, numprocessors//2, filtered_image2))]
    
    # Wait for all processes to finish
    # pool.close()
    # pool.join()

    # filtered_image1 = result_queue.get()
    # filtered_image2 = result_queue.get()
    # filtered_image1 = im.image_filter(image,filter_mask1,numprocessors//2,filtered_image1)
    # filtered_image2 = im.image_filter(image,filter_mask2,numprocessors//2,filtered_image2)