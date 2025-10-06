from django.db import models
from authentication.models import User


class Role(models.Model):
    """
    Role model for RBAC system
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'roles'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserRole(models.Model):
    """
    Junction table for many-to-many relationship between Users and Roles
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_roles'
    )
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE, 
        related_name='role_users'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        unique_together = ('user', 'role')
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


class BusinessElement(models.Model):
    """
    Business elements/resources that can have access control
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'business_elements'
        ordering = ['name']

    def __str__(self):
        return self.name


class AccessRoleRule(models.Model):
    """
    Access control rules defining permissions for each role on each business element
    """
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE, 
        related_name='access_rules'
    )
    element = models.ForeignKey(
        BusinessElement, 
        on_delete=models.CASCADE, 
        related_name='access_rules'
    )
    
    # Permission fields
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        db_table = 'access_roles_rules'
        unique_together = ('role', 'element')
        ordering = ['role', 'element']

    def __str__(self):
        return f"{self.role.name} - {self.element.name}"
