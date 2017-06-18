from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
import os
import RPi.GPIO as GPIO
import time
import json

print("gestart")
from DbClass import DbClass
time.sleep(30)
print("running")

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pins = {
    17 : {'name' : 'verlichting beneden', 'state' : GPIO.LOW},
    24 : {'name' : 'verlichting boven', 'state' : GPIO.LOW},
    12 : {'name': 'muziek', 'state':GPIO.LOW},
    13 : {'name': 'PIN2motor', 'state':GPIO.LOW},
    21: {'name': 'verlichting buiten','state':GPIO.LOW}
   }

delay = 0.0055
steps = 1000

coil_A_1_pin = 19
coil_A_2_pin = 13
coil_B_1_pin = 6
coil_B_2_pin = 5

for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# ----------------------------------------------------------------------------------------------------------------------

@app.route('/')
def home():
    if 'email' in session:
        mail_session = escape(session['email'])

        database = DbClass()
        listVerlichting = database.getNameLights()

        database = DbClass()
        listMuziek = database.getNameMusic()

        database = DbClass()
        listWering = database.getNameWering()

        database = DbClass()
        listLightOUT = database.getnameLightOUT()


        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)

        templateData = {
            'pins': pins,
            'typeWering': listWering,
            'typeLicht': listVerlichting,
            'typeMuziek': listMuziek,
            'typeLightOUT' : listLightOUT
        }
        return render_template('home.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    database = DbClass()
    error = None
    if 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email_form = request.form['email']
        password_form = request.form['password']

        list_user = database.getUser(email_form)
        print(list_user)

        for user in list_user:
            if email_form == user[2]:
                UserTrying = user
                print(UserTrying)

                password = password_form
                salt = "24mei1998@Aalst"
                password = password.encode('utf-8')
                salt = salt.encode('utf-8')

                sha = hashlib.sha256()
                sha.update(password)
                sha.update(salt)
                fullpassword = sha.hexdigest()

                if fullpassword == UserTrying[3]:
                    session['email'] = request.form['email']
                    return redirect(url_for('home'))
                else:
                    error = "Dit wachtwoord komt niet overeen met deze gebruiker"
            else:
                error = "Deze gegevens bestaan niet in onze database"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

app.secret_key = 'A0ZrdfedyXdRdXHHrjmNjjLWXpffRT'

@app.route('/registreren' , methods=['GET', 'POST'])
def registreren():
    database = DbClass()
    error = None
    if request.method == 'POST':
        fullname_form = request.form['fullname']
        email_form = request.form['email']
        password_form = request.form['password']
        passwordConf_form = request.form['confPassword']

        list_user = database.getUser(email_form)

        if list_user == []:
            if password_form == passwordConf_form:

                password = password_form
                salt = "24mei1998@Aalst"
                password = password.encode('utf-8')
                salt = salt.encode('utf-8')

                sha = hashlib.sha256()
                sha.update(password)
                sha.update(salt)
                fullpassword = sha.hexdigest()

                database = DbClass()
                database.setNewUser(fullname_form,email_form,fullpassword)
                return render_template('login.html')
            else:
                error = "De 2 wachtwoorden komen niet overeen."
        else:
            error = "Deze gegevens bestaan al in onze database"

    return render_template('registreren.html', error=error)

@app.route('/wachtwoord-vergeten')
def wachtwoord_vergeten():
    return render_template('wachtwoord_vergeten.html')

@app.route('/home')
def start():
    if 'email' in session:
        mail_session = escape(session['email'])

        database = DbClass()
        listVerlichting = database.getNameLights()

        database = DbClass()
        listMuziek = database.getNameMusic()

        database = DbClass()
        listWering = database.getNameWering()

        database = DbClass()
        listLightOUT = database.getnameLightOUT


        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)

        templateData = {
            'pins': pins,
            'typeWering': listWering,
            'typeLicht': listVerlichting,
            'typeMuziek': listMuziek,
            'typeLightOUT' : listLightOUT

        }
        return render_template('home.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route('/zonnewering')
def zonnewering():
    if 'email' in session:
        mail_session = escape(session['email'])

        return render_template('zonwering.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/muziek')
def muziek():
    if 'email' in session:
        mail_session = escape(session['email'])

        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)

        database = DbClass()
        dataMusic = database.getDataMuziek()

        templateData = {
            'data': dataMusic,
            'pins': pins
        }

        return render_template('muziek.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route("/muziek/<veranderPin>/<actionMuziek>")
def actionMuziek(veranderPin, actionMuziek):
    if 'email' in session:
        mail_session = escape(session['email'])
        veranderPin = int(veranderPin)

        deviceName = pins[veranderPin]['name']

        if actionMuziek == "on":
          database = DbClass()
          database.setMuziek(1,1,1)
          GPIO.output(veranderPin, GPIO.HIGH)

        if actionMuziek == "off":
          GPIO.output(veranderPin, GPIO.LOW)
        if actionMuziek == "toggle":

          GPIO.output(veranderPin, not GPIO.input(veranderPin))


        for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)


        database = DbClass()
        dataMusic = database.getDataMuziek()

        templateData = {
            'data': dataMusic,
            'pins': pins
        }

        return render_template('muziek.html', mail_session=mail_session, **templateData)

