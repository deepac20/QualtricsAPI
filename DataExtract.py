# Python 3

import requests
import zipfile
import io
import os
import shutil

class DataExtract:
    path = ''
    coachman_surveyId = {}
    techsupport_surveyId = {}
    apiToken = ''
    fileFormat = ''
    dataCenter = ''

    def __init__(self,path):
        self.path = path
        self.coachman_surveyId = {'SV_1Y6KITcfdDhDxzf': 'Intervention', 'SV_5AXohDSPN0nRFzv': 'Intervention',
                                  'SV_3XmGCUidoKUB6Yd': 'Intervention', 'SV_86vGUl5C11oL2Yd': 'Intervention',
                                  'SV_3dZm5NnigVR35n7': 'Intervention', 'SV_7PdiL93lIhl1n37': 'Intervention',
                                  'SV_5zPnMfJiXFkW9aR': 'Controlled'}

        self.techsupport_surveyId = {"SV_bQNtPmy7DLiJMR7": "Intervention", "SV_d7pEOjmSwoaOyl7": "Intervention",
                                "SV_1RMYw7EF1Xjnkr3": "Intervention",
                                "SV_9HRkRYLyvMDueC9": "Intervention", "SV_b8ZNGcVEiYZbxjv": "Intervention",
                                "SV_0TmZRjJFTfHYdhP": "Intervention",
                                "SV_0IzHtl6hEhDSTIh": "Intervention", "SV_9KrN32YcytCuZPn": "Intervention",
                                "SV_0HhLMRamxhwLI5D": "Intervention",
                                "SV_3dADbHE1XIFsUmh": "Intervention", "SV_9zaWaPKj2aX6YHr": "Intervention",
                                "SV_0AmO4LTg8l59xfD": "Intervention",
                                "SV_5mr1oIM6xbyP1CB": "Controlled", "SV_aaOLypw2xdJAvch": "Controlled",
                                "SV_3jxd6fUaExvzg3j": "Controlled",
                                "SV_es4qEccWBqj92IJ": "Controlled", "SV_e4A1l3Z19TRDgzj": "Controlled",
                                "SV_9ZCeivMpURLjglT": "Controlled"}
        self.apiToken = raw_input('Enter token: ')
        self.fileFormat = 'csv'
        self.dataCenter = 'cwru.az1'
        self.p = self.path+"/Patient Reminder"
        if os.path.exists(self.p):
            shutil.rmtree(self.p)
            os.mkdir(self.p)
            os.mkdir(self.p+"/MyQualtricsDownload")
        else:
            os.mkdir(self.p)
            os.mkdir(self.p + "/MyQualtricsDownload")
        self.p=self.p+"/MyQualtricsDownload"
        self.filedownload(self.techsupport_surveyId,'TechSupport')
        self.filedownload(self.coachman_surveyId,'Coachman')

    def filedownload(self, survey, study):
        dest_path = self.p +"/" +study
        for surveyId, group in survey.items():
            # Setting static parameters
            requestCheckProgress = 0.0
            progressStatus = "inProgress"
            baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(self.dataCenter, surveyId)
            headers = {
                "content-type": "application/json",
                "x-api-token": self.apiToken,
            }

            # Step 1: Creating Data Export
            downloadRequestUrl = baseUrl
            downloadRequestPayload = '{"format":"' + self.fileFormat + '"}'
            downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload,
                                                       headers=headers)
            progressId = downloadRequestResponse.json()["result"]["progressId"]
            print(downloadRequestResponse.text)

            # Step 2: Checking on Data Export Progress and waiting until export is ready
            while progressStatus != "complete" and progressStatus != "failed":
                print ("progressStatus=", progressStatus)
                requestCheckUrl = baseUrl + progressId
                requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
                requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
                print("Download is " + str(requestCheckProgress) + " complete")
                progressStatus = requestCheckResponse.json()["result"]["status"]

            # step 2.1: Check for error
            if progressStatus is "failed":
                raise Exception("export failed")

            fileId = requestCheckResponse.json()["result"]["fileId"]

            # Step 3: Downloading file
            requestDownloadUrl = baseUrl + fileId + '/file'
            requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

            # Step 4: Unzipping the file
            if group == "Intervention":
                zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall(
                    dest_path+"/Intervention")
                print('Complete')
            else:
                zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall(
                    dest_path+"/Controlled")
                print('Complete')
        return None
