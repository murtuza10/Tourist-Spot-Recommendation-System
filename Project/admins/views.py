from flask import Blueprint,render_template,redirect,url_for,flash,request,abort
from flask_login  import login_user,login_required,logout_user
from Project import db
from Project.models import Admin
#from Project import Home
from Project.admins.forms import AdminLoginForm,AdminRegistrationForm

admins_blueprint = Blueprint('admins',__name__, template_folder = 'templates/admins')

@admins_blueprint.route('/account',methods=['GET','POST'])
@login_required
def account():
    #profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('admin_account.html')

@admins_blueprint.route('/welcome')
@login_required
def welcome_admin():
    return render_template('welcome_admin.html')

@admins_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('index'))


@admins_blueprint.route('/login',methods=['GET','POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()

        if admin.check_password(form.password.data) and admin is not None:
            login_user(admin)
            flash("Logged in Successfully!")
            next = request.args.get('next')
            if next is None or not next[0]=='/':
                next = url_for('admins.welcome_admin')

            return redirect(next)
    return render_template('admin.html',form=form)

@admins_blueprint.route('/register',methods=['GET','POST'])
def register():
    form = AdminRegistrationForm()

    if form.validate_on_submit():
        admin   = Admin(name=form.name.data,email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash("Thanks for registration!")
        return redirect(url_for('admins.login'))
    return render_template('admin_register.html',form=form)
