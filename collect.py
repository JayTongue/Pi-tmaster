import requests
from datetime import date, datetime
import time

from graph import make_graph


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
    filename = f'{current_date.strftime("%Y-%m-%d")}'
    open(f'{filename}.txt', 'a')
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
    with open(f'{filename}.txt', 'a') as data_file:
        print(datapoint, file=data_file)


if __name__ == '__main__':
    thermometer_main()
