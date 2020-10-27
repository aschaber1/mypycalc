import json

from flask import Flask, render_template, request

api = Flask('MyPyCalc')

@api.route('/', methods=['GET'])
def get_mypycalc():
    return render_template('form.html')

@api.route('/', methods=['POST'])
def post_mypycalc():
    a = int(request.form['a'])
    b = int(request.form['b'])
    result = a-b
    result_str = str(result)
    return render_template('form.html') + result_str, 201

if __name__ == "__main__":
    api.run(host='0.0.0.0', port=8080)
