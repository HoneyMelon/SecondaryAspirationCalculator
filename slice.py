def create_slices(interest):
    slices = []
    start_y = 17
    len_y = 18
    offset_y = 36
    start_x = 4
    len_x = 82
    offset_x = 28
    for i in range(18):
        # first column
        if i % 3 == 0:
            slices.append(interest[start_y:start_y+len_y, start_x:start_x+len_x])
        # second column
        if i % 3 == 1:
            slices.append(interest[start_y:start_y + len_y, start_x:start_x + len_x])
        # third column
        if i % 3 == 2:
            slices.append(interest[start_y:start_y + len_y, start_x:start_x + len_x])
            start_y = start_y + offset_y
        start_x = start_x + len_x + offset_x
        if start_x > interest.shape[1]:
            start_x = 4
    return slices


def interpret_match(y_value):
    """
    :param y_value: y_coord of template match
    :return: number of bars filled
    """
    if y_value < 18 * 1:
        return 0
    if y_value < 18 * 2:
        return 1
    if y_value < 18 * 3:
        return 2
    if y_value < 18 * 4:
        return 3
    if y_value < 18 * 5:
        return 4
    if y_value < 18 * 6:
        return 5
    if y_value < 18 * 7:
        return 6
    if y_value < 18 * 8:
        return 7
    if y_value < 18 * 9:
        return 8
    if y_value < 18 * 10:
        return 9
    if y_value < 18 * 11:
        return 10
    else:
        return -1
