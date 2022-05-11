# Using Cognite Python SDK
[![Code Quality Checks](https://github.com/cognitedata/using-cognite-python-sdk/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/cognitedata/using-cognite-python-sdk/actions/workflows/code-quality.yaml)

A step by step guide with practical examples and code for using Cognite Python SDK.
https://cognite-docs.readthedocs-hosted.com/projects/cognite-sdk-python/en/latest/

## Getting Started:

1. First clone the repository using git
```
git clone git@github.com:cognitedata/using-cognite-python-sdk.git
```
2. Make sure that you've [poetry](https://python-poetry.org/) installed.
Also change the following setting in `poetry`
```
poetry config virtualenvs.in-project true
```
Open the repo in IDE (e.g. VS code) and run the following command in the terminal/commandline after navigating to the repo folder, this installs the dependencies defined in the `pyproject.toml` file.
```
poetry install
```

Now you're ready to run the code in jupyter notebooks.


## Additional notes for developers:
3. Also install pre-commit hooks. ( Make sure you've [pre-commit](https://pre-commit.com/) installed prior to this command)
```
pre-commit install
```

Note : Before committing to github, Always run below command, to check that pre-commit checks are passed.
```
poetry run pre-commit run --all-files
``` 

4. Add new libraries as needed
```
poetry add pandas numpy
```
or if only required for development
```
poetry add --dev pandas
```
