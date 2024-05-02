from flask import Flask, render_template, url_for, redirect
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
        with open("python för healhub/static/wiki.json", "r") as my_file:
            info = json.load(my_file)
        return info
    except FileNotFoundError:
        with open("static/wiki.json", "w") as my_file:
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
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


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

# Route som tar en till huvud.html
@app.route("/om-oss.html")
def serve_om_oss():
    return render_template("om-oss.html")
# Route som tar en till huvud.html
@app.route("/huvud.html")
def serve_huvud():
    return render_template("huvud.html")

# Route som tar en till vaxel.html (vänster axel)
@app.route("/vaxel.html")
def serve_vaxel():
    return render_template("vaxel.html")

# Route som tar en till haxel.html (höger axel)
@app.route("/haxel.html")
def serve_haxel():
    return render_template("haxel.html")

# Route som tar en till bröst.html
@app.route("/bröst.html")
def serve_bröst():
    return render_template("bröst.html")

# Route som tar en till varm.html (vänster arm)
@app.route("/varm.html")
def serve_varm():
    return render_template("varm.html")

# Route som tar en till harm.html (höger arm)
@app.route("/harm.html")
def serve_harm():
    return render_template("harm.html")

# Route som tar en till mage.html
@app.route("/mage.html")
def serve_mage():
    return render_template("mage.html")

# Route som tar en till vben.html (vänster ben)
@app.route("/vben.html")
def serve_vben():
    return render_template("vben.html")

# Route som tar en till hben.html (höger ben)
@app.route("/hben.html")
def serve_hben():
    return render_template("hben.html")

# Route som tar en till vhand.html (vänster hand)
@app.route("/vhand.html")
def serve_vhand():
    return render_template("vhand.html")

# Route som tar en till hhand.html (höger hand)
@app.route("/hhand.html")
def serve_hhand():
    return render_template("hhand.html")

# Route som tar en till vfot.html (vänster fot)
@app.route("/vfot.html")
def serve_vfot():
    return render_template("vfot.html")

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

# Route till tipsa övningar.html
@app.route("/tipsa-ovningar")
def serve_tipsa_ovningar():
    return render_template("tipsa övningar.html")

# Route till Fysioterapeut.html
@app.route("/Fysioterapeut")
def serve_fysioterapeut():
    return render_template("Fysioterapeut.html")

# Kör servern
if __name__ == "__main__":
    db.create_all()
    app.run(host="127.0.0.1", port=8080, debug=True)