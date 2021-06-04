import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="okcoin-GBRUNNER", # Replace with your own username
    version="0.0.1c",
    author="Gregory Brunner",
    author_email="gregory.brunner@protonmail.com",
    description="A Python package for interfacing with okcoin.",
    long_description="Longer description here.",
    long_description_content_type="text/markdown",
    url="https://github.com/gbrunner/python-api-for-okcoin",
    project_urls={
        "Bug Tracker": "https://github.com/gbrunner/python-api-for-okcoin/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)