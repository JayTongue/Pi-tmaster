import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ast


def make_graph(filename):
    with open(f'{filename}.txt', 'r') as file:
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
    plt.title(f'{filename} Temperatures')
    plt.legend()
    return plt


if __name__ == '__main__':
    plt = make_graph('INSERT DATE')  # YYYY-MM-DD
    plt.show()