#import csv
#
#with open('Questionario.csv', 'r', newline='\n') as csvfile:
#    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#    for row in spamreader:
#        print(', '.join(row))

with open('Questionario.csv', 'r') as csvfile:
    for line in csvfile:
        print(line.split(',')[1])
