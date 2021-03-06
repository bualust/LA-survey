# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as image
import matplotlib.ticker as mticker
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
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
     parser.add_option("--age", dest="age", default="15",help="Apply minimum cut on age [default: %default]", type=int)
     parser.add_option("--agemax", dest="agemax", default="85",help="Apply max cut on age [default: %default]", type=int)
     parser.add_option("--gender", dest="gender", default=True,help="Split plots based on gender [default: %default]", metavar="STRING")

     try:
         (options, args) = parser.parse_args()
     except:
         parser.print_help()
         exit()

     global age
     age = options.age

     global agemax
     agemax = options.agemax

     global gender_opt
     gender_opt = options.gender

     global w
     w = 0.2

     print (options)

     looper()
     exit()

# ---------------------------
# Looper: loops over answers 
# ---------------------------
def looper():
    FILE = 'Questionario_Sept2021.tsv'
    print('--- Opening data file:',FILE)
    num_lines = sum(1 for line in open(FILE))
    print('--- Number of answers available: ',num_lines-1)

    arr_tsv = np.genfromtxt(FILE, delimiter='\t', dtype='object',encoding='utf-8') #cp1252 to be used to decode
    number_of_questions = len(arr_tsv[0,:]) -1  #number of plots (the first one is the date, we can ignore it)
    print('--- Number of questions posed: ',number_of_questions)

    i=1
    while i <= number_of_questions: 
       if i==27 or i==5 or i==39:
          print('Skipping question number:  ',arr_tsv[0,i].decode('cp1252'))
          i=i+1
       else:
          print('Currently processing question number: ',arr_tsv[0,i].decode('cp1252'),i)
          fig, (ax1) = plt.subplots(1)
          do_hist = 0
          if i==1:
             pps = age_plot(arr_tsv,ax1,i)
          else:
             order,do_hist = check_order(i)
             if(do_hist):
                data = arr_tsv[1:,i]
                age_values = np.array(arr_tsv[1:,1],dtype=int)
                data_filter = data[(age_values>=age) & (age_values<agemax)]
                #ax1.hist(data_filter)
                cnt_data_filter = Counter(data_filter)
                total = sum(cnt_data_filter.values())
                percent = {key: round(100*value/total,2) for key, value in cnt_data_filter.items()}
                #print(percent.most_common(1))
                print(cnt_data_filter.most_common(3))
                list_common = cnt_data_filter.most_common(4)
                most_comm_dic = {}
                for k in range(3):
                   most_comm_dic[list_common[k][0].decode("utf-8")] = list_common[k][1]
                x = np.arange(len(most_comm_dic.keys()))
                ax1.bar(x,most_comm_dic.values(),label='inclusivo',width=w) 
                ax1.xaxis.set_major_locator(mticker.FixedLocator(x))
                xaxis_labels = most_comm_dic.keys()
                ax1.xaxis.set_major_formatter(mticker.FixedFormatter(xaxis_labels))
                ax1.set_xticklabels(xaxis_labels)
             else:
                pps = bar_chart(arr_tsv,ax1,i,order)
          if do_hist==0:
             percentage_on_bins(ax1,pps)
          ax1.set_title(arr_tsv[0,i].decode('cp1252'))
          #add age range label
          custom_label = 'Eta ['+str(age)+'-'+str(agemax)+'] anni'
          leg = ax1.legend(title=custom_label)
          yax_lim = ax1.get_ylim()
          ax1.text(-0.05, yax_lim[1]*1.1,'Ladispoli Attiva*', size=15, color='black',fontstyle='italic')
          ax1.set_ylim(yax_lim[0],yax_lim[1]*1.2)
          if i==1:
             y_pos_text = -7
          elif i==6 or i==5 or i==41 or i==4:
             y_pos_text = yax_lim[0]-40
          elif i==13 or i==22:
             y_pos_text = yax_lim[0]-20
          else:
             y_pos_text = yax_lim[0]-27
          ax1.text(-0.05, y_pos_text,'*dati raccolti tra il 25/06/2021 e il 13/09/2021', size=5, color='black',fontstyle='italic')
          #########################
          #UNCOMMENT FOR THE LOGO
          #im = image.imread('./LA_logo.pdf')
          #imagebox = OffsetImage(im, zoom=0.025)
          #ab = AnnotationBbox(imagebox, (-0.02, yax_lim[1]*1.1))
          #ax1.add_artist(ab)
          #########################
          plt.draw()
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

