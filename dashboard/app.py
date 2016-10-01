import errno
import logging
import json
import subprocess
import os

from datetime import datetime, timedelta
from flask import Flask, render_template
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from tzlocal import get_localzone

app = Flask(__name__)

curr_dir = os.path.dirname(__file__)
data_dir = curr_dir + "/../data"
log_dir = curr_dir + "/../logs"

# Setup logging
try:
    os.makedirs(log_dir)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

handler = TimedRotatingFileHandler(log_dir + '/vnchart.log',
                                   when="H",
                                   interval=1,
                                   backupCount=24)
handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(module)s:%(lineno)d]'
))
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


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
    return json.loads(stat.decode("utf-8"))


def stats_data(vnstat_dict, unit_key):
    tz = get_localzone()

    def hour_key(date_elem):
        date = date_elem['date']
        return tz.localize(
            datetime(
                year=date['year'],
                month=date['month'],
                day=date['day'],
                hour=date_elem['id']),
            is_dst=None)  # id is hour

    def day_key(date_elem):
        date = date_elem['date']
        return tz.localize(
            datetime(
                year=date['year'],
                month=date['month'],
                day=date['day']),
            is_dst=None)

    if unit_key == 'hours':
        key_by = hour_key

        def key_inc(dt_key):
            return dt_key + timedelta(hours=1)
    elif unit_key == 'days':
        key_by = day_key

        def key_inc(dt_key):
            return dt_key + timedelta(days=1)
    else:
        raise ValueError("Argument [ unit_key ] should be {'hours', 'days'}")

    datasets = []
    labels = None

    for ifc in vnstat_dict['interfaces']:
        if_id = ifc['id']

        # start from the most recent
        traffic = sorted([(key_by(elem), kb_to_mb(elem['rx']), kb_to_mb(elem['tx']))
                          for elem in ifc['traffic'][unit_key]], key=lambda k: k[0])

        # only init labels once
        if not labels:
            dt_list = [x[0] for x in traffic]
            # add one more tick for the last bar on chart
            dt_list.append(key_inc(dt_list[-1]))
            labels = [str(dt) for dt in dt_list]

        # create received data list
        rx_list = [(x[1]) for x in traffic]
        dataset_in = {
            "label": if_id + '-in',
            'transfer': rx_list
        }

        # create sent data list
        tx_list = [(x[2]) for x in traffic]
        dataset_out = {
            "label": if_id + '-out',
            'transfer': tx_list
        }

        # filter zero values
        if any(float(v) != 0 for v in rx_list) or any(float(v) != 0 for v in tx_list):
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
        # compute last month's data only when exists
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
    return render_template('error.html', msg=err_msg)


def dashboard(mode):
    if mode == 'demo':
        # for servers without vnstat >= 1.14
        # using generated json
        try:

            vnstat_hour = read_json(data_dir + '/demo/hour.json')
            vnstat_day = read_json(data_dir + '/demo/day.json')
            vnstat_month = read_json(data_dir + '/demo/month.json')
        except IOError as err:
            return error_page(err)
    elif mode == '':
        try:
            vnstat_hour = vnstat('h')
            vnstat_day = vnstat('d')
            vnstat_month = vnstat('m')
        except subprocess.CalledProcessError as err:
            msg = 'Command [ {} ] ends with [ {} ]'.format(
                ' '.join(err.cmd), err.output.decode("utf-8").rstrip())
            return error_page(msg)
    else:
        raise ValueError("Argument [ mode ] should be {'demo', ''}")

    return render_template('index.html',
                           month=month_name(),
                           last_month=last_month_name(),
                           hourly=stats_data(vnstat_hour, 'hours'),
                           daily=stats_data(vnstat_day, 'days'),
                           usage=last_two_month_trans(vnstat_month))


@app.route("/")
def index():
    return dashboard("")


@app.route("/demo")
def demo():
    return dashboard("demo")


if __name__ == "__main__":
    app.run()
