from flask import Flask
from traffic import *

app = Flask(__name__)


@app.route("/")
def root():
    data = load_json_data()
    df = create_df(data)
    daily_trends, cur = traffic_in_current_month(df)
    monthly_trends = traffic_in_last_year(df)
    now = datetime.datetime.now()
    month = now.strftime("%B")
    return "Current Usage in " + month + ": " + cur + "\n\n" + \
           "Daily Trends in " + month + ": \n" + daily_trends + "\n\n" + \
           "Monthly Trends in " + now.year + ": \n" + monthly_trends + ""


if __name__ == "__main__":
    app.run()
