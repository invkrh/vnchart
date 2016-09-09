from datetime import datetime
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


def fill_zero(a_list, max_len):
    return a_list + [None] * (max_len - len(a_list))


def day_num_in_month(dt):
    import calendar
    return calendar.monthrange(dt.year, dt.month)[1]


def traffic_in_month(df, dt=datetime.now()):
    df['total'] = df['in'] + df['out']
    filtered = df[(df['year'] == dt.year) & (df['month'] == dt.month)]
    grouped = filtered.groupby(['year', 'month', 'day'])['total'].sum() \
        .reset_index(name='traffic') \
        .sort_values(by=['year', 'month', 'day'])
    grouped['traffic'] = grouped['traffic'].apply(lambda x: to_mb_int(x))

    sel = grouped[['day', 'traffic']]
    sel.columns = ['xValues', 'yValues']
    data = sel.to_dict(orient='list')

    max_num = day_num_in_month(dt)
    data['xValues'] = list(range(1, max_num + 1))
    data['yValues'] = fill_zero(data['yValues'], max_num)
    curr = sum(grouped['traffic']).item()
    return data, prec(curr)


def year_month(dt):
    return dt.year, dt.month


def last_year_months():
    import dateutil.relativedelta
    dt = datetime.now()
    return [year_month(dt - dateutil.relativedelta.relativedelta(months=x))
            for x in range(0, 12)]


def traffic_in_last_year(df):
    df['total'] = df['in'] + df['out']
    grouped = df.groupby(['year', 'month'])['total'].sum() \
        .reset_index(name='traffic') \
        .sort_values(by=['year', 'month']) \
        .head(12)
    grouped['traffic'] = grouped['traffic'].apply(lambda x: to_mb_int(x))

    d = grouped.to_dict(orient='list')
    tf_dict = dict(zip(zip(d['year'], d['month']), d['traffic']))
    keys = last_year_months()
    data = dict()
    data['xValues'] = [str(year) + "/" + str(month) for year, month in keys][::-1]
    data['yValues'] = [tf_dict.get((year, month), None) for year, month in keys][::-1]
    return data


def result_in_html(df):
    daily_trends, cur = traffic_in_month(df)
    monthly_trends = traffic_in_last_year(df)
    now = datetime.datetime.now()
    month = now.strftime("%B")
    return "Current Usage in " + month + ": " + cur + " MB<br/><br/>" + \
           "Daily Trends in " + month + ": \n" + \
           daily_trends.to_html(index=False) + "<br/><br/>" + \
           "Monthly Trends in the last 12 month" + ": \n" + \
           monthly_trends.to_html(index=False)
