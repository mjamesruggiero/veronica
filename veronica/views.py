from flask import render_template, redirect, url_for, request, session, flash
from veronica import app
from twilio.twiml.voice_response import VoiceResponse

from veronica.view_helpers import twiml

@app.route('/')
@app.route('/veronica')
def home():
    return render_template('index.html')


@app.route('/veronica/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    with response.gather(numDigits=1,
                         action=url_for('menu'),
                         method='POST') as g:
        g.play(url="http://howtodocs.s3.amazonaws.com/et-phone.mp3", loop=3)
    return twiml(response)

@app.route('/veronica/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    option_actions = {'1': _give_instructions,
                      '2': _list_planets}

    if option_actions.has_key(selected_option):
        response = VoiceResponse()
        option_actions[selected_option](response)
        return twiml(response)

    return _redirect_welcome()


@app.route('/veronica/planets')
def planets():
    selected_option = request.form['Digits']
    option_actions = {'2': '+12024173378',
                      '3': '+12027336386',
                      '4': '+12027336637'}

    if option_actions.has_key(selected_option):
        response = VoiceResponse()
        response.dial(option_actions[selected_option])
        return twiml(response)
    return _redirect_welcome()

# ~~~~~~~~~~~~~~~~~~~
#    p r i v a t e
# ~~~~~~~~~~~~~~~~~~~


def _give_instructions(response):
    response.say("To get to your extraction point, get on your bike " +
                 "and go down the street. Then left down the alley. Avoid" +
                 "the police cars and turn left into an uninhabited housing " +
                 "development. Fly over the roadblock. Go past the moon. " +
                 "Soon you will see the mother ship.",
                 voice='Alice',
                 language='en-GB')


def _list_planets(response):
    with response.gather(numDigits=1,
                         action=url_for('planets'),
                         method='POST') as g:
        g.say("To call the planet Broh doe As O G, press 2. " +
              "To call the planet DuhGo bah, press 3. To call " +
              "an oober asteroid to your location, press 4." +
              "To go back to the main menu, press the star key.",
              voice='alice',
              language='en-GB',
              loop=3)

    return response


def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu", voice='alice', language='en-GB')
    response.redirect(url_for('welcome'))

    return twiml(response)
