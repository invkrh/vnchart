from flask import Flask
from traffic import *

app = Flask(__name__)


def page():
    data = load_json_data()
    df = create_df(data)
    return result_in_html(df)


@app.route("/")
def root():
    return page()


if __name__ == "__main__":
    app.run()
