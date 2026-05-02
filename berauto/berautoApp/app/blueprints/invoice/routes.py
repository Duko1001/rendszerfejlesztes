from app.blueprints.invoice import bp
from app.blueprints.invoice.schemas import InvoiceResponseSchema
from app.blueprints.invoice.service import InvoiceService
from apiflask import HTTPError
from app.extensions import auth

@bp.get("/rental/<int:rid>")
@bp.output(InvoiceResponseSchema)
@bp.auth_required(auth)
def get_invoice_by_rental(rid):

    from app.blueprints import role_required

    @role_required(["ADMIN", "USER"])
    def inner():
        current_user = auth.current_user
        success, res = InvoiceService.get_by_rental(rid, current_user)
        if success:
            return res
        raise HTTPError(404, message=res)

    return inner()