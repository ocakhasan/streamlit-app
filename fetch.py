import requests
import pandas as pd
import numpy as np
from datetime import datetime

def change_date(date):
    d = date.split('.')
    return d[2] + "-" + d[1] + "-" + d[0]

def change_num(data):
    data = data.replace('.', '')
    return int(data)

def get_latest_data():

    response = requests.get("https://covid19.saglik.gov.tr/covid19api?getir=sondurum")
    print("\nconnected to website\n")

    last_day = list(response.json())[0]
    confirmed = change_num(last_day['toplam_vaka'])
    recovered = change_num(last_day['toplam_iyilesen'])

    deaths = change_num(last_day['toplam_vefat'])
    tests = change_num(last_day["gunluk_test"])
    date = change_date(last_day["tarih"])

    new_row = {"Country/Region": "Turkey", "Latitude": 38.9637, "Longitude": 35.2433, "Confirmed":confirmed, "Recovered": recovered, "Deaths": deaths, "Date": date, "Tests": tests}

    df = pd.read_csv("turkey_covid19_all.csv")
    if date != df["Date"].values[-1]:
        df = df.append(new_row, ignore_index=True)
        df.to_csv("turkey_covid19_all.csv", index=False)

        print("Created new data for {}\n".format(date))
        print("New dataset is created")
    else:
        print("Dataset is up to date")


if __name__ == "__main__":
    get_latest_data()