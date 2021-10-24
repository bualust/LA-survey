# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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
          do_hist = 0
          if i==1:
             pps = age_plot(arr_tsv,ax1,i)
          else:
             order,do_hist = check_order(i)
             if(do_hist):
                ax1.hist(arr_tsv[1:,i])
             else:
                pps = bar_chart(arr_tsv,ax1,i,order)
          if do_hist==0:
             percentage_on_bins(ax1,pps)
          ax1.set_title(arr_tsv[0,i].decode('cp1252'))
          ax1.legend()
          plt.show()
          i=i+1
    print('Next bunch of plots')

def group_age_data(cnt_data,age_bins):
   order = []
   for index in range(15,86,1):
       order.append(index)
   ordered_data = {ans:cnt_data[ans] for ans in order}
   grouped_data = np.zeros(len(age_bins))
   for age_key,age_count in zip(ordered_data.keys(),ordered_data.values()):
       for i in range(len(age_bins)-1):
          if age_key>=age_bins[i] and age_key<age_bins[i+1]:
             grouped_data[i]+=age_count
   return grouped_data

def split_gender(data,gender,order, isAge):
   data_f = data[(gender==b'femminile')]
   data_m = data[(gender==b'maschile')]
   cnt_data_f = Counter(data_f)
   cnt_data_m = Counter(data_m)
   if isAge:
      ordered_data_f = group_age_data(cnt_data_f,order)
      ordered_data_m = group_age_data(cnt_data_m,order)
   else:
      ordered_data_f = {ans:cnt_data_f[ans] for ans in order}
      ordered_data_m = {ans:cnt_data_m[ans] for ans in order}
   return ordered_data_f,ordered_data_m

def check_order(i):
   do_hist = 0
   if (i>=9 and i<=14) or (i>=16 and i<=25) or (i==28) or (i>=32 and i<=38) or (i==40) or (i==42):
      order = [b"non so", b"per nulla",b"poco",b"abbastanza",b"molto"]
   elif i>=29 and i<=31: 
      order = [b"1", b"2",b"3",b"4",b"5"]
   else:
      do_hist = 1
      order = []
   return order,do_hist

def age_plot(arr_tsv,ax1,i):
   age_bins = [15,20,25,30,35,40,45,50,55,60,65,70,75]
   data = np.array(arr_tsv[1:,i],dtype=int)
   cnt_data = Counter(data)
   grouped_data = group_age_data(cnt_data,age_bins)
   x = np.arange(len(age_bins))
   w = 0.2
   pps = ax1.bar(x-w,grouped_data,label='inclusivo',width=w) 
   #gender split
   gender = np.array(arr_tsv[1:,2])
   ordered_data_f, ordered_data_m = split_gender(data,gender,age_bins,1)
   ax1.bar(x,ordered_data_f,color='lightpink',label='femminile',width=w)
   ax1.bar(x+w,ordered_data_m,color='cornflowerblue',label='maschile',width=w)
   age_bins_label = ['15-20','20-25','25-30','30-35','35-40','40-45','45-50','50-55','55-60','60-65','65-70','70-75','75-80']
   xaxis = np.array(age_bins_label,dtype=str)
   #this prevents the x-labels to be cropped
   ax1.xaxis.set_major_locator(mticker.FixedLocator(x))
   ax1.xaxis.set_major_formatter(mticker.FixedFormatter(xaxis))
   ax1.set_xticklabels(xaxis)
   return pps

def bar_chart(arr_tsv,ax1,i,order):
   data = np.array(arr_tsv[1:,i])
   cnt_data = Counter(data)
   ordered_data = {ans:cnt_data[ans] for ans in order}
   x = np.arange(len(ordered_data.keys()))
   w = 0.2
   pps = ax1.bar(x-w,ordered_data.values(),label='inclusivo',width=w) 
   #gender split
   gender = np.array(arr_tsv[1:,2])
   ordered_data_f, ordered_data_m = split_gender(data,gender,order,0)
   ax1.bar(x,ordered_data_f.values(),color='lightpink',label='femminile',width=w)
   ax1.bar(x+w,ordered_data_m.values(),color='cornflowerblue',label='maschile',width=w)
   xaxis = np.array(order,dtype=str)
   #this prevents the x-labels to be cropped
   ax1.xaxis.set_major_locator(mticker.FixedLocator(x))
   ax1.xaxis.set_major_formatter(mticker.FixedFormatter(xaxis))
   ax1.set_xticklabels(xaxis)
   return pps

def percentage_on_bins(ax1,pps):
  sum_of_answers = 0
  for p in pps:
     height = p.get_height()
     sum_of_answers+=height
  for p in pps:
     height_perc = round(100*p.get_height()/sum_of_answers,1)
     print(height_perc,sum_of_answers)
     ax1.text(x=p.get_x() + p.get_width() / 2, y=p.get_height()+.10,
                s="{}%".format(height_perc),
                ha='center')
# __main__
if __name__ == '__main__':
  main()
