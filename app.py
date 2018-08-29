from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index(exp=0, gs='Extinguish Big Fire At Byeng'):
    p = {1:'lala'}
    return render_template('index.html', canAskForExplanations=exp, plan=p)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
