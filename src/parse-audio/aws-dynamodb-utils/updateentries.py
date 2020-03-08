"""
This is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

Copyright (c) 2020 Romit Raj
Copyright (c) 2020 Thejesh GN 
"""

import sys
import os
import json
import decimal
import urllib.request
import boto3
from boto3.dynamodb import table

CREDS_PATH = "../creds.secret"
FOLDER_PATH = "../../recorder-app/audio/audio"
RECORDS_PATH = "https://junglesounds.s3-ap-southeast-1.amazonaws.com/analysis/records.txt"

all_samples = os.listdir(FOLDER_PATH)
all_parsed_files = []


with open(CREDS_PATH) as f:
    temp = f.readlines()
    API_KEY, API_SECRET = [lines.strip() for lines in temp]

session = boto3.Session(
    aws_access_key_id=API_KEY,
    aws_secret_access_key=API_SECRET
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('sample_collection')

# get the records file with all parsed files listed
request = urllib.request.Request(RECORDS_PATH)
textrecords = urllib.request.urlopen(request)

# save it as a temporary file
FILE = "~temprecords~.txt"
file = open(FILE, 'wb')
file.write(textrecords.read())
file.close()

# open the temporary file and read in the lines
with open(FILE) as f:
    all_parsed_files = f.readlines()
    all_parsed_files = [lines.strip() for lines in all_parsed_files]

os.remove(FILE)


def main():
    for parsed_file in all_parsed_files:
        fileName = parsed_file.split("-")[0]
        validation = int(parsed_file.split("-")[1])

        response = table.update_item(
            Key={
                'sample_file_name': fileName
            },
            UpdateExpression="set validation = :r",
            ExpressionAttributeValues={
                ':r': validation
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Updated : {}".format(fileName))


if (__name__ == '__main__'):
    main()
