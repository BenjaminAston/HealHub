from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.app_context().push()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

'''Retunerar en lista av titlar och artiklarna från filen: "wiki.json" '''
def get_info_from_file():
    try:
        with open("/static/wiki.json", "r") as my_file:
            info = json.load(my_file)
        return info
    except FileNotFoundError:
        with open("HealHub_code/static/wiki.json", "w") as my_file:
            json.dump([], my_file)
        return []

# Funktion som genererar ett unikt ID till nya "entries"
def create_id(info):
    """
    Retunerar en integer som representerar det nuvarande högsta id + 1 
    
    Retunerar
        int : det nuvarande högsta id + 1 
    """
    highest_id = 1
    for entry in info:
        if entry["id"] >= highest_id:
            highest_id = entry["id"] + 1
    return highest_id

def search_website(query):
    # For simplicity, let's assume we have a dictionary of page names and their URLs
    pages = {
        'start': '/',
        'övningar': '/ovningar',
        'fysioterapeut': '/Fysioterapeut',
        'tipsa': '/tipsa-ovningar',
        'kontakta oss': '/kontakta-oss',
        'huvud': '/huvud.html',
        'axel': '/haxel.html',
        'arm': '/harm.html',
        'bröst': '/bröst.html',
        'mage': '/mage.html',
        'ben': '/hben.html',
        'hand': '/hhand.html',
        'fot': '/hfot.html',
    }

    # Search for pages containing the query string (case insensitive)
    results = {name: url for name, url in pages.items() if query.lower() in name.lower()}
    return results

# Route som tar en till huvud sidan (index)
@app.route("/")
def index():
    info = get_info_from_file()
    return render_template("index.html", info=info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/progress_report', methods=['POST'])
def progress_report():
    if request.method == 'POST':
        progress = request.form['progress']
        return 'framsteg sparad: ' + progress


# Route som tar en till huvud.html
@app.route("/om-oss.html")
def serve_om_oss():
    return render_template("om-oss.html")
# Route som tar en till huvud.html
@app.route("/huvud.html")
def serve_huvud():
    return render_template("huvud.html")

logged_reps = {
    'haxel': [],
    'harm': [],
    'bröst': [],
    'hben': [],
    'mage': [],
    'hfot': [],
    'hhand': [],
    'huvud': []
}

def get_logged_reps(category):
    return logged_reps.get(category, [])

@app.route("/<category>.html")
def serve_template(category):
    if category not in logged_reps:
        return "Template not found", 404
    return render_template(f"{category}.html", previous_reps=get_logged_reps(category), enumerate=enumerate, category=category)

@app.route('/track_exercise/<category>', methods=['POST'])
def track_exercise(category):
    reps = request.form.get('reps')
    if reps and category in logged_reps:
        logged_reps[category].append(int(reps))
    return redirect(url_for('serve_template', category=category))

@app.route('/delete_exercise/<category>/<int:index>', methods=['POST'])
def delete_exercise(category, index):
    if category in logged_reps and 0 <= index < len(logged_reps[category]):
        logged_reps[category].pop(index)
    return redirect(url_for('serve_template', category=category))

# Route som tar en till bröst.html
@app.route("/bröst.html")
def serve_bröst():
    return render_template("bröst.html")


# Route som tar en till harm.html (höger arm)
@app.route("/harm.html")
def serve_harm():
    return render_template("harm.html")

# Route som tar en till mage.html
@app.route("/mage.html")
def serve_mage():
    return render_template("mage.html")


# Route som tar en till hben.html (höger ben)
@app.route("/hben.html")
def serve_hben():
    return render_template("hben.html")


# Route som tar en till hhand.html (höger hand)
@app.route("/hhand.html")
def serve_hhand():
    return render_template("hhand.html")

# Route som tar en till hfot.html (höger fot)
@app.route("/hfot.html")
def serve_hfot():
    return render_template("hfot.html")

# Route till static CSS fil
@app.route("/Flask/static/css/<filename>")
def serve_css(filename):
    return render_template(filename, root="static/css")

# En till route till den andra CSS filen (style3.css)
@app.route("/Flask/static/css/style3.css")
def serve_css3():
    return render_template("style3.css", root="static/css")

# Route till kontakta oss.html
@app.route("/kontakta-oss")
def serve_kontakta_oss():
    return render_template("kontakta oss.html")

# Route till övningar.html
@app.route("/ovningar")
def serve_ovningar():
    return render_template("övningar.html")

# Route till tack.html
@app.route("/tack")
def serve_tack():
    return render_template("tack.html")

@app.route("/t-tack")
def serve_ttack():
    return render_template("t-tack.html")

@app.route("/tips-tack")
def serve_tipstack():
    return render_template("tips-tack.html")

# Route till tipsa övningar.html
@app.route("/tipsa-ovningar")
def serve_tipsa_ovningar():
    return render_template("tipsa övningar.html")

# Route till Fysioterapeut.html
@app.route("/Fysioterapeut")
def serve_fysioterapeut():
    return render_template("Fysioterapeut.html")

@app.route('/info')
def info():
    faqs = [
        {"question": "Hur registrerar jag mig?", "answer": "Klicka på registreringslänken på hemsidan och fyll i de nödvändiga uppgifterna."},
        {"question": "Hur spårar jag mina framsteg?", "answer": "Gå till sektionen för övningsspårning och logga dina repetitioner."},
        {"question": "Kan jag föreslå nya övningar?", "answer": "Ja, du kan föreslå nya övningar genom sidan 'Tipsa Övningar'."},
    ]
    
    tips = [
        "Värm alltid upp innan du börjar dina övningar.",
        "Använd rätt teknik för att undvika skador.",
        "Håll dig hydrerad under träningen.",
        "Variera dina övningar för att träna olika muskelgrupper.",
        "Börja alltid med en nedvarvning och stretching."
    ]
    
    return render_template('info.html', faqs=faqs, tips=tips)
    
    
    return render_template('info.html', faqs=faqs, tip=tip)

@app.route("/login")
def serve_login():
    return render_template("login.html")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('index'))  # Redirect to home if no query

    results = search_website(query)

    if results:
        # If there are results, check if there's only one match
        if len(results) == 1:
            # Redirect to the single result
            return redirect(next(iter(results.values())))
        else:
            # Show the search results if multiple matches are found
            return render_template('search.html', query=query, results=results)
    else:
        # Show a message if no results are found
        return render_template('search.html', query=query, results=None)

# Kör servern
if __name__ == "__main__":
    db.create_all()
    app.run(host="127.0.0.1", port=8080, debug=True)