# Copyright (c) 2019 Heizelnut
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from setuptools import setup

def get_file_conts(file):
    with open(file, "r") as f:
        contents = f.read()
    
    return contents

requirements = get_file_conts("./requirements.txt").split("\n")

dependencies = [line for line in requirements 
    if not line.startswith("//") or line != ""]

setup(
    name="hawkloon",
    version="0.2.0",
    description="Python framework to build synchronous workers.",
    long_description=get_file_conts("../README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/heizelnut/hawkloon",
    author="Heizelnut",
    author_email="emalillo270304@gmail.com",
    license="MIT",
    packages=["hawk"],
    install_requires=dependencies,
    zip_safe=False
)
