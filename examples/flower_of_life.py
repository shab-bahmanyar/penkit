from penkit import shapes
import numpy as np
from penkit.write import write_plot
from penkit.textures.util import concat
import math

def vertical_overlapping_circles(lowerBound, upperBound, x, offset):
    l = ([], [])
    for i in range(lowerBound,upperBound):
        circle = shapes.circle((x,i+offset), 1)
        l = concat([l, circle, ([np.nan], [np.nan])])
    return l

l = ([], [])
# centers at [0,-1], [0,0], [0,1]
l = concat([l, vertical_overlapping_circles(-1, 2, 0, 0)])

horizontal = math.sqrt(3)/2
vertical = 1/2
l = concat([l, vertical_overlapping_circles(-2, 2, horizontal, 0.5)])
l = concat([l, vertical_overlapping_circles(-2, 3, horizontal*2, 0)])
l = concat([l, vertical_overlapping_circles(-2, 2, horizontal*3, 0.5)])
l = concat([l, vertical_overlapping_circles(-1, 2, horizontal*4, 0)])

# outer circles
l = concat([l, shapes.circle((horizontal*2,0), 3), ([np.nan], [np.nan]), shapes.circle((horizontal*2,0), 3.1)])

write_plot([l], 'examples/flower_of_life.svg', height=8.5, width=8.5, stroke_thickness_pct=0.0015)