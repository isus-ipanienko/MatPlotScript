import sys

from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QAction, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import csv
import random

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("MatPlotScript")
        self.row_count = None
        self.col_count = None
        self.data = [[],[]]

        ### user input setup
        self.b_plot = QPushButton('Plot')
        self.b_plot.clicked.connect(self.plot)

        self.b_read = QPushButton('Read')
        self.b_read.clicked.connect(self.read)
        
        self.l_path = QLabel('Path (relative or absolute):')
        self.e_path = QLineEdit('chart.csv')
        self.l_delimiter = QLabel('Delimiter:')
        self.e_delimiter = QLineEdit(',')
        self.l_title = QLabel('Title:')
        self.e_title = QLineEdit('chart')
        self.l_xlabel = QLabel('xlabel:')
        self.e_xlabel = QLineEdit('xlabel')
        self.l_ylabel = QLabel('ylabel:')
        self.e_ylabel = QLineEdit('ylabel')
        
        self.input_box = QVBoxLayout()
        self.input_box.addWidget(self.b_plot)
        self.input_box.addWidget(self.b_read)
        self.input_box.addWidget(self.l_path)
        self.input_box.addWidget(self.e_path)
        self.input_box.addWidget(self.l_delimiter)
        self.input_box.addWidget(self.e_delimiter)
        self.input_box.addWidget(self.l_title)
        self.input_box.addWidget(self.e_title)
        self.input_box.addWidget(self.l_xlabel)
        self.input_box.addWidget(self.e_xlabel)
        self.input_box.addWidget(self.l_ylabel)
        self.input_box.addWidget(self.e_ylabel)


        ### options setup
        self.t_options = QTableWidget()
        self.t_options.setRowCount(1)
        self.t_options.setColumnCount(5)
        self.t_options.setVerticalHeaderLabels(['Options'])
        self.t_options.setItem(0,0, QTableWidgetItem('axis (x/y)'))
        self.t_options.setItem(0,1, QTableWidgetItem('domain'))
        self.t_options.setItem(0,2, QTableWidgetItem('colour'))
        self.t_options.setItem(0,3, QTableWidgetItem('pattern'))
        self.t_options.setItem(0,4, QTableWidgetItem('markersize'))


        ### matplot setup
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.matplot_box = QVBoxLayout()
        self.matplot_box.addWidget(self.canvas)
        self.matplot_box.addWidget(self.toolbar)


        ### spreadsheet setup
        self.t_spread = QTableWidget()


        ### layout setup
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.input_box)
        self.layout.addWidget(self.t_options)
        self.layout.addLayout(self.matplot_box)
        self.layout.addWidget(self.t_spread)
        self.setLayout(self.layout)
        

    def read(self):

        with open(self.e_path.text()) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.e_delimiter.text())
            self.data = list(csv_reader)

            self.t_spread.setRowCount(len(self.data)-1)
            self.row_count = len(self.data) - 1
            self.t_spread.setColumnCount(len(self.data[0]))
            self.col_count = len(self.data[0])
            self.t_options.setRowCount(len(self.data[0])+1)

            for row in range(5):
                for element in range(len(self.data)-1):
                    if row == 0:
                        if element == 0:
                            temp_item = QTableWidgetItem('x')
                        else:
                            temp_item = QTableWidgetItem('y')
                    elif row == 1:
                        temp_item = QTableWidgetItem('1')
                    elif row == 2:
                        if element == 1:
                            temp_item = QTableWidgetItem('b')
                        elif element == 2:
                            temp_item = QTableWidgetItem('r')
                        elif element == 3:
                            temp_item = QTableWidgetItem('y')
                        elif element == 4:
                            temp_item = QTableWidgetItem('m')
                        else:
                            temp_item = QTableWidgetItem('g')
                    elif row == 3:
                        temp_item = QTableWidgetItem('.-')
                    else:
                        temp_item = QTableWidgetItem('10')

                    self.t_options.setItem(element+1, row, temp_item)


            for row in range(len(self.data)):
                if row == 0:
                    self.t_spread.setHorizontalHeaderLabels(self.data[0])
                    self.t_options.setVerticalHeaderLabels(['Options'] + self.data[0])
                else:
                    for element in range(len(self.data[0])):
                        self.t_spread.setItem(row-1,element, QTableWidgetItem(self.data[row][element]))


    def plot(self):

        # clear figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # create domain map
        domain_list = []
        for col in range(self.col_count):
            domain_list.append(self.t_options.item(col+1,0).text()+self.t_options.item(col+1,1).text()) 
        
        # plot data
        handle_tab = []
        for col in range(self.col_count):
            if domain_list[col][0] == 'y':
                temp_domain_index = domain_list.index('x' + domain_list[col][1]) # get index of x domain

                temp_y = []
                temp_x = []
                for row in range(self.row_count):
                    temp_y.append(float(self.data[row+1][col]))
                    temp_x.append(float(self.data[row+1][temp_domain_index]))

                #                            colour                                  pattern                                   markersize
                ax.plot(temp_x, temp_y, self.t_options.item(col+1,2).text() + self.t_options.item(col+1,3).text(), ms = int(self.t_options.item(col+1,4).text()))
                #                                                  colour                             label
                handle_tab.append(mpatches.Patch(color=self.t_options.item(col+1,2).text(), label=self.data[0][col]))
        
        # draw legend
        ax.set_title(self.e_title.text())
        ax.set_xlabel(self.e_xlabel.text())
        ax.set_ylabel(self.e_ylabel.text())
        ax.legend(handles=handle_tab)
        ax.grid(True)
        
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
