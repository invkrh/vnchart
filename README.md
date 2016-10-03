# vnchart

[![Build Status](https://travis-ci.org/invkrh/vnchart.svg?branch=master)](https://travis-ci.org/invkrh/vnchart)
[![codecov](https://codecov.io/gh/invkrh/vnchart/branch/master/graph/badge.svg)](https://codecov.io/gh/invkrh/vnchart)

A tiny python web app to show network traffic of a sever with `vnstat`.

Thanks [@vergoh](https://github.com/vergoh) for all the work on `vnstat`

## Demo

To give you a quick idea on what it looks like, you could have a look at the following page.

[Here](http://vps.invkrh.me/demo)

## Requirements

* python 2.7 or 3.5

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
        
        Take a look at `INSTALL` file in the source zip file. Normally, there will be no more lib deps to install.
        
        ```bash
        $ ./configure --prefix=/usr --sysconfdir=/etc && make
        $ make install
        ```
    - **Check version**: `vnstat --version`

## Features

* Data transfer dashboard 
    -   current month
    -   last month
    -   last 24 hours
    -   last 30 days

* UI Chart
    -   responsive
    -   filter dataset by clicking on legend
    -   all the leading zeor-value bars will not be shown
    
## Install

```bash
git clone https://github.com/invkrh/vnchart.git
cd vnstat
pip install -r requirements.txt
```
    
## Run

```bash
./start.sh
```

## Configuration

If you want to change port(default: `80`, only available for root), please check `start.sh` file.

## Troubleshooting

Check `./logs` which is hourly rotated within the recent 24 hours
