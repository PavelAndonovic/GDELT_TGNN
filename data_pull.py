import gdelt
import pandas as pd
import datetime

if __name__ == '__main__':
    gd2 = gdelt.gdelt(version=2)

    # Single 15 minute interval pull, output to json format with mentions table
    start = datetime.datetime.now()
    date_to_search = "2016/11/01"
    results = gd2.Search(date_to_search, table='events', output='csv')
    with open("temp_pull.csv", "w", encoding="utf-8") as f:
        f.write(results)
    temp = pd.read_csv("temp_pull.csv")
    temp = temp[["SQLDATE", "Actor1CountryCode", "Actor2CountryCode",
                 "QuadClass", "GoldsteinScale", "NumArticles", "AvgTone",
                 "Actor1Geo_Lat", "Actor2Geo_Lat", "Actor1Geo_Long", "Actor2Geo_Long"]]
    print("".join(date_to_search.split("/")))
    temp = temp[temp["SQLDATE"] == int("".join(date_to_search.split("/")))]

    temp.dropna(subset=['Actor1CountryCode'], how='all', inplace=True)
    temp.dropna(subset=['Actor2CountryCode'], how='all', inplace=True)
    temp['NumberOfRowsBetweenCountries'] = 1
    temp['AlternateGoldsteinScale'] = temp.apply(lambda x: x.GoldsteinScale * x.NumArticles, axis=1)

    temp = temp.groupby(["Actor1CountryCode", "Actor2CountryCode"]).agg(
        {"Actor1CountryCode": "max", "Actor2CountryCode": "max", "AlternateGoldsteinScale": "sum",
         "SQLDATE": "max", "QuadClass": "max", "GoldsteinScale": "mean", "NumArticles": "sum",
         "AvgTone": "mean", "Actor1Geo_Lat": "mean", "Actor2Geo_Lat": "mean",
         "Actor1Geo_Long": "mean", "Actor2Geo_Long": "mean", 'NumberOfRowsBetweenCountries': "sum"})
    temp['AlternateGoldsteinScale'] = temp.apply(lambda x: x.AlternateGoldsteinScale / x.NumArticles, axis=1)

    temp.to_csv("temp_pull.csv", encoding="utf-8", index=False)
    print(datetime.datetime.now()-start)




