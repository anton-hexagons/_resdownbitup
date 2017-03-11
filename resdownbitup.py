import sys
import math
import warnings
import numpy as np
import scipy.misc
from PIL import Image
import png
# from libtiff import TIFF


warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning) 


if len(sys.argv) - 1 not in [2, 3]:
	print('args: [img] [res_shift_steps]')
	exit()

img_in_path = sys.argv[1]
if " " in img_in_path:
	print("spaces in path not supported")
	exit()
res_shift_steps = int(sys.argv[2])
if res_shift_steps == 0:
	print('arg: [res_shift_steps], can not be zero')
	exit()

img_in = Image.open(img_in_path)
img_in_arr = np.asarray(img_in, dtype=np.int)
print('input img res:', img_in_arr.shape[:2])

res_pow = pow(2, res_shift_steps)

bit_pow = res_shift_steps * 2
bit_target = 8 + res_shift_steps
int_type = np.uint16
# if bit_target > 32:
# 	int_type = np.uint64
#el
if bit_target > 16:
	int_type = np.uint32

color_count = img_in_arr.shape[2]


img_out_arr_shape_y = img_in_arr.shape[0] / res_pow
img_out_arr_shape_x = img_in_arr.shape[1] / res_pow

img_out_arr_cropped_y = int(img_out_arr_shape_y)
img_out_arr_cropped_x = int(img_out_arr_shape_x)
if (img_out_arr_cropped_y / 2) % 1 == 0.5:
	img_out_arr_cropped_y -= 1
if (img_out_arr_cropped_x / 2) % 1 == 0.5:
	img_out_arr_cropped_x -= 1
img_out_arr_crop_y = img_out_arr_shape_y - img_out_arr_cropped_y
img_out_arr_crop_x = img_out_arr_shape_x - img_out_arr_cropped_x
if (img_out_arr_crop_y or img_out_arr_crop_x):
	print('output img crop: x:' + str(img_out_arr_crop_x) + 'px y:' + str(img_out_arr_crop_y) + 'px')

img_out_arr_shape = (int(img_out_arr_cropped_y), int(img_out_arr_cropped_x), color_count)
img_out_arr = np.zeros(img_out_arr_shape, dtype=int_type)
print('output img res:', img_out_arr_shape[:2])

img_out_arr_crop_offset_y = (img_out_arr_crop_y / 2) * res_pow
img_out_arr_crop_offset_x = (img_out_arr_crop_x / 2) * res_pow


print('start render')
for pix_y in range(img_out_arr.shape[0]):
	print(str(int((pix_y + 1) / img_out_arr.shape[0] * 100)) + '%', ' y:', pix_y + 1, '/', img_out_arr.shape[0])
	for pix_x in range(img_out_arr.shape[1]):
		pix = [0 for i in range(color_count)]
		for subpix_x in range(res_pow):
			for subpix_y in range(res_pow):
				for color in range(color_count):
					in_pix_x = pix_y * res_pow + subpix_y + img_out_arr_crop_offset_y
					in_pix_y = pix_x * res_pow + subpix_x + img_out_arr_crop_offset_x
					pix_color = img_in_arr[in_pix_x, in_pix_y, color]
					# hot spot fix
					# if pix_color == 255:
					# 	pix_color = 250
					pix[color] += pix_color
		img_out_arr[pix_y, pix_x] = pix

print('render done')


img_out_arr = img_out_arr / (pow(res_pow, 2) * 255)
# print(img_out_arr)

# img_out_arr = img_out_arr.astype(int_type)

#4080 2
#16320 3

# print(img_out_arr)

img_out_path = img_in_path.split('.')[0] + '__resdownbitup_' + str(res_shift_steps) + '.png'

# img = scipy.misc.toimage(img_out_arr) #low=0.0, high=1.0
# img.save(img_out_path)

# tiff = TIFF.open(img_out_path, mode='w')
# tiff.write_image(img_out_arr)
# tiff.close()

# img_out = Image.fromarray(img_out_arr)
# print(img_out)
# # img_out.save(img_out_path, format='png')

# Convert y to 16 bit unsigned integers.
img_out_arr_16 = (65535 * ((img_out_arr - img_out_arr.max()) / img_out_arr.ptp())).astype(np.uint16)
# print(img_out_arr_16)

# Use pypng to write z as a color PNG.
with open(img_out_path, 'wb') as file:
    writer = png.Writer(width=img_out_arr_16.shape[1], height=img_out_arr_16.shape[0], bitdepth=16)
    # Convert z to the Python list of lists expected by
    # the png writer.
    img_out_arr_16_2list = img_out_arr_16.reshape(-1, img_out_arr_16.shape[1]*img_out_arr_16.shape[2]).tolist()
    writer.write(file, img_out_arr_16_2list)

print('resdownbitup done!')
