from main import login_manager

def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        
        db_user = User.query.filter_by(username=form.username.data).first()
        if not db_user:
            flash("Login unsucessful")
            return redirect(url_for('login'))
        if db_user.password == form.password.data:
            user = DbUser(db_user)
            if login_user(user):
                flash("Logged in successfully.")
                return redirect(request.args.get("next") or url_for("admin"))
            else:
                flash("Login unsucessful")
                return redirect(url_for("login"))
        else:
            flash("Login failed...")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next = request.args.get('next')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        if authenticate(app.config['AUTH_SERVER'], username, password):
            user = User.query.filter_by(username=username).first()
            if user:
                if login_user(DbUser(user)):
                    # do stuff
                    flash("You have logged in")

                    return redirect(next or url_for('index', error=error))
        error = "Login failed"
    return render_template('login.html', login=True, next=next, error=error)


@login_required
def logout():
    logout_user()
    return redirect(url_for("admin"))


@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("admin"))
    return render_template("reauth.html")


@login_required
def user_add():
    form = UserAddForm(request.form)
    db = get_url_db()
    if request.method == 'POST' and form.validate():
        db.execute('insert into users (username, password, email) values (?, ?, ?)',
            [request.form['username'], request.form['password'], request.form['email']])
        g.db.commit()
        flash('User added...')
    return render_template("add.html", form=form)
