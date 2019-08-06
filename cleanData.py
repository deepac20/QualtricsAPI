import os
import glob
import pandas as pd

dir = os.getcwd()
os.chdir(dir + "/MyQualtricsDownload/TechSupport Intervention")
extension = "csv"

all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# export to csv
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')


#print all_filenames
for i,file in enumerate(all_filenames):
 #   print file
    module = "HTN" in file and "HTN" or "PPT"
    fname = file.strip("TechSuPPort_-HTN_-_")
    fname = fname.replace(' + INTRO','')
    os.rename(file,fname)
    all_filenames[i] = fname
    week = fname[6:7]
    df = pd.read_csv(fname)
    df['Module'] = module
    df['Week'] = week
    df = df.drop(df.index[[0,1]],axis=0)
    df_subset = df[['Module','Week','ResponseID','StartDate','EndDate','RecipientFirstName','RecipientLastName','RecipientEmail','Finished','Status']]
    df_subset = df_subset[df_subset.Status == '0']
    fsub = fname.strip(".csv")
    fsub = fsub + "_sub.csv"
    df_subset.to_csv(fsub,index=False)