from setuptools import setup

setup(
    name="sandcraft",
    version="0.1",
    author=["John Hook", "Anthony Kane", "Levi Mutter", "Jonathan Sessa", "Lukas Vaiciunas"],
    author_email="jsessa@ufl.edu",
    packages=["sandcraft",],
    url="https://github.com/jonathansessa/Sandcraft",
    license="MIT",
    description="Particle physics sandbox game",
    include_package_data=True,
    install_requires=["pygame>=2.0", "cx_Freeze>=6.4",],
    entry_points=
    {
        "console_scripts":
            [
                "play sandcraft = sandcraft.main:main"
            ]
    }
)