# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
from collections import Counter

#pretty plots style
plt.style.use('ggplot')
#plt.style.use('fivethirtyeight')

# -------
# main
# -------
def main(argv):
     parser = OptionParser()
     parser.add_option("--age", dest="age", default="15",help="Apply minimum cut on age [default: %default]", metavar="INT")
     parser.add_option("--gender", dest="gender", default="femminile",help="Apply selection on gender [default: %default]", metavar="STRING")

     try:
         (options, args) = parser.parse_args()
     except:
         parser.print_help()
         exit()

     global age
     age = options.age

     global gender
     gender = options.gender

     looper(age)
     exit()

# -------
# Looper: loops over answers 
# -------

def looper(AGE):

    FILE = 'Questionarion_Sept2021.tsv'
    print('--- Opening data file:',FILE)
    num_lines = sum(1 for line in open(FILE))
    print('--- Number of answers available: ',num_lines)

    variables_name = []
    with open(FILE, 'r') as csvfile:
        variables_name = (csvfile.readline()).split('	')
        number_of_variables = np.size(variables_name)
        arr_age    = np.zeros(num_lines-1,dtype=int)
        arr_gender = np.zeros(num_lines-1,dtype="object")
        arr_study  = np.zeros(num_lines-1,dtype="object")
        arr_nat    = np.zeros(num_lines-1,dtype="object")
        i=0
        for line in csvfile:
            result_line = line.split('	')
        #    for i in variables_name:
        #        exec(object'arr_{i} = result_line[i+1]')
            arr_age[i]    = result_line[1]
            arr_gender[i] = result_line[2]
            arr_study[i]  = result_line[3]
            arr_nat[i]    = result_line[4]
            #if result_line[1] < AGE: 
            #  arr_age[i] = -99
            #else:
            #  arr_age[i] = result_line[1]
            i=i+1
    
        print('Gender: ',Counter(arr_gender))
        print('Study: ',Counter(arr_study))
        print('Nationality: ',Counter(arr_nat))
        fig, ax = plt.subplots(2,2)
        ax[0,0].hist(arr_age, [15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100])
        ax[0,0].set_title("Eta\'")
        ax[0,1].hist(arr_gender)
        ax[0,1].set_title("Genere")
        ax[1,0].hist(arr_study)
        ax[1,0].set_title("Titolo di studio")
        ax[1,1].hist(arr_nat)
        ax[1,1].set_title("Nazionalita\'")
        plt.show()

# __main__
if __name__ == '__main__':
  main(sys.argv[1:])
