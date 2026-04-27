from app.blueprints.invoice import bp
from app.blueprints.invoice.schemas import InvoiceResponseSchema
from app.blueprints.invoice.service import InvoiceService
from apiflask import HTTPError

@bp.get("/rental/<int:rid>")
@bp.output(InvoiceResponseSchema)
def get_invoice_by_rental(rid):
    success, res = InvoiceService.get_by_rental(rid)
    if success: return res
    raise HTTPError(404, message=res)