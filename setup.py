import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiopypixel",
    version="1.0.11",
    author="TrustedMercury & Iapetus11",
    description="An asynchronous python wrapper for the Hypixel API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Villager-Dev/aiopypixel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
