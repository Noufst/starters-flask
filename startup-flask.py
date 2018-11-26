from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

# import CRUD operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from startup_setup import Base, Startup, Founder

# create session and connect to DB
engine = create_engine('sqlite:///startup.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/startups')
def showStartups():
    startups = session.query(Startup).all()
    return render_template("startups.html", startups = startups)

@app.route('/startup/<int:startup_id>')
def showStartup(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    founders = session.query(Founder).filter_by(startup_id=startup_id).all()
    return render_template("startup.html", startup = startup, founders = founders)

@app.route('/startup/new', methods=['GET','POST'])
def newStartup():
    if request.method == 'POST':
        startup = Startup(name=request.form['name'])
        session.add(startup)
        session.commit()
        flash('New Startup Created')
        return redirect(url_for('showStartups'))
    else:
        return render_template('newStartup.html')

@app.route('/startup/<int:startup_id>/edit', methods=['GET','POST'])
def editStartup(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    if request.method == 'POST':
        if request.form['name']:
            startup.name = request.form['name']
        session.add(startup)
        session.commit()
        flash('Startup Modified')
        return redirect(url_for('showStartups'))
    else:
        return render_template('editStartup.html', startup = startup)

@app.route('/startup/<int:startup_id>/delete', methods=['GET','POST'])
def deleteStartup(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    if request.method == 'POST':
        session.delete(startup)
        session.commit()
        flash('Startup Deleted')
        return redirect(url_for('showStartups'))
    else:
        return render_template('deleteStartup.html', startup = startup)

@app.route('/startup/<int:startup_id>/founder/new', methods=['POST'])
def newFounder(startup_id):
    founder = Founder(name = request.form['name'], bio = request.form['bio'], startup_id = startup_id)
    session.add(founder)
    session.commit()
    flash('New Founder Created')
    return redirect(url_for('showStartup', startup_id = startup_id))

@app.route('/startup/<int:startup_id>/founder/<int:founder_id>/edit', methods=['GET','POST'])
def editFounder(startup_id, founder_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    founder = session.query(Founder).filter_by(id=founder_id).one()
    if request.method == 'POST':
        if request.form['name']:
            founder.name = request.form['name']
        if request.form['bio']:
            founder.bio = request.form['bio']
        session.add(founder)
        session.commit()
        flash('Founder Modified')
        return redirect(url_for('showStartup', startup_id = startup_id))
    else:
        return render_template('editFounder.html', startup = startup, founder = founder)

@app.route('/startup/<int:startup_id>/founder/<int:founder_id>/delete', methods=['GET','POST'])
def deleteFounder(startup_id, founder_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    founder = session.query(Founder).filter_by(id=founder_id).one()
    if request.method == 'POST':
        session.delete(founder)
        session.commit()
        flash('Founder Deleted')
        return redirect(url_for('showStartup', startup_id = startup_id))
    else:
        return render_template('deleteFounder.html', startup = startup, founder = founder)



if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
