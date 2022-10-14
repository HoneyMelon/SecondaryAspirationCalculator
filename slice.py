def create_slices(interest):
    slices = []
    start_y = 17
    len_y = 18
    offset_y = 36
    start_x = 4
    len_x = 82
    offset_x = 28
    print(interest.shape[1])
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
