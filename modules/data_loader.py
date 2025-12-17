import pandas as pd

def load_data():
    data = pd.read_csv("data/data_asia.csv")
    return data