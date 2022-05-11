# Python Project
This is a template for a basic python project.

* Ensure that URL points to file in your repository.
[![Code Quality Checks](https://github.com/choukha/python-basic-template/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/choukha/python-basic-template/actions/workflows/code-quality.yaml)


To get started with this repo :

1. First clone the repository, example such as
```
git clone git@github.com:your-user/your-repo-name.git
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

3. Also install pre-commit hooks
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
