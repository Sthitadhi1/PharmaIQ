from fastapi import APIRouter
from security.roles import RoleManager
from security.permissions import ROLE_PERMISSIONS

router = APIRouter(prefix='/api/auth', tags=['Security'])
role_manager = RoleManager()


@router.get('/roles')
def list_roles():
    return {'roles': role_manager.list_roles(), 'permissions': ROLE_PERMISSIONS}
