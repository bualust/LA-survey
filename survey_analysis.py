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
    number_of_questions = len(arr_tsv[0,:]) -1  #number of plots (ghe first one is the date, we can ignore it)
    print('--- Number of questions posed: ',number_of_questions)

    i=1
    while i <= number_of_questions-4: 
       print('Currently processing question number: ',i)
       fig, ax = plt.subplots(2,2)
       if i==1:
          ax[0,0].hist(np.array(arr_tsv[1:,1],dtype=int), [15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100])
       else:
          ax[0,0].hist(arr_tsv[1:,i])
       ax[0,0].set_title(arr_tsv[0,i].decode('cp1252'))
       ax[0,1].hist(arr_tsv[1:,i+1])
       ax[0,1].set_title(arr_tsv[0,i+1].decode('cp1252'))
       ax[1,0].hist(arr_tsv[1:,i+2])
       ax[1,0].set_title(arr_tsv[0,i+2].decode('cp1252'))
       ax[1,1].hist(arr_tsv[1:,i+3])
       ax[1,1].set_title(arr_tsv[0,i+3].decode('cp1252'))
       plt.show()
       i=i+4
    print('Next bunch of plots')

# __main__
if __name__ == '__main__':
  main()
