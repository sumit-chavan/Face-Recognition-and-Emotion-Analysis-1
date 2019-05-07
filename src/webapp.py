import os, sys, csv, cv2, subprocess, numpy
from subprocess import call
from flask import Flask, render_template, request
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
import unicodedata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trial.db'
app.config['UPLOAD_FOLDER']='/home/yash/Desktop/Final/Face reco KNN/src/uploadfolder'
db=SQLAlchemy(app)

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frameno = db.Column(db.Integer)
    actorname = db.Column(db.String(50))
    emotionname=db.Column(db.String(50))
    emotionprobability=db.Column(db.Float)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    z = db.Column(db.Integer)
    w = db.Column(db.Integer)

    def __repr__(self):
        return "Actor('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(self.frameno,self.actorname,self.emotionname,self.emotionprobability,self.image_file,self.x,self.y,self.z,self.w)

class Object(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    frameno = db.Column(db.Integer)
    objectname= db.Column(db.String(50))
    objectconfidence=db.Column(db.Float)

    def __repr__(self):
        return "Object('{}','{}','{}')".format(self.frameno,self.objectname,self.objectconfidence)

db.create_all()

@app.route("/")
def index():
    return render_template("/index.html")



@app.route("/upload", methods=['POST'])
def upload():
    for file in request.files.getlist("file"):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        destination=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(destination)
        comm="python video_emotion_color_demo.py '"+destination+"'"
        subprocess.check_output(comm,shell=True)
    
    return render_template("complete.html", value = destination)



@app.route("/search", methods=['GET', 'POST'])
def search():
    actor_dict={}
    frame_emo={}
    frame_emopro={}
    frame_actor={}
    
    if request.method == 'POST': 
        Query=request.form['query']
        Query=Query.split(" ")
        Actorss=Actor.query.all()
        Objects=Object.query.all()
        
        if len(Query)==1:
            resultt=(db.session.query(Actor,Object).filter(Actor.actorname==Query[0]).all())
            print(resultt)
        if len(Query)==2:
            resultt=(db.session.query(Actor,Object).filter(Actor.actorname==Query[0]).filter(Actor.emotionname==Query[1]).filter(Actor.frameno==Object.frameno).all())    
            print(resultt)
        if len(Query)==3:
            resultt=(db.session.query(Actor,Object).filter(Actor.actorname==Query[0]).filter(Actor.emotionname==Query[1]).filter(Object.objectname==Query[2]).filter(Actor.frameno==Object.frameno).all())
            print(resultt)
        print(resultt)
        for x in resultt:
            print(x.Actor.actorname)
##        print("--------------------------DATABASE ACTORS---------------------------------------")
##        # print(Actorss)
##        print("--------------------------DATABASE ACTORS END---------------------------------------")
##        print("--------------------------DATABASE OBJECTS---------------------------------------")
##        # print(Objects)
##        print("--------------------------DATABASE OBJECTS END---------------------------------------")
    else:
        return render_template('index.html')
   

    return render_template("input.html",resultt=resultt,length=len(resultt))


if __name__ == "__main__":
    app.run(debug = True)

