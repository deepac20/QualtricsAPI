import os
import glob
import pandas as pd

dir = os.getcwd()
os.chdir(dir + "/MyQualtricsDownload")
extension = "csv"

all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# export to csv
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

Module = [];
Week = [];
for file in all_filenames:
    print file
    Module.append("HTN" in file and "HTN" or "PPT")
    fname = file.strip("TechSuPPort_-HTN_-_")
    fname = fname.replace(' - Copy','')
    fname = fname.replace(' + INTRO','')
    os.rename(file,fname)
    Week.append(file[5:6])

#print Module
#print Week

#for w in Week:


