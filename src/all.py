import os
from PIL import Image
import glob


def is_black(rgb_pixel_value):
    return rgb_pixel_value[0] < 50 \
           and rgb_pixel_value[0] == rgb_pixel_value[1] \
           and rgb_pixel_value[0] == rgb_pixel_value[2]


def find_first_none_black(image, start_i=0, start_j=0):
    size = image.size
    im_rgb = image.convert("RGB")
    for j in range(start_j, size[1]):
        for i in range(start_i, int(size[0] / 2)):
            rgb_pixel_value = im_rgb.getpixel((i, j))
            if not is_black(rgb_pixel_value):
                return i, j
    return None


def find_first_black_line(image, start_j=0):
    size = image.size
    im_rgb = image.convert("RGB")

    def is_black_line(j):
        for i in range(0, size[0]):
            rgb_pixel_value = im_rgb.getpixel((i, j))
            if not is_black(rgb_pixel_value):
                return False
        return True

    for j in range(start_j, size[1]):
        if is_black_line(j):
            return j
    return None


def handle_image(image):
    size = image.size
    start = (0, 0)
    i = 0
    while True:
        left = find_first_none_black(image, start[0], start[1])
        if not left:
            return

        right = find_first_black_line(image, left[1])
        if not right:
            return

        box = (left[0], left[1], size[0] - left[0], right)
        region = image.crop(box)
        outfile = f"{output_folder}/{i}.jpg"
        region.save(outfile)

        i += 1
        start = (0, right)


input_folder = "../files"

jpg_file_names_list = glob.glob(f"{input_folder}/*.jpg")

for file_name in jpg_file_names_list:
    im = Image.open(file_name)

    output_folder = os.path.splitext(file_name)[0]
    os.mkdir(output_folder)

    handle_image(im)

