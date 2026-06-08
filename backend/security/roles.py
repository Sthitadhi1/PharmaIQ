from typing import Optional

ROLES = ['ADMIN', 'CLINICAL_ANALYST', 'SALES_ANALYST', 'EXECUTIVE']


class RoleManager:
    def __init__(self):
        self.roles = ROLES

    def is_valid(self, role: str) -> bool:
        return role in self.roles

    def get_access(self, role: str, resource: str) -> bool:
        from .permissions import ROLE_PERMISSIONS
        return resource in ROLE_PERMISSIONS.get(role, [])

    def list_roles(self):
        return self.roles
