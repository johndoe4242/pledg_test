import pytest
import unittest

from sqlalchemy.exc import IntegrityError

from app.models import Pledger, Purchase


@pytest.mark.usefixtures('session')
class PledgerTestCase(unittest.TestCase):

    def test_insert(self):
        pledger = Pledger(email='jean.valjean@gmail.com')

        self.session.add(pledger)
        self.session.commit()

        assert pledger.id > 0

    def test_unique_email(self):
        pledger = Pledger(email='jean.valjean@gmail.com')

        # We add the same user twice to test the `email` field.
        self.session.add(pledger)

        with pytest.raises(IntegrityError):
            self.session.commit()


@pytest.mark.usefixtures('session')
class PurchaseTestCase(unittest.TestCase):

    def test_insert(self):
        # We first make a pledger to initiate the purchase.
        pledger = Pledger(email='jean.valjean@gmail.com')
        purchase = Purchase(amount=42.50, leader_id=pledger.id)
        pledger.purchases = [purchase]

        self.session.add(pledger)
        self.session.commit()

        assert purchase.id > 0
