from . import solid
from . import liquid
from . import gas
from . import fixed


"""
    Template particles that can be used for the Painter, or elsewhere.
"""

template_sand = solid.Solid(
                    0, 0,                   # position
                    0.0, 1.0,               # velocity
                    0.0, 0.0,               # acceleration
                    20, 1000, 2230,         # temperature (temp, freeze, boil)
                    1.6,                    # density
                    (255, 255, 0),          # color
                    "sand",                 # name
                    0,                      # flammability
                    "solid")                # state (solid, liquid, gas, fixed)

template_water = liquid.Liquid(
                    0, 0,                   # position
                    0.0, 1.0,               # velocity
                    0.0, 0.0,               # acceleration
                    20, 0, 100,             # temperature
                    1.0,                    # density
                    (0, 0, 255),            # color
                    "water",                # name
                    0,                      # flammability
                    "liquid")               # state

template_lava = liquid.Liquid(
                    0, 0,                   # position
                    0.0, 1.0,               # velocity
                    0.0, 0.0,               # acceleration
                    2000, 800, 10000,       # temperature
                    3.0,                    # density
                    (153, 0, 0),            # color
                    "lava",                 # name
                    0,                      # flammability
                    "liquid")               # state

template_steam = gas.Gas(
                    0, 0,                   # position
                    0.0, -1.0,              # velocity
                    0.0, 0.0,               # acceleration
                    10, -100, 10000,        # temperature
                    0.5,                    # density
                    (125, 125, 125),        # color
                    "steam",                # name
                    0.95,                   # flammability
                    "gas")                  # state

template_wood = fixed.Fixed(
                    0, 0,                   # position
                    0.0, 0.0,               # velocity
                    0.0, 0.0,               # acceleration
                    20, 400, 7000,          # temperature
                    5.0,                    # density
                    (160, 82, 45),          # color
                    "wood",                 # name
                    0.2,                    # flammability
                    "fixed")                # state

template_metal = fixed.Fixed(
                    0, 0,                   # position
                    0.0, 0.0,               # velocity
                    0.0, 0.0,               # acceleration
                    20, 1200, 10000,        # temperature
                    15.0,                   # density
                    (192, 192, 192),        # color
                    "metal",                # name
                    0.1,                    # flammability
                    "fixed")                # state

template_basalt = fixed.Fixed(
                    0, 0,                   # position
                    0.0, 0.0,               # velocity
                    0.0, 0.0,               # acceleration
                    600, 1500, 800,         # temperature
                    15.0,                   # density
                    (53, 72, 96),           # color
                    "basalt",               # name
                    0.1,                    # flammability
                    "fixed")                # state

template_fire = gas.Gas(
                    0, 0,                   # position
                    0.0, -1.0,              # velocity
                    0.0, 0.0,               # acceleration
                    800, -300, 10000,       # temperature
                    0.5,                    # density
                    (201, 75, 44),          # color
                    "fire",                 # name
                    0,                      # flammability
                    "gas")                  # state

template_powder = solid.Solid(
                    0, 0,                   # position
                    0.0, 1.0,               # velocity
                    0.0, 0.0,               # acceleration
                    20, 300, 2230,          # temperature (temp, freeze, boil)
                    1,                      # density
                    (249, 218, 159),        # color
                    "powder",               # name
                    0.9,                    # flammability
                    "solid")                # state

template_snow = solid.Solid(
                    0, 0,                   # position
                    0.0, 1.0,               # velocity
                    0.0, 0.0,               # acceleration
                    -30, 0, 100,            # temperature (temp, freeze, boil)
                    .9,                     # density
                    (255, 250, 250),        # color
                    "snow",                 # name
                    0,                      # flammability
                    "solid")                # state

template_ice = fixed.Fixed(
                    0, 0,                   # position
                    0.0, 0.0,               # velocity
                    0.0, 0.0,               # acceleration
                    -80, 0, 100,            # temperature
                    1,                      # density
                    (47, 230, 239),         # color
                    "ice",                  # name
                    0,                      # flammability
                    "fixed")                # state

template_oil = liquid.Liquid(
                    0, 0,                   # position
                    0.0, 1.0,               # velocity
                    0.0, 0.0,               # acceleration
                    20, -100, 100,          # temperature
                    0.3,                    # density
                    (86, 63, 43),           # color
                    "oil",                  # name
                    0.98,                   # flammability
                    "liquid")               # state

template_fog = gas.Gas(
                    0, 0,                   # position
                    0.0, 0.0,               # velocity
                    0.0, 0.0,               # acceleration
                    20, -100, 100,          # temperature
                    0.3,                    # density
                    (218, 234, 232),        # color
                    "fog",                  # name
                    0,                      # flammability
                    "gas")                  # state

template_stone = solid.Solid(
                    0, 0,                   # position
                    0.0, 1.0,               # velocity
                    0.0, 0.0,               # acceleration
                    20, 1100, 2230,         # temperature (temp, freeze, boil)
                    20,                     # density
                    (137, 137, 137),        # color
                    "stone",                # name
                    0,                      # flammability
                    "solid")                # state
                    
template_generator = fixed.Fixed(
                    0, 0,                   # position
                    0.0, 0.0,               # velocity
                    0.0, 0.0,               # acceleration
                    20, -100, 1000,         # temperature
                    15.0,                   # density
                    (0, 153, 153),          # color
                    "Water Generator",      # name
                    0,                      # flammability
                    "fixed")                # state

# Particle dictionary used to create particle selection tool
ELEMENTS = {
    "FIXED": [template_wood, template_metal, template_basalt, template_ice],
    "SOLIDS": [template_sand, template_powder, template_stone, template_snow],
    "LIQUIDS": [template_water, template_lava, template_oil],
    "GASES": [template_steam, template_fire, template_fog],
    "SPECIAL": [template_generator]
}
