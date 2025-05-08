import csv
from datetime import datetime 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import numpy as np 



def playback_data(played_file: str, animation_file_name: str ):

    column_names = ['X_val', 'Y_val', 'CoF_val', 'time']
    data = pd.read_csv(played_file, header=None, names=column_names)

    data['time'] = pd.to_datetime(data['time'])
    data.sort_values('time', inplace=True)
    fig, ax = plt.subplots()

    def update(num):
        ax.clear()
        ax.scatter(data['Y_val'].iloc[:num], data['X_val'].iloc[:num], c=data['CoF_val'].iloc[:num], cmap='gray_r', vmin=0, vmax=1)
        ax.set_ylim([data['Y_val'].min(), data['Y_val'].max()])
        ax.set_xlim([data['X_val'].min(), data['X_val'].max()])
        plt.gca().set_title('Time: {}'.format(data['time'].iloc[num]))

    ani = FuncAnimation(fig, update, frames=range(len(data)), repeat=False)
    ani.save(animation_file_name, writer='pillow')
    plt.show()



def playback_data_grayscale(played_file: str, animation_file_name: str):

    column_names = ['X_val', 'Y_val', 'CoF_val', 'time']
    data = pd.read_csv(played_file, header=None, names=column_names)
    data['time'] = pd.to_datetime(data['time'])
    data.sort_values('time', inplace=True)
    fig, ax = plt.subplots()

    grid_size_x = data['X_val'].max() + 1
    grid_size_y = data['Y_val'].max() + 1

    def update(num):
        ax.clear()
        grid = np.zeros((grid_size_x, grid_size_y))
        for i in range(num):
            x = data['X_val'].iloc[i]
            y = data['Y_val'].iloc[i]
            CoF = data['CoF_val'].iloc[i]
            grid[x, y] = CoF
        # Rotate grid 90 degrees clockwise
        grid = np.fliplr(grid.T)
        ax.imshow(grid, cmap='gray_r', vmin=0, vmax=1, origin='lower')
        plt.gca().set_title('Time: {}'.format(data['time'].iloc[num]))

    ani = FuncAnimation(fig, update, frames=range(len(data)), repeat=False)
    ani.save(animation_file_name, writer='ffmpeg')
    plt.show()





def record_data(file_path: str):

    with open(file_path,"a+",newline='') as file:

        file_writer = csv.writer(file)
        file_writer.writerow(["CoF_Type" ,"X_val" ,"Y_val","CoF_val" ,"time" ])

        i = 0 
        while i <= 1000:
            i += 1 

            CoF_Type = str(input("CoF Type:\n"))
            X_val = str(input("x value:\n"))
            Y_val = str(input("y value:\n"))
            CoF_val = str(input("CoF value:\n"))
            time = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

            written_line = [CoF_Type, X_val , Y_val, CoF_val, time]

            file_writer.writerow(written_line)
            print(str(written_line))


def main():
    written_file_path: str = 'test.csv'
    record_data(written_file_path)

    # saved_file_name: str = 'colorized_cof.gif'
    # played_file_path: str = 'data_collection_3.csv'
    # playback_data_grayscale(played_file_path,saved_file_name)

if __name__ == '__main__':
    main()