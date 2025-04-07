from setuptools import setup, find_packages

setup(
    name="hugewoodhash",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["cli"],
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "hugewood=cli:main",
        ],
    },
    author="ShweHollow",
    description="A real-time jurisprudential consensus mechanism based on U.S. law, born as a wedding gift.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ShweHollow/Hugewood_Hash",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
