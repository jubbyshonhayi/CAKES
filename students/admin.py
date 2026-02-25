"""Student model intentionally not registered in admin.

Superusers manage tenants (schools and users) only.
Student operations are restricted to school users through tenant-scoped views.
"""
