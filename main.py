import numpy as np
from skimage.io import imread, imshow
from skimage.color import rgb2gray
from skimage.feature import match_template
import matplotlib.pyplot as plt
from slice import create_slices, interpret_match

INTEREST_ORDER = np.array(['Politics', 'Money', 'Environment',
                           'Crime', 'Entertainment', 'Culture',
                           'Food', 'Health', 'Fashion',
                           'Sports', 'Paranormal', 'Travel',
                           'Work', 'Weather', 'Animals',
                           'School', 'Toys', 'Sci-Fi'])

interests = imread('example2.PNG')[:, :, :3]
templates_grey = imread('../SecAspCalc/data/templates.png')[:, :, :3]
plt.figure(num=None, figsize=(8, 6), dpi=80)
interests_grey = interests
slices = create_slices(interests)
slice = slices[10]

result = match_template(templates_grey, slice)
ij = np.unravel_index(np.argmax(result), result.shape)
x, y = ij[1], ij[0]
print(x, y)
print(interpret_match(y))

fig = plt.figure(figsize=(8, 3))
ax1 = plt.subplot(1, 3, 1)
ax2 = plt.subplot(1, 3, 2)

ax1.imshow(slice)
ax1.set_axis_off()
ax1.set_title('template')

ax2.imshow(templates_grey)
ax2.set_axis_off()
ax2.set_title('image')
# highlight matched region
hcoin, wcoin = slice.shape[:2]
rect = plt.Rectangle((x, y), wcoin, hcoin, edgecolor='r', facecolor='none')
ax2.add_patch(rect)

plt.show()
