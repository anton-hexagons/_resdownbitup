# resdownbitup


## info
Shifts resolution from pixels to bits.

This method dose not increase dynamic range.


## dependencies
numpy

Pillow

pypng


## use
[img] - path to image

[res_shift_steps] - image res is halfed and raised by 2 bits per step

([res_shift_steps] of 4 will give a perfect 16bit image)