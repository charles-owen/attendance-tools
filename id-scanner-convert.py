"""
Convert the output of an ID scanner to files suitable for uploading to
online systems such as D2L.

Generates a CSV files suitable for D2L and other systems with
the name and PID. If the class list is loaded, the output includes
the names from the class list and MSU net ID

Based on code provided by Sebnum Onsay as used in CSE 331

Usage:
    id-scanner-convert [--d2l=<d2l>] [--include-z] [--class-list=<class-list>...] [--absent=<absent-file>] <files>...

Options:
    <files>                     Files to convert
    --d2l=<d2l>                 Create a .csv file suitable for uploading to D2L and other systems
    --include-z                 Include any Z PID values (default: false)
    --class-list=<class-list>   Specifies a class list ot load
    --absent=<absent-list>      Absent students (requires --class-list)
"""

import os
from docopt import docopt
import pandas as pd


class IdScannerConverter(object):
    def __init__(self, args):
        # Files to convert
        self._files = args['<files>']

        # Any D2L output?
        self._d2l = args['--d2l']

        self._include_z = args['--include-z']

        self._class_lists = args['--class-list']

        self._absent = args['--absent']

        # Will store the data from the input files
        self._data = []

        # Students who are attending
        self._attending = []

        # Where we store the class list data after loading
        self._class_list_data = {}

    def convert(self):
        # Read the input files
        for file in self._files:
            extension = os.path.splitext(file)[1]
            if extension == '.txt':
                self._read_txt(file)

            elif extension == '.xlsx':
                self._read_xlsx(file)

        for class_list in self._class_lists:
            self._read_class_list(class_list)

        #
        # Iterate over the data, extracting the PID from each line
        #
        for whole_string in self._data:

            # Means it was done using the card reader
            if whole_string[0] == "%": 
                row_split = whole_string.split("^")
                # Extract the name
                name = row_split[1].strip()
                index_to_pid = 7
                # index_to_pid = row_split[2].find("A") #FInd where the A is in the string for APID
                # Extract the PID
                apid = row_split[2][index_to_pid:index_to_pid+9].strip()
                if apid[0] != 'Z' or self._include_z:
                    # Do we have the class list?
                    if len(self._class_list_data) > 0:
                        # Convert APID to PID
                        pid = '1' + apid[1:]

                        if pid in self._class_list_data:
                            student = self._class_list_data[pid]
                            name = student['name']
                            self._attending.append((name, apid, pid, student['net_id']))
                            student['present'] = True
                    else:
                        self._attending.append((name, apid))
            else:
                # We did not get the info using card reader, so we leave it as is
                # This allows a name to be manually added to the file
                name = whole_string
                self._attending.append((name, "No PID Available"))

        #
        # Output the result
        #
        if self._d2l is not None:
            self._write_d2l(self._d2l)

    def _write_d2l(self, filename):
        if len(self._class_lists) == 0:
            df = pd.DataFrame(self._attending, columns=["Name", "APID"])
            df.to_csv(filename, index=False)
        else:
            df = pd.DataFrame(self._attending, columns=["Name", "APID", "PID", "NET_ID"])
            df.to_csv(filename, index=False)

            if self._absent is not None:
                absent = []
                for pid in self._class_list_data:
                    student = self._class_list_data[pid]
                    if not student['present']:
                        absent.append(( student['name'], pid, student['net_id']))

                df = pd.DataFrame(absent, columns=["Name", "PID", "NET_ID"])
                df.to_csv(self._absent, index=False)

        print(f"Successfully generated {filename}")

    def _read_txt(self, file):
        with open(file, 'r') as f:
            for line in f:
                self._data.append(line)

    def _read_xlsx(self, file):
        df = pd.read_excel(file, header=None)
        for row in df.values:
            self._data.append(row[0])

    def _read_class_list(self, class_list):
        df = pd.read_csv(class_list, index_col=False)
        for row, data in df.iterrows():
            pid = str(data['Student_ID']).strip()
            name = str(data['Student_Name']).strip()
            net_id = str(data['MSUNet_ID']).strip()
            self._class_list_data[pid] = {'name': name, 'net_id': net_id, 'present': False}


if __name__ == '__main__':
    args = docopt(__doc__)
    # print(args)

    converter = IdScannerConverter(args)
    converter.convert()



