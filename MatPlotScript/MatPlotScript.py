import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import csv
import sys


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
    with open(title) as csv_file:
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


plt.plot(x, y1, 'b' + pattern, ms = markersize)
handle_tab = [mpatches.Patch(color='b', label=y1_t)]
if y2_t != None:
    plt.plot(x, y2, 'r' + pattern, ms = markersize)
    handle_tab.append(mpatches.Patch(color='r', label=y2_t))
if y3_t != None:
    plt.plot(x, y3, 'y' + pattern, ms = markersize)
    handle_tab.append(mpatches.Patch(color='y', label=y3_t))
if y4_t != None:
    plt.plot(x, y4, 'm' + pattern, ms = markersize)
    handle_tab.append(mpatches.Patch(color='m', label=y4_t))


plt.title(title.replace('_', ' ')[:-4])
plt.xlabel(x_t)
plt.legend(handles=handle_tab)
plt.grid()
plt.show()
