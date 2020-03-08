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
import boto3
from boto3.dynamodb import table

CREDS_PATH = "../creds.secret"
FOLDER_PATH = "../../recorder-app/audio/audio"

all_samples = os.listdir(FOLDER_PATH)


with open(CREDS_PATH) as f:
    temp = f.readlines()
    API_KEY, API_SECRET = [lines.strip() for lines in temp]

session = boto3.Session(
    aws_access_key_id=API_KEY,
    aws_secret_access_key=API_SECRET
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('sample_collection')


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def main():
    global table
    counter = 1
    for batches in chunker(all_samples, 25):
        items = []
        for fileName in batches:
            items.append({
                'sample_file_name': fileName,
                'validation': 0
            })
        with table.batch_writer() as batch:
            for r in items:
                batch.put_item(Item=r)
        print("Batch complete {}".format(counter))
        counter += 1


if (__name__ == '__main__'):
    main()
