# Getting Started with Adding Content to this Documentation

## Setting Up Your Environment

0. Install Python >= 3.10
1. Create a virtual environment using Python's `venv` module:
    ```bash
    python -m venv venv
    ```
    _depending on your installation you may have to use py, python3 instead of python here_

2. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On Unix/Linux:
        ```bash
        source venv/bin/activate
        ```

3. To deactivate the virtual environment, simply run:
    ```bash
    deactivate
    ```

## Installing Dependencies

Make sure to install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

In case you'd like to update the requirements.txt file:
```bash
pip freeze > requirements.txt
```

## Serving the documentation locally

To preview your documentation locally, you can use MKDocs' built-in development server. Make sure your virtual environment is activated, then run:

```bash
mkdocs serve
```

Then navigate to the URL provided by the local server, usually
[http://127.0.0.1:8000/](http://127.0.0.1:8000/) or
[http://localhost:8000/](http://localhost:8000/)

## Building the documentation

Once you're satisfied with your changes, you can simply push your changes and the automatic deployment of the new version will be handled by github actions

Alternatively use `mkdocs build` in your command line to build the documentation locally


