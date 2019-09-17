import os
import DataExtract
import CleanData
import glob

if __name__ == "__main__":
    path = os.getcwd()
    m = DataExtract.DataExtract(path)
    for Study in ['TechSupport', 'Coachman']:
        for Group in ['Intervention','Controlled']:
            os.chdir(path + "/MyQualtricsDownload/{}/{}".format(Study,Group))
            extension = "csv"
            all_file_names = [i for i in glob.glob('*.{}'.format(extension))]
            cd = CleanData.CleanData(path, all_file_names)
            cd.rename_files()
            cd.merge_files()
            cd.remove_duplicates()
            cd.get_id(Study,Group)