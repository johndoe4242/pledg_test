from datetime import datetime

from sqlalchemy_utils import EmailType
from sqlalchemy_utils.types.choice import ChoiceType

from app import constants, db


class BaseModelMixin(db.Model):
    """Base providing generic fields common to many models."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '{class_name} <id {id}>'.format(
           class_name=self.__class__.__name__,
           id=self.id
        )


# Describe the relationship between a `Purchase` and a `Pledger`.
purchase_pledgers = db.Table(
    'purchase_pledgers',
    db.Column('pledger_id', db.Integer, db.ForeignKey('pledger.id'), primary_key=True),
    db.Column('purchase_id', db.Integer, db.ForeignKey('purchase.id'), primary_key=True)
)


class Purchase(BaseModelMixin):
    """Describe a purchase made by using pledg."""

    uuid = db.Column(db.String(36), unique=True, nullable=False)

    status = db.Column(
        ChoiceType(constants.STATES),
        nullable=False,
        default=constants.STATE_INITIALIZED
    )

    # This is the total amount for the purchase. It is supposed to be divided in many shares.
    amount = db.Column(db.Float, nullable=False)

    # TODO: Not sure right know about how to handle the product as it below to the merchants.

    # The leader initiate the purchase.
    leader_id = db.Column(
        db.Integer,
        db.ForeignKey('pledger.id'),
        nullable=False,
    )
    # The pledgers are contributing to the purchase.
    pledgers = db.relationship(
        'Pledger',
        secondary=purchase_pledgers,
        lazy='subquery',
        backref=db.backref('purchase', lazy=True),
    )

    # A purchase is divided in many shares depending of the number of contributors.
    shares = db.relationship('Share', backref='purchase', lazy=True)


class Pledger(BaseModelMixin):
    """Describe a contributor to a Purchase."""

    email = db.Column(EmailType)

    initiated_purchases = db.relationship('Purchase', backref='leader', lazy=True)
    purchases = db.relationship('Purchase', backref='pledger', lazy=True)

    shares = db.relationship('Share', backref='pledger', lazy=True)


class Share(BaseModelMixin):

    uuid = db.Column(db.String(36), unique=True, nullable=False)

    pledger_id = db.Column(db.Integer, db.ForeignKey('pledger.id'), nullable=False)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)

    # This is the amount the pledger have to pay as a part of the total purchase amount.
    amount = db.Column(db.Float, nullable=False)