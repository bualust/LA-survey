# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from optparse import OptionParser
from collections import Counter
import pdb

#pretty plots style
plt.style.use('ggplot')
#plt.style.use('fivethirtyeight')

# ---------------------------
# main
# ---------------------------
def main():
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

# ---------------------------
# Looper: loops over answers 
# ---------------------------
def looper(AGE):
    FILE = 'Questionario_Sept2021.tsv'
    print('--- Opening data file:',FILE)
    num_lines = sum(1 for line in open(FILE))
    print('--- Number of answers available: ',num_lines-1)

    arr_tsv = np.genfromtxt(FILE, delimiter='\t', dtype='object',encoding='utf-8') #cp1252 to be used to decode
    number_of_questions = len(arr_tsv[0,:]) -1  #number of plots (the first one is the date, we can ignore it)
    print('--- Number of questions posed: ',number_of_questions)

    i=1
    while i <= number_of_questions: 
       if i==27 or i==5:
          print('Skipping question number:  ',i)
          i=i+1
       else:
          print('Currently processing question number: ',i)
          fig, (ax1) = plt.subplots(1)
          if i==1:
             data = np.array(arr_tsv[1:,i],dtype=int)
             age_bins = [15,20,25,30,35,40,45,50,55,60,65,70,75,80,85]
             ax1.hist(data,age_bins,color='orange',label='inclusivo')
             gender = np.array(arr_tsv[1:,2])
             data_hist_f = data[(gender==b'femminile')]
             data_hist_m = data[(gender==b'maschile')]
             ax1.hist(data_hist_f,age_bins,color='lightpink',label='femminile')
             ax1.hist(data_hist_m,age_bins,color='cornflowerblue',label='maschile')
          elif (i>=9 and i<=14) or (i>=16 and i<=25) or (i==28) or (i>=32 and i<=38) or (i==40) or (i==42):
             order = [b"non so", b"per nulla",b"poco",b"abbastanza",b"molto"]
             data = Counter(np.array(arr_tsv[1:,i]))
             ordered_data = {ans:data[ans] for ans in order}
             ax1.bar(ordered_data.keys(),ordered_data.values()) 
             #gender = np.array(arr_tsv[1:,2])
             #data_hist_f = ordered_data[(gender==b'femminile')]
             #data_hist_m = ordered_data[(gender==b'maschile')]
             #ax1.bar(ordered_data.keys(),data_hist_f,color='lightpink',label='femminile')
             #ax1.bar(ordered_data.keys(),data_hist_m,color='cornflowerblue',label='maschile')
          elif i>=29 and i<=31: 
             order = [b"1", b"2",b"3",b"4",b"5"]
             data = Counter(np.array(arr_tsv[1:,i]))
             ordered_data = {ans:data[ans] for ans in order}
             ax1.bar(ordered_data.keys(),ordered_data.values()) 
          else:
             ax1.hist(arr_tsv[1:,i])
          ax1.set_title(arr_tsv[0,i].decode('cp1252'))
          plt.show()
          i=i+1
    print('Next bunch of plots')

# __main__
if __name__ == '__main__':
  main()
