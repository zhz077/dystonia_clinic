import sys
import os
import csv 
import numpy as np
import pandas as pd

#run after postprocess
def main():
    for root, dirs, files in os.walk('processed'):
        with open("numberofRepeated.csv",'w') as csvf:
            counter =0;
            for f in files:
                df = pd.read_csv(os.path.join(root,f),sep='\t')
                fields = ["patient","reviewer"]
                for i in df.stepnumber:
                    fields.append(i)
                writer = csv.DictWriter(csvf,fieldnames = fields)
                if counter == 0:
                    writer.writeheader() 
                    counter =1              
                dc = {}
                dc['patient'] =  f.split('.')[0]
                dc['reviewer'] = df.reviewer1[0]
                for i in range(len(df.stepnumber)):
                    if pd.isnull(df.start1[i]):
                       dc[df.stepnumber[i]] = 0
                    else:
                        dc[df.stepnumber[i]] = len(str(df.start1[i]).split(" "))
                writer.writerow(dc)
                dc['reviewer'] = df.reviewer2[0]
                for i in range(len(df.stepnumber)):
                    if pd.isnull(df.start2[i]):
                       dc[df.stepnumber[i]] = 0
                    else:
                        dc[df.stepnumber[i]] = len(str(df.start2[i]).split(" "))
                writer.writerow(dc)                
                
if __name__=="__main__":
    main() 
