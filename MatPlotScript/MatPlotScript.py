import sys

from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import csv
import random

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        ### defaults
        self.title = 'chart.csv'
        self.delimiter = ','
        self.pattern = '.-'
        self.markersize = 10
        self.x = []
        self.y1 = []
        self.y2 = []
        self.y3 = []
        self.y4 = []

        ### canvas setup
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        ### toolbar setup
        self.toolbar = NavigationToolbar(self.canvas, self)

        ### user input setup
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        
        self.e_path = QLineEdit('chart.csv')
        self.e_path.textChanged[str].connect(self.pathchanged)
        self.e_delimiter = QLineEdit(',')
        self.e_delimiter.textChanged[str].connect(self.delimiterchanged)
        self.e_pattern = QLineEdit('.-')
        self.e_pattern.textChanged[str].connect(self.patternchanged)
        self.e_markersize = QLineEdit('10')
        self.e_markersize.textChanged[str].connect(self.mschanged)
        
        self.input_box = QHBoxLayout()
        self.input_box.addWidget(self.button)
        self.input_box.addWidget(self.e_path)
        self.input_box.addWidget(self.e_delimiter)
        self.input_box.addWidget(self.e_pattern)
        self.input_box.addWidget(self.e_markersize)

        ### layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(self.input_box)
        self.setLayout(layout)
        
    def pathchanged(self, text):
        self.title = text

    def delimiterchanged(self, text):
        self.delimiter = text

    def patternchanged(self, text):
        self.pattern = text

    def mschanged(self, text):
        self.markersize = int(text)

    def plot(self):
        self.x = []
        self.y1 = []
        self.y2 = []
        self.y3 = []
        self.y4 = []
        try:
            #with open(f'C:/Users/pawel/Desktop/{self.title}') as csv_file:
            with open(self.title) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
                line_count = 0
                for row in csv_reader:
                    #print(", ".join(row))
                    if line_count == 0:
                        self.x_t = row[0]
                        self.y1_t = row[1]
                        try:
                            self.y2_t = row[2]
                        except:
                            self.y2_t = None
                        try:
                            self.y3_t = row[3]
                        except:
                            self.y3_t = None
                        try:
                            self.y4_t = row[4]
                        except:               
                            self.y4_t = None
                    else:
                        self.x.append(float(row[0]))
                        self.y1.append(float(row[1]))
                        if self.y2_t != None:
                            self.y2.append(float(row[2]))
                        if self.y3_t != None:
                            self.y3.append(float(row[3]))
                        if self.y4_t != None:
                            self.y4.append(float(row[4]))
                    line_count += 1
                #print(f'Processed {line_count} lines.')
        except:
            self.x = [4]


        # clear figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(self.x, self.y1, 'b' + self.pattern, ms = self.markersize)
        handle_tab = [mpatches.Patch(color='b', label=self.y1_t)]
        if self.y2_t != None:
            ax.plot(self.x, self.y2, 'r' + self.pattern, ms = self.markersize)
            handle_tab.append(mpatches.Patch(color='r', label=self.y2_t))
        if self.y3_t != None:
            ax.plot(self.x, self.y3, 'y' + self.pattern, ms = self.markersize)
            handle_tab.append(mpatches.Patch(color='y', label=self.y3_t))
        if self.y4_t != None:
            ax.plot(self.x, self.y4, 'm' + self.pattern, ms = self.markersize)
            handle_tab.append(mpatches.Patch(color='m', label=self.y4_t))
        
        ax.set_title(self.title.replace('_', ' ')[:-4])
        ax.set_xlabel(self.x_t)
        ax.legend(handles=handle_tab)
        ax.grid(True)
        
        # refresh canvas
        self.canvas.draw()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
