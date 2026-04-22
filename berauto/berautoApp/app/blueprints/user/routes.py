from app.blueprints.user import bp
from app.blueprints.user.schemas import UserRequestSchema, UserResponseSchema, UserLoginSchema
from app.blueprints.user.service import UserService
from app.blueprints.user.schemas import RoleSchema, UserRoleAssignSchema
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

@bp.get('/roles')
@bp.output(RoleSchema(many=True))
def list_roles():
    success, res = UserService.list_roles()
    if success: return res
    raise HTTPError(400, message=res)


@bp.get('/roles/<int:uid>')
@bp.output(RoleSchema(many=True))
def user_roles(uid):
    success, res = UserService.get_user_roles(uid)
    if success: return res
    raise HTTPError(400, message=res)


@bp.post('/roles/add')
@bp.input(UserRoleAssignSchema)
@bp.output(RoleSchema(many=True))
def add_role(data):
    success, res = UserService.add_role_to_user(data)
    if success:
        return res.roles
    raise HTTPError(400, message=res)