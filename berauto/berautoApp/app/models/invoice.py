from datetime import datetime
from app import db

class Invoice(db.Model):
    tablename = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    rental_id = db.Column(
        db.Integer,
        db.ForeignKey("rentals.id"),
        nullable=False,
        unique=True
    )

    amount = db.Column(db.Float, nullable=False)

    issued_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    paid = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    rental = db.relationship(
        "Rental",
        back_populates="invoice"
    )

    def repr(self):
        return f"<Invoice {self.id} rental={self.rental_id}>"