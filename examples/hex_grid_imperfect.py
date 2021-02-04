import numpy as np
from penkit import shapes
from penkit.write import write_plot
from penkit.textures.util import rotate_texture, fit_texture

def hex_grid_imperfect_1(n=10):
    grid = (np.array([]), np.array([]))

    seg1 = shapes.line((0,0), length=1.0, angle=-np.pi/3)
    seg1 = (
        np.concatenate([seg1[0], [np.nan]]),
        np.concatenate([seg1[1], [np.nan]])
    )
    seg2 = shapes.line((seg1[0][-2],seg1[1][-2]), length=1.0, angle=0.0)
    seg2 = (
        np.concatenate([seg2[0], [np.nan]]),
        np.concatenate([seg2[1], [np.nan]])
    )
    seg3 = shapes.line((seg2[0][-2],seg2[1][-2]), length=1.0, angle=np.pi/3)
    seg3 = (
        np.concatenate([seg3[0], [np.nan]]),
        np.concatenate([seg3[1], [np.nan]])
    )
    half_hex_zero_origin = (
        np.concatenate([seg1[0], seg2[0], seg3[0]]),
        np.concatenate([seg1[1], seg2[1], seg3[1]])
    )

    half_hex_row_zero_origin = (
        np.concatenate([half_hex_zero_origin[0] + 3.0 * i for i in range(int(n/2))]),
        np.concatenate([half_hex_zero_origin[1] for i in range(int(n/2))])
    )

    for i in range(n):
        if i % 2 == 0:
            grid = (
                np.concatenate([grid[0], half_hex_row_zero_origin[0]]),
                np.concatenate([grid[1], half_hex_row_zero_origin[1] - np.sqrt(3)/2 * i])
            )
        else:
            grid = (
                np.concatenate([grid[0], half_hex_row_zero_origin[0] + 1.5 ]),
                np.concatenate([grid[1], half_hex_row_zero_origin[1] - np.sqrt(3)/2 * i])
            )

    # time to remove stuff
    seg_length = len(seg1[0])
    layer_length = len(grid[0])
    num_segments = int(layer_length / seg_length)
    mask = np.repeat(np.random.uniform(size=num_segments) < 0.7, seg_length)
    grid = (
        grid[0][mask],
        grid[1][mask]
    )

    return grid

def hex_grid_imperfect(n=10):
    grid = (np.array([]), np.array([]))

    hexagon = shapes.hexagon((0,0), resolution=2)

    hex_row_zero_origin = (
        np.concatenate([hexagon[0] + 3.0 * i for i in range(int(n/2))]),
        np.concatenate([hexagon[1] for i in range(int(n/2))])
    )

    for i in range(n):
        if i % 2 == 0:
            grid = (
                np.concatenate([grid[0], hex_row_zero_origin[0]]),
                np.concatenate([grid[1], hex_row_zero_origin[1] - np.sqrt(3)/2 * i])
            )
        else:
            grid = (
                np.concatenate([grid[0], hex_row_zero_origin[0] + 1.5 ]),
                np.concatenate([grid[1], hex_row_zero_origin[1] - np.sqrt(3)/2 * i])
            )

    # time to remove stuff
    seg_length = len(hexagon[0])
    layer_length = len(grid[0])
    num_segments = int(layer_length / seg_length)
    mask = np.repeat(np.random.uniform(size=num_segments) < 0.6, seg_length)
    grid = (
        grid[0][mask],
        grid[1][mask]
    )

    return grid


texture = hex_grid_imperfect(80)
texture = fit_texture(texture)
texture = (
    0.5 * texture[0],
    0.5 * texture[1]
)

# rotate the texture
#texture = rotate_texture(texture, 50)

# create the surface
from penkit.surfaces import make_cylinder_surface, make_noise_surface
surface = make_cylinder_surface()

# project the texture onto the surface
from penkit.projection import project_and_occlude_texture
proj = project_and_occlude_texture(texture, surface, angle=45)

write_plot([proj], 'examples/imperfect_hex_cylinder.svg', height=11.0, width=8.5)