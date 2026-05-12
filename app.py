from flask import Flask, request, redirect
from flask import render_template
import http.client
import json
from equation import getPercentage
from csv_handler import transformToCSV
from predict_agent import predictTrust
from html_builder import buildUnorderedList
from NLP_Insta import NLPResponse
app = Flask(__name__)

# To add a picture
# <img src="{{ url_for('static', filename='pic.png') }}" alt="">

#https://rapidapi.com/omarmhaimdat/api/instagram230/playground/apiendpoint_1b8255ef-2848-4751-863a-12d553c02ed6


@app.route("/")
def home():
    return render_template('GP.html', details=None, nlp="", error=False)


@app.route("/search", methods=['post'])
def search():
    account = request.form['account']


    conn = http.client.HTTPSConnection("instagram230.p.rapidapi.com")
                            

    headers = {
        'x-rapidapi-key': "SET YOUR API KEY HERE",
        'x-rapidapi-host': "instagram230.p.rapidapi.com"
    }

    conn.request("GET", f"/user/details?username={account}", headers=headers)
    res = conn.getresponse()
    data = res.read()


    details = json.loads(data.decode("utf-8"))
    try:
        account = details['data']['user']
    except Exception as e:
        print(e)
        print(details)
        return render_template("GP.html", details=None,nlp="", error=True)    


    importantDetails = transformToCSV(details)
    percentage = getPercentage()
    trust = predictTrust()
    ulList = buildUnorderedList(importantDetails)
    
    nlp_text = NLPResponse(details)
    details['percentage'] = str(percentage) + "%"
    details['trust'] = trust[0]
    details['ulList'] = ulList

    if percentage >= 85:
        details['trust'] = "Trusted"

    return render_template("GP.html", details=details,nlp=nlp_text ,error=False)
    


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)