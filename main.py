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
from helper import qt_pixmap_to_array
from aspCalculator import calculate_aspiration_values


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.target_image = None
        self.pushButton.clicked.connect(self.recalculate)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            print('pressed A')
        if event.matches(QKeySequence.Paste):
            self.paste()

    def display_result_values(self, result_values):
        self.politics_edit.setText(str(result_values[0]))
        self.crime_edit.setText(str(result_values[3]))
        self.food_edit.setText(str(result_values[6]))
        self.sports_edit.setText(str(result_values[9]))
        self.work_edit.setText(str(result_values[12]))
        self.school_edit.setText(str(result_values[15]))

        self.money_edit.setText(str(result_values[1]))
        self.entertainment_edit.setText(str(result_values[4]))
        self.health_edit.setText(str(result_values[7]))
        self.paranormal_edit.setText(str(result_values[10]))
        self.weather_edit.setText(str(result_values[13]))
        self.toys_edit.setText(str(result_values[16]))

        self.environment_edit.setText(str(result_values[2]))
        self.culture_edit.setText(str(result_values[5]))
        self.fashion_edit.setText(str(result_values[8]))
        self.travel_edit.setText(str(result_values[11]))
        self.animals_edit.setText(str(result_values[14]))
        self.scifi_edit.setText(str(result_values[17]))

    def display_recommended_aspiration(self, result_values):
        aspiration_list = calculate_aspiration_values(result_values)
        self.label_20.setText("1. {}: {} \n "
                              "2. {}: {} \n "
                              "3. {}: {} \n "
                              "4. {}: {} \n "
                              "5. {}: {} \n "
                              "6. {}: {}".format(aspiration_list[0][0], aspiration_list[0][1],
                                                 aspiration_list[1][0], aspiration_list[1][1],
                                                 aspiration_list[2][0], aspiration_list[2][1],
                                                 aspiration_list[3][0], aspiration_list[3][1],
                                                 aspiration_list[4][0], aspiration_list[4][1],
                                                 aspiration_list[5][0], aspiration_list[5][1]))

    def paste(self):
        clipboard = QGuiApplication.clipboard()
        mimeData = clipboard.mimeData()

        if mimeData.hasImage():
            self.target_image = mimeData.imageData()
            self.label.setPixmap(QPixmap(mimeData.imageData()).scaled(250, 180, Qt.KeepAspectRatio))
            result_values = calculate_interest_values(self.target_image)
            self.display_result_values(result_values)
            self.display_recommended_aspiration(result_values)
        else:
            self.label.setText("Cannot display data")

    def recalculate(self):
        INTEREST_ORDER = ['Politics', 'Money', 'Environment',
                          'Crime', 'Entertainment', 'Culture',
                          'Food', 'Health', 'Fashion',
                          'Sports', 'Paranormal', 'Travel',
                          'Work', 'Weather', 'Animals',
                          'School', 'Toys', 'Sci-Fi']
        politics = int(self.politics_edit.text())
        money = int(self.money_edit.text())
        environment = int(self.environment_edit.text())
        crime = int(self.crime_edit.text())
        entertainment = int(self.entertainment_edit.text())
        culture = int(self.culture_edit.text())

        food = int(self.food_edit.text())
        health = int(self.health_edit.text())
        fashion = int(self.fashion_edit.text())
        sports = int(self.sports_edit.text())
        paranormal = int(self.paranormal_edit.text())
        travel = int(self.travel_edit.text())

        work = int(self.work_edit.text())
        weather = int(self.weather_edit.text())
        animals = int(self.animals_edit.text())
        school = int(self.school_edit.text())
        toys = int(self.toys_edit.text())
        sci_fi = int(self.scifi_edit.text())

        interests_values = [politics, money, environment,
                            crime, entertainment, culture,
                            food, health, fashion,
                            sports, paranormal, travel,
                            work, weather, animals,
                            school, toys, sci_fi]

        self.display_recommended_aspiration(interests_values)


def match_screenshot_to_interest_panel(screenshot):
    # TODO: multi-scale template matching probably
    interests = imread('example.PNG')[:, :, :3]
    interests_width = interests.shape[1]
    interests_height = interests.shape[0]
    result = match_template(screenshot, interests)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[1], ij[0]
    cut_image = screenshot[y:y + interests_height, x:x + interests_width, :3]
    print(interests.shape, cut_image.shape)
    return cut_image


def calculate_interest_values(qimage):
    interests = imread('example.PNG')[:, :, :3]
    interests = qt_pixmap_to_array(QPixmap(qimage.rgbSwapped()))
    templates_grey = imread('../SecAspCalc/data/templates.png')
    plt.figure(num=None, figsize=(8, 6), dpi=80)
    slices = create_slices(interests)
    result_values = []

    for slice in slices:
        result = match_template(templates_grey, slice)
        ij = np.unravel_index(np.argmax(result), result.shape)
        y = ij[0]
        result_values.append(interpret_match(y))

    slice = slices[17]

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
    return result_values


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
