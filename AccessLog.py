from pathlib import Path
import csv
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def loadAccessFile():
    
    logList = []
    uniqueID = set()
    
    fr = open("AccessLog.txt", "rt")
    
    for x in fr:
        tempList = x.split()
        logList.append([tempList[2], ((tempList[3])[1:]), tempList[8], tempList[2] + ((tempList[3])[1:])])
        uniqueID.add(tempList[2] + ((tempList[3])[1:]))
    
    fr.close()   
    
    Database = Path("static/js/Database.csv")
    Database.touch(exist_ok=True)
    
    with open("static/js/Database.csv", 'w', newline='') as Database:
        dataWriter = csv.writer(Database)
        
        dataWriter.writerow(["UserID","Date", "Daily_Logins"])
        
        for x in uniqueID:
            length = len(x)
            loginCount = 0
            name = x[0:length + -11]
            date = x[length + -11:]
        
            for y in logList:
                if y[3] == x and y[2] == "200":
                    loginCount += 1
            
            dataWriter.writerow([name, date, loginCount]) 
    
    return render_template("index.html")

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