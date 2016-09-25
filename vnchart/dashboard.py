import logging
import json
import subprocess

from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, render_template

app = Flask(__name__)


def vnstat(basis, fmt='json'):
    """Call vnstat cmd in a subprocess

    basis:
    'h' => last 24 hours
    'd' => last 30 days
    'm' => last 12 months

    fmt: 'json' or 'xml'
    """
    assert basis == 'h' or basis == 'd' or basis == 'm'
    assert fmt == 'xml' or fmt == 'json'
    stat = subprocess.check_output(["vnstat", '--' + fmt, basis])
    return json.loads(stat)


def stats_data(vnstat, basis):
    datasets = []
    for ifc in vnstat['interfaces']:
        if_id = ifc['id']
        offsets = []
        in_mb = []
        out_mb = []
        for elem in ifc['traffic'][basis]:
            offsets.append(elem['id'])
            in_mb.append(kb_to_mb(elem['rx']))
            out_mb.append(kb_to_mb(elem['tx']))
        dataset_in = {
            "interface": if_id + '-in',
            'transfer': in_mb
        }
        dataset_out = {
            "interface": if_id + '-out',
            'transfer': out_mb
        }
        datasets.append(dataset_in)
        datasets.append(dataset_out)

    return {
        'datasets': datasets,
        'offsets': offsets
    }


def kb_to_mb(num):
    return "%.2f" % (num / 1024.0)


def current_month():
    import datetime
    mydate = datetime.datetime.now()
    return mydate.strftime("%B")

def current_usage(vnstat):
    usage = 0
    for ifc in vnstat['interfaces']:
        curr = ifc['traffic']['months'][0]
        usage += curr["rx"] + curr["tx"]
    return kb_to_mb(usage)


def read_json(json_file):
    with open(json_file) as data_file:
        return json.load(data_file)


def dashboard(is_demo=False):
    if is_demo:
        # Debug on server without vnstat >= 1.14
        vnstat_hour = read_json('data/hour.json')
        vnstat_day = read_json('data/day.json')
        vnstat_month = read_json('data/month.json')
    else:
        try:
            vnstat_hour = vnstat('h')
            vnstat_day = vnstat('d')
            vnstat_month = vnstat('m')
        except subprocess.CalledProcessError as err:
            msg = 'Command [ {} ] ends with [ {} ]'.format(
                ' '.join(err.cmd), err.output.decode("utf-8").rstrip())
            app.logger.error(msg)
            return render_template('error.html', msg=msg)

    return render_template('index.html',
                           month=current_month(),
                           hourly=stats_data(vnstat_hour, 'hours'),
                           daily=stats_data(vnstat_day, 'days'),
                           usage=current_usage(vnstat_month))


@app.route("/")
def root():
    return dashboard()


@app.route("/demo")
def demo():
    return dashboard(is_demo=True)

if __name__ == "__main__":

    import os
    import errno

    try:
        os.makedirs("../log")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    handler = TimedRotatingFileHandler('../log/vps-traffic.log',
                                       when="midnight",
                                       # when="S",
                                       # interval=1,
                                       backupCount=5)
    handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(module)s:%(lineno)d]'
    ))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
