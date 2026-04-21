from app.blueprints.user import bp
from app.blueprints.user.schemas import UserRequestSchema, UserResponseSchema, UserLoginSchema
from app.blueprints.user.service import UserService
from apiflask import HTTPError

@bp.post("/register")
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def register(json_data):
    success, response = UserService.register(json_data)
    if success:
        return response
    raise HTTPError(400, message=response)


@bp.post("/login")
@bp.input(UserLoginSchema, location="json")
@bp.output(UserResponseSchema)
def login(json_data):
    success, response = UserService.login(json_data)
    if success:
        return response
    raise HTTPError(400, message=response)