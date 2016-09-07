import datetime
import json
import subprocess
import pandas


def in_mb(number):
    return format(number / 1024, '.2f') + " MB"


def load_json_data():
    try:
        js = subprocess.check_output(["vnstat", "--json", "d"])
        return json.loads(js)
    except subprocess.CalledProcessError:
        print("Please check vnstat version >= 1.14")


def create_df(json_data):
    row_buffer = []
    for interface in json_data['interfaces']:
        for day_data in interface['traffic']['days']:
            d = dict()
            d['interface'] = interface['id']
            d['year'] = day_data['date']['year']
            d['month'] = day_data['date']['month']
            d['day'] = day_data['date']['day']
            d['in'] = day_data['rx']
            d['out'] = day_data['tx']
            row_buffer.append(d)
    return pandas.DataFrame(row_buffer)


def traffic_in_month(df, dt=datetime.datetime.now()):
    df['total'] = df['in'] + df['out']
    res = df[(df['year'] == dt.year) & (df['month'] == dt.month)]
    curr = sum(res['total']).item()
    return res[['year', 'month', 'day', 'total']], curr


def traffic_in_last_year(df):
    df['total'] = df['in'] + df['out']
    return df.groupby(['year', 'month'])['total'].sum().reset_index(name='traffic') \
        .sort_values(by=['year', 'month'], ascending=False).head(12)


def result_in_text(df):
    daily_trends, cur = traffic_in_month(df)
    monthly_trends = traffic_in_last_year(df)
    now = datetime.datetime.now()
    month = now.strftime("%B")
    return "Current Usage in " + month + ": " + str(cur) + "\n\n" + \
           "Daily Trends in " + month + ": \n" + daily_trends.to_string(index=False) + "\n\n" + \
           "Monthly Trends in " + str(now.year) + ": \n" + monthly_trends.to_string(index=False)
