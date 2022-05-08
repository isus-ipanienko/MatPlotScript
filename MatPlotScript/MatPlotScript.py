import sys

from PyQt5.QtWidgets import QComboBox, QDialog, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QCheckBox
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
        self.dataSetLength = None
        self.dataSetCount = None
        self.data = [[],[]]
        self.y_fit = []


        ### plotting options setup
        # t_options
        self.t_options = QTableWidget()
        self.t_options.setRowCount(1)
        self.t_options.setColumnCount(5)
        self.t_options.setVerticalHeaderLabels(['Options'])
        self.t_options.resizeColumnsToContents()
        self.t_options.verticalHeader().sectionClicked.connect(self.onHeaderClicked)
        self.t_options.setItem(0,0, QTableWidgetItem('axis (x/y)'))
        self.t_options.setItem(0,1, QTableWidgetItem('domain'))
        self.t_options.setItem(0,2, QTableWidgetItem('colour'))
        self.t_options.setItem(0,3, QTableWidgetItem('pattern'))
        self.t_options.setItem(0,4, QTableWidgetItem('markersize'))
        # buttons
        self.b_plot = QPushButton('Plot')
        self.b_plot.clicked.connect(lambda: self.plot('just plot'))
        self.b_read = QPushButton('Read')
        self.b_read.clicked.connect(self.read)
        # labels and textboxes
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
        self.l_legend = QLabel('Legend:')
        # labels and checkboxes
        self.cb_legend = QCheckBox()
        self.cb_legend.setChecked(True)
        
        ### linear regression options setup
        # buttons
        self.l_plot_reg = QLabel('Linear regression:')
        self.b_plot_reg = QPushButton('Calculate fit')
        self.b_plot_reg.clicked.connect(lambda: self.plot('plot_reg'))
        # labels
        self.l_sig_num = QLabel('Significant numbers:')
        self.e_sig_num = QLineEdit('3')
        self.l_y_target = QLabel('y-axis (click a label):')
        self.e_y_target = QLineEdit('y1')
        self.l_params = QLabel('Fit params:')
        self.e_params = QLineEdit('')
        
        ### error label setup
        self.l_error = QLabel('Error: None')

        ### matplot setup
        # figure
        self.figure = plt.figure()
        self.fft_figure = plt.figure()
        # canvas
        self.canvas = FigureCanvas(self.figure)
        self.fft_canvas = FigureCanvas(self.fft_figure)
        # toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.fft_toolbar = NavigationToolbar(self.fft_canvas, self)

        ##########################
        ## t_settings #         ##
        ##   input    #  plots  ##
        ##    box     #         ##
        ##########################

        ### layout setup
        ## settings section
        # create boxes
        self.input_box = QVBoxLayout()
        self.bottom_input_box = QHBoxLayout()
        self.left_input_box = QVBoxLayout()
        self.right_input_box = QVBoxLayout()
        # box hierarchy
        self.input_box.addWidget(self.t_options)
        self.input_box.addLayout(self.bottom_input_box)
        self.bottom_input_box.addLayout(self.left_input_box)
        self.bottom_input_box.addLayout(self.right_input_box)
        # left input box contents
        self.left_input_box.addWidget(self.b_plot) # plot data
        self.left_input_box.addWidget(self.l_path)
        self.left_input_box.addWidget(self.l_delimiter)
        self.left_input_box.addWidget(self.l_title)
        self.left_input_box.addWidget(self.l_xlabel)
        self.left_input_box.addWidget(self.l_ylabel)
        self.left_input_box.addWidget(self.l_legend)
        self.left_input_box.addWidget(self.l_plot_reg)
        self.left_input_box.addWidget(self.l_sig_num)
        self.left_input_box.addWidget(self.l_y_target)
        self.left_input_box.addWidget(self.l_params)
        # right input box contents
        self.right_input_box.addWidget(self.b_read) # read from file
        self.right_input_box.addWidget(self.e_path) # path to .csv file
        self.right_input_box.addWidget(self.e_delimiter) # .csv file delimiter
        self.right_input_box.addWidget(self.e_title) # plot title
        self.right_input_box.addWidget(self.e_xlabel) # plot xlabel
        self.right_input_box.addWidget(self.e_ylabel) # plot ylabel
        self.right_input_box.addWidget(self.cb_legend) # legend toggle
        self.right_input_box.addWidget(self.b_plot_reg) # plot with linear regression
        self.right_input_box.addWidget(self.e_sig_num) # significant numbers *only* on legend
        self.right_input_box.addWidget(self.e_y_target) # which function to target
        self.right_input_box.addWidget(self.e_params) # regression parameters output
        # error label
        self.input_box.addWidget(self.l_error) # error output
        ## matplot section
        # box creation 
        self.plt_box = QVBoxLayout()
        self.matplot_box = QVBoxLayout()
        self.fft_matplot_box = QVBoxLayout()
        self.plt_box.addLayout(self.matplot_box)
        self.plt_box.addLayout(self.fft_matplot_box)
        # add contents
        self.matplot_box.addWidget(self.canvas)
        self.matplot_box.addWidget(self.toolbar)
        self.fft_matplot_box.addWidget(self.fft_canvas)
        self.fft_matplot_box.addWidget(self.fft_toolbar)
        ## top layer section
        # create top section
        self.layout = QHBoxLayout()
        # add contents
        self.layout.addLayout(self.input_box)
        self.layout.addLayout(self.plt_box)
        # set top layout
        self.setLayout(self.layout)

    def filter_data(self, unfiltered_data):
        filtered_data = []
        for entry in unfiltered_data:
            if entry:
                filtered_data.append(entry)
        for entry in range(1, len(filtered_data)):
            for item in range(len(filtered_data[0])):
                filtered_data[entry][item] = filtered_data[entry][item].replace(' ','')
        return filtered_data

    def read(self):
        try:
            with open(self.e_path.text()) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=self.e_delimiter.text())
                unfiltered_data = list(csv_reader)

            self.data = self.filter_data(unfiltered_data)
            self.dataSetLength = len(self.data) - 1
            self.dataSetCount = len(self.data[0])
            self.t_options.setRowCount(self.dataSetCount + 1) # create a row for each data set + a row for descriptions

            for option in range(5):
                for dataSet in range(self.dataSetCount):
                    if option == 0: # sets this set as x or y
                        temp_item = QComboBox()
                        temp_item.addItem('x')
                        temp_item.addItem('y')
                        if dataSet != 0:
                            temp_item.setCurrentText('y')
                        self.t_options.setCellWidget(dataSet+1, option, temp_item)
                        continue
                    elif option == 1: # domain id option
                        temp_item = 'a'
                    elif option == 2: # plot colour option
                        if dataSet == 1:
                            temp_item = 'b'
                        elif dataSet == 2:
                            temp_item = 'r'
                        elif dataSet == 3:
                            temp_item = 'y'
                        elif dataSet == 4:
                            temp_item = 'm'
                        else:
                            temp_item = 'g'
                    elif option == 3: # plot line style option
                        temp_item = '.-'
                    else: # plot line thickness option
                        temp_item = '10'
                    self.t_options.setItem(dataSet+1, option, QTableWidgetItem(temp_item))

            if self.dataSetCount:
                self.t_options.setVerticalHeaderLabels(['Options'] + self.data[0])
        except Exception as e:
            self.l_error.setText(str(e))
            return

    def plot(self, curve):
        self.figure.clear()
        self.fft_figure.clear()
        ax = self.figure.add_subplot(111)
        fft_ax = self.fft_figure.add_subplot(111)

        domains = []
        try:
            for col in range(self.dataSetCount):
                domains.append(str(self.t_options.cellWidget(col+1,0).currentText())+self.t_options.item(col+1,1).text()) 
        except Exception as e:
                self.l_error.setText('no data')
                return

        # plot data
        handle_tab = []
        for col in range(self.dataSetCount):
            if domains[col][0] == 'y':
                try:
                    temp_domain_index = domains.index('x' + domains[col][1:]) # get index of x domain
                except:
                    self.l_error.setText('missing domain')
                    return

                temp_y = []
                temp_x = []
                try:
                    for row in range(self.dataSetLength):
                        temp_y.append(float(self.data[row+1][col]))
                        temp_x.append(float(self.data[row+1][temp_domain_index]))
                except:
                    self.l_error.setText('chart ValueError')
                    return

                #                            colour                                  pattern                                   markersize
                ax.plot(temp_x, temp_y, self.t_options.item(col+1,2).text() + self.t_options.item(col+1,3).text(), ms = int(self.t_options.item(col+1,4).text()))
                #                                                  colour                             label
                handle_tab.append(mpatches.Patch(color=self.t_options.item(col+1,2).text(), label=self.data[0][col]))

                ft = abs(np.fft.fft(temp_y))
                ft = 20 * np.log10(np.fft.fftshift(ft))
                freq = np.fft.fftfreq(len(temp_y))
                freq = np.fft.fftshift(freq)
                fft_ax.plot(freq, ft, self.t_options.item(col+1,2).text() + self.t_options.item(col+1,3).text(), ms = int(self.t_options.item(col+1,4).text()))

        # plot linear regression
        if curve == 'plot_reg':
            try:
                temp_y_index = self.data[0].index(self.e_y_target.text()) # get index of y
                temp_domain_index = domains.index('x' + domains[temp_y_index][1:]) # get index of x domain
            except:
                    self.l_error.setText('missing domain')
                    return
        
            temp_y = []
            temp_x = []
            try:
                for row in range(self.dataSetLength):
                    temp_y.append(float(self.data[row+1][temp_y_index]))
                    temp_x.append(float(self.data[row+1][temp_domain_index]))
                temp_y = np.array(temp_y)
                temp_x = np.array(temp_x)
            except:
                    self.l_error.setText('chart ValueError')
                    return
        
            try:
                slope, intercept, r_value, p_value, std_err = linregress(temp_x, temp_y)
                significant_numbers = int(self.e_sig_num.text())
                rounded_slope =  round(slope, significant_numbers - int(m.floor(m.log10(abs(slope)))) - 1)
                rounded_intercept =  round(intercept, significant_numbers - int(m.floor(m.log10(abs(intercept)))) - 1)
            except:
                    self.l_error.setText('regression error')
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
        if self.cb_legend.isChecked():
            ax.legend(handles=handle_tab)
        ax.grid(True)
        fft_ax.grid(True)
    
        # refresh canvas
        self.canvas.draw()
        self.fft_canvas.draw()

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        print(e.mimeData().text())
        self.e_path.setText(e.mimeData().text()[7:])
        self.read()
        self.plot('just plot')

    def onHeaderClicked(self, row):
        self.e_y_target.setText(self.t_options.verticalHeaderItem(row).text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
