from solid import Solid
from liquid import Liquid
from gas import Gas
from fixed import Fixed


"""
    Template particles that can be used for the Painter, or elsewhere.
"""

template_sand = Solid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    20, -100, 500,          # temperature
                    1.5,                    # density
                    (255, 255, 0),          # color
                    "Sand")                 # name

template_water = Liquid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    20, 0, 100,             # temperature
                    1.0,                    # density
                    (0, 0, 255),            # color
                    "Water")                # name

template_lava = Liquid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    1000, -1000, 10000,     # temperature
                    2.0,                    # density
                    (153, 0, 0),            # color
                    "Lava")                 # name

template_steam = Gas(
                    0, 0,                   # position
                    0, -1,                  # velocity
                    20, -100, 10000,        # temperature
                    0.5,                    # density
                    (125, 125, 125),        # color
                    "Steam")                # name

template_wood = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    20, 0, 200,             # temperature
                    5.0,                    # density
                    (160, 82, 45),          # color
                    "Wood")                 # name

template_metal = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    20, -100, 1000,         # temperature
                    15.0,                   # density
                    (192, 192, 192),        # color
                    "Metal")                # name

template_generator = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    20, -100, 1000,         # temperature
                    15.0,                   # density
                    (0, 153, 153),          # color
                    "Water Generator")      # name

# Particle dictionary used to create particle selection tool
ELEMENTS = {
    "FIXED": [template_wood, template_metal],
    "SOLIDS": [template_sand],
    "LIQUIDS": [template_water, template_lava],
    "GASES": [template_steam],
    "SPECIAL": [template_generator]
}
