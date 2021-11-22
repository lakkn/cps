import pandas as pd
import sqlite3 as sql

def scrape():
    try:
        url = "http://scoreboard.uscyberpatriot.org/"

        df = pd.read_html(url)
        x = df[0]
        x.columns = x.iloc[0]
        x = x[1:]
        x.columns = x.columns.fillna('qdrop')
        x = x.drop(x.columns[[0]], axis=1)

        conn = sql.connect('database.db')
        x.to_sql('info',conn)
    except:
        print("no tables")
