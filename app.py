#!/usr/bin/env python3
import requests
import json
import os
import sys

if len(sys.argv) < 2:
    print("Please provide a destination section from your configfile")
    exit()

destination_orthanc = sys.argv[1] #"living-lab-gateway" #"c0100-orthanc.curapacs.ch"

try:
    with open("/home/schumi/Bachelor/secrets/orthanc-secret.json","r") as secretstore:
        data = json.load(secretstore)
        http_credentials = data.get(destination_orthanc,None)
        http_hostname = http_credentials.get("http_hostname")
        http_username = http_credentials.get("user")
        http_password = http_credentials.get("password")
except FileNotFoundError:
    with open("C:/Users/taadrar1/Documents/secrets.txt","r") as secretstore:
        data = json.load(secretstore)
        http_credentials = data.get(destination_orthanc, None)
        http_hostname = http_credentials.get("http_hostname")
        http_username = http_credentials.get("user")
        http_password = http_credentials.get("password")


response = requests.get(f"{http_hostname}/patients", auth=(http_username, http_password))
#response.content (== body ) --> what you get from the get request + status
print((response.status_code))
# bytestring --> so you try to get response.json() --> you get list of strings of orthanc patient ids
# json.loads(response.content) --> so you get back from the server a structured DATA
orthanc_patient_uids = json.loads(response.content)

for uid in orthanc_patient_uids:
    delete_response = requests.delete(f"{http_hostname}/patients/{uid}", auth=(http_username, http_password)) 

# see the remaining patients --> so you dont have to go over the stauts reports
remaining_patients_response = requests.get(f"{http_hostname}/patients", auth=(http_username, http_password))
print(remaining_patients_response.json())

# iterate over directories, subdirectories and so on
# with open(image_path, "rb") as dicom_file:
#         requests.post("/instances", data=dicom_file, headers={"Content-Type": "application/dicom"}, timeout=timeout)

# /home/schumi/lc2/testdaten/bachelor_testdaten
for subdir, dirs, files in os.walk(r'/home/schumi/lc2/testdaten/bachelor_testdaten'):
    for filename in files:
        filepath = subdir + os.sep + filename
        
        if filepath.endswith(".dcm"):  
            # line 47 is called context manager its like an if statement (first it opens the file, reads it and after it closes the file)
            with open(filepath, "rb") as dicom_file:
                requests.post(f"{http_hostname}/instances", auth=(http_username, http_password), 
                                data=dicom_file, headers={"Content-Type": "application/dicom"})
            print (filepath)


 
