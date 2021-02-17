import csv

atomicMassDict = {}

with open("atomicMass.csv", newline='') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        atomicMassDict[row[0]] = float(row[1])

def get(elementName):
    return atomicMassDict[elementName]
