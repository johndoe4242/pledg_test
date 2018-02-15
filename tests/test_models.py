import pytest

from sqlalchemy.exc import IntegrityError

from app.models import Pledger, Purchase


def test_pledger_insert_with_email(session):
    """Test to insert a `Pledger` with an email address."""
    email = 'Jean.Valjean@gmail.com'
    pledger = Pledger(email=email)

    session.add(pledger)
    session.commit()

    # Assert the model has been correctly saved.
    assert pledger.id > 0
    # Assert the email has been correctly saved as lower case.
    assert pledger.email == email.lower()


def test_pledger_unique_email(session):
    """Assert that an Integrity error is raised if trying to save two pledgers with a same email
    address."""
    # We add the same user twice to test the `email` field.
    session.add_all([
        Pledger(email='jean.valjean@gmail.com'),
        Pledger(email='jean.valjean@gmail.com')
    ])
    with pytest.raises(IntegrityError):
        session.commit()


def test_purchase_insert(session):
    """Test the association of a `Purchase` to a `Pledger`."""
    # We first make a pledger to initiate the purchase.
    pledger = Pledger(email='jean.valjean@gmail.com')
    # We then create a Purchase associated to the `Pledger`.
    purchase = Purchase(amount=42.50, leader_id=pledger.id)
    pledger.purchases = [purchase]

    session.add(pledger)
    session.commit()

    assert pledger.id > 0

    assert purchase.id > 0
    assert purchase.leader_id == pledger.id
    assert purchase.amount == 42.50
