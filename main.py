# Python 2.7

import requests
import zipfile
import json
import io



coachman_surveyid = ["SV_1Y6KITcfdDhDxzf","SV_5AXohDSPN0nRFzv","SV_3XmGCUidoKUB6Yd","SV_86vGUl5C11oL2Yd",
                     "SV_3dZm5NnigVR35n7","SV_7PdiL93lIhl1n37"]
#Intervention survey ids
techsupport_surveyidI = ["SV_bQNtPmy7DLiJMR7","SV_d7pEOjmSwoaOyl7","SV_1RMYw7EF1Xjnkr3","SV_9HRkRYLyvMDueC9",
                        "SV_b8ZNGcVEiYZbxjv","SV_0TmZRjJFTfHYdhP","SV_0IzHtl6hEhDSTIh",
                        "SV_9KrN32YcytCuZPn","SV_0HhLMRamxhwLI5D","SV_3dADbHE1XIFsUmh","SV_9zaWaPKj2aX6YHr",
                        "SV_0AmO4LTg8l59xfD"]

#controlled survey ids
techsupport_surveyidC = ["SV_5mr1oIM6xbyP1CB","SV_aaOLypw2xdJAvch","SV_3jxd6fUaExvzg3j","SV_es4qEccWBqj92IJ",
                         "SV_e4A1l3Z19TRDgzj","SV_9ZCeivMpURLjglT"]
# Setting user Parameters
apiToken = raw_input("Enter token")
#surveyId = techsupport_surveyid
fileFormat = "csv"
dataCenter = 'cwru.az1'

# Setting static parameters
requestCheckProgress = 0
progressStatus = "in progress"
baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/".format(dataCenter)
headers = {
    "content-type": "application/json",
    "x-api-token": apiToken,
    }
for surveyId in techsupport_surveyidC:

    # Step 1: Creating Data Export
    downloadRequestUrl = baseUrl
    downloadRequestPayload = '{"format":"' + fileFormat + '","surveyId":"' + surveyId + '"}'
    downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
    progressId = downloadRequestResponse.json()["result"]["id"]
    print downloadRequestResponse.text

    # Step 2: Checking on Data Export Progress and waiting until export is ready

    isFile = None
    #print("download req payload: "+ str(downloadRequestPayload))

    while requestCheckProgress < 100 and progressStatus is not "complete" and isFile is None:
        requestCheckUrl = baseUrl + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        isFile = (requestCheckResponse.json()["result"]["file"])
        if isFile is None:
            print  "file not ready"
        else:
            print  "file created:", requestCheckResponse.json()["result"]["file"]
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        #print "Download is " + str(requestCheckProgress) + " complete"

    # Step 3: Downloading file
    requestDownloadUrl = baseUrl + progressId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)
    #print ("req download: "+ str(requestDownload))
# Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall("MyQualtricsDownload")
    print('Complete')

