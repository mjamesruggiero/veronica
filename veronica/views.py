from flask import render_template, redirect, url_for, request, session, flash
import datetime
from twilio.twiml.voice_response import VoiceResponse, Gather
from veronica import app
from veronica import utils
from veronica.view_helpers import twiml

@app.route('/')
@app.route('/veronica')
def home():
    return render_template('index.html')


@app.route('/veronica/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    gather = Gather(numDigits=1,
                    action=url_for('menu'),
                    method='POST')
    message ='Please press 1 and then the pound sign for Bob, ' \
              +'2 for Ted, 3 for Alice or 4 for Carol.'
    gather.say(message,
               voice='Alice',
               language='en-US')
    response.append(gather)
    return twiml(response)

@app.route('/veronica/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    option_actions = {'1': _bob,
                      '2': _ted,
                      '3': _alice,
                      '4': _carol}

    if option_actions.has_key(selected_option):
        response = VoiceResponse()
        option_actions[selected_option](response)
        return twiml(response)

    return _redirect_welcome()


# ~~~~~~~~~~~~~~~~~~~
#    p r i v a t e
# ~~~~~~~~~~~~~~~~~~~

def _human(response, name, birthdate):
    fancy_date = utils.get_fancy_date(birthdate)
    age = utils.get_age(birthdate,
                        datetime.datetime(2017, 9, 02, 0 , 0))

    text = "{n} has a birthday on {d}; {n} is {a}".format(n=name,
                                                          d=fancy_date,
                                                          a=age)

    response.say(text,
                 voice='Alice',
                 language='en-US')
    response.hangup()
    return response


def _bob(response):
    bday = datetime.datetime(2009, 2, 23, 0, 0)
    return _human(response, 'Bob', bday)


def _alice(response):
    bday = datetime.datetime(1994, 2, 6, 0, 0)
    return _human(response, 'Alice', bday)


def _ted(response):
    bday = datetime.datetime(2006, 10, 14, 0, 0)
    return _human(response, 'Ted', bday)


def _carol(response):
    bday = datetime.datetime(1969, 04, 21, 0, 0)
    return _human(response, 'Carol', bday)


def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu",
                 voice='alice',
                 language='en-US')
    response.redirect(url_for('welcome'))

    return twiml(response)
