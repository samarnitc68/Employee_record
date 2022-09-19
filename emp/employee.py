

from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient


#connectio to docker database
myclient = MongoClient('mongodb://localhost:27023')
db = myclient["employee"]


app = Flask(__name__)

# Homepage
@app.route('/')
def index():
    return render_template('home.html')

# Form page for entering data to save in database
@app.route('/form')
def form():
    return render_template('form.html')

# Save data to database and run return the save data using another page result.html
@app.route('/result', methods=['POST','GET'])
def result():
    data ={}
    if request.method =="POST":
        data['id'] = request.form['id']
        data['fname'] = request.form['fname']
        data['lname'] = request.form['lname']
        data['dept'] = request.form['dept']
        data['doj'] = request.form['doj']
        data['eod'] = request.form['eod']
        if  data['id'] and data['fname'] and  data['lname'] and data['dept'] and data['doj']:
            db.employee.insert_one(data)
            return render_template('result.html',data =data)
    return "Please fill all required field"
# Show the record saved in database
@app.route('/showrecord')
def showrecord():
    l=[]
    x=db.employee.find({},{'_id':0})
    for record in x:
        l.append(record)
        # print(type(record))
    return render_template('showrecord.html',data=l)

# Enter department to find total employee working in perticular department
@app.route('/totalemp')
def totalemp():
    return render_template('totalemp.html')

# Finding total employee working in perticular department
@app.route('/countd', methods=['POST','GET'])
def countdept():
    # return 'hi'
    data ={}
    department = ['it', 'python developer', 'devops', 'testing','hr']
    if request.method =="POST":
        data['dept'] = request.form['dept']
        if data['dept'] not in department:
            return 'data not found'
        x=db.employee.find({"dept":request.form['dept']})
        if x:
            print('enter')
            x=db.employee.count_documents({"dept":{"$eq":data['dept']}})
            data[data['dept']] = x
            return render_template('result.html',data =data)
    
    else:
        return "not find"
# Page for selecting data based on conditions
@app.route('/name')
def name():
    return render_template('name.html')

# Function for returning data based on condition
#  like, startwith, endwith, upper case, lowercase
@app.route('/empwithcondition', methods=['POST','GET'])
def empwithcondition():
    data={}
    
    if request.method =="POST":
        # print('hi')
        data['name'] = request.form['name']
        data['val'] = request.form['val']
        if data['val'] == ("like"):
            l=[]
            print(data['name'],data['val'])
            x=db.employee.find({"$or": [ { "fname": request.form['name']  }]})
            print(x)
            for p in x:
                l.append(p)
            
            if len(l):   
                return render_template('conditiondata.html',data =l)
        elif data['val'] == ("upper"):
            l=[]
            x=db.employee.find({"fname":request.form['name'].upper()})
            for p in x:
                l.append(p)
            if len(l):
                return render_template('conditiondata.html',data =l)

        elif data['val'] == ("lower"):
            l=[]
            x=db.employee.find({"fname":request.form['name'].lower()})
            for p in x:
                l.append(p)
            if len(l):
                return render_template('conditiondata.html',data =l)
        elif data['val'] == ("startwith"):
            l=[]
            myquery = { "fname": { "$regex": "^"+request.form['name'] } }
            x =db.employee.find(myquery)
            for p in x:
                l.append(p)
            if len(l):    
                return render_template('conditiondata.html',data =l)
        else:
            l=[]
            myquery = { "lname": { "$regex": request.form['name']+"$" } }
            x =db.employee.find(myquery)
            for p in x:
                l.append(p)
            if len(l):
                return render_template('conditiondata.html',data =l)





    return "data not found"  

#driver code 

if __name__ =='__main__':
    app.run(debug=True ,port=5000, host="0.0.0.0")
