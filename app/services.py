from app import db
from app import models


# Notes: Maybe we should also add a kind of DAO to totally separate the business logic from
# our db access.
class PurchasesService:
    """Service layer to access to the purchases."""

    _model = models.Purchase
    _session = db.session

    @property
    def base_query(self):
        return self._session.query(self._model).order_by(self._model.created_at)

    def list(self, status=None):
        """Return a list of purchases.

        Parameters
        ----------
        status: str, optional
            Filter the purchases on their status.
        """
        query = self.base_query
        if status:
            query = query.filter(self._model.status == status)
        return query.all()
