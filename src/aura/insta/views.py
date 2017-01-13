from flask import Blueprint, current_app, render_template, redirect, url_for, request
import requests as req


insta = Blueprint('insta', __name__, url_prefix='/insta')

@insta.route('/login')
def login():
    config = current_app.config

    client = config['CLIENT_ID']
    redirect_uri = config['REDIRECT_URL']
    authorized_url = config['AUTHORIZE_URL']

    url = authorized_url.format(client, redirect_uri)
    return redirect(url)


@insta.route('/access')
def access():
    args = request.args
    if not args.get('code'):
        print "No access code"
        return None

    config = current_app.config
    data = {
        'client_id': config['CLIENT_ID'],
        'client_secret': config['CLIENT_SECRET'],
        'redirect_uri': config['REDIRECT_URL'],
        'code': args.get('code'),
        'grant_type': 'authorization_code',
    }

    res = req.post(config['OAUTH_URL'], data=data)
    if res.status_code != 200:
        print "access token request failed"
        return None

    print "response....", res.json()
    return redirect(url_for('home.index'))
