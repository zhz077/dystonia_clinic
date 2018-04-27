import sys
import os
import csv 
import numpy as np
import pandas as pd

#run after postprocess
def main():
    for root, dirs, files in os.walk('processed'):
        with open("numberofInstances.csv",'w') as csvf:
            with open ("repeated steps.csv", 'w') as repeated:
                counter =0;
                for f in files:
                    df = pd.read_csv(os.path.join(root,f),sep='\t')
                    fields = ["patient","reviewer"]
                    for i in df.stepnumber:
                        fields.append(i)
                    writer = csv.DictWriter(csvf,fieldnames = fields)
                    writerRepeated = csv.DictWriter(repeated,fieldnames=['patient','step','reviewer1','reviewer2','R1 #repeats','R2 #repeats','interval1','interval2'])
                    if counter == 0:
                        writer.writeheader()
                        writerRepeated.writeheader() 
                        counter =1              
                    dc = {}
                    dcrepeated = {}
                    dc['patient'] =  f.split('.')[0]
                    dcrepeated['patient'] =  f.split('.')[0]
                    for i in range(len(df.stepnumber)):
                        if pd.isnull(df.start1[i]):
                            dc[df.stepnumber[i]] = 0
                        else:
                            dc['reviewer'] = df.reviewer1[i]
                            dcrepeated ['reviewer1'] = df.reviewer1[i]
                            dcrepeated ['step'] = df.stepnumber[i]
                            dcrepeated ['R1 #repeats'] = len(str(df.start1[i]).split(" "))
                            dcrepeated ['reviewer2'] = df.reviewer2[i]
                            dcrepeated ['R2 #repeats'] = len(str(df.start2[i]).split(" "))
                            dcrepeated['interval1'] = []
                            dcrepeated['interval2'] = []
                            interliststart1 = str(df.start1[i]).split(" ")
                            interliststart2 = str(df.start2[i]).split(" ")
                            interlistend1 =  str(df.end1[i]).split(" ")
                            interlistend2 = str(df.end2[i]).split(" ")
                            for i in range(len(interliststart1)):
                                dcrepeated['interval1'].append('->'.join([interliststart1[i],interlistend1[i]]))
                            for i in range(len(interliststart2)):
                                dcrepeated['interval2'].append('->'.join([interliststart2[i],interlistend2[i]]))
                            dc[df.stepnumber[i]] = len(str(df.start1[i]).split(" "))
                            dcrepeated['interval1'] = ' '.join(dcrepeated['interval1'])
                            dcrepeated['interval2'] = ' '.join(dcrepeated['interval2'])
                            if len(interliststart1) >1  or len(interliststart2) >1:
                                writerRepeated.writerow(dcrepeated)
                    writer.writerow(dc)
                    for i in range(len(df.stepnumber)):
                        if pd.isnull(df.start2[i]):
                            dc[df.stepnumber[i]] = 0
                        else:
                            dc['reviewer'] = df.reviewer2[i]
                            dc[df.stepnumber[i]] = len(str(df.start2[i]).split(" "))
                    writer.writerow(dc)                
                
if __name__=="__main__":
    main() 
