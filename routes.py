from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    request,
    url_for,
    session
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError
from werkzeug.utils import secure_filename
import os

from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User, Data
from forms import login_form,register_form,data_capture_form

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="KZN BUSINESSES",
        btn_action="Login"
        )

# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
#@login_required
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data
            newuser = User(
                    username=username,
                    email=email,
                    pwd=bcrypt.generate_password_hash(pwd))
            
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))
        
        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create user account",
        title="Add user",
        btn_action="Add user account"
        )
#business capture route
@app.route("/businesses/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def businesses():
    form = data_capture_form()
    if form.validate_on_submit():
        try:
            business_name = form.business_name.data
            value_value = form.value_value.data
            new_business = Data(business_name=business_name,value_value=value_value,)
            db.session.add(new_business)
            db.session.commit()
            flash(f"Business Succesfully Added", "success")
            #return redirect(url_for('dashboard'))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"Business already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")

    return render_template("add_data.html",form=form,
                           text="Add Business to the Database",title="Add Business",btn_action="Add Business")
#business quer - Listing all businesses in the database
@app.route('/business_list/', methods=("GET", "POST"), strict_slashes=False)
@login_required
def business_list():
    business_data = Data.query.all()
    return render_template("business_list.html", text="Business list",title="Business list",
                           business_data=business_data)
#delete business route
@app.route('/delete_business/', methods=("GET", "POST"), strict_slashes=False)
@login_required
def delete_business():
    business_data = Data.query.all()
    return render_template("delete_business.html", text="Delete Business From list",title="Delete Business",
                           business_data=business_data)

#delete business
@app.route("/erase/<int:id>")
def erase(id):
    data = Data.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('dashboard'))
#paginate business list
@app.route('/pagination/<int:page_num>')
def pagination(page_num):
    pages = Data.query.paginate(per_page=1, page=page_num, error_out=True )
    return render_template("dashboard.html", text="Dashboard",title="Dashboard",pages=pages)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html",title="Home")

@app.route("/base", methods=("GET", "POST"), strict_slashes=False)
@login_required
def base():
    user = session.get(current_user)
    return render_template("base.html", user=user)

@app.route("/emails/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def emails():
    # Handle form submission for receiving emails
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            flash(f"Email {email} has been received successfully!", "success")
        else:
            flash("Please enter a valid email address.", "danger")
    # Handle form submission for sending emails
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            flash(f"Email {email} has been sent successfully!", "success")
        else:
            flash("Please enter a valid email address.", "danger")
    return render_template("emails.html",title="Emails")

@app.route("/home", methods=("GET", "POST"), strict_slashes=False)
def home():
    return render_template("home.html")

@app.route('/dashboard/', methods=("GET", "POST"), strict_slashes=False)
@login_required
def dashboard():
    business_data = Data.query.all()
    return render_template("dashboard.html", text="Dashboard",title="Dashboard",
                           business_data=business_data)


#map using folium
import folium
# Create a map centered at a specific location
m = folium.Map(location=[-29.8587, 31.0218], zoom_start=12)
# Add a marker to the map
folium.Marker(location=[-29.8587, 31.0218], popup="University of KwaZulu-Natal").add_to(m)
# Save the map to an HTML file
m.save("map.html")
@app.route('//map', methods=("GET", "POST"), strict_slashes=False)
@login_required
def map_view():
    return render_template("map.html")

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
