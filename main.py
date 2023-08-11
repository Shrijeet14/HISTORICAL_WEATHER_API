import pandas as pd
from flask import Flask , render_template

app = Flask("__name__")

stations=pd.read_csv("D:\PLACEMENTS\PYTHON\course\PROJECTS\PROJECT6_HISTORICAL_WEATHER\data_small\stations.txt",skiprows=17)
stations=stations[["STAID","STANAME                                 "]]

@app.route("/")
def Home():
    return render_template("home.html",data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def station(station , date):
    filename= "D:\PLACEMENTS\PYTHON\course\PROJECTS\PROJECT6_HISTORICAL_WEATHER\data_small\TG_STAID"+str(station).zfill(6)+".txt"

    df=pd.read_csv(filename,skiprows=20,parse_dates=["    DATE"])
    df["TG"]=df["   TG"]/10
    temperature=df[df["    DATE"]==date]["TG"].squeeze()
    return {
        'Station' : station,
        'Date'   : date,
        'temperature' : temperature
    }

@app.route("/api/v1/<station>")
def only_station(station):
    filename= "D:\PLACEMENTS\PYTHON\course\PROJECTS\PROJECT6_HISTORICAL_WEATHER\data_small\TG_STAID"+str(station).zfill(6)+".txt"
    df=pd.read_csv(filename,skiprows=20,parse_dates=["    DATE"])
    df["TG"]=df["   TG"]/10
    all=df[["    DATE","TG"]]
    all=all.to_dict(orient='records')
    return all




@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station,year):
    filename= "D:\PLACEMENTS\PYTHON\course\PROJECTS\PROJECT6_HISTORICAL_WEATHER\data_small\TG_STAID"+str(station).zfill(6)+".txt"
    df=pd.read_csv(filename,skiprows=20,parse_dates=["    DATE"])
    df["    DATE"]=df["    DATE"].astype(str)
    result= df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")

    return result




if(__name__=="__main__"):
    app.run(debug=True)