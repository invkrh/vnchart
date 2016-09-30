# vnchart

[![Build Status](https://travis-ci.org/invkrh/vnchart.svg?branch=master)](https://travis-ci.org/invkrh/vnchart)
[![codecov](https://codecov.io/gh/invkrh/vnchart/branch/master/graph/badge.svg)](https://codecov.io/gh/invkrh/vnchart)

A tiny python web app to show network traffic of a sever with `vnstat`.

Thanks [@vergoh](https://github.com/vergoh) for all the work on `vnstat`

## Demo

To give you a quick idea on what it looks like, you could have a look at the following page.

[Here](http://vps.invkrh.me:8080/demo)

## Requirements

* [vnstat >= 1.14](http://humdi.net/vnstat/)
    
    - **ubutun / debian**: 
    
        ```bash
        $ sudu apt-get install vnstat
        ```
    - **centos / redhat**: 
    
        The vnStat rpm packages are on the EPEL Repo, so you'll need that setup on your server. Then you should be able to just install with yum.
    
        ```bash
        $ sudo yum -y install vnstat
        ```
    - **source**: 
        
        If the version is not satisfied, you can always install it from source.
        Take a look at INSTALL file in the source zip file
        
        ```bash
        $ ./configure --prefix=/usr --sysconfdir=/etc && make
        $ make install
        ```
    - **Check version**: `vnstat --version`
         
* python 2.7 or 3.5

## Features

* Data transfer dashboard 
    -   current month
    -   last month
    -   last 24 hours
    -   last 30 days

* UI Chart
    -   reponsive
    -   filter dataset by clicking on legend
    
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
