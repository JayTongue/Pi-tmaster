import requests
from datetime import date, datetime
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ast


def thermometer_main():
    filename = setup_files()
    try:
        while True:
            datapoint = collect_data()
            save_data(datapoint, filename)
            time.sleep(20)

    except KeyboardInterrupt:
        plt = make_graph(filename)
        plt.show()
        jpeg_filename = f"{filename}.jpeg"
        plt.savefig(jpeg_filename, format='jpeg')


def setup_files():
    current_date = date.today()
    filename = f'{current_date.strftime("%Y-%m-%d")}.txt'
    open(filename, 'a')
    return filename


def collect_data():
    thermometer_api = "http://192.168.1.1"
    response = requests.get(thermometer_api)
    datapoint = dict(response.json())
    datapoint['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datapoint = f'{datapoint}, '
    print(datapoint)
    return datapoint


def save_data(datapoint, filename):
    with open(filename, 'a') as file:
        print(datapoint, file=file)


def make_graph(filename):
    with open(filename, 'r') as file:
        file_contents = file.read()

    finished_data = ast.literal_eval(f"[{file_contents.strip().rstrip(',')}]")
    finished_data = pd.DataFrame(finished_data)
    finished_data['time'] = pd.to_datetime(finished_data['time'])

    plt.plot(finished_data['time'], finished_data['fire'], label='Fire', color='blue', linestyle='-')
    plt.plot(finished_data['time'], finished_data['meat'], label='Meat', color='black')
    plt.axhspan(225, 275, color='green', alpha=0.3)
    plt.xlabel('Time')
    plt.ylabel('Temperature (F)')
    plt.xticks(rotation=90)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.title(f'{filename} Cook')
    plt.legend()
    return plt


if __name__ == '__main__':
    thermometer_main()
