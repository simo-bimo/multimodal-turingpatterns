import numpy as np

def generate_grid(dx=1, dy=1, bottom_left=(-5,-5), top_right=(5,5)):
    '''
    Generates a grid of x values and y values, 
    based on the distance between points (dx, dy),
    and the corners specified.
    Returns a grid of x values, a grid of y values,
    the number of x values, and the number of y values.
    '''

    x_start = bottom_left[0]
    x_stop = top_right[0]
    
    y_start = bottom_left[1]
    y_stop = top_right[1]

    x_num = round((x_stop - x_start) / dx) + 1
    y_num = round((y_stop - y_start) / dy) + 1

    x = np.linspace(x_start, x_stop, x_num)
    y = np.linspace(y_start, y_stop, y_num)

    x_vals, y_vals = np.meshgrid(x,y)

    return x_vals, y_vals, x_num, y_num