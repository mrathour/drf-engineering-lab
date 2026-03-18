# Little Lemon API

REST API for managing restaurant menu items built using **Django REST Framework (DRF)**.

This project is part of a structured DRF learning roadmap where the framework is learned **progressively from low abstraction to high abstraction**.

Current Stage: **Function-Based API using `@api_view`**

The goal of this stage is to understand the **core mechanics of DRF** before moving to higher abstractions like APIView, Generic Views, and ViewSets.

---

# Project Status

Learning Stage: **Stage 1 – Function-Based Views (`@api_view`)**

Focus of this stage:

- Understanding DRF Request vs Django Request
- Serializers and validation
- Response objects
- HTTP status codes
- CRUD API implementation
- Token authentication
- Role-based access control using Django Groups
- Clean project structure with selectors

---

# Tech Stack

Backend Framework:
- Django
- Django REST Framework

Authentication:
- Djoser
- Token Authentication

Database:
- SQLite (development)

---

# API Endpoints

## Menu Items

| Method | Endpoint | Description | Access |
|------|------|------|------|
| GET | `/api/menu-items` | List all menu items | Authenticated |
| POST | `/api/menu-items` | Create new menu item | Manager only |
| GET | `/api/menu-items/{id}` | Retrieve menu item | Authenticated |
| PUT | `/api/menu-items/{id}` | Update menu item | Manager only |
| PATCH | `/api/menu-items/{id}` | Partial update | Manager only |
| DELETE | `/api/menu-items/{id}` | Delete menu item | Manager only |

---

# Authentication

Authentication is implemented using **Djoser with Token Authentication**.

## Register User

POST `/auth/users/`

Example request:

```json
{
 "username": "john",
 "password": "strongpassword123"
}
````

---

## Login

POST `/auth/token/login/`

Example response:

```json
{
 "auth_token": "abc123xyz"
}
```

Use the token in requests:

```
Authorization: Token abc123xyz
```

---

# Roles and Permissions

The API uses **Django Groups** for role-based access control.

Groups used in the system:

* Manager
* Delivery Crew
* Customer

Permissions implemented:

Managers can:

* create menu items
* update menu items
* delete menu items

All authenticated users can:

* view menu items

---

# Project Structure

```
LittleLemonAPI
│
├── models.py
├── serializers.py
├── selectors.py
├── views.py
├── urls.py
```

Explanation:

| File           | Responsibility                     |
| -------------- | ---------------------------------- |
| models.py      | database schema                    |
| serializers.py | validation and JSON transformation |
| selectors.py   | database queries                   |
| views.py       | API endpoint logic                 |
| urls.py        | routing                            |

Architecture pattern used:

```
views → selectors → models
```

This helps keep the code organized and easier to maintain.

---

# Key DRF Concepts Practiced

### Function-Based API Views

Using the DRF decorator:

```python
@api_view(['GET','POST'])
def menu_items(request):
```

This converts a standard Django view into a DRF API view.

---

### Serializers

Serializers handle:

* converting model objects → JSON
* validating request data

Example usage:

```python
serializer = MenuItemSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()
```

---

### request.data

DRF automatically parses incoming JSON requests.

Example request:

```json
{
 "title": "Pizza",
 "price": 12,
 "inventory": 5
}
```

Accessed inside views as:

```python
request.data
```

---

### HTTP Status Codes

Examples used in the API:

| Code | Meaning            |
| ---- | ------------------ |
| 200  | Successful request |
| 201  | Resource created   |
| 204  | Resource deleted   |
| 400  | Validation error   |
| 403  | Permission denied  |

---

# DRF Request Lifecycle

When a request hits the API, DRF processes it as follows:

Client Request
↓
URL Routing
↓
APIView Dispatch
↓
Authentication
↓
Permission Checks
↓
View Logic
↓
Serializer Validation
↓
Response Rendering
↓
JSON Response

Understanding this lifecycle helps explain why DRF introduces higher abstractions later.

---

# Learning Objective

This stage focuses on understanding **how DRF works internally** without using high-level abstractions.

Instead of ViewSets or Generic Views, CRUD logic is written manually using `@api_view`.

This helps understand:

* request processing
* serializer validation
* authentication flow
* permission checks
* API response handling

---

# Next Stage

Next step in the roadmap:

**Stage 2 – APIView**

In the next stage the function-based views will be converted into **class-based views using `APIView`** to improve structure and reduce method-checking logic.

---

# Author Notes

This project is part of a personal learning roadmap focused on mastering Django REST Framework from foundational concepts to advanced abstractions.

```
```
