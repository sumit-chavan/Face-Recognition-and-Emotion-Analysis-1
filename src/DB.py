from webapp import db


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actorname = db.Column(db.String(50))
    frameno = db.Column(db.Integer)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    z = db.Column(db.Integer)
    w = db.Column(db.Integer)

    def __repr__(self):
        #return "Actor('{self.actorname}', '{self.frameno}', '{self.image_file}','{self.x}','{self.y}','{self.z}','{self.w}')"
		return "Actor('{}', '{}', '{}','{}','{}','{}','{}')".format(self.actorname,self.frameno,self.image_file,self.x,self.y,self.z,self.w)

db.create_all()
