import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="input2midi",
    version="0.8.0",
    author="Midilab",
    author_email="contact@midilab.co",
    description="A package intend to transform different common computer input devices into a midi device",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://midilab.co/input2midi",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
