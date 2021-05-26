from pathlib import Path
from datetime import datetime
import csv
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def loadAccessFile():
    logList = []
    localList = []
    uniqueID = set()
    uniqueDate = set()
    uniqueName = set()

    fr = open("app.qcr.io.access.log", "r")

    for x in fr:
        tempList = x.split()
        logList.append([tempList[2], ((tempList[3])[1:]), tempList[8], tempList[2] + ((tempList[3])[1:])])
        uniqueID.add(tempList[2] + ((tempList[3])[1:]))
        uniqueDate.add((tempList[3])[1:])
        uniqueName.add(tempList[2])

    fr.close()

    uniqueDate = list(uniqueDate)
    uniqueDate.sort(key = lambda date: datetime.strptime(date, '%d/%b/%Y'))
    uniqueName = sorted(uniqueName)

    for x in uniqueID:
        length = len(x)
        loginCount = 0
        name = x[0:length + -11]
        date = x[length + -11:]

        for y in logList:
            if y[3] == x and y[2] == "200":
                loginCount += 1

        localList.append([name, date, loginCount])

    finalList = []

    for date in uniqueDate:
        tempList = [0] * 85
        tempList[0] = date
        finalList.append(tempList)

    for record in localList:
        row = uniqueDate.index(record[1])
        col = uniqueName.index(record[0]) + 1
        finalList[row][col] = record[2]

    Database = Path("static/js/Database.csv")
    Database.touch(exist_ok=True)
    with open("static/js/Database.csv", 'w', newline='') as Database:
        dataWriter = csv.writer(Database)

        csvHeader = []
        csvHeader.append("Date")

        for x in uniqueName:
            csvHeader.append(x)

        dataWriter.writerow(csvHeader)

        for x in finalList:
            dataWriter.writerow(x)



    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


#print(finalList)
#print(localList)
#print(len(uniqueName))
# print(len(uniqueDate))

#for x in logList:
    #strA = str(x[0])
    #strB = str(x[1])
    #strC = str(x[2])
    #tempStr = strA + "," + strB + "," + strC
    #fw.write(tempStr)
    #fw.write("\n")

#print(uniqueID)
#print(logList[0][2], (logList[0][3])[1:], logList[0][8])
#print(logList)
#print(f.read())
