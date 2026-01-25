# LibraryProject

This is a basic Django project created to demonstrate Django project setup and running the development server.


## Permissions and Groups

Custom permissions were added to the Book model:
- can_view
- can_create
- can_edit
- can_delete

User groups were created using the Django admin interface:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: all permissions

Views are protected using Django's permission_required decorator.
