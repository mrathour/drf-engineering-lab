# Authentication and Permissions in DRF

Django REST Framework separates **authentication** from **authorization (permissions)**.

Authentication answers:

```
Who is the user?
```

Permissions answer:

```
Is the user allowed to perform this action?
```

---

# Authentication

Authentication identifies the user making the request.

Common DRF authentication methods:

* Session Authentication
* Token Authentication
* JWT Authentication

Example configuration:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ]
}
```

When authentication succeeds:

```
request.user
```

contains the authenticated user.

---

# Token Authentication Example

Client sends:

```
Authorization: Token 123abc456
```

DRF verifies the token and associates it with a user.

---

# Permissions

Permissions determine whether a user can access a view.

Example permission classes:

```
AllowAny
IsAuthenticated
IsAdminUser
```

Example:

```python
permission_classes = [IsAuthenticated]
```

This allows access only to authenticated users.

---

# Custom Permissions

DRF allows custom permission classes.

Example:

```python
class IsManagerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user.groups.filter(name="manager").exists()
```

This allows:

* read access to everyone
* write access only to managers

---

# Permission Execution Order

When a request arrives:

```
Authentication
↓
Permission Check
↓
View Logic
```

If permission fails:

```
403 Forbidden
```

---

# Why Permissions Matter

Permissions allow APIs to implement:

* role-based access control
* protected resources
* secure operations
* admin-only endpoints
