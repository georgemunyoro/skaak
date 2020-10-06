## Contributing to Skaak

👍🎉 First off, thanks for taking the time to contribute! 🎉👍

The following is a set of guidelines for contributing to Skaak. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

### Your First Code Contribution
Unsure where to begin contributing? You can start by looking through the beginner and help-wanted issues:
 - Beginner issues - issues which should only require a few lines of code, and a test or two.
 - Help wanted issues - issues which should be a bit more involved than beginner issues.

### Styleguide
All Python code is formatted with [Black](https://pypi.org/project/black/). There is a `pyproject.toml` file with the black config of this project. I recommended creating a virtual environment, installing the packages in `requirements.txt` and using the version of black installed in your virtual environment. 

### Setting up a development environment
 - Install Python3.8
 - Install pip
 - In your command line, run the following commands while at the root of the project:
    1. `python -m venv venv`
    2. `./venv/Scripts/activate`
    3. `pip install -r requirements.txt`

### Testing
To run tests, simply run `python setup.py pytest`

### Building the library
In order to build the library: `python setup.py bdist_wheel`

The wheel file is stored in the `dist` folder that is created. You can install the library by using:
`pip install /path/to/wheelfile.whl`
