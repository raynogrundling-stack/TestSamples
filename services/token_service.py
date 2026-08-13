from flask import current_app

from itsdangerous import (

    URLSafeTimedSerializer,

    BadSignature,

    SignatureExpired

)

from models.user import User


class TokenService:

    EMAIL_VERIFICATION_SALT = (
        "email-verification"
    )

    PASSWORD_RESET_SALT = (
        "password-reset"
    )

    USER_INVITATION_SALT = (
        "user-invitation"
    )

    @staticmethod
    def serializer():

        return URLSafeTimedSerializer(

            current_app.config[
                "SECRET_KEY"
            ]

        )

    #
    # EMAIL VERIFICATION
    #

    @staticmethod
    def create_verification_token(
        user_id
    ):

        serializer = (
            TokenService.serializer()
        )

        return serializer.dumps(

            {

                "user_id": user_id

            },

            salt=
            TokenService
            .EMAIL_VERIFICATION_SALT

        )

    @staticmethod
    def verify_email_token(

        token,

        max_age=86400

    ):
        """
        Default:
        24 hours
        """

        serializer = (
            TokenService.serializer()
        )

        try:

            payload = (

                serializer.loads(

                    token,

                    salt=
                    TokenService
                    .EMAIL_VERIFICATION_SALT,

                    max_age=max_age

                )

            )

            return User.query.get(
                payload["user_id"]
            )

        except (

            BadSignature,

            SignatureExpired

        ):

            return None

    #
    # PASSWORD RESET
    #

    @staticmethod
    def create_reset_token(
        user_id
    ):

        serializer = (
            TokenService.serializer()
        )

        return serializer.dumps(

            {

                "user_id": user_id

            },

            salt=
            TokenService
            .PASSWORD_RESET_SALT

        )

    @staticmethod
    def verify_reset_token(

        token,

        max_age=3600

    ):
        """
        Default:
        1 hour
        """

        serializer = (
            TokenService.serializer()
        )

        try:

            payload = (

                serializer.loads(

                    token,

                    salt=
                    TokenService
                    .PASSWORD_RESET_SALT,

                    max_age=max_age

                )

            )

            return User.query.get(
                payload["user_id"]
            )

        except (

            BadSignature,

            SignatureExpired

        ):

            return None

    #
    # USER INVITATIONS
    #

    @staticmethod
    def create_invitation_token(
        user_id
    ):

        serializer = (
            TokenService.serializer()
        )

        return serializer.dumps(

            {

                "user_id": user_id

            },

            salt=
            TokenService
            .USER_INVITATION_SALT

        )

    @staticmethod
    def verify_invitation_token(

        token,

        max_age=604800

    ):
        """
        Default:
        7 days
        """

        serializer = (
            TokenService.serializer()
        )

        try:

            payload = (

                serializer.loads(

                    token,

                    salt=
                    TokenService
                    .USER_INVITATION_SALT,

                    max_age=max_age

                )

            )

            return User.query.get(
                payload["user_id"]
            )

        except (

            BadSignature,

            SignatureExpired

        ):

            return None

    #
    # GENERIC TOKEN
    #

    @staticmethod
    def create_token(
        payload,
        salt
    ):

        serializer = (
            TokenService.serializer()
        )

        return serializer.dumps(
            payload,
            salt=salt
        )

    @staticmethod
    def verify_token(
        token,
        salt,
        max_age=3600
    ):

        serializer = (
            TokenService.serializer()
        )

        try:

            return serializer.loads(

                token,

                salt=salt,

                max_age=max_age

            )

        except (

            BadSignature,

            SignatureExpired

        ):

            return None