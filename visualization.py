import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

pairs = [("T1","T2"),("T1","T2_2"),("T3","T4")]

def read_csv(candidate_name):
    data = pd.read_csv("./data/"+candidate_name+".csv", index_col=None)
    return data

def merge_both_candidate(df1, df2):
    df1 = df1.rename(columns={'Latitude': 'lat1', 'Longitude': 'lon1'})
    df2 = df2.rename(columns={'Latitude': 'lat2', 'Longitude': 'lon2'})
    return pd.merge(df1, df2, on='Time (s)')

def render(data, pair):
    fig, ax = plt.subplots()

    lat1 = data['lat1']
    lat2 = data['lat2']
    lon1 = data['lon1']
    lon2 = data['lon2']
    
    ax.legend()

    def update(frame):
        ax.scatter(lon1[0:frame], lat1[0:frame], color='red', label='1')
        ax.scatter(lon2[0:frame], lat2[0:frame], color='blue', label='2')

        ax.plot(lon1[0:frame], lat1[0:frame], color='red')
        ax.plot(lon2[0:frame], lat2[0:frame], color='blue')
        
        ax.set_title("Pair:"+str(pair)+"\nFrame:"+str(frame))

    ani = FuncAnimation(fig, update, frames=len(data), interval=100, repeat=False)

    plt.show()

def calculate_leading(data, pair):
    lat1 = data['lat1'].tolist()
    lat2 = data['lat2'].tolist()
    lon1 = data['lon1'].tolist()
    lon2 = data['lon2'].tolist()

    v1 = (lat1[-1] - lat1[0], lon1[-1] - lon1[0])
    v2 = (lat2[-1] - lat2[0], lon2[-1] - lon2[0])

    if np.cross(v1, v2)>0:
        print(pair[0]+" is leading")
        print(pair[1]+" is following")
    else:
        print(pair[1]+" is leading")
        print(pair[0]+" is following")


for pair in pairs:
    candidate1 = pair[0]
    candidate2 = pair[1]
    data1 = read_csv(candidate1)
    data2 = read_csv(candidate2)
    data = merge_both_candidate(data1, data2)
    # render(data, pair)
    calculate_leading(data, pair)
    # break


