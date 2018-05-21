from flask import Flask, render_template, request, redirect, url_for, json, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/tupham/PycharmProjects/Multiple Choice/data.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'super secret'    
api = Api(app)


class Taikhoan(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ten = db.Column(db.String(80))
    matkhau = db.Column(db.String(80))
    lagiaovien = db.Column(db.Boolean, default=False, nullable=False)

class Hocsinh(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ten = db.Column(db.String(80))
    tuoi = db.Column(db.Integer)
    diachi = db.Column(db.String(80))
    tenid = db.Column(db.Integer, db.ForeignKey('taikhoan.id'))
    _name = db.relationship('Taikhoan')

class Giaovien(db.Model):
    id = db.Column(db.Integer, primary_key = True)    
    ten = db.Column(db.String(80))
    tuoi = db.Column(db.Integer)
    diachi = db.Column(db.String(80))
    tenid = db.Column(db.Integer, db.ForeignKey('taikhoan.id'))
    _name = db.relationship('Taikhoan')
class Debai(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    made = db.Column(db.String(80))
    tende = db.Column(db.String(80))
    giaodienid = db.Column(db.Integer, db.ForeignKey('giaovien.id'))
    __name = db.relationship('Giaovien')

class Cauhoi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cauhoi = db.Column(db.String(80))
    dapana = db.Column(db.String(80))
    dapanb = db.Column(db.String(80))
    dapanc = db.Column(db.String(80))
    dapand = db.Column(db.String(80))
    dapan = db.Column(db.String(80))
    nguoitaoid = db.Column(db.Integer, db.ForeignKey('giaovien.id'))
    __name = db.relationship('Giaovien')

class Debaicauhoi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    debaiid = db.Column(db.Integer, db.ForeignKey('debai.id'))
    cauhoiid = db.Column(db.Integer, db.ForeignKey('cauhoi.id'))
    __namecauhoi = db.relationship('Cauhoi')
    __namedebai = db.relationship('Debai')

class Debainguoithi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    debaiid = db.Column(db.Integer, db.ForeignKey('debai.id'))
    hocsinhid = db.Column(db.Integer, db.ForeignKey('hocsinh.id'))
    diem = db.Column(db.Integer)
    __namehocsinh = db.relationship('Hocsinh')
    __namedebai = db.relationship('Debai')
class debainguoithicauhoi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hocsinhid = db.Column(db.Integer, db.ForeignKey('hocsinh.id'))   
    debaiid = db.Column(db.Integer, db.ForeignKey('debai.id'))
    cauhoiid = db.Column(db.Integer, db.ForeignKey('cauhoi.id'))
    __namecauhoi = db.relationship('Cauhoi')
    __namedebai = db.relationship('Debai')
    __namehocsinh = db.relationship('Hocsinh')

class ChoiceRes(Resource):
    def post(self):
        json = request.get_json()
        id = json['id']
        ten = json['ten']
        tuoi = json['tuoi']
        diachi = json['diachi']
        tenid = json['tenid']
        checkupdate = Hocsinh.query.filter_by(ten = ten, tuoi = tuoi, diachi = diachi, tenid = tenid).first() # check data update
        if checkupdate:
            return redirect(url_for('giaovien'))
        else:
            Hocsinh.query.filter_by(id=id).update(dict(ten = json['ten'], tuoi = json['tuoi'], diachi = json['diachi'], tenid = json['tenid']))
            db.session.commit()
            return {"sucess": 1}
api.add_resource(ChoiceRes, '/api/student')

@app.route('/')
def hello_world():

    return redirect(url_for('login'))

@app.route('/delete/<id>')
def delete(id):

    data = Hocsinh.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('giaovien'))

@app.route('/infosv', methods = ['GET', 'POST'])
def infosv():

    if request.method == 'POST':
        ten = session.get('ten')
        tenid = db.session.query(Taikhoan.id).filter(Taikhoan.ten == ten)
        infosv = Hocsinh(ten = request.form['ten'], tuoi = request.form['tuoi'], diachi = request.form['diachi'], tenid = tenid)
        checkinfosv = Hocsinh.query.filter_by(ten = request.form['ten'], tuoi = request.form['tuoi'], diachi = request.form['diachi'], tenid = tenid).first()
        if checkinfosv:
            return redirect(url_for('giaovien'))
        else:
            db.session.add(infosv)
            db.session.commit()
            return redirect(url_for('giaovien'))
    return render_template('infosv.html')

@app.route('/add', methods = ['GET', 'POST'])
def add():

    ten = session.get('ten')
    if request.method == 'POST':
        tensv = Taikhoan(ten = request.form['ten'], matkhau = request.form['matkhau'], lagiaovien = 0)
        checktensv = Taikhoan.query.filter_by(ten = request.form['ten'], matkhau = request.form['matkhau'], lagiaovien = 0).first()#check ID exited
        if checktensv:
            return redirect(url_for('giaovien'))
        else:
            db.session.add(tensv)
            db.session.commit()
            return redirect(url_for('infosv'))            
    return render_template('giaovien.html')

@app.route('/cauhoi')
def cauhoi():
    return render_template('cauhoi.html')

@app.route('/addcauhoi', methods = ['GET','POST'])
def addcauhoi():
    ten = session.get('ten')
    nguoitaoid = db.session.query(Giaovien.id).filter(Giaovien.ten == ten)
    if request.method == 'POST':

        addcauhoi=Cauhoi(cauhoi=request.form['cauhoi'],dapana=request.form['dapana'],dapanb=request.form['dapanb'],
        dapanc=request.form['dapanc'],dapand=request.form['dapand'],dapan=request.form['dapan'],nguoitaoid=nguoitaoid)

        checkaddcauhoi = Cauhoi.query.filter_by(cauhoi=request.form['cauhoi'],dapana=request.form['dapana'],dapanb=request.form['dapanb'],
        dapanc=request.form['dapanc'],dapand=request.form['dapand'],dapan=request.form['dapan'],nguoitaoid=nguoitaoid).first()#check ID exited
        if checkaddcauhoi:
            # return redirect(url_for('debaidetail'))
            return "OK1"
        else:
            cauhoiid=db.session.query(Cauhoi.id).filter(Cauhoi.cauhoi==request.form['cauhoi'])
            debaiid=db.session.query(Debai.id).filter(Debai.giaodienid==ten)
            adddebaicauhoi=Debaicauhoi(debaiid=debaiid, cauhoiid=1)
            checkdebaicauhoi=Debaicauhoi.query.filter_by(debaiid=debaiid, cauhoiid=1).first()
            if checkdebaicauhoi:
                return "OK"
            else:
                db.session.add(adddebaicauhoi)
                # db.session.add(addcauhoi)
                db.session.commit()
                return "OK2"
    return render_template('debaidetail.html')

@app.route('/debaidetail/<id>')
def debaidetail(id):
    cauhoi = Cauhoi.query.filter(Debai.id==Debaicauhoi.debaiid).filter(Debaicauhoi.cauhoiid==Cauhoi.id).filter(Debai.id==id)
    return render_template('debaidetail.html', cauhoi = cauhoi)

@app.route('/debai', methods = ['GET', 'POST'])
def debai():
    ten = session.get('ten')
    giaodienid = db.session.query(Debai.giaodienid).filter(Giaovien.id == Debai.giaodienid).filter(Giaovien.ten == ten)
    if request.method == 'POST':
        showdebais = Debai.query.filter_by(giaodienid = giaodienid)
        return render_template('debai.html', showdebais = showdebais)
    return render_template('debai.html')
@app.route('/giaovien')
def giaovien():
    # session.pop('ten', None)
    ten = session.get('ten')
    tenid = db.session.query(Taikhoan.id).filter(Taikhoan.ten == ten)
    debais = Debai.query.filter(Giaovien.id == Debai.giaodienid).filter(Giaovien.ten == ten)
    students = Hocsinh.query.filter(Hocsinh.tenid == Taikhoan.id).filter(Taikhoan.ten == ten)#show hocsinh withten login
    return render_template('giaovien.html', students = students, debais = debais)

@app.route('/index/', methods = ['GET','POST'])
def index():

    ten = session.get('ten')
    students = Hocsinh.query.filter_by(ten = ten)
    return render_template('index.html', students = students)

@app.route('/login', methods = ['GET', 'POST'])
def login():

    errorlogin = None
    if request.method == 'POST':
        ten = request.form['ten']
        matkhau = request.form['matkhau']
        session['ten'] = ten
        checkten = Taikhoan.query.filter_by(ten = ten, matkhau = matkhau).first()
        if checkten:
            if checkten.lagiaovien == 0:
                return redirect(url_for('index'))
            elif checkten.lagiaovien == 1:
                return redirect(url_for('giaovien'))
        else:
            errorlogin = 'Incorrect password.!!!!!'
    return render_template('login.html', errorlogin = errorlogin)

if __name__ == '__main__':
    app.run()
