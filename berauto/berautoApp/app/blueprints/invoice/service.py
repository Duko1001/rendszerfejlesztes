from app.extensions import db
from app.models.invoice import Invoice

class InvoiceService:

    @staticmethod
    def get_by_rental(rid):
        invoice = db.session.query(Invoice).filter_by(rental_id=rid).first()
        if not invoice:
            return False, "Invoice not found"
        return True, invoice