import sys

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import csv
import random

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # canvas setup
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        #toolbar setup
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):

        # clear figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(x, y1, 'b' + pattern, ms = markersize)
        handle_tab = [mpatches.Patch(color='b', label=y1_t)]
        if y2_t != None:
            ax.plot(x, y2, 'r' + pattern, ms = markersize)
            handle_tab.append(mpatches.Patch(color='r', label=y2_t))
        if y3_t != None:
            ax.plot(x, y3, 'y' + pattern, ms = markersize)
            handle_tab.append(mpatches.Patch(color='y', label=y3_t))
        if y4_t != None:
            ax.plot(x, y4, 'm' + pattern, ms = markersize)
            handle_tab.append(mpatches.Patch(color='m', label=y4_t))
        
        ax.set_title(title.replace('_', ' ')[:-4])
        ax.set_xlabel(x_t)
        ax.legend(handles=handle_tab)
        ax.grid(True)
        
        # refresh canvas
        self.canvas.draw()


title = input("Enter filename (default: 'chart.csv'): ")
if title == '':
    title = 'chart.csv'
delimiter = input("Enter delimiter (default: ','): ")
if delimiter == '':
    delimiter = ','
pattern= input("Enter line pattern (default: '.-'): ")
if pattern == '':
    pattern = '.-'
try:
    markersize= int(input("Enter marker size (default: 10): "))
except:
    markersize = 10
if markersize == '':
    markersize = 10
x = []
y1 = []
y2 = []
y3 = []
y4 = []
try:
    with open(f'C:/Users/pawel/Desktop/{title}') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        line_count = 0
        for row in csv_reader:
            print(", ".join(row))
            if line_count == 0:
                x_t = row[0]
                y1_t = row[1]
                try:
                    y2_t = row[2]
                except:
                    y2_t = None
                try:
                    y3_t = row[3]
                except:
                    y3_t = None
                try:
                    y4_t = row[4]
                except:               
                    y4_t = None
            else:
                x.append(float(row[0]))
                y1.append(float(row[1]))
                if y2_t != None:
                    y2.append(float(row[2]))
                if y3_t != None:
                    y3.append(float(row[3]))
                if y4_t != None:
                    y4.append(float(row[4]))
            line_count += 1
        print(f'Processed {line_count} lines.')
except:
    print('FileNotFoundError: no such file or directory')
    input("Press Enter to continue...")
    sys.exit()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
