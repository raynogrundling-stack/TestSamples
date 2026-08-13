from extensions import db


class Sequence(db.Model):
    __tablename__ = "sequences"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    next_value = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    def __repr__(self):
        return (
            f"<Sequence {self.name}>"
        )
