import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mimg
import concurrent.futures # multiprocessing dependency

def rgba2rgb(img):
    height, width, _ = img.shape
    rgb_img_arr = np.zeros(shape=(height, width, 3))

    for i in range(height):
        for j in range(width):
            for k in range(3):
                rgb_img_arr[i, j, k] = img.item((i, j, k))

    return rgb_img_arr


def _get_image(path, ignore_alpha = True):
    img = mimg.imread(path)

    if path.endswith('.jpg') or path.endswith('.tif') or path.endswith('.jpeg'):
        return img / 255 
        
    elif path.endswith('.png') and ignore_alpha:
        return rgba2rgb(img)

    return img

img2 = _get_image('Input Images/Oogway_forest.jpg')


# stop width for blur
def _find_stop_blur(height, width, grid_size, start_pixel) -> list:
    x_dim, y_dim = start_pixel
    padding = grid_size//2
    _stop = (padding + 1) if grid_size & 1 else padding

    if x_dim < height or y_dim < width:
        e_h = height - x_dim if (height - x_dim) <= padding and (x_dim < height) else _stop
        e_w = width - y_dim if (width - y_dim) <= padding and (y_dim < width) else _stop

    if x_dim >= height or y_dim >= width:
        e_h = height - (x_dim - padding) if (height - x_dim) <= padding and (x_dim >= height) else _stop
        e_w = width - (y_dim - padding) if (width - y_dim) <= padding and (y_dim >= width) else _stop

    return [e_h, e_w]


# blur, pixelate dependency
def _avg_color_in_grid(img, grid_size, start_pixel, img_type):

    x_dim, y_dim = start_pixel
    padding = grid_size//2 # no. of pixels on either side of central pixel

    _stop = (padding + 1) if grid_size & 1 else padding  # (less on right side if even)

    r_total, g_total, b_total = 0, 0, 0

    # height, width, _ = img.shape

    # if x_dim < height - _stop and y_dim < width - _stop:
    try:
        r_total, g_total, b_total = 0, 0, 0

        # default grid_size^2 for all pixels not on top or left edge
        total_pixels = grid_size**2 if x_dim > padding and y_dim > padding else 0

        for _i in range(-padding, _stop):
            for _j in range(-padding, _stop):

                if (x_dim + _i >= 0 ) and (y_dim + _j >= 0):

                    r_total += img.item((x_dim + _i, y_dim + _j, 0))
                    g_total += img.item((x_dim + _i, y_dim + _j, 1))
                    b_total += img.item((x_dim + _i, y_dim + _j, 2))

                    # increment by one if pixels on top or left edge
                    total_pixels += 1 and total_pixels != grid_size**2

    # else:
    except IndexError:
        r_total, g_total, b_total = 0, 0, 0
        height, width, _ = img.shape

        if img_type == "BLUR":
            empty_stop_height, empty_stop_width = _find_stop_blur(height, width, grid_size, start_pixel)

        total_pixels = 0
        for _i in range(-padding, empty_stop_height):
            for _j in range(-padding, empty_stop_width):

                r_total += img.item((x_dim + _i, y_dim + _j, 0))
                g_total += img.item((x_dim + _i, y_dim + _j, 1))
                b_total += img.item((x_dim + _i, y_dim + _j, 2))

                total_pixels+=1

    return np.array((r_total, g_total, b_total)) / total_pixels








# BLUR MULTIPROCESSING

THRESHOLD_SIZE = 600 # TODO: adjust values

# + list of offsets?

def put_together(all_chunks_l, img):

    height, width, _ = img.shape

    new_img_arr = np.zeros(shape=(height, width, 3))

    for i_1d, chunk in enumerate(all_chunks_l):
        _offset = [ i_1d // (width//THRESHOLD_SIZE + 1), i_1d % (width//THRESHOLD_SIZE + 1)] # This is correct

        chunk_h, chunk_w, _ = chunk.shape
        for i in range(chunk_h):
            for j in range(chunk_w):
                for k in range(3):
                    new_img_arr[i + (_offset[0] * THRESHOLD_SIZE), j + (_offset[1] * THRESHOLD_SIZE), k] = chunk.item((i, j, k))

    return new_img_arr





l_blur_img = img2

# + - Has to be nested - to avoid reference to img
# TODO: Refactor the HELL out of this - optimize
def blur_chunk(offset, blur_size = 3) -> np.ndarray:

    img_height, img_width, _ = l_blur_img.shape

    down_dist = img_height - offset[0]
    right_dist = img_width - offset[1]

    # TODO: test perf_counter - if-block faster than calculating new_img_height ? -

    if (down_dist >= THRESHOLD_SIZE) and (right_dist >= THRESHOLD_SIZE):
        
        cropped_arr_blurred = np.zeros(shape=(THRESHOLD_SIZE, THRESHOLD_SIZE, 3))
        
        # Blur one THRESHOLD chunk
        for _i, i in enumerate(range(offset[0], offset[0] + THRESHOLD_SIZE)):
            for _j, j in enumerate(range(offset[1], offset[1] + THRESHOLD_SIZE)):
                cropped_arr_blurred[_i, _j] = _avg_color_in_grid(l_blur_img, blur_size, (i, j), "BLUR")
    else:

        # find dimensions of edge chunk
        new_img_height = down_dist if down_dist < THRESHOLD_SIZE else THRESHOLD_SIZE
        new_img_width  = right_dist if right_dist < THRESHOLD_SIZE else THRESHOLD_SIZE

        cropped_arr_blurred = np.zeros(shape=(new_img_height, new_img_width, 3))

        # Blur edge chunk
        for _i, i in enumerate(range(offset[0], offset[0] + new_img_height)):
            for _j, j in enumerate(range(offset[1], offset[1] + new_img_width)):
                cropped_arr_blurred[_i, _j] = _avg_color_in_grid(l_blur_img, blur_size, (i, j), "BLUR")

    return cropped_arr_blurred





def blur_mproc(img, blur_size = 3):

    img_height, img_width, _ = img.shape
    
    # all_chunks = []
    offset_arr = []

    number_of_blurs = (img_height//THRESHOLD_SIZE + 1, img_width//THRESHOLD_SIZE + 1) # This is correct since range(0, …)

    for offset_h in range(number_of_blurs[0]):
        for offset_w in range(number_of_blurs[1]):
            
            offset_arr.append( [offset_h*THRESHOLD_SIZE, offset_w*THRESHOLD_SIZE] )

            # all_chunks.append(blur_chunk([offset_h * THRESHOLD_SIZE, offset_w * THRESHOLD_SIZE]))
        
    all_chunks_blurred = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # results = [executor.submit(blur, chunk) for chunk in all_
        
        sizes_arr = np.full(len(offset_arr) - 1, blur_size)
        results = executor.map(blur_chunk, offset_arr, sizes_arr)


        for result in results:
            all_chunks_blurred.append(result)
    

    return put_together(all_chunks_blurred, img)

if __name__ == '__main__':
    plt.imsave('helpmemlml.png', blur_mproc(img2, blur_size=6))

# To beat: 1min 33 secs
    