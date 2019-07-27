# Author:  RADERMECKER Oskar, DINDIN Meryll, MISSLER Pierre-Louis
# Date:    09 July 2019
# Project: AsTeR

try: from service_WEB.imports import *
except: from imports import *

# Load credentials
with open('configs/config.yaml') as raw: crd = yaml.safe_load(raw)
SQL_URL = crd['sql_api']
API_KEY = crd['api_key']
# Secure application
application = Flask(__name__)
application.secret_key = crd['secret_key']

@application.context_processor
def inject_api_keys():

    return dict(googlemaps_key=crd['googlemaps_api'])

# Index
@application.route('/')
@application.route('/home/')
def index():

    return render_template('home.html')

# About AsTeR
@application.route('/about')
def about():

    return render_template('about.html')

# Team
@application.route('/team')
def team():

    return render_template('team.html')

# Features
@application.route('/call_analysis')
def call_analysis():

    return render_template('call_analysis.html')

@application.route('/unit_dispatching')
def unit_dispatching():

    return render_template('unit_dispatching.html')

@application.route('/feedback_integration')
def feedback_integration():

    return render_template('feedback_integration.html')

@application.route('/backup_plans')
def backup_plans():

    return render_template('backup_plans.html')

@application.route('/record')
def record():

    return render_template('record.html')

# Additional test environment
# MASK WHEN NOT IN USE AND BEFORE DEPLOYMENT
# @application.route('/test')
# def test():
#     return render_template('test.html')

# Register form class
class RegisterForm(Form):

    firstname = StringField('First Name', [validators.Length(min=2, max=50)])
    lastname = StringField('Last Name', [validators.Length(min=2, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.data_required(),
        validators.equal_to('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# Register page
@application.route('/register', methods=['GET', 'POST'])
def register():

    def register_user(profile, api_key, url):

        url = '/'.join([url, 'register'])
        header = {'apikey': api_key}
        prm = dict(zip(['username', 'password', 'firstname', 'lastname', 'email'], profile))
        req = requests.post(url, headers=header, params=prm)

        return json.loads(req.content)

    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():

        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        result = register_user((username, password, first_name, last_name, email), API_KEY, SQL_URL)

        if not result['success']:
            return render_template('register.html', error=result['reason'])
        else:
            flash('You are now registered. Log in to access your simulation dashboard!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Login page
@application.route('/login', methods=['GET', 'POST'])
def login():

    def check_connection(profile, api_key, url):

        warnings.simplefilter('ignore')

        url = '/'.join([url, 'connect'])
        username, password = profile
        header = {'apikey': api_key}
        params = {'username': username, 'password': sha256_crypt.hash(password)}
        req = requests.post(url, headers=header, params=params)

        return json.loads(req.content)

    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        password = request.form['password']

        result = check_connection((username, password), API_KEY, SQL_URL)

        if result['success']:
            session['username'] = username
            session['first_name'] = result['first_name']
            session['last_name'] = result['last_name']
            session['logged_in'] = True
            flash('You are now logged in!', 'success')
            return redirect(url_for('dashboard_summary'))
        else:
            return render_template('login.html', error=result['reason'])

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to log in before you can access your dashboard!', 'danger')
            return redirect(url_for('login'))
    return wrap

# Summary Dashboard
@application.route('/dashboard/summary')
@is_logged_in
def dashboard_summary():

    def list_units(api_key, url):
    
        url = '/'.join([url, 'get_unit'])
        header = {'apikey': api_key}
        req = requests.post(url, headers=header)
        
        return json.loads(req.content)

    def format_path(unit):

        pth = np.asarray([e.split(':') for e in unit['path'].split('|')]).astype('float')
        pth = [{'lng': e[0], 'lat': e[1]} for e in pth]

        return {'coordinates': pth, 'type': unit['unit_type'], 'unit_id': unit['unit_id']}

    def list_calls(api_key, url, time=10.0):

        url = '/'.join([url, 'get_call'])
        header = {'apikey': api_key}
        req = requests.post(url, headers=header, params={'timing': time})

        return json.loads(req.content)

    def formatting(idx, dic, key_name='unit_id'):
    
        dic.update({key_name: idx})
        return dic

    units = [formatting(k, v, key_name='unit_id') for k, v in list_units(API_KEY, SQL_URL).items()]
    paths = [format_path(unit) for unit in units if unit['path'] != 'none']
    calls = [formatting(k, v, key_name='call_id') for k, v in list_calls(API_KEY, SQL_URL).items()]

    map_parameters = {
        'identifier': "emergency_map",
        'zoom': 11,
        'lat': 37.7649,  # San Francisco Coordinates
        'lng': -122.4194,
        'mapType': 'terrain',
        'units': units,
        'calls': calls,
        'djikstra_path': paths,
        'streetview_control': False,
        'fullscreen_control': False,
        'maptype_control': False,
        'fit_markers_to_bounds': False,
        'center_on_user_location': False,
        'night_mode': False,
        'info_on_mouseover': False
    }

    return render_template('dashboard/dashboard_map.html', map_parameters=map_parameters)

# Calls Dashboard
@application.route('/dashboard/calls')
@is_logged_in
def dashboard_calls():

    return render_template('dashboard/dashboard_calls.html')

# Units Dashboard
@application.route('/dashboard/units')
@is_logged_in
def dashboard_units():

    return render_template('dashboard/dashboard_units.html')

# User log out page
@application.route('/logout')
@is_logged_in
def logout():

    session.clear()
    flash('Successfully logged out', 'success')
    return redirect(url_for('index'))




# Contact form class
class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=2, max=50), validators.DataRequired("Please enter your name.")])
    email = StringField('Email', [validators.Length(min=2, max=50), validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    subject = StringField('Subject', [validators.Length(min=2, max=100), validators.DataRequired("Please enter a subject.")])
    message = TextAreaField('Message', [validators.Length(min=2, max=1000), validators.DataRequired("Please enter a message.")])
    submit = SubmitField("Send")

# Contact page
@application.route('/contact', methods=['GET', 'POST'])

def contact():
  form = ContactForm(request.form)
 
  if request.method == 'POST':
    if form.validate() == False:
        flash('All fields are required.')
        return render_template('contact.html', form=form)
    else:
        msg = Message(subject=form.subject.data, sender='aster0project@gmail.com', recipients=['aster0project@gmail.com'])
        msg.body = """
        From: %s 
        <%s>
        Subject: %s

        -Message throught the contact page of www.project-aster.com-

        %s
        """ % (form.name.data,form.subject.data, form.email.data, form.message.data)
        mail.send(msg)
        # flash('Thank you for your message. We will get back to you shortly.', 'success' )
        return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
        return render_template('contact.html', form=form)

application.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 587,
    MAIL_USE_SSL = False,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = 'aster0project',
    MAIL_PASSWORD = 'AsTeRproject'
    )

mail=Mail(application)


if __name__ == '__main__':

    application.run(host='127.0.0.1', port=8080)
    #application.run()
