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
pip install cognite-sdk msal pandas
```

For more adavanced users, you can also use [poetry](https://python-poetry.org/) to manage your Python virtual environment. If you would like to use this, please follow the steps detailed in the next section.

## Additional notes for developers:

2. (Advanced) Make sure that you've [poetry](https://python-poetry.org/) installed.
Also change the following setting in `poetry`
```
poetry config virtualenvs.in-project true
```
Open the repo in IDE (e.g. VS code) and run the following command in the terminal/commandline after navigating to the repo folder, this installs the dependencies defined in the `pyproject.toml` file.
```
poetry install
```

Now you're ready to run the code in jupyter notebooks. ( Note : Change the "Kernel" to use the virtual environment created by poetry.)

3. Add new libraries as needed
```
poetry add pandas numpy
```
or if only required for development
```
poetry add --dev pandas
```
