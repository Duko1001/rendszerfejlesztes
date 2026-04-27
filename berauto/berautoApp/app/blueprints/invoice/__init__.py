from app.blueprints.rental import bp as bp_rental
bp.register_blueprint(bp_rental, url_prefix='/rental')

from app.blueprints.invoice import bp as bp_invoice
bp.register_blueprint(bp_invoice, url_prefix='/invoice')