import os
import pandas as pd


class CleanData:
    def __init__(self, p,all_files):
        self.path = p
        self.all_file_names = all_files

    def rename_files(self):
        for i, file in enumerate(self.all_file_names):
            module = "HTN" in file and "HTN" or "PPT"
            if module=="HTN":
                file_name = file.replace("TechSuPPorT_-_HTN_-_", 'HTN_')
            else:
                file_name = file.replace("TechSuPPorT_-_PPT_-_", 'PPT_')
            file_name = file_name.replace(' + INTRO', '')
            file_name = file_name.replace(' + Intro', '')
            os.rename(file, file_name)
            self.all_file_names[i] = file_name
            week = [x.isdigit() for x in file_name].index(True)
            df = pd.read_csv(file_name)
            df['Module'] = module
            df['Week'] = file_name[week]
            # remove duplicate row (header and first row were same)
            df = df.drop(df.index[[0, 1]], axis=0)
            df_subset = df[df.Status=='0']  # remove rows with Status = 1
            # creating subset of data
            col = ['Module', 'Week', 'StartDate', 'EndDate', 'RecipientFirstName', 'RecipientLastName',
                   'RecipientEmail',
                   'Status', 'Progress', 'Finished', 'Duration (in seconds)', 'LocationLatitude', 'LocationLongitude']
            df_subset = df_subset[col]
            # remove rows for which names are empty
            df_subset = df_subset[~df_subset['RecipientFirstName'].isnull()]
            df_subset.to_csv(file_name, index=False)

    def merge_files(self):
        all_data = pd.DataFrame()
        for file in self.all_file_names:
            data = pd.read_csv(file)
            all_data = all_data.append(data, sort=False)
        all_data.to_csv("Combined.csv", index=False)

    def remove_duplicates(self):
        data = pd.read_csv("Combined.csv")
        data['StartDate'] = pd.to_datetime(data['StartDate'])
        new_data = pd.DataFrame()
        pd.set_option('display.max_columns', 30)
        for email in set(data['RecipientEmail']):
            df = data.loc[data['RecipientEmail']==email]
            weeks = set(df['Week'])
            modules = set(df['Module'])
            c = list(df.columns)
            c.remove('LocationLatitude')
            c.remove('LocationLongitude')
            for module in modules:

                for week in weeks:
                    subset = df.loc[(df['Module']==module) & (df['Week']==week)]
                    if subset.shape[0]==1:
                        new_data = new_data.append(subset)

                    else:
                        if subset.loc[subset['Finished']==1].shape[0]==1:
                            new_data = new_data.append(subset.loc[subset['Finished']==1])
                        elif subset.loc[subset['Finished']==1].shape[0] > 1:
                            s_subset = subset.loc[subset['Finished']==1]
                            max_date = max(list(s_subset['StartDate']))
                            new_data = new_data.append(s_subset.loc[s_subset['StartDate']==max_date])
                        elif subset.loc[subset['Finished']==0].shape[0]==1:
                            new_data = new_data.append(subset.loc[subset['Finished']==0])
                        else:
                            s_subset = subset.loc[subset['Finished']==0]
                            dates = list(pd.to_datetime(s_subset['StartDate']))
                            if len(dates)!=0:
                                max_date = max(list(pd.to_datetime(s_subset['StartDate'])))
                                new_data = new_data.append(s_subset.loc[s_subset['StartDate']==max_date])
        new_data.to_csv("Cleaned.csv", index=False)

    def get_id(self, study, group):
        if group == 'Intervention' and study == 'TechSupport':
            all_modules = ['HTN 1', 'HTN 2', 'HTN 3', 'HTN 4', 'HTN 5', 'HTN 6', 'PPT 1', 'PPT 2', 'PPT 3', 'PPT 4',
                           'PPT 5', 'PPT 6', ]
        elif group == 'Intervention' and study == 'Coachman':
            all_modules = ['HTN 1', 'HTN 2', 'HTN 3', 'HTN 4', 'HTN 5', 'HTN 6']
        elif group == 'Controlled' and study == 'TechSupport':
            all_modules = ['HTN 1', 'HTN 2', 'HTN 3', 'HTN 4', 'HTN 5', 'HTN 6']
        else:
            all_modules = ['HTN 2']
        log = [[]]
        data = pd.read_csv("Cleaned.csv")
        for email in set(data['RecipientEmail']):
            temp = [None] * 4
            completed_module = []
            subset = data.loc[data['RecipientEmail'] == email]
            pname = str(subset['RecipientFirstName']).split()[1] + " " + str(subset['RecipientLastName']).split()[1]
            for module in subset['Module']:
                for week in subset['Week']:
                    module_week = module + " " + str(week)
                    completed_module.append(module_week)
            completed_module = set(completed_module)
            incomplete_modules = list(set(all_modules) - set(completed_module))
            temp[0] = pname
            temp[1] = study
            temp[2] = group
            if len(incomplete_modules) == 0:
                temp[3] = "None"
            else:
                temp[3] = incomplete_modules
            if len(log) == 0:
                log[0]=temp
            else:
                log.append(temp)
        out = pd.DataFrame(log)
        out.columns = ['Patient Name', 'Study','Group', 'Incomplete Modules']
        print(out)
        dest = self.path + "/Patient Reminder/{}_{}".format(study, group) + ".csv"
        out.to_csv(dest, index=False)
