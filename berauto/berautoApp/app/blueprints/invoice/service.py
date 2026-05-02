from app.extensions import db
from app.models.invoice import Invoice
from app.models.rental import Rental

class InvoiceService:

    @staticmethod
    def get_by_rental(rid, current_user):
        rental = db.session.get(Rental, rid)

        if not rental or not rental.invoice:
            return False, "Invoice not found"

        user_roles = [r["name"] for r in current_user.get("roles")]

        if "ADMIN" in user_roles or "STAFF" in user_roles:
            return True, rental.invoice

        if rental.user_id != current_user.get("user_id"):
            return False, "Not allowed"

        return True, rental.invoice