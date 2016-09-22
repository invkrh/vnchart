import logging
import json
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

import pandas
from flask import Flask, render_template

app = Flask(__name__)


class TrafficStat:

    def __init__(self, raw_hour, raw_day):
        # TODO: vnstat version check
        self.hour_df = self.create_data_frame(raw_hour, 'hours')
        self.day_df = self.create_data_frame(raw_day, 'days')

    def vnstat(self, basis, fmt='json'):
        """Call vnstat cmd in a subprocess

        basis:
        'h' => last 24 hours
        'd' => last 30 days
        'm' => last 12 months

        fmt: 'json' or 'xml'
        """
        assert basis == 'h' or basis == 'd'
        assert fmt == 'xml' or fmt == 'json'
        stat = subprocess.check_output(["vnstat", '--' + fmt, basis])
        return json.loads(stat)

    def stat_by_hour(self):
        return self.indexed_stat(self.hour_df)

    def stat_by_day(self):
        return self.indexed_stat(self.day_df)

    def current_usage(self):
        # TODO: filter day in current month
        return 100

    @staticmethod
    def to_mb(x):
        return "%.2f" % (x / 1024.0)

    @staticmethod
    def indexed_stat(df):
        data = df[['id', 'traffic']]
        data.columns = ['xValues', 'yValues']
        res = data.to_dict(orient='list')
        res['yValues'] = res['yValues'][::-1]
        return res

    @staticmethod
    def create_data_frame(vnstat, basis):
        row_buffer = []
        for ifc in vnstat['interfaces']:
            for elem in ifc['traffic'][basis]:
                row_buffer.append({
                    'if': ifc['id'],
                    'id': elem['id'],
                    'year': elem['date']['year'],
                    'month': elem['date']['month'],
                    'day': elem['date']['day'],
                    'total': elem['rx'] + elem['tx'],
                })
        keys = ['id', 'year', 'month', 'day']
        df = pandas.DataFrame(row_buffer) \
            .groupby(keys)['total'].sum() \
            .reset_index(name='traffic') \
            .sort_values(by=keys)
        df['id'] = df['id'].apply(float)
        df['traffic'] = df['traffic'].apply(TrafficStat.to_mb)
        return df


@app.route("/")
def root():

    # vnstat_hour = ts.stat('h')
    # vnstat_day = ts.stat('d')

    with open('tests/hour.json') as data_file:
        vnstat_hour = json.load(data_file)
    with open('tests/day.json') as data_file:
        vnstat_day = json.load(data_file)

    ts = TrafficStat(vnstat_hour, vnstat_day)
    return render_template('index.html',
                           hourly=ts.stat_by_hour(),
                           daily=ts.stat_by_day(),
                           usage=ts.current_usage())

    # try:
    #     data = get_vnstat_data()
    # except subprocess.CalledProcessError as err:
    #     msg = 'Run command [{}] with error [{}]'.format(
    #               ' '.join(err.cmd), err.output.decode("utf-8").rstrip())
    #     app.logger.error(msg)
    #     return msg

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
