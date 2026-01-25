## Permissions and Groups Setup

Custom permissions were added to the Book model using Django Meta permissions:
- can_view
- can_create
- can_edit
- can_delete

Groups were created using the Django admin interface:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: all permissions

Views are protected using the permission_required decorator to enforce access control.
