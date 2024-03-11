from flask import Flask, render_template, request, redirect, url_for, flash
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import os, requests, json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flashing messages

MAILCHIMP_LIST_ID = os.environ.get("MAILCHIMP_LIST_ID", None)
MAILCHIMP_API_KEY = os.environ.get("MAILCHIMP_API_KEY", None)
MAILCHIMP_USER= os.environ.get("MAILCHIMP_USER", None)

mc_auth = (MAILCHIMP_USER, MAILCHIMP_API_KEY)
print(mc_auth)
mc_headers = {'Content-Type': 'application/json'}
mc_base_url = f'https://us12.api.mailchimp.com/3.0'

# test first
ping = requests.get(f'{mc_base_url}/ping', auth=mc_auth)
print(ping.status_code, ping.text)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'consent' in request.form and request.form['email']:
            email_address = request.form['email']
            data = {
                'email_address': email_address,
                'status': 'subscribed',
            }

            url = f"{mc_base_url}/lists/{MAILCHIMP_LIST_ID}/members/"
            response = requests.post(url, auth=mc_auth, headers=mc_headers, json=data)

            if response.status_code == 200 or response.status_code == 201:
                flash('Email successfully added!', 'success')
            else:
                error_message = json.loads(response.text).get('title', 'An error occurred')
                flash(f"{error_message}", 'error')
        else:
            flash('You must consent and provide an email address.', 'error')

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)