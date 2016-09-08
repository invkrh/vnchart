from flask import Flask
from traffic import *

app = Flask(__name__)


def page():
    err_msg = "Please check vnstat version >= 1.14"
    try:
        data = load_json_data()
    except subprocess.CalledProcessError:
        print(err_msg)
        return err_msg
    df = create_df(data)
    return result_in_html(df)


@app.route("/")
def root():
    return page()


if __name__ == "__main__":
    app.run()
