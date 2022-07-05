from flask import Flask , render_template ,url_for , redirect ,request  
#       THIS BELONGES TO LOGIN / REGISTER
#from flask_bootstrap import Bootstrap
from sqlalchemy import desc, func 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin , login_user , login_required , logout_user , current_user , LoginManager
import json
from flask_bootstrap import Bootstrap
from flask_swagger_ui import get_swaggerui_blueprint
from forms import LoginForm , RegisterForm , PostsForm




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databse.db'
app.config['SECRET_KEY'] = 'totomabyttajnykluc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'users' : 'sqlite:///databse.db',
    'posts' : 'sqlite:///databse.db' 
}

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask aplication"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
create_tables()

@app.route("/")
def home():
  return render_template('layout.html' , nadpis = "Home")

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html' , nadpis = "Profile" , meno = current_user)

class users(UserMixin , db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(15) , unique = True)
    password = db.Column(db.String(80) , unique = True)
    email = db.Column(db.String(80))

class posts(UserMixin , db.Model):
    __bind_key__ = 'posts'
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(80))
    text = db.Column(db.String(80))

@app.route("/signup" , methods=['GET' , 'POST'])
def signup():
    form = RegisterForm(request.form) 
    if request.method == 'POST' and form.validate():
        new_user = users(username = form.username.data , email = form.email.data , password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html' , nadpis = "Register" , form = form)

@app.route("/login" , methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('profile'))
        return '<h1> Invalid username or password </h1>'
    return render_template('login.html' , nadpis = "Login" , form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/allposts" , methods=['GET' , 'POST'])
def allposts():
    page = request.args.get('page', 1, type=int)
    post = posts.query.paginate(page = page , per_page = 20)
    return render_template('allposts.html' , nadpis = "All posts" , post = post , edit = 0)

@app.route("/yourposts" , methods=['GET' , 'POST'])
@login_required
def yourposts():
    page = request.args.get('page', 1, type=int)
    if int(current_user.get_id()) == 1:
        post = posts.query.paginate(page = page , per_page = 20)
    else:
        post = posts.query.filter_by(user_id = current_user.get_id()).paginate(page = page , per_page = 20)

    return render_template('allposts.html' , nadpis = "Your posts" , post = post , edit = 1)

@app.route("/add_post" , methods=['POST' , 'GET'])
@login_required
def add_post():
    form = PostsForm()
    if request.method == 'POST':
        new_post = posts(user_id = current_user.get_id() , title = form.title.data , text = form.body.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_post.html' , nadpis = "Add post" , form = form)

@app.route("/editpost/<int:id>" , methods=['POST' , 'GET'])
def editpost(id):
    post = posts.query.filter_by(id = id).first()
    form = PostsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_data = posts(id = id , title = form.title.data , text = form.body.data)
            db.session.delete(post)
            db.session.commit()
            db.session.add(new_data)
            db.session.commit()
            return redirect(url_for('yourposts'))
        form.title.data = post.title
        form.body.data = post.text
    return render_template('editpost.html' , nadpis = "Text" , post = post , form = form)

@app.route('/deletepost/<int:id>' , methods=['GET' , 'POST'])
def deletepost(id):
    uploads = posts.query.get(id)
    db.session.delete(uploads)
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/deleteallposts' , methods=['GET' , 'POST'])
def deleteallposts():
    db.session.query(posts).delete()
    db.session.commit()
    return redirect(url_for('profile'))

@app.route("/fake_users" , methods=['GET' , 'POST'])
@login_required
def fake_users():
    if int(current_user.get_id()) == 1 and request.method == "POST":
        json_data = open("src\\users.json")
        json_obj = json.load(json_data)
        for item in json_obj:

            new_user_id = users.query.order_by(desc(users.id)).first()
            new_username = item.get("username")
            new_password = item.get("password")
            new_email = item.get("email")
            new_user = users(id = int(new_user_id.id) +1, username = new_username , password = new_password , email = new_email)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('fakeusers.html' , nadpis = "Fake users" , info = "10 new users?")

@app.route("/fake_posts" , methods=['GET' , 'POST'])
@login_required
def fake_posts():
    if int(current_user.get_id()) == 1 and request.method == "POST":
        json_data = open("src\\posts.json")
        json_obj = json.load(json_data)
        for item in json_obj:
            new_id = posts.query.order_by(desc(posts.id)).first()
            if new_id == None:
                new_id = 1
            else:
                new_id = int(new_id.id) +1
            new_user_id = item.get("userId")
            new_title = item.get("title")
            new_text = item.get("body")
            new_post = posts(id = new_id, user_id = new_user_id , title = new_title , text = new_text)
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('fakeusers.html' , nadpis = "Fake posts" , info = "100 new posts?")

if __name__ == "__main__":
    app.run(debug=True , port=2451)