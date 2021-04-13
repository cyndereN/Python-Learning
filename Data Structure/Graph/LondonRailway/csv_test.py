import csv
with open('londonstations.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        stationDict[row['Station name']] = (float(row['Latitude']), float(row['Longitude']))
    print(stationDict)
    