# Attendance tools for use with ID card readers

The id-scanner-convert program converts the output of commercial ID card readers to .csv files
suitable for loading into D2L or other system. 

To convert card reader files to a .csv file suitable for loading into D2L:

    python id-scanner-convert.py --d2l="result.csv" id-card-data.txt

Data can be in .txt or .xlsx files and there can be more than one file:

    python id-scanner-convert.py --d2l="result.csv" id-card-data1.txt id-card-data2.txt id-card-data3.txt

These examples assume the script is copied into the same directory as the files. 

Output consists of a .csv file with two columns: Name and APID. For example:

    Name,APID
    VULNAVIA,A58429522
    VESALIUS/JOSEPH,A85622542
    LONGSTREET/TERRY,A13241688
    VESALIUS/LEM,A50548529
    ALLEN/SUSAN,A63486880

## Using class lists

You can add one or more class lists to the command using the --class-lists option:

    python id-scanner-convert.py --d2l="result.csv" --class-list=CSE335.csv id-card-data.txt

Class lists are as exported by instructor systems. When a class list is provided the output will 
be 4 columns, adding PID and NET_ID. The name in the output will be replace with 
the name from the class list.

    Name,APID,PID,NET_ID
    Vulnavia,A58429522,158429522,vulnav84
    "Vesalius, Joseph",A85622542,185622542,vesali59
    "Longstreet, Terry",A13241688,113241688,longst41
    "Vesalius, Lem",A50548529,150548529,vesali61
    "Allen, Susan",A63486880,163486880,allensu

Adding the --absent option will export a list of all students in the class list who 
do not appear in the card reader data file:

python id-scanner-convert.py --d2l="result.csv" --class-list=CSE335.csv --absent="absent.csv" id-card-data.txt
