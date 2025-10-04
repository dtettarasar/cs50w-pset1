# cs50w-pset1

Source code for **CS50W's Problem Set 1: Wiki**

Project specification: https://cs50.harvard.edu/web/projects/1/wiki/

---

## Overview

This project is a simple Wikipedia-like encyclopedia built with Django, as part of the CS50W course.
It allows users to view, search, create, edit, and randomly access encyclopedia entries.

---

## Use the project with uv 

This project uses uv, a modern Python package and project manager.

More info here: https://docs.astral.sh/uv/

If you don’t already have it installed, please follow the installation guide: 

https://docs.astral.sh/uv/getting-started/installation/

Alternatively, you can install it with pip:
~~~
$ pip install uv
~~~

Once uv is installed, sync all project dependencies:
~~~
$ uv sync
~~~

Then, use uv to run Django management commands:
~~~
$ uv run manage.py makemigrations
$ uv run manage.py migrate
$ uv run manage.py runserver
~~~

The project should now be available at http://127.0.0.1:8000/

---

## Notes

- The project has been tested with Python 3.12+.

- Dependencies are defined in pyproject.toml (handled automatically by uv sync).

- No additional configuration is required before running the server.

---

*Developed as part of Harvard’s CS50W course.*