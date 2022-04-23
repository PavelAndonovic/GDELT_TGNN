import gdelt
import pandas as pd
import datetime

if __name__ == '__main__':
    gd2 = gdelt.gdelt(version=1)

    # Single 15 minute interval pull, output to json format with mentions table
    for year in range(1979, 2015):
        start = datetime.datetime.now()
        base = datetime.datetime(year, 1, 1)
        date_list = [base + datetime.timedelta(days=x) for x in range(int(365.25*(2015-1979)))]
        if datetime.datetime(year+1, 1, 1) in date_list:
            date_list.pop(-1)
        #for date in date_list:
        date_list_ = [" ".join(str(date).split(" ")[0].split("-")) for date in date_list]
        results = gd2.Search(date_list_, table='events', output='csv')
        with open("..\\data\\temp_pull.csv", "w", encoding="utf-8") as f:
            f.write(results)
        temp = pd.read_csv("..\\data\\temp_pull.csv")
        temp = temp[["SQLDATE", "Actor1CountryCode", "Actor2CountryCode",
                     "QuadClass", "GoldsteinScale", "NumArticles", "AvgTone",
                     "Actor1Geo_Lat", "Actor2Geo_Lat", "Actor1Geo_Long", "Actor2Geo_Long"]]
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
        temp.to_csv("..\\data\\temp_pull.csv", encoding="utf-8", index=False)

        temp.to_csv(f"..\\data\\gdelt_data\\{year}_gdelt.csv")
        print(datetime.datetime.now()-start)




