from flask import Flask, render_template
from datetime import datetime, timedelta
import pytz
import pandas as pd

app = Flask(__name__)

def date_time(country):
    current_date_time = pytz.timezone(country)
    time = datetime.now(current_date_time)
    #print("Current time in %s:"%country, time.strftime('%Y-%m-%d %H:%M:%S'))
    return time.strftime('%Y-%m-%d %H:%M:%S')

@app.route("/")
def index():

    dt = date_time("Asia/Bangkok")
    date = dt.split(" ")[0]

    file = rf"C:\Users\User\Desktop\bot-payment-gateway-deposit-method-status-check\data_bot_{date}.xlsx"
    sheets = pd.ExcelFile(file).sheet_names
    sheet_data = {}

    print("sheet_name:%s"%sheets)
    for sheet in sheets:
        print("sheet_name:%s"%sheet)
        #if sheet != 'S345T':
        #    break
        df = pd.read_excel(file,sheet_name=sheet)

        df["date_time"] = pd.to_datetime(df["date_time"]).astype(str)
        labels = df["date_time"].tolist()
        datasets = []
        colors = [
        "rgb(75, 192, 192)",
        "rgb(255, 99, 132)",
        "rgb(54, 162, 235)",
        "rgb(255, 205, 86)"
        ]

        #print(labels)

        for i, col in enumerate(df.columns):
            points = []
            if col == "date_time":
                continue
            #print(col)
            for idx, val in df[col].items():
                #print("idx:%s, val:%s"%(idx,val))
                if val == 1:
                    points.append({
                                    "x": i,
                                    "y": df.at[idx, "date_time"]
                                })
                #print("points:%s"%points)
            datasets.append({
            "label": col,
            "data": points,
            "backgroundColor": colors[i % len(colors)],
            "borderColor": colors[i % len(colors)],
            "tension": 0.3,
            "fill": True,
            "pointRadius": 5
            })
            #print(datasets)
        #break
        sheet_data[sheet] = {"labels": labels, "datasets": datasets}
        #print(sheet_data)

    return render_template(
                            'index.html',
                            sheet_data=sheet_data
                        )
                            

if __name__ == "__main__":
    app.run(debug = True)

