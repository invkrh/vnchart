import logging
import json
import pytz
import subprocess

from datetime import datetime, timedelta
from flask import Flask, render_template
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

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


def stats_data(vnstat_dict, unit_key):
    def hour_key(date_elem):
        dt = date_elem['date']  # id is hour
        return datetime(year=dt['year'], month=dt['month'], day=dt['day'],
                        hour=date_elem['id'], tzinfo=pytz.UTC)

    def day_key(date_elem):
        dt = date_elem['date']
        return datetime(year=dt['year'], month=dt['month'], day=dt['day'],
                        tzinfo=pytz.UTC)

    if unit_key == 'hours':
        key_by = hour_key
        # def key_inc(dt):
            # give more space for the last bar on chart
            # return dt + timedelta(hours=1)
    elif unit_key == 'days':
        key_by = day_key
        # def key_inc(dt):
            # no space needed for day chart
            # return dt
    else:
        raise ValueError("Argument [ unit_key ] should be {'hours', 'days'}")

    datasets = []
    labels = None
    for ifc in vnstat_dict['interfaces']:
        if_id = ifc['id']

        # Start from the most recent
        traffic = sorted([(key_by(elem), kb_to_mb(elem['rx']), kb_to_mb(elem['tx']))
                          for elem in ifc['traffic'][unit_key]], key=lambda k: k[0])

        if not labels:
            labels = [x[0] for x in traffic]
            # labels.append(key_inc(labels[-1]))

        rx = [(x[1]) for x in traffic]
        dataset_in = {
            "label": if_id + '-in',
            'transfer': rx
        }

        tx = [(x[2]) for x in traffic]
        dataset_out = {
            "label": if_id + '-out',
            'transfer': tx
        }

        if any(float(v) != 0 for v in rx) or any(float(v) != 0 for v in tx):
            datasets.append(dataset_in)
            datasets.append(dataset_out)

    return {"labels": labels, "datasets": datasets}


def kb_to_mb(num):
    return "%.2f" % (num / 1024.0)


def month_name():
    date = datetime.now()
    return date.strftime("%B")


def last_month_name():
    first = datetime.now().replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month.strftime("%B")


def last_two_month_trans(vnstat_dict):
    curr_trans = 0
    last_trans = 0
    for ifc in vnstat_dict['interfaces']:
        curr = ifc['traffic']['months'][0]
        curr_trans += curr["rx"] + curr["tx"]
        if len(ifc['traffic']['months']) >= 2:
            last = ifc['traffic']['months'][1]
            last_trans += last["rx"] + last["tx"]
    return {
        'curr': kb_to_mb(curr_trans),
        'last': None if last_trans == 0 else kb_to_mb(last_trans)
    }


def read_json(json_file):
    with open(json_file) as data_file:
        return json.load(data_file)


def error_page(err_msg):
    app.logger.error(err_msg)
    return render_template('error.html', msg=err_msg)


def dashboard(mode):
    if mode:
        # Debug on server without vnstat >= 1.14
        try:
            import os
            data_dir = os.path.dirname(__file__) + "/../data"
            vnstat_hour = read_json(data_dir + '/' + mode + '/hour.json')
            vnstat_day = read_json(data_dir + '/' + mode + '/day.json')
            vnstat_month = read_json(data_dir + '/' + mode + '/month.json')
        except IOError as err:
            return error_page(err)
    else:
        try:
            vnstat_hour = vnstat('h')
            vnstat_day = vnstat('d')
            vnstat_month = vnstat('m')
        except subprocess.CalledProcessError as err:
            msg = 'Command [ {} ] ends with [ {} ]'.format(
                ' '.join(err.cmd), err.output.decode("utf-8").rstrip())
            return error_page(msg)

    return render_template('index.html',
                           month=month_name(),
                           last_month=last_month_name(),
                           hourly=stats_data(vnstat_hour, 'hours'),
                           daily=stats_data(vnstat_day, 'days'),
                           usage=last_two_month_trans(vnstat_month))


@app.route("/")
def index():
    return dashboard(None)


@app.route("/demo")
def demo():
    return dashboard("demo")


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
