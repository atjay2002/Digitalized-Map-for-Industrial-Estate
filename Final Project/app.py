from flask import Flask, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for the session
app.static_folder = 'static'

@app.route('/')
def get_location():
    return render_template('get_location.html')

@app.route('/map')
def show_map():
    # Pass user's location to the map template
    user_latitude = session.get('latitude', 0)
    user_longitude = session.get('longitude', 0)
    return render_template('map.html', latitude=user_latitude, longitude=user_longitude)

@app.route('/store_location', methods=['POST'])
def store_location():
    data = request.get_json()
    session['latitude'] = data['latitude']
    session['longitude'] = data['longitude']
    return 'Location stored successfully!'

# Add a new route to handle the industry details and redirection
@app.route('/industry_details')
def industry_details():
    # Get user and industry location from session
    user_latitude = session.get('latitude', 0)
    user_longitude = session.get('longitude', 0)
    industry_latitude = session.get('industry_latitude', 0)
    industry_longitude = session.get('industry_longitude', 0)

    # Render industry_details.html with location parameters
    return render_template('industry_details.html',
                           user_latitude=user_latitude,
                           user_longitude=user_longitude,
                           industry_latitude=industry_latitude,
                           industry_longitude=industry_longitude)

@app.route('/index')
def index():
    # Get user and industry location from session or URL parameters
    user_latitude = float(request.args.get('user_latitude', session.get('latitude', 0)))
    user_longitude = float(request.args.get('user_longitude', session.get('longitude', 0)))
    industry_latitude = float(request.args.get('industry_latitude', 0))
    industry_longitude = float(request.args.get('industry_longitude', 0))

    # Store the values in the session for later use
    session['latitude'] = user_latitude
    session['longitude'] = user_longitude
    session['industry_latitude'] = industry_latitude
    session['industry_longitude'] = industry_longitude

    # Render the index.html template with the location parameters
    return render_template('index.html', user_latitude=user_latitude, user_longitude=user_longitude, industry_latitude=industry_latitude, industry_longitude=industry_longitude)

if __name__ == '__main__':
    app.run(debug=True)
