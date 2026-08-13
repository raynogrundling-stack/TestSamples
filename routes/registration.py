@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:
        return redirect(
            url_for("forms.index")
        )

    form = RegisterForm()

    if form.validate_on_submit():

        existing = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        password_hash = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=password_hash,
            role="user"
        )

        db.session.add(user)

        db.session.commit()

        flash(
            "Registration successful.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html",
        form=form
    )