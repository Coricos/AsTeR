# Author:  RADERMECKER Oskar, DINDIN Meryll, MISSLER Pierre-Louis
# Date:    09 July 2019
# Project: AsTeR

try: from service_WEB.imports import *
except: from imports import *

# Load credentials
with open('configs/config.yaml') as raw: crd = yaml.safe_load(raw)
SQL_URL = crd['sql_api']
API_KEY = crd['api_key']
MAIL_PASSWORD = crd['mail_password']

# Secure application
application = Flask(__name__)
application.secret_key = crd['secret_key']

# Setting up Mails
application.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='aster0project',
    MAIL_PASSWORD=MAIL_PASSWORD
)
mail = Mail(application)

# Contact form class
class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=2, max=50), validators.DataRequired("Please enter your name.")])
    email = StringField('Email', [validators.Length(min=2, max=50), validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    subject = StringField('Subject', [validators.Length(min=2, max=100), validators.DataRequired("Please enter a subject.")])
    message = TextAreaField('Message', [validators.Length(min=2, max=1000), validators.DataRequired("Please enter a message.")])
    submit = SubmitField("Send")

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


@application.context_processor
def inject_api_keys():
    return dict(googlemaps_key=crd['googlemaps_api'])

# Index
@application.route('/', methods=['GET', 'POST'])
@application.route('/home', methods=['GET', 'POST'])
def index():
    form = ContactForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('home.html', form=form)
        else:
            msg = Message(subject=form.subject.data, sender='aster0project@gmail.com',
                          recipients=['aster0project@gmail.com'])
            msg.body = """
                From: %s 
                <%s>
                Subject: %s

                -Message from www.project-aster.com-

                %s
                """ % (form.name.data, form.subject.data, form.email.data, form.message.data)
            mail.send(msg)
            flash('Thank you for your message. We will get back to you shortly.', 'success')
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('home.html', form=form)


# About AsTeR
@application.route('/about')
def about():
    return render_template('about.html')

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

# Summary Dashboard
@application.route('/dashboard')
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

    times = datetime.now().minute*60 + datetime.now().second
    units = [formatting(k, v, key_name='unit_id') for k, v in list_units(API_KEY, SQL_URL).items()]
    paths = [format_path(unit) for unit in units if unit['path'] != 'none']
    calls = [formatting(k, v, key_name='call_id') for k, v in list_calls(API_KEY, SQL_URL, time=times).items()]

    map_parameters = {
        'identifier': "emergency_map",
        'zoom': 11.5,
        'lat': 37.8212,  # San Francisco Coordinates
        'lng': -122.3709,
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

@application.route('/calls_content')
def return_content():
    def list_calls(api_key, url, time=0.0):

        url = '/'.join([url, 'get_call'])
        header = {'apikey': api_key}
        req = requests.post(url, headers=header, params={'timing': time})

        return json.loads(req.content)

    def formatting(idx, dic, key_name='unit_id'):

        dic.update({key_name: idx})
        return dic

    times = (datetime.now().minute*60 + datetime.now().second) * 2
    calls = [formatting(k, v, key_name='call_id') for k, v in list_calls(API_KEY, SQL_URL, time=times).items()]
    return jsonify(calls=calls)

# Calls Dashboard
@application.route('/dashboard/calls')
def dashboard_calls():
    return render_template('dashboard/dashboard_calls.html')

# Units Dashboard
@application.route('/dashboard/units')
def dashboard_units():
    return render_template('dashboard/dashboard_units.html')

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080)
