import concurrent.futures # multiprocessing dependency
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mimg


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






THRESHOLD_SIZE = 180 # TODO: adjust values



# Crops main array given [height_offset, width_offset] 
# * Works
# TODO: Optimize  - (nested functions) - else block
def select_chunk(img, offset) -> np.ndarray:
    img_height, img_width, _ = img.shape

    if (img_height - offset[0] >= THRESHOLD_SIZE) and (img_width - offset[1] >= THRESHOLD_SIZE):
        
        cropped_arr = np.zeros(shape=(THRESHOLD_SIZE, THRESHOLD_SIZE, 3))
        
        for _i, i in enumerate(range(offset[0], offset[0] + THRESHOLD_SIZE)):
            for _j, j in enumerate(range(offset[1], offset[1] + THRESHOLD_SIZE)):
                for k in range(3):
                    cropped_arr[_i, _j, k] = img.item((i, j, k))
    else:

        new_img_height = img_height - offset[0] if (img_height - offset[0]) < THRESHOLD_SIZE else THRESHOLD_SIZE
        new_img_width  = img_width  - offset[1] if (img_width  - offset[1]) < THRESHOLD_SIZE else THRESHOLD_SIZE

        cropped_arr = np.zeros(shape=(new_img_height, new_img_width, 3))

        for _i, i in enumerate(range(offset[0], offset[0] + new_img_height)):
            for _j, j in enumerate(range(offset[1], offset[1] + new_img_width)):
                for k in range(3):
                    cropped_arr[_i, _j, k] = img.item((i, j, k))

    return cropped_arr

# Blurs a given 2D array
# * Works
def blur(img, blur_size = 3) -> np.ndarray:
    # blur_size = int(input("Blur size: "))
    # 2 - 18.5s
    # 3 - 24.6s
    # 5 - ~47s
    # 7 - 1m 57.2s
    # 10 - 2m 37.5s

    height, width, _ = img.shape

    new_img_arr = np.zeros(shape=(height, width, 3))

    for i in range(height):
        for j in range(width):

            new_img_arr[i, j] = _avg_color_in_grid(img, blur_size, (i, j), "BLUR")

    return new_img_arr


# Concatenates 1D array of img chunks
# * Works
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

# + This should be the parent function
# Rn: makes a 1D array of all chunks
def concatenate_blur_imgs(img, blur_size = 3):

    # * region Separating Chunks
    height, width, _ = img.shape

    all_chunks = []

    number_of_blurs = (height//THRESHOLD_SIZE + 1, width//THRESHOLD_SIZE + 1) # This is correct since range(0, …)

    for offset_h in range(number_of_blurs[0]):
        for offset_w in range(number_of_blurs[1]):
            all_chunks.append(select_chunk(img, [offset_h * THRESHOLD_SIZE, offset_w * THRESHOLD_SIZE]))
            # all_chunks[offset_h, offset_w] = select_chunk(img, [offset_h * THRESHOLD_SIZE, offset_w * THRESHOLD_SIZE])

    # return all_chunks

    # I now have a 1-D array of each chunk in the pic
    # * endregion



    # * region Multiprocessing 
    all_chunks_blurred = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # results = [executor.submit(blur, chunk) for chunk in all_chunks]

        sizes_arr = np.full(len(all_chunks) - 1, blur_size)
        results = executor.map(blur, all_chunks, sizes_arr)

        for result in results:
            all_chunks_blurred.append(result)

    # * endregion

    # * region Concatenation
    return put_together(all_chunks_blurred, img)
    # * endregion


if __name__ == "__main__":
    plt.imsave('bruh.png', concatenate_blur_imgs(img2, 10))
# plt.imshow(put_together(concatenate_blur_imgs(img2, 20)))