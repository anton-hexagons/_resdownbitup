# resdownbitup


## info
Result: Shifts resolution from pixels to bits.

HDR: This script dose not increase dynamic range, it increase dynamic resolution.

Pros / Cons: By sacrificing pixel size resolution, we gain pixel bit depth resolution.

Example: 4K 8bit to 1080p 10bit

## dependencies
[numpy](http://www.numpy.org/)

[Pillow](https://python-pillow.org/)

[pypng](https://pypi.python.org/pypi/pypng)


## use
python resdownbitup.py image.jpg 4

[img] - path to image

[res_shift_steps] - image res is halfed and raised by 2 bits per step

([res_shift_steps] of 4 will give a perfect 16bit image)
