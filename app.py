from flask import Flask, render_template, flash, request

# No need to specify template_folder since it's the default
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Process the form data (e.g., save it, send an email, etc.)
        # For now, we'll just flash a success message
        flash(f"Thank you, {name}! Your message has been sent.")
        return render_template('contact.html')

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
