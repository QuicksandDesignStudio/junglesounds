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