def split_gender(data,gender,order, isAge,arr_tsv):
   age_values = np.array(arr_tsv[1:,1],dtype=int)
   data_f = data[(gender==b'femminile') & (age_values>=age) & (age_values<agemax)]
   data_m = data[(gender==b'maschile') & (age_values>=age) & (age_values<agemax)]
   cnt_data_f = Counter(data_f)
   cnt_data_m = Counter(data_m)
   if isAge:
      ordered_data_f = group_age_data(cnt_data_f,order)
      ordered_data_m = group_age_data(cnt_data_m,order)
   else:
      ordered_data_f = {ans:cnt_data_f[ans] for ans in order}
      ordered_data_m = {ans:cnt_data_m[ans] for ans in order}
      ordered_data_f=ordered_data_f.values()
      ordered_data_m=ordered_data_m.values()
   return ordered_data_f,ordered_data_m

def check_order(i):
   do_hist = 0
   if (i>=9 and i<=14) or (i>=16 and i<=25) or (i==28) or (i>=40 and i!=41):
      order = [b"non so", b"per nulla",b"poco",b"abbastanza",b"molto"]
   elif i>=29 and i<=31: 
      order = [b"1", b"2",b"3",b"4",b"5"]
   elif (i>=32 and i<=38):
      order = [b"per nulla",b"poco",b"abbastanza",b"molto"]
   elif (i==7):
      order = [b"centro",b"cerreto",b"domitilla",b"palo laziale",b'miami',b'ex campo sportivo',b'monteroni/boietto',b'lungomare']
   elif (i==8):
      order = [b'Roma',b'Ladispoli',b'Altri comuni limitrofi',b'Altro']
   elif (i==41):
      order = [b'si',b'no',b'forse']
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
   pps = ax1.bar(x-w,grouped_data,label='inclusivo',width=w) 
   #gender split
   if gender_opt==True:
      add_gender_bars(arr_tsv,data,age_bins,True,ax1,x)
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
   pps = ax1.bar(x-w,ordered_data.values(),label='inclusivo',width=w) 
   #gender split
   if gender_opt==True:
      add_gender_bars(arr_tsv,data,order,False,ax1,x)
   xaxis = np.array(order,dtype=str)
   if i>=29 and i<=31: 
      if i==29:
         age_bins_label = ['1 (sicura)','2','3','4','5 (insicura)']
      elif i==30:
         age_bins_label = ['1 (bella)','2','3','4','5 (brutta)']
      elif i==31:
         age_bins_label = ['1 (ospitale)','2','3','4','5 (ostile)']
      xaxis = np.array(age_bins_label,dtype=str)
   #this prevents the x-labels to be cropped
   ax1.xaxis.set_major_locator(mticker.FixedLocator(x))
   ax1.xaxis.set_major_formatter(mticker.FixedFormatter(xaxis))
   ax1.set_xticklabels(xaxis)
   return pps

def apply_age_cut(arr_tsv,data):
   age_values = np.array(arr_tsv[1:,1],dtype=int)
   data_age = data[(age_values>=age) & (age_values<agemax)]
   return data_age

def add_gender_bars(arr_tsv,data,order,isAge,ax1,x):
   gender = np.array(arr_tsv[1:,2])
   ordered_data_f, ordered_data_m = split_gender(data,gender,order,isAge,arr_tsv)
   ax1.bar(x,ordered_data_f,color='lightpink',label='femminile',width=w)
   ax1.bar(x+w,ordered_data_m,color='cornflowerblue',label='maschile',width=w)

def percentage_on_bins(ax1,pps):
  sum_of_answers = 0
  for p in pps:
     height = p.get_height()
     sum_of_answers+=height
  for p in pps:
     height_perc = round(100*p.get_height()/sum_of_answers,1)
     ax1.text(x=p.get_x() + p.get_width() / 2, y=p.get_height()+.10,
                s="{}%".format(height_perc),
                ha='center')
# __main__
if __name__ == '__main__':
  main()
