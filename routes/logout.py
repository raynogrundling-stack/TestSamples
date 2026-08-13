@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out.",
        "info"
    )

    return redirect(
        url_for("auth.login")
    )