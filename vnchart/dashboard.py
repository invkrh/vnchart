import logging
import json
import subprocess

from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, render_template

app = Flask(__name__)


def vnstat(unit, fmt='json'):
    """Call vnstat cmd in a subprocess

    basis:
    'h' => last 24 hours
    'd' => last 30 days
    'm' => last 12 months

    fmt: 'json' or 'xml'
    """
    assert unit == 'h' or unit == 'd' or unit == 'm'
    assert fmt == 'xml' or fmt == 'json'
    stat = subprocess.check_output(["vnstat", '--' + fmt, unit])
    return json.loads(stat)


def stats_data(vnstat, unit_key):
    from datetime import datetime, timedelta

    def hour_key(elem):
        dt = elem['date'] # id is hour
        return datetime(year=dt['year'], month=dt['month'], day=dt['day'],
                        hour=elem['id']) \
            + timedelta(hours=1) # adjust to the end of the period

    def day_key(elem):
        dt = elem['date']
        return datetime(year=dt['year'], month=dt['month'], day=dt['day']) \
            + timedelta(days=1) # adjust to the end of the period

    if unit_key == 'hours':
        key = hour_key
    elif unit_key == 'days':
        key = day_key
    else:
        raise ValueError("Argument [ unit_key ] should be {'hours', 'days'}")

    datasets = []
    for ifc in vnstat['interfaces']:
        if_id = ifc['id']

        traffic = sorted([(key(elem), kb_to_mb(elem['rx']), kb_to_mb(elem['tx']))
                          for elem in ifc['traffic'][unit_key]], reverse=True)
        dataset_in = {
            "label": if_id + '-in',
            'transfer': [(x[0].isoformat(), x[1]) for x in traffic]
        }
        dataset_out = {
            "label": if_id + '-out',
            'transfer': [(x[0].isoformat(), x[2]) for x in traffic]
        }
        datasets.append(dataset_in)
        datasets.append(dataset_out)

    return datasets


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


def dashboard(mode):
    if mode == 'debug':
        # Debug on server without vnstat >= 1.14
        try:
            vnstat_hour = read_json('data/debug/hour.json')
            vnstat_day = read_json('data/debug/day.json')
            vnstat_month = read_json('data/debug/month.json')
        except IOError as err:
            app.logger.error(err)
            return render_template('error.html', msg=err)
    elif mode == 'demo':
        try:
            vnstat_hour = read_json('data/demo/hour.json')
            vnstat_day = read_json('data/demo/day.json')
            vnstat_month = read_json('data/demo/month.json')
        except IOError as err:
            app.logger.error(err)
            return render_template('error.html', msg=err)
    elif mode == '':
        try:
            vnstat_hour = vnstat('h')
            vnstat_day = vnstat('d')
            vnstat_month = vnstat('m')
        except subprocess.CalledProcessError as err:
            msg = 'Command [ {} ] ends with [ {} ]'.format(
                ' '.join(err.cmd), err.output.decode("utf-8").rstrip())
            app.logger.error(msg)
            return render_template('error.html', msg=msg)
    else:
        raise ValueError("Argument [ mode ] should be {'debug', 'demo', ''}")


    return render_template('index.html',
                           month=current_month(),
                           hourly=stats_data(vnstat_hour, 'hours'),
                           daily=stats_data(vnstat_day, 'days'),
                           usage=current_usage(vnstat_month))


@app.route("/")
def index():
    return dashboard("")

@app.route("/demo")
def demo():
    return dashboard("demo")

@app.route("/debug")
def debug():
    return dashboard("debug")


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
