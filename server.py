#import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/return_message',methods=['POST','GET'])
def return_message():

    print("Answering client ...")

    return 'the message number '+str(request.args.get('f1'))


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')


