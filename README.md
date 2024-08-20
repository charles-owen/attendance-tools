# Attendance tools for use with ID card readers

The id-scanner-convert program converts the output of commercial ID card readers to .csv files
suitable for loading into D2L or other system. 

To convert card reader files to a .csv file suitable for loading into D2L:

    python id-scanner-convert.py --d2l="result.csv" id-card-data.txt

Data can be in .txt or .xlsx files and there can be more than one file:

    python id-scanner-convert.py --d2l="result.csv" id-card-data1.txt id-card-data2.txt id-card-data3.txt

These examples assume the script is copied into the same directory as the files. 