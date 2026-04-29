from app.blueprints.user import bp
from app.blueprints.user.schemas import UserRequestSchema, UserResponseSchema, UserLoginSchema
from app.blueprints.user.service import UserService
from app.blueprints.user.schemas import RoleSchema, UserRoleAssignSchema
from apiflask import HTTPError
from app.extensions import auth
from app.blueprints import role_required

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
@bp.auth_required(auth)
@role_required(["ADMIN"])
def list_roles():
    success, res = UserService.list_roles()
    if success: return res
    raise HTTPError(400, message=res)


@bp.get('/myroles')
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
def my_roles():
    user_id = auth.current_user.get("user_id")
    success, res = UserService.get_user_roles(user_id)
    if success: return res
    raise HTTPError(400, message=res)


@bp.post('/roles/add')
@bp.input(UserRoleAssignSchema)
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["ADMIN"])
def add_role(json_data):
    success, res = UserService.add_role_to_user(json_data)
    if success:
        return res.roles
    raise HTTPError(400, message=res)

@bp.delete('/delete/<int:uid>')
@bp.auth_required(auth)
@role_required(["ADMIN"])
def delete_user(uid):
    success, res = UserService.delete(uid)
    if success:
        return {"message": res}
    raise HTTPError(400, message=res)

@bp.get('/list')
@bp.output(UserResponseSchema(many=True))
@bp.auth_required(auth)
@role_required(["ADMIN"])
def list_users():
    success, res = UserService.get_all_users()
    if success:
        return res
    raise HTTPError(400, message=res)