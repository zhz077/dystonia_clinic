import sys
import os
import csv 
import argparse

def sortfunc(r):
    return int (r[0])
def main():

    parser = argparse.ArgumentParser(description='run csv builder')
    parser.add_argument('p_processed', help='p_processed')
    args = parser.parse_args()
    p_processed= args.p_processed
   
    df = []
    header = []
    filecounter =0
    maxFrame = -1
    for root, dirs, files in os.walk(p_processed):
        for d in dirs:
            if len(d.split('_')) !=1:
                dframe = int(d.split('_')[0].split('frame')[1])
                if dframe > maxFrame:
                    maxFrame = dframe            
        for f in files:
            if len(f.split('csv')) != 1 and len(f.split('.')) <3:
                #print (f)
                face = f.split('.csv')[0].split('frame')[1]
                #print (face)
                csvFile = open(os.path.join(root,f),'r')
                reader = csv.reader(csvFile, delimiter=',')
                firstrow = 1;
                filecounter = filecounter+1
                for row in reader:
                    if filecounter ==1 and firstrow ==1:
                        firstrow = 0;
                        header = row
                        continue
                    if filecounter != 1  and firstrow ==1:
                        firstrow =0;
                        continue
                    row[0] =int(face);
                    df.append(row)

    df = sorted(df,key=sortfunc)
    for r in df:
        print(r[0],' ')
    missing = []
    pos = 0;
    for row in df:
        while row[0] != pos:
            missingRow=[]
            for i in range(len(row)):
               missingRow.append('n/a')
            missingRow[0] = pos
            missing .append(missingRow)
            pos = pos+1
        pos = pos+1

    while  pos <= maxFrame:
        missingRow=[]
        for i in range(len(row)):
            missingRow.append('n/a')
        missingRow[0] = pos
        missing .append(missingRow)
        pos = pos+1

    df = df+missing
    df = sorted(df,key=sortfunc)
    df = [header]+df
    with open ('summary.csv','w') as result:
        writer = csv.writer(result,delimiter=',')
        writer.writerows(df)

if __name__=="__main__":
    main()                        
                        
