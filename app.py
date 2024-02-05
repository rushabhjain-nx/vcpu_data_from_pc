from flask import Flask, render_template, request, redirect, url_for
import time,csv
import json
app = Flask(__name__)

from vcpu_weekly import main

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    #print(request.form.getlist("ip"))

    field1 = request.form.get("ip")
    field2 = request.form.get("user")
    field3 = request.form.get("pass")
    data = {}
    data["PC_IP"]  = field1
    data["Username"]  = field2
    data["Password"] = field3

    with open("data.json","w") as json_file:
         json.dump(data,json_file,indent=4)

    
    return render_template("output.html"),main()
  
   
    

@app.route('/result')
def result():
   
    return render_template('output.html')

if __name__ == '__main__':
    app.run(debug=True)
