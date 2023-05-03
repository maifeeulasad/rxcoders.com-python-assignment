import pandas as pd
import numpy as np

pairs = [("T1","T2"),("T1","T2_2"),("T3","T4")]

def read_csv(candidate_name):
    data = pd.read_csv("./data/"+candidate_name+".csv", index_col=None)
    return data

def merge_both_candidate(df1, df2):
    df1 = df1.rename(columns={'Latitude': 'lat1', 'Longitude': 'lon1'})
    df2 = df2.rename(columns={'Latitude': 'lat2', 'Longitude': 'lon2'})
    return pd.merge(df1, df2, on='Time (s)')

def calculate_ttc(data, pair):
    times = data['Time (s)'].tolist()

    lat1 = data['lat1'].tolist()
    lon1 = data['lon1'].tolist()

    lat2 = data['lat2'].tolist()
    lon2 = data['lon2'].tolist()

    x11 = np.cos(lat1[0]) * np.cos(lon1[0])
    y11 = np.cos(lat1[0]) * np.sin(lon1[0])

    x12 = np.cos(lat1[-1]) * np.cos(lon1[-1])
    y12 = np.cos(lat1[-1]) * np.sin(lon1[-1])

    x21 = np.cos(lat2[0]) * np.cos(lon2[0])
    y21 = np.cos(lat2[0]) * np.sin(lon2[0])

    x22 = np.cos(lat2[-1]) * np.cos(lon2[-1])
    y22 = np.cos(lat2[-1]) * np.sin(lon2[-1])

    dist1 = np.sqrt(np.square(x11-x12)+np.square(y11-y12))
    dist2 = np.sqrt(np.square(x21-x22)+np.square(y21-y22))

    time1 = times[0]
    time2 = times[-1]
    diff_time = time2 - time1

    vel1 = dist1 / diff_time
    vel2 = dist2 / diff_time

    dist = np.sqrt(np.square(x12-x22)+np.square(y21-y22))

    return (dist) / np.abs(vel1 - vel2)


for pair in pairs:
    candidate1 = pair[0]
    candidate2 = pair[1]
    data1 = read_csv(candidate1)
    data2 = read_csv(candidate2)
    data = merge_both_candidate(data1, data2)
    # render(data, pair)
    ttc = calculate_ttc(data, pair)
    print("for pair",str(pair)+", ttc: ",ttc)


