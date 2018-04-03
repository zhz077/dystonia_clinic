import sys
import os
import argparse
import tempfile
import subprocess
import cv2
#notice run this under OpenFace folder where bin folder locates
def seg(vi,vi_name):
    newpath =os.path.abspath( r"/Volumes/Sirius/openface/%s"%vi_name)
    print(newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    vidcap = cv2.VideoCapture(vi)
    success,image = vidcap.read()
    count = 0
    success = True
    while success:
        cv2.imwrite("%s/frame%d.jpg" %(newpath,count), image)  
        success,image = vidcap.read()
        count = count+1
    return newpath

    
def main():
    print("enter")
    parser = argparse.ArgumentParser(description='Running wrapper')
    parser.add_argument('input_dir', help='input_dir')

    args = parser.parse_args()
    input_dir =args.input_dir

    execute_script_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    if (os.path.isfile(input_dir)):
         print("yes!")   
         path = seg(input_dir,"singleVideo1")
         cmd  = "/Users/apple/Developer/OpenFace-master/bin/FaceLandmarkImg -fdir %s"%(path)
         execute_script_file.write(cmd+"\n")
    else:    
        for root, dirs, files in os.walk(input_dir):        
            for name in files:
                path = seg(os.path.join(root, name),name.split(".")[0])
                cmd = "./bin/FaceLandmarkImg -fdir %s"%(path)
                execute_script_file.write(cmd+"\n")
    execute_script_file.close()
    
    cmd = "sh %s"%(execute_script_file.name)
    os.system(cmd);
    os.unlink(execute_script_file.name)

if __name__=="__main__":
    main()
