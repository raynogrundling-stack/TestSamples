@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("forms.index")
        )

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and bcrypt.check_password_hash(
            user.password_hash,
            form.password.data
        ):

            login_user(user)

            flash(
                "Logged in successfully.",
                "success"
            )

            return redirect(
                url_for("forms.index")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )