from setuptools import setup

setup(
    name="sandcraft",
    version="0.1",
    packages=["sandcraft",],
    url="https://github.com/jonathansessa/Sandcraft",
    license="MIT",
    description="Particle physics sandbox game",
    install_requires=["pygame>=2.0",],

    entry_points =
    {
        "console_scripts":
            [
                "play sandcraft = sandcraft:main"
            ]
    }
)