import sys

from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import csv
import numpy as np 
import math as m 
from scipy.stats import linregress 


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setWindowTitle("MatPlotScript")
        self.row_count = None
        self.col_count = None
        self.data = [[],[]]
        self.y_fit = []


        ### options setup
        # t_options
        self.t_options = QTableWidget()
        self.t_options.setRowCount(1)
        self.t_options.setColumnCount(5)
        self.t_options.setVerticalHeaderLabels(['Options'])
        self.t_options.resizeColumnsToContents()
        self.t_options.setItem(0,0, QTableWidgetItem('axis (x/y)'))
        self.t_options.setItem(0,1, QTableWidgetItem('domain'))
        self.t_options.setItem(0,2, QTableWidgetItem('colour'))
        self.t_options.setItem(0,3, QTableWidgetItem('pattern'))
        self.t_options.setItem(0,4, QTableWidgetItem('markersize'))


        ### user input setup
        # buttons
        self.b_plot = QPushButton('Plot')
        self.b_plot.clicked.connect(lambda: self.plot('no_curve'))
        self.b_read = QPushButton('Read')
        self.b_read.clicked.connect(self.read)
        # labels
        self.l_path = QLabel('Path (drag and drop):')
        self.e_path = QLineEdit('chart.csv')
        self.l_delimiter = QLabel('Delimiter:')
        self.e_delimiter = QLineEdit(',')
        self.l_title = QLabel('Title:')
        self.e_title = QLineEdit('chart')
        self.l_xlabel = QLabel('xlabel:')
        self.e_xlabel = QLineEdit('xlabel')
        self.l_ylabel = QLabel('ylabel:')
        self.e_ylabel = QLineEdit('ylabel')
        # input_box
        self.input_box = QVBoxLayout()
        self.input_box.addWidget(self.t_options)
        self.top_input_box = QHBoxLayout()
        self.input_box.addLayout(self.top_input_box)
        self.left_input_box = QVBoxLayout()
        self.right_input_box = QVBoxLayout()
        self.top_input_box.addLayout(self.left_input_box)
        self.top_input_box.addLayout(self.right_input_box)
        self.left_input_box.addWidget(self.b_plot)
        self.right_input_box.addWidget(self.b_read)
        self.left_input_box.addWidget(self.l_path)
        self.right_input_box.addWidget(self.e_path)
        self.left_input_box.addWidget(self.l_delimiter)
        self.right_input_box.addWidget(self.e_delimiter)
        self.left_input_box.addWidget(self.l_title)
        self.right_input_box.addWidget(self.e_title)
        self.left_input_box.addWidget(self.l_xlabel)
        self.right_input_box.addWidget(self.e_xlabel)
        self.left_input_box.addWidget(self.l_ylabel)
        self.right_input_box.addWidget(self.e_ylabel)
        

        ### curve_fit setup
        # buttons
        self.l_curve_calc = QLabel('Linear regression:')
        self.b_curve_calc = QPushButton('Calculate fit')
        self.b_curve_calc.clicked.connect(lambda: self.plot('calc_curve'))
        # labels
        self.l_expression = QLabel('Significant numbers:')
        self.e_expression = QLineEdit('3')
        self.l_x_curve = QLabel('x-axis (domain):')
        self.e_x_curve = QLineEdit('x1')
        self.l_y_curve = QLabel('y-axis (label):')
        self.e_y_curve = QLineEdit('y1')
        self.l_params = QLabel('Fit params:')
        self.e_params = QLineEdit('')
        # input_box
        self.left_input_box.addWidget(self.l_curve_calc)
        self.right_input_box.addWidget(self.b_curve_calc)
        self.left_input_box.addWidget(self.l_expression)
        self.right_input_box.addWidget(self.e_expression)
        self.left_input_box.addWidget(self.l_x_curve)
        self.right_input_box.addWidget(self.e_x_curve)
        self.left_input_box.addWidget(self.l_y_curve)
        self.right_input_box.addWidget(self.e_y_curve)
        self.left_input_box.addWidget(self.l_params)
        self.right_input_box.addWidget(self.e_params)


        ### error_label
        self.l_error = QLabel('Error: None')
        self.input_box.addWidget(self.l_error)


        ### matplot setup
        # figure
        self.figure = plt.figure()
        # canvas
        self.canvas = FigureCanvas(self.figure)
        # toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        # matplot_box
        self.matplot_box = QVBoxLayout()
        self.matplot_box.addWidget(self.canvas)
        self.matplot_box.addWidget(self.toolbar)


        ### spreadsheet setup
        # t_spread
        self.t_spread = QTableWidget()


        ### layout setup
        # layout
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.input_box)
        self.layout.addLayout(self.matplot_box)
        self.layout.addWidget(self.t_spread)
        self.setLayout(self.layout)


    def read(self):
        try:
            with open(self.e_path.text()) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=self.e_delimiter.text())
                self.data = list(csv_reader)
                for row in range(1, len(self.data)):
                    for col in range(len(self.data[0])):
                        self.data[row][col] = self.data[row][col].replace(' ','')

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
        except:
            self.l_error.setText('wrong file name')
            return
        


    def plot(self, curve):

        # clear figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # create domain map
        domain_list = []
        try:
            for col in range(self.col_count):
                domain_list.append(self.t_options.item(col+1,0).text()+self.t_options.item(col+1,1).text()) 
        except:
                self.l_error.setText('no data')
                return
        
        # plot data
        handle_tab = []
        for col in range(self.col_count):
            if domain_list[col][0] == 'y':
                try:
                    temp_domain_index = domain_list.index('x' + domain_list[col][1]) # get index of x domain
                except:
                    self.l_error.setText('missing domain')
                    return

                temp_y = []
                temp_x = []
                try:
                    for row in range(self.row_count):
                        temp_y.append(float(self.data[row+1][col]))
                        temp_x.append(float(self.data[row+1][temp_domain_index]))
                except:
                    self.l_error.setText('chart ValueError')
                    return

                #                            colour                                  pattern                                   markersize
                ax.plot(temp_x, temp_y, self.t_options.item(col+1,2).text() + self.t_options.item(col+1,3).text(), ms = int(self.t_options.item(col+1,4).text()))
                #                                                  colour                             label
                handle_tab.append(mpatches.Patch(color=self.t_options.item(col+1,2).text(), label=self.data[0][col]))
        
        # plot user fit
        #if curve == 'plot_curve':
        #    try:
        #        temp_domain_index = domain_list.index(self.e_x_curve.text()) # get index of x domain
        #        temp_y_index = self.data[0].index(self.e_y_curve.text()) # get index of y
        #    except:
        #            self.l_error.setText('missing domain')
        #            return
            
        #    try:
        #        temp_x = []
        #        for row in range(self.row_count):
        #            temp_x.append(float(self.data[row+1][temp_domain_index]))
        #        temp_x = np.array(temp_x)
        #    except:
        #            self.l_error.setText('chart ValueError')
        #            return

        #    try:
        #        temp_params = self.e_expression.text().split(', ') # user input
        #        temp_params = [float(k) for k in temp_params]
        #    except:
        #            self.l_error.setText('params ValueError')
        #            return
        #    try:
        #        temp_y = []
        #        temp_y = temp_params[0] * temp_x + temp_params[1]
        #    except:
        #            self.l_error.setText('wrong params')
        #            return
            
        #    #                            colour                                 pattern                         markersize
        #    ax.plot(temp_x, temp_y, self.t_options.item(temp_y_index+1,2).text() + '-', ms = int(self.t_options.item(temp_y_index+1,4).text()))
        #    #                                                  colour                              label
        #    handle_tab.append(mpatches.Patch(color=self.t_options.item(temp_y_index+1,2).text(), label=self.data[0][temp_y_index] + ' fit test'))
        
        # plot linear regression
        if curve == 'calc_curve':
            try:
                temp_domain_index = domain_list.index(self.e_x_curve.text()) # get index of x domain
                temp_y_index = self.data[0].index(self.e_y_curve.text()) # get index of y
            except:
                    self.l_error.setText('missing domain')
                    return
        
            temp_y = []
            temp_x = []
            try:
                for row in range(self.row_count):
                    temp_y.append(float(self.data[row+1][temp_y_index]))
                    temp_x.append(float(self.data[row+1][temp_domain_index]))
                temp_y = np.array(temp_y)
                temp_x = np.array(temp_x)
            except:
                    self.l_error.setText('chart ValueError')
                    return
        
            try:
                slope, intercept, r_value, p_value, std_err = linregress(temp_x, temp_y)
                significant_numbers = int(self.e_expression.text())
                rounded_slope =  round(slope, significant_numbers - int(m.floor(m.log10(abs(slope)))) - 1)
                rounded_intercept =  round(intercept, significant_numbers - int(m.floor(m.log10(abs(intercept)))) - 1)
            except:
                    self.l_error.setText('mismatched domain or wrong significant numbers')
                    return
        
            #                            colour                                 pattern                         markersize
            ax.plot(temp_x, slope * temp_x + intercept, self.t_options.item(temp_y_index+1,2).text() + '-', ms = int(self.t_options.item(temp_y_index+1,4).text()))
            #                                                  colour                              label
            handle_tab.append(mpatches.Patch(color=self.t_options.item(temp_y_index+1,2).text(), label=f'y = {rounded_slope} * x + {rounded_intercept}'))

            # output parameters
            self.e_params.setText(f'y = {slope} * x + {intercept} R^2: {r_value**2}, P: {p_value}, STD: {std_err}')

        # draw legend
        try:
            ax.set_title(self.e_title.text())
        except:
            self.l_error.setText('title error')
            return
        try:
            ax.set_xlabel(self.e_xlabel.text())
        except:
            self.l_error.setText('xlabel error')
            return
        try:
            ax.set_ylabel(self.e_ylabel.text())
        except:
            self.l_error.setText('ylabel error')
            return
        ax.legend(handles=handle_tab)
        ax.grid(True)
        
        # refresh canvas
        self.canvas.draw()

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        self.e_path.setText(e.mimeData().text()[8:])
        self.read()
        self.plot('no curve')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
