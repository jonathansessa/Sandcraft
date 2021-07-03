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
                    20, 1000, 2230,         # temperature (temp, freeze, boil)
                    1.6,                    # density
                    (255, 255, 0),          # color
                    "sand",                 # name
                    0,                      # flammability
                    "solid")                # state (solid, liquid, gas, fixed)

template_water = Liquid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    20, 0, 100,             # temperature
                    1.0,                    # density
                    (0, 0, 255),            # color
                    "water",                # name
                    0,                      # flammability
                    "liquid")               # state

template_lava = Liquid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    2000, 800, 10000,       # temperature
                    3.0,                    # density
                    (153, 0, 0),            # color
                    "lava",                 # name
                    0,                      # flammability
                    "liquid")               # state

template_steam = Gas(
                    0, 0,                   # position
                    0, -1,                  # velocity
                    10, -100, 10000,        # temperature
                    0.5,                    # density
                    (125, 125, 125),        # color
                    "steam",                # name
                    0.95,                   # flammability
                    "gas")                  # state

template_wood = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    20, 400, 7000,          # temperature
                    5.0,                    # density
                    (160, 82, 45),          # color
                    "wood",                 # name
                    0.2,                    # flammability
                    "fixed")                # state

template_metal = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    20, 1200, 10000,        # temperature
                    15.0,                   # density
                    (192, 192, 192),        # color
                    "metal",                # name
                    0.1,                    # flammability
                    "fixed")                # state

template_basalt = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    600, 1500, 800,         # temperature
                    15.0,                   # density
                    (53, 72, 96),           # color
                    "basalt",               # name
                    0.1,                      # flammability
                    "fixed")                # state

template_fire = Gas(
                    0, 0,                   # position
                    0, -1,                  # velocity
                    800, -300, 10000,       # temperature
                    0.5,                    # density
                    (201, 75, 44),          # color
                    "fire",                 # name
                    0,                      # flammability
                    "gas")                  # state


template_powder = Solid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    20, 300, 2230,          # temperature (temp, freeze, boil)
                    1,                      # density
                    (249, 218, 159),        # color
                    "powder",               # name
                    0.9,                    # flammability
                    "solid")                # state

template_ice = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    -80, 0, 100,            # temperature
                    1,                      # density
                    (47, 230, 239),         # color
                    "ice",                  # name
                    0,                      # flammability
                    "fixed")                # state

template_oil = Liquid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    20, -100, 100,          # temperature
                    0.3,                    # density
                    (86, 63, 43),           # color
                    "oil",                  # name
                    0.98,                   # flammability
                    "liquid")               # state

template_fog = Gas(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    20, -100, 100,          # temperature
                    0.3,                    # density
                    (218, 234, 232),        # color
                    "fog",                  # name
                    0,                      # flammability
                    "gas")                  # state

template_stone = Solid(
                    0, 0,                   # position
                    0, 1,                   # velocity
                    20, 1100, 2230,         # temperature (temp, freeze, boil)
                    20,                     # density
                    (137, 137, 137),        # color
                    "stone",                # name
                    0,                      # flammability
                    "solid")                # state
                    
template_generator = Fixed(
                    0, 0,                   # position
                    0, 0,                   # velocity
                    20, -100, 1000,         # temperature
                    15.0,                   # density
                    (0, 153, 153),          # color
                    "Water Generator",      # name
                    0,                      # flammability
                    "fixed")                # state

# Particle dictionary used to create particle selection tool
ELEMENTS = {
    "FIXED": [template_wood, template_metal, template_basalt, template_ice],
    "SOLIDS": [template_sand, template_powder, template_stone],
    "LIQUIDS": [template_water, template_lava, template_oil],
    "GASES": [template_steam, template_fire, template_fog],
    "SPECIAL": [template_generator]
}