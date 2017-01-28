import sys
import math
import numpy as np
from PIL import Image
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 


if len(sys.argv) - 1 not in [2, 3]:
	print('args: [img] [res_shift_steps]')
	exit()

img_in_path = sys.argv[1]
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
float_type = np.float16
if bit_target > 32:
	float_type = np.float64
elif bit_target > 16:
	float_type = np.float32

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
img_out_arr = np.zeros(img_out_arr_shape, dtype=float_type)
print('output img res:', img_out_arr_shape[:2])

img_out_arr_crop_offset_y = (img_out_arr_crop_y / 2) * res_pow
img_out_arr_crop_offset_x = (img_out_arr_crop_x / 2) * res_pow


for pix_y in range(img_out_arr.shape[0]):
	for pix_x in range(img_out_arr.shape[1]):
		pix = [0.0 for i in range(color_count)]
		for subpix_x in range(res_pow):
			for subpix_y in range(res_pow):
				for color in range(color_count):
					in_pix_x = pix_y * subpix_y + img_out_arr_crop_offset_y
					in_pix_y = pix_x * subpix_x + img_out_arr_crop_offset_x
					pix[color] += float(img_in_arr[in_pix_x, in_pix_y, color])
		img_out_arr[pix_y, pix_x] = pix

img_out_arr /= pow(res_pow, 2) * 255


img_out_path = img_in_path.split('.')[0] + '__resdownbitup_' + str(res_shift_steps) + '.png'

print(img_out_path)

# img_out = Image.fromarray(img_out_arr)
# img_out.save(img_out_path, format='png')

# print('resdownbitup done!')

print('_')
