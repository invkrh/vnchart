import json
import subprocess
import pandas


def in_mb(number):
    return format(number / 1024, '.2f') + " MB"


def load_json_data():
    js = subprocess.check_output(["vnstat", "--json", "d"])
    return json.loads(js)


def create_df(json_data):
    d = dict()
    df = pandas.DataFrame(columns=['interface', 'year', 'month', 'day', 'in', 'out'])
    for interface in json_data['interfaces']:
        for day_data in interface['traffic']['days']:
            d['interface'] = interface['id']
            d['year'] = day_data['date']['year']
            d['month'] = day_data['date']['month']
            d['day'] = day_data['date']['day']
            d['in'] = day_data['rx']
            d['out'] = day_data['tx']
            df = df.append([d])

    return df

# TODO
# def daily_traffic_in_current_month():
# def monthly_traffic_in_last_year():
