# CislunarSim Documentation

This folder contains the auto-docuemntation infrastructure provided by Sphinx. Sphinx provides autodocumentation features which automatically parse docstrings within files and organizes them in an HTML format. We are using the Google style of docstrings, which look like the following:

```
"""
This is an example of Google style.

Args:
    param1: This is the first param.
    param2: This is a second param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
```

## How to use
Sphinx was set up pretty much according to the following StackOverflow post https://stackoverflow.com/a/60159862. The first function to call is:
```console
/CislunarSim/docs$ sphinx-apidoc -o ./source ../src
```
This function automatically generates `.rst` files based upon the files in our `src/` directory. Make sure when running this, you delete all the `.rst` files except for `index.rst` so updated files get generated (script to encapsulate all this to come!)
```console
/CislunarSim/docs$ make html
```
This function generates the html files and places them in the `docs/build/` directory. The `build/` directory is in the `.gitignore` file but could be helpful in debugging locally.
