import copy
import numpy as np
from PyQt5.QtGui import QImage


def qt_pixmap_to_array(pixmap):
    channels_count = 4
    image = pixmap.toImage()
    s = image.bits().asstring(pixmap.width() * pixmap.height() * channels_count)
    arr = np.frombuffer(s, dtype=np.uint8).reshape((pixmap.height(), pixmap.width(), channels_count))
    return arr
