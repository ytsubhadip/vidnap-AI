from flask import Flask,request,render_template
import uuid
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'user_upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg',}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create_rell", methods=["GET","POST"])
def create_rell():
    myid = uuid.uuid1()

    if request.method == "POST":
        #print all file in console:
        for key, value in request.files.items():
            print(key, value)
        unic_id = request.form.get('fileid')
        desc = request.form.get('text')   

        print(f"{unic_id}\n{desc}")

        #upload file
        input_file=[]
        # file = request.files[key]
        for key, file in request.files.items():
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                if (not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], unic_id)))):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], unic_id))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],unic_id, filename))
                input_file.append(file.filename)

                #save description of reel in fie
                with open(os.path.join(app.config['UPLOAD_FOLDER'], unic_id,"desc.txt"),"w")as f:
                    f.write(desc)

        for fl in input_file:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], unic_id,"input.txt"),"a") as f1:
                f1.write(f"file '{fl}'\n duration 1\n") 
        

    return render_template("create_rell.html", myid = myid)

@app.route("/gallery")
def gallery():  
    reels = os.listdir("static/rells")
    return render_template("gallery.html", reels = reels)

app.run(debug=True, port=8000)