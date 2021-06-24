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
                    20, 600, 5000,          # temperature (temp, freeze, boil)
                    1.5,                    # density
                    (255, 255, 0),          # color
                    "sand",                 # type
                    0.4)                    # flammability

template_water = Liquid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    20, 0, 100,             # temperature
                    1.0,                    # density
                    (0, 0, 255),            # color
                    "water",                # type
                    0)                      # flammability

template_lava = Liquid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    2000, 800, 10000,       # temperature
                    2.0,                    # density
                    (153, 0, 0),            # color
                    "lava",                 # type
                    0)                      # flammability

template_steam = Gas(
                    0, 0,                   # position
                    0, -1,                  # velocity
                    20, -100, 10000,        # temperature
                    0.5,                    # density
                    (125, 125, 125),        # color
                    "steam",                # type
                    0.95)                   # flammability

template_wood = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    20, 400, 200,           # temperature
                    5.0,                    # density
                    (160, 82, 45),          # color
                    "wood",                 # type
                    0.2)                    # flammability

template_metal = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    20, 700, 10000,         # temperature
                    15.0,                   # density
                    (192, 192, 192),        # color
                    "metal",                # type
                    0.1)                   # flammability

template_basalt = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    600, 300, 800,          # temperature
                    15.0,                   # density
                    (41, 58, 79),           # color
                    "basalt",               # type
                    0.1)                   # flammability

template_fire = Gas(
                    0, 0,                   # position
                    0, -1,                  # velocity
                    800, 300, 10000,        # temperature
                    0.5,                    # density
                    (201, 75, 44),          # color
                    "fire",                 # type
                    0)                      # flammability

# Particle dictionary used to create particle selection tool
ELEMENTS = {
    "FIXED": [template_wood, template_metal],
    "SOLIDS": [template_sand, template_basalt],
    "LIQUIDS": [template_water, template_lava],
    "GASES": [template_steam, template_fire]
}