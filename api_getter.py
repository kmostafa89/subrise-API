import numpy as np
import pandas as pd
import requests

from datetime import datetime as dt
from matplotlib import pyplot as plt
import seaborn as sns


lat = "48.1625424"
lon = "11.598604"

raw_api = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}"

proxies = {
    "https": "httpproxy.munich.munichre.com:3128",
    "http": "httpproxy.munich.munichre.com:3128"
}

response = requests.get(raw_api, proxies=proxies)
resp = response.json()


data = pd.DataFrame(resp)
todays_results = data.T.loc["results"]


today = dt.now().strftime("%d/%m/%Y")

todays_results.loc["Date"] = today


# data_ = pd.DataFrame(columns = ['astronomical_twilight_begin', 'astronomical_twilight_end',
#        'civil_twilight_begin', 'civil_twilight_end', 'day_length',
#        'nautical_twilight_begin', 'nautical_twilight_end', 'solar_noon',
#        'sunrise', 'sunset', 'Date'])


data_ = pd.read_csv("./historical sunrise.csv")
data_.drop(data_.columns[data_.columns.str.contains(
    "Unnamed: 0")], 1, inplace=True)


data_ = data_.append(todays_results)

data_.drop_duplicates(inplace=True)


data_.day_length = pd.to_timedelta(data_.day_length)

data_.day_length = data_.day_length / np.timedelta64(1, 'h')

sns.barplot(data_.Date, data_.day_length, palette='rocket')
plt.xticks(rotation=40)
plt.title("Day Lenght by date")
plt.xlabel("Date")
plt.ylabel("Lenght")

plt.show()


data_.to_csv("./historical sunrise.csv")
