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

    #dt = date_time("Asia/Bangkok")
    dt = '2025-12-17 02:17:31'
    date = dt.split(" ")[0]

    # for real time plot
    file = rf"C:\Users\User\Desktop\bot-payment-gateway-deposit-method-status-check\data_bot_{date}.xlsx"
    sheets = pd.ExcelFile(file).sheet_names
    sheet_data = {}

    #print("sheet_name:%s"%sheets)
    for sheet in sheets:
        #print("sheet_name:%s"%sheet)
        #if sheet != 'J8T':
        #    continue
        df = pd.read_excel(file,sheet_name=sheet)

        df["date_time"] = pd.to_datetime(df["date_time"]).astype(str)
        labels = df["date_time"].tolist()
        datasets = []
        colors = [
            "rgb(31, 119, 180)",   # blue
            "rgb(255, 127, 14)",   # orange
            "rgb(44, 160, 44)",    # green
            "rgb(214, 39, 40)",    # red
            "rgb(148, 103, 189)",  # purple
            "rgb(140, 86, 75)",    # brown
            "rgb(227, 119, 194)",  # pink
            "rgb(127, 127, 127)",  # gray
            "rgb(188, 189, 34)",   # olive
            "rgb(23, 190, 207)",   # cyan
        
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 206, 86)",
            "rgb(75, 192, 192)",
            "rgb(153, 102, 255)",
            "rgb(255, 159, 64)",
        
            "rgb(199, 199, 199)",
            "rgb(83, 102, 255)",
            "rgb(255, 102, 102)",
            "rgb(102, 255, 102)",
            "rgb(102, 102, 255)",
        
            "rgb(255, 204, 102)",
            "rgb(204, 102, 255)",
            "rgb(102, 204, 255)",
            "rgb(255, 102, 204)",
            "rgb(204, 255, 102)",
        
            "rgb(102, 255, 204)",
            "rgb(255, 153, 153)",
            "rgb(153, 255, 153)",
            "rgb(153, 153, 255)",
            "rgb(255, 204, 204)"
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
        print("Sheet data:%s"%sheet_data)
    
    # for overall plot
    file = rf"C:\Users\User\data_bot_daily_total.xlsx"
    sheets = pd.ExcelFile(file).sheet_names
    sheet_overall_data = {}

    #print("sheet_name:%s"%sheets)
    for sheet in sheets:
        #print("sheet_name:%s"%sheet)
        #if sheet != 'J8T':
        #    continue
        df = pd.read_excel(file,sheet_name=sheet)
        
        labels = []
        for col in df.columns:
            if col == "date":
                 continue
            labels.append(col)
        #print("Overall_labels:%s"%labels)

        datasets = []
        colors = [
            "rgb(31, 119, 180)",   # blue
            "rgb(255, 127, 14)",   # orange
            "rgb(44, 160, 44)",    # green
            "rgb(214, 39, 40)",    # red
            "rgb(148, 103, 189)",  # purple
            "rgb(140, 86, 75)",    # brown
            "rgb(227, 119, 194)",  # pink
            "rgb(127, 127, 127)",  # gray
            "rgb(188, 189, 34)",   # olive
            "rgb(23, 190, 207)",   # cyan
        
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 206, 86)",
            "rgb(75, 192, 192)",
            "rgb(153, 102, 255)",
            "rgb(255, 159, 64)",
        
            "rgb(199, 199, 199)",
            "rgb(83, 102, 255)",
            "rgb(255, 102, 102)",
            "rgb(102, 255, 102)",
            "rgb(102, 102, 255)",
        
            "rgb(255, 204, 102)",
            "rgb(204, 102, 255)",
            "rgb(102, 204, 255)",
            "rgb(255, 102, 204)",
            "rgb(204, 255, 102)",
        
            "rgb(102, 255, 204)",
            "rgb(255, 153, 153)",
            "rgb(153, 255, 153)",
            "rgb(153, 153, 255)",
            "rgb(255, 204, 204)"
        ]


        for i,date in enumerate(df["date"].items()):
            points = []
            date_str = date[1].strftime('%Y-%m-%d')
            #print("i:%s,date:%s,date_str:%s"%(i,date,date_str))
            for j, col in enumerate(df.columns):
                if col == "date":
                    continue
                print("j:%s,col:%s"%(j,col))
                for idx, val in df[col].items():
                    print("idx:%s, val:%s"%(idx,val))
                    if df.at[idx, "date"] in date:
                        points.append({
                                        "x": col,
                                        "y": [val],
                                    })
                    else:
                        continue
                    #print("overall_points:%s"%points)
            datasets.append({
                "label": date_str,
                "data": points,
                "backgroundColor": colors[i % len(colors)],
                "borderColor": colors[i % len(colors)],
                "tension": 0.3,
                "fill": True,
                "pointRadius": 5
            })
        sheet_overall_data[sheet] = {"labels": labels, "datasets": datasets}
        #print("overall_sheets_data:%s"%sheet_overall_data)

    return render_template(
                            'index.html',
                            sheet_data=sheet_data,
                            sheet_overall_data=sheet_overall_data
                        )
                            

if __name__ == "__main__":
    app.run(debug = True)

