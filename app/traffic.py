import datetime
import json
import subprocess
import pandas


def prec(number, p=2):
    return format(number, '.{}f'.format(p))


def to_mb_str(number):
    return prec(number / 1024.0)


def to_mb_int(number):
    return float(to_mb_str(number))


def load_json_data():
    js = subprocess.check_output(["vnstat", "--json", "d"])
    return json.loads(js)


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
    filtered = df[(df['year'] == dt.year) & (df['month'] == dt.month)]
    res = filtered.groupby(['year', 'month', 'day'])['total'].sum() \
        .reset_index(name='traffic (MB)') \
        .sort_values(by=['year', 'month', 'day'], ascending=False)
    res['traffic (MB)'] = res['traffic (MB)'].apply(lambda x: to_mb_int(x))
    curr = sum(res['traffic (MB)']).item()
    return res, prec(curr)


def traffic_in_last_year(df):
    df['total'] = df['in'] + df['out']
    res = df.groupby(['year', 'month'])['total'].sum() \
        .reset_index(name='traffic (MB)') \
        .sort_values(by=['year', 'month'], ascending=False) \
        .head(12)
    res['traffic (MB)'] = res['traffic (MB)'].apply(lambda x: to_mb_int(x))
    return res


def result_in_html(df):
    daily_trends, cur = traffic_in_month(df)
    monthly_trends = traffic_in_last_year(df)
    now = datetime.datetime.now()
    month = now.strftime("%B")
    return "Current Usage in " + month + ": " + cur + " MB<br/><br/>" + \
           "Daily Trends in " + month + ": \n" + \
           daily_trends.to_html(index=False) + "<br/><br/>" + \
           "Monthly Trends in " + str(now.year) + ": \n" + \
           monthly_trends.to_html(index=False)
