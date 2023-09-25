from flask import Flask, render_template, redirect, url_for
from flask import request
import db
from flask_security import roles_accepted


app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def index():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg=""
    # if the form is submitted
    if request.method == 'POST':
    # check if user already exists
        user = db.User.query.filter_by(email=request.form['email']).first()
        msg=""
        # if user already exists render the msg
        if user:
            msg="User already exist"
            # render signup.html if user exists
            return render_template('signup.html', msg=msg)
         
        # if user doesn't exist
         
        # store the user to database
        user = db.User(email=request.form['email'], active=1, password=request.form['password'])
        # store the role
        role = db.Role.query.filter_by(id=request.form['options']).first()
        user.roles.append(role)
         
        # commit the changes to database
        db.session.add(user)
        db.session.commit()
         
        # login the user to the app
        # this user is current user
        db.login_user(user)
        # redirect to index page
        return redirect(url_for('index'))
         
    # case other than submitting form, like loading the page itself
    else:
        return render_template("signup.html", msg=msg)
    

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg=""
    if request.method == 'POST':
        # search user in database
        user = db.User.query.filter_by(email=request.form['email']).first()
        # if exist check password
        if user:
            if  user.password == request.form['password']:
                # if password matches, login the user
                db.login_user(user)
                return redirect(url_for('index'))
            # if password doesn't match
            else:
                msg="Wrong password"
         
        # if user does not exist
        else:
            msg="User doesn't exist"
        return render_template('signin.html', msg=msg)
         
    else:
        return render_template("signin.html", msg=msg)
    

@app.route('/teachers')
# only Admin can access the page
@roles_accepted('Admin')
def teachers():
    teachers = []
    # query for role Teacher that is role_id=2
    role_teachers = db.session.query(db.roles_users).filter_by(role_id=2)
    # query for the users' details using user_id
    for teacher in role_teachers:
        user = db.User.query.filter_by(id=teacher.user_id).first()
        teachers.append(user)
    # return the teachers list
    return render_template("teachers.html", teachers=teachers)