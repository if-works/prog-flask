from flask import Flask, render_template, request, redirect, url_for, flash
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'consent' in request.form and request.form['email']:
            try:
                client = MailchimpMarketing.Client()
                client.set_config({
                    "api_key": "YOUR_API_KEY",
                    "server": "YOUR_SERVER_PREFIX"
                })

                email_address = request.form['email']
                response = client.lists.add_list_member("list_id", {
                    "email_address": email_address,
                    "status": "subscribed"  # or 'pending' if you want double opt-in
                })
                flash('Email successfully added!', 'success')
            except ApiClientError as error:
                flash(f"An error occurred: {error.text}", 'error')
        else:
            flash('You must consent and provide an email address.', 'error')
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
