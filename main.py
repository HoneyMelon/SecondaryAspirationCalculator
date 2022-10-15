import numpy as np
import sys

from PyQt5.QtGui import *
from skimage.io import imread
from skimage.feature import match_template
import matplotlib.pyplot as plt
from slice import create_slices, interpret_match
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from MainWindow import Ui_MainWindow
from helper import convert_qimage_to_mat


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.target_image = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            print('pressed A')
        if event.matches(QKeySequence.Paste):
            self.paste()

    def paste(self):
        clipboard = QGuiApplication.clipboard()
        mimeData = clipboard.mimeData()

        if mimeData.hasImage():
            self.target_image = mimeData.imageData()
            self.label.setPixmap(QPixmap(mimeData.imageData()).scaled(250, 180, Qt.KeepAspectRatio))
            calculate_interest_values(self.target_image)
        else:
            self.label.setText("Cannot display data")


INTEREST_ORDER = np.array(['Politics', 'Money', 'Environment',
                           'Crime', 'Entertainment', 'Culture',
                           'Food', 'Health', 'Fashion',
                           'Sports', 'Paranormal', 'Travel',
                           'Work', 'Weather', 'Animals',
                           'School', 'Toys', 'Sci-Fi'])


def match_screenshot_to_interest_panel(screenshot):
    # TODO: multi-scale template matching probably
    interests = imread('example.PNG')[:, :, :3]
    interests_width = interests.shape[1]
    interests_height = interests.shape[0]
    result = match_template(screenshot, interests)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[1], ij[0]
    cut_image = screenshot[y:y+interests_height, x:x+interests_width, :3]
    # width and height of result image should do it?
    print(interests.shape, cut_image.shape)
    return cut_image


def calculate_interest_values(qimage):
    interests = imread('example.PNG')[:, :, :3]
    # interests = convert_qimage_to_mat(qimage)
    cut_image = match_screenshot_to_interest_panel(convert_qimage_to_mat(qimage))
    templates_grey = imread('../SecAspCalc/data/templates.png')[:, :, :3]
    plt.figure(num=None, figsize=(8, 6), dpi=80)
    slices = create_slices(interests)
    result_values = []

    for slice in slices:
        result = match_template(templates_grey, slice)
        ij = np.unravel_index(np.argmax(result), result.shape)
        y = ij[0]
        result_values.append(interpret_match(y))

    slice = slices[10]

    result = match_template(templates_grey, slice)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[1], ij[0]
    print(result_values)

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

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
