from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
import os
import RPi.GPIO as GPIO
import time

from DbClass import DbClass
time.sleep(15)

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    17 : {'name' : 'verlichting beneden', 'state' : GPIO.LOW},
    24 : {'name' : 'verlichting boven', 'state' : GPIO.LOW},
    12 : {'name': 'muziek', 'state':GPIO.LOW}
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

        print(listVerlichting)

        database = DbClass()
        listMuziek = database.getNameMusic()
        print(listMuziek)


        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins,
            'typeLicht': listVerlichting,
            'typeMuziek': listMuziek
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
        listMuziek = database.getNameWering()

        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins,
            'typeLicht': listVerlichting,
            'typeMuziek': listMuziek,
            'typeWering': listWering

        }
        return render_template('home.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route('/zonnewering')
def zonnewering():
    if 'email' in session:
        mail_session = escape(session['email'])
        # for pin in axisx:
        #    GPIO.setup(pin,GPIO.OUT)
        #    GPIO.output(pin,0)
        return render_template('zonwering.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/muziek')
def muziek():
    if 'email' in session:
        mail_session = escape(session['email'])
        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins
        }
        # Pass the template data into the template main.html and return it to the user
        return render_template('muziek.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route("/muziek/<veranderPin>/<actionMuziek>")
def actionMuziek(veranderPin, actionMuziek):
    if 'email' in session:
        mail_session = escape(session['email'])
        # Convert the pin from the URL into an integer:
        veranderPin = int(veranderPin)
        # Get the device name for the pin being changed:
        deviceName = pins[veranderPin]['name']
        # If the action part of the URL is "on," execute the code indented below:
        if actionMuziek == "on":
          # Set the pin high:
          GPIO.output(veranderPin, GPIO.HIGH)
          # Save the status message to be passed into the template:
        if actionMuziek == "off":
          GPIO.output(veranderPin, GPIO.LOW)
        if actionMuziek == "toggle":
          # Read the pin and set it to whatever it isn't (that is, toggle it):
          GPIO.output(veranderPin, not GPIO.input(veranderPin))

        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)

        # Along with the pin dictionary, put the message into the template data dictionary:
        templateData = {
          'pins' : pins
        }

        return render_template('muziek.html', mail_session=mail_session, **templateData)

@app.route('/grafieken')
def grafieken():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('grafieken.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('contact.html', mail_session=mail_session)
    return redirect(url_for('login'))

pins={
    17: {'name': 'ledGelijkvloers', 'state': GPIO.HIGH},
    24: {'name': 'ledVerdiep1', 'state': GPIO.HIGH},
    12 : {'name': 'muziek', 'state':GPIO.HIGH}
}


@app.route("/verlichting")
def verlichting():
    if 'email' in session:
        mail_session = escape(session['email'])
        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins
        }
        # Pass the template data into the template main.html and return it to the user
        return render_template('verlichting.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route("/verlichting/<changePin>/<action>")
def action(changePin, action):
    if 'email' in session:
        mail_session = escape(session['email'])
        # Convert the pin from the URL into an integer:
        changePin = int(changePin)
        # Get the device name for the pin being changed:
        deviceName = pins[changePin]['name']
        # If the action part of the URL is "on," execute the code indented below:
        if action == "on":
          # Set the pin high:
          GPIO.output(changePin, GPIO.HIGH)
          database = DbClass()
          database.setBinnenverlichting(1, 1, 1)
          # Save the status message to be passed into the template:
        if action == "off":
          GPIO.output(changePin, GPIO.LOW)
          database = DbClass()
          database.setBinnenverlichting(0, 1, 1)
        if action == "toggle":
          # Read the pin and set it to whatever it isn't (that is, toggle it):
          GPIO.output(changePin, not GPIO.input(changePin))

        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)

        # Along with the pin dictionary, put the message into the template data dictionary:
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
            # Convert the pin from the URL into an integer:
            def setStep(w1, w2, w3, w4):
                GPIO.output(coil_A_1_pin, w1)
                GPIO.output(coil_A_2_pin, w2)
                GPIO.output(coil_B_1_pin, w3)
                GPIO.output(coil_B_2_pin, w4)

            # loop through step sequence based on number of steps

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
            # Function for step sequence

            def setStep(w1, w2, w3, w4):
                GPIO.output(coil_A_1_pin, w1)
                GPIO.output(coil_A_2_pin, w2)
                GPIO.output(coil_B_1_pin, w3)
                GPIO.output(coil_B_2_pin, w4)

            # Reverse previous step sequence to reverse motor direction

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

# # Css refreshen
#
# @app.context_processor
# def override_url_for():
#     return dict(url_for=dated_url_for)
# def dated_url_for(endpoint, **values):
#     if endpoint == 'static':
#         filename = values.get('filename', None)
#         if filename:
#             file_path = os.path.join(app.root_path,
#                                      endpoint, filename)
#             values['q'] = int(os.stat(file_path).st_mtime)
#     return url_for(endpoint, **values)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",8080))
    host="0.0.0.0"
    app.run(host=host, port=port,debug=True)