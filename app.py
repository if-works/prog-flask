from flask import Flask, render_template, request, redirect, url_for, flash
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flashing messages

MAILCHIMP_LIST_ID = os.environ.get("MAILCHIMP_SERVER_PREFIX")
MAILCHIMP_API_KEY = os.environ.get("MAILCHIMP_API_KEY"),
MAILCHIMP_SERVER_PREFIX = os.environ.get("MAILCHIMP_SERVER_PREFIX")

client = MailchimpMarketing.Client()
client.set_config({
    "api_key": MAILCHIMP_API_KEY,
    "server": MAILCHIMP_SERVER_PREFIX
})

response = mailchimp.ping.get()
print(response)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'consent' in request.form and request.form['email']:
            try:
                email_address = request.form['email']
                response = client.lists.add_list_member(MAILCHIMP_LIST_ID, {
                    "email_address": email_address,
                    "status": "subscribed"  # or 'pending' for double opt-in
                })
                flash('Email successfully added!', 'success')
            except ApiClientError as error:
                print(error)
                flash(f"An error occurred.", 'error')
        else:
            flash('You must consent and provide an email address.', 'error')
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
