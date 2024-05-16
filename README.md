# Using Cognite Python SDK

A step by step guide with practical examples and code for using Cognite Python SDK.
https://cognite-docs.readthedocs-hosted.com/projects/cognite-sdk-python/en/latest/

## Getting Started:

1. First clone the repository using git
```
git clone https://github.com/cognitedata/using-cognite-python-sdk.git
```

2. Install the required packages by opening up the terminal on your machine and running the following command

```
pip install "cognite-sdk[pandas]"
```

For more advanced users, you can also use [poetry](https://python-poetry.org/) to manage your Python virtual environment. If you would like to use this tool, please follow the steps detailed in the next section.

## Additional notes for developers:

2. (Advanced) Make sure that you have a recent version of [poetry](https://python-poetry.org/) installed.
Also change the following setting in `poetry`
```
poetry config virtualenvs.in-project true
```
Open the repo in an IDE (e.g. VS code) and run the following command in the terminal/command line after navigating to the repo folder, this installs the dependencies defined in the `pyproject.toml` file.
```
poetry install
```

Now you're ready to run the code in jupyter notebooks. (Note: You might need to change the "kernel" to use the virtual environment that was created by poetry.)

3. Add new libraries if needed
```
poetry add pandas numpy
```
