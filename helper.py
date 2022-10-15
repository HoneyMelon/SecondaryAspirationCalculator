import numpy as np


def convert_qimage_to_mat(incomingImage):
    """  Converts a QImage into an opencv MAT format  """

    incomingImage = incomingImage.convertToFormat(4)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)
    return arr
