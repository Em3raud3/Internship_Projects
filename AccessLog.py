from pathlib import Path
from datetime import datetime, date, timedelta
import csv
from flask import Flask, render_template , request
import os
import gzip
import glob
import time
import sys

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('Update')
def createAccessFile():
    #calculate time period to look back based on user preference 
    #Checks for numbers of days to look back either from the sys.argv or api request
    
    daysToLookBack = request.args.get("Days")
    
    if daysToLookBack == None:
        try:
            daysToLookBack = int(sys.argv[1])
        
        except: 
            daysToLookBack = 150
            
    else: daysToLookBack = int(daysToLookBack)
    
    todayDate = date.today()
    deltaDay = timedelta(days=daysToLookBack)
    
    #This will be the earlist date we look back
    earliestDate = todayDate - deltaDay
    
    #Listed all file names in directory in directory and sort by time
    fileFolder = glob.glob("nginx/access.log.*")
    fileFolder.sort(key=os.path.getmtime, reverse=True)
    
    #Will contain all data from all longs
    totalData =""
    
    pathToFolder= "/nginx"
    
    #Iterate through files and add them to totalData
    for fileName in fileFolder:
    
        print("Processing Log: " + fileName)
        
        fr = None
    
        if fileName[len(fileName) - 3:] == ".gz":
            fr = gzip.open(fileName,"rt")  
        
        else:
            fr = open(fileName, "r") 
        
        #Split the lines into arrays to choose what data we is desired, had to format a lot to get it in right form
        for line in fr:
            line = line.split()
            tempDate = line[3]
            tempDate = tempDate[:12] + " " + tempDate[13:] +"]"
            line[3] = tempDate
            selection =""
            
            if len(line[2]) > 1 and len(line[2]) < 21:
                del line[4]
                
            
            try:
                if datetime.date(datetime.strptime(line[3][1:21], "%d/%b/%Y %H:%M:%S")) > earliestDate and line[7] =="200":
                
                    for items in line[0:10]:
                        selection += items
                        selection += " "
            
            
                    if len(line[2]) > 1 and len(line[2]) < 21:
                        totalData += selection + "\n"
            
            except:
                continue
        
        fr.close()

        
    Database = Path("app.qcr.io.access.log")
    Database.touch(exist_ok=True)
    
    with open("app.qcr.io.access.log", 'w') as Database:
       # Database.write(Data)
    
       for line in totalData:
           Database.write(line)

    return render_template("Updated.html")


@app.route('/')
def loadAccessFile():
    logList = []
    localList = []
    uniqueID = set()
    uniqueDate = set()
    uniqueName = set()

    fr = open("app.qcr.io.access.log", "r")
    
    #parsed though each line and selected the parts I wanted for each list to have
    for x in fr:
        tempList = x.split()
        logList.append([tempList[2], ((tempList[3])[1:]), tempList[8], tempList[2] + ((tempList[3])[1:])])
        uniqueID.add(tempList[2] + ((tempList[3])[1:]))
        uniqueDate.add((tempList[3])[1:])
        uniqueName.add(tempList[2])

    fr.close()

    uniqueDate = list(uniqueDate)
    uniqueName = sorted(uniqueName)
    
    #sorted by date in proper form
    uniqueDate.sort(key = lambda date: datetime.strptime(date, '%d/%b/%Y'))
    
    

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


