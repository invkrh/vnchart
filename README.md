# vnchart

[![Build Status](https://travis-ci.org/invkrh/vnchart.svg?branch=master)](https://travis-ci.org/invkrh/vnchart)
[![codecov](https://codecov.io/gh/invkrh/vnchart/branch/master/graph/badge.svg)](https://codecov.io/gh/invkrh/vnchart)

A tiny python web app to show network traffic of a sever with vnstat.

Thanks @vergoh for all the work on `vnstat`

## Requirements

* [vnstat >= 1.4](http://humdi.net/vnstat/)
* python 2.7 or 3.5

## Features

* Show data transfer during 
    -   current month
    -   last month
    -   last 24 hours
    -   last 30 days
    
## Install

```bash
cd /path/to/vnstat
pip install -r requirements.txt
```

    
## Run

```bash
cd /path/to/vnstat
python run.py
```

## Configuration

If you want to change port, please check `run.py` file

## Demo
[Here](http://vps.invkrh.me/demo)