@app.route('/grafieken')
def grafieken():
    if 'email' in session:
        mail_session = escape(session['email'])

        database = DbClass();
        dataGrafiek = database.getDataLichtIN()

        return render_template('grafieken.html', mail_session=mail_session, dataGrafiek=json.dumps(dataGrafiek))
    return redirect(url_for('login'))

@app.route("/grafiek/<typeGrafiek>/")
def buildGrafiek(typeGrafiek):
    if 'email' in session:
        mail_session = escape(session['email'])

        if typeGrafiek == "lichten":
            database = DbClass();
            dataGrafiek = database.getDataLichtIN()

        if typeGrafiek == "zonwering":
            database = DbClass();
            dataGrafiek = database.getDataZon()

        return render_template('grafieken.html', mail_session=mail_session, dataGrafiek=json.dumps(dataGrafiek))
    return redirect(url_for('login'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'email' in session:
        mail_session = escape(session['email'])

        if request.method == 'POST':
            db = DbClass()
            Naam = request.form['naam']
            Email = request.form['mail']
            Onderwerp = request.form['onderwerp']
            Bericht = request.form['bericht']
            db.toevoegenContact(Naam,Email,Onderwerp,Bericht)

        return render_template('contact.html', mail_session=mail_session)
    return redirect(url_for('login'))

pins={
    17: {'name': 'ledGelijkvloers', 'state': GPIO.HIGH},
    24: {'name': 'ledVerdiep1', 'state': GPIO.HIGH},
    12 : {'name': 'muziek', 'state':GPIO.HIGH},
    13 : {'name': 'motor', 'state':GPIO.HIGH},
    21: {'name': 'verlichting buiten','state':GPIO.HIGH}
}


@app.route("/verlichting")
def verlichting():
    if 'email' in session:
        mail_session = escape(session['email'])

        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)

        templateData = {
            'pins': pins
        }

        return render_template('verlichting.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route("/verlichting/<changePin>/<action>")
def action(changePin, action):
    if 'email' in session:
        mail_session = escape(session['email'])

        changePin = int(changePin)

        deviceName = pins[changePin]['name']

        if action == "on":
            GPIO.output(changePin, GPIO.HIGH)
            database = DbClass()
            if changePin == 17:
                database.setBinnenverlichting(1, 1, 1)
            if changePin == 24:
                database.setBinnenverlichting(1, 2, 1)
        if action == "off":
          GPIO.output(changePin, GPIO.LOW)
          database = DbClass()
          if changePin == 17:
              database.setBinnenverlichting(0, 1, 1)
          if changePin == 24:
              database.setBinnenverlichting(0, 2, 1)
        if action == "toggle":
          GPIO.output(changePin, not GPIO.input(changePin))


        for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)

        templateData = {
          'pins' : pins
        }

        return render_template('verlichting.html', mail_session=mail_session, **templateData)

    return redirect(url_for('login'))

@app.route("/zonnewering/<actie>")
def actie(actie):
    if 'email' in session:
        mail_session = escape(session['email'])

        if actie == "down":

            def setStep(w1, w2, w3, w4):
                GPIO.output(coil_A_1_pin, w1)
                GPIO.output(coil_A_2_pin, w2)
                GPIO.output(coil_B_1_pin, w3)
                GPIO.output(coil_B_2_pin, w4)

            for i in range(0, steps):
                setStep(0, 1, 1, 0)
                time.sleep(delay)
                setStep(0, 1, 0, 1)
                time.sleep(delay)
                setStep(1, 0, 0, 1)
                time.sleep(delay)
                setStep(1, 0, 1, 0)
                time.sleep(delay)

            database = DbClass()
            database.setZonnewering(1,1,1)
            beneden = True

        if actie == "up":
            def setStep(w1, w2, w3, w4):
                GPIO.output(coil_A_1_pin, w1)
                GPIO.output(coil_A_2_pin, w2)
                GPIO.output(coil_B_1_pin, w3)
                GPIO.output(coil_B_2_pin, w4)

            for i in range(0, steps):
                setStep(1, 0, 0, 0)
                time.sleep(delay)
                setStep(1, 0, 0, 1)
                time.sleep(delay)
                setStep(0, 0, 0, 1)
                time.sleep(delay)
                setStep(0, 0, 1, 1)
                time.sleep(delay)
                setStep(0, 0, 1, 0)
                time.sleep(delay)
                setStep(0, 1, 1, 0)
                time.sleep(delay)
                setStep(0, 1, 0, 0)
                time.sleep(delay)
                setStep(1, 1, 0, 0)
                time.sleep(delay)

            database = DbClass()
            database.setZonnewering(0,1,1)
            beneden = False
        templateData = {
          'state' : beneden
        }

        return render_template('zonwering.html', mail_session=mail_session, **templateData)

    return redirect(url_for('login'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT",8080))
    host="0.0.0.0"
    app.run(host=host, port=port,debug=True)