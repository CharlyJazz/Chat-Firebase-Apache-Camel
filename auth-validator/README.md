# Auth Validator for the Microservices

Just for DRY.

### Run tests

`pytest tests --disable-warnings -rP`


### Resources

- https://packaging.python.org/en/latest/tutorials/packaging-projects/


### Generating distribution archives

The next step is to generate distribution packages for the package. These are archives that are uploaded to the Python Package Index and can be installed by pip.

Make sure you have the latest version of PyPA’s build installed:

`python3 -m pip install --upgrade build`

`python3 -m build`

I am not 100% about this section. I need still stuying python packaging.. is kind of shitty
