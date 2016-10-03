#!/usr/bin/env bash

export FLASK_APP=dashboard/app.py
flask run --host=0.0.0.0 --port=80 --with-threads