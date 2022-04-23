#!/usr/bin/sh 

poetry run pylint $(find . -name "*.py" | xargs)
