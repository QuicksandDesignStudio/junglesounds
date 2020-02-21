from prettytable import PrettyTable
from datetime import datetime
import os

object_list = []

PATH = "audio/audio"
x = PrettyTable()
all_files = os.listdir(PATH)
x.field_names = ["#", "Filename", "Filesize in KB", "Date & Time"]

for i in all_files:
    object_list.append({'name': str(i), 'size': os.path.getsize(
        PATH+"/"+i), 'datetime': datetime.fromtimestamp(int(i.split(".")[0]))})

object_list.sort(key=lambda r: r["datetime"])

counter = 1
for i in object_list:
    x.add_row([counter, i["name"], i["size"], i["datetime"]])
    counter += 1

print(x)
