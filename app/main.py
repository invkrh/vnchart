from flask import Flask, render_template
from traffic import *

app = Flask(__name__)


@app.route("/")
def root():
    err_msg = "Please check vnstat version >= 1.14"
    try:
        data = load_json_data()
    except subprocess.CalledProcessError:
        print(err_msg)
        return err_msg
    df = create_df(data)
    daily, curr = traffic_in_month(df)
    monthly = traffic_in_last_year(df)
    print(daily)
    print(monthly)
    return render_template('traffic.html', daily=daily, monthly=monthly)


if __name__ == "__main__":
    app.run()
