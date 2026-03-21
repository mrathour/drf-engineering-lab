# 🍋 Little Lemon API — DRF Engineering Lab (Stage 04)

---

## 🚀 Project Overview

This project is a **RESTful API built using Django REST Framework (DRF)** for managing menu items in a restaurant system.

It is part of a structured **DRF Engineering Lab**, where the same API is implemented across multiple abstraction levels to deeply understand how DRF works internally.

This stage focuses on:

```text
GenericAPIView + Mixins
````

The goal is to understand how DRF **injects reusable CRUD behavior using mixins**, reducing boilerplate while maintaining flexibility.

---

## 📌 Project Status

**Current Stage:**
✅ **Stage 04 — GenericAPIView + Mixins**

Progression:

```
Stage 01 — @api_view
Stage 02 — APIView
Stage 03 — GenericAPIView (manual methods)
Stage 04 — GenericAPIView + Mixins  ← Current
Stage 05 — Concrete Generic Views (Next)
```

---

## 🛠️ Tech Stack

| Technology            | Purpose                  |
| --------------------- | ------------------------ |
| Django                | Web framework            |
| Django REST Framework | API development          |
| Djoser                | Authentication endpoints |
| Token Authentication  | Secure API access        |
| SQLite                | Development database     |

---

## ✨ Features Implemented

* Full CRUD API for menu items
* Token-based authentication (Djoser)
* Custom role-based permissions
* Filtering using query parameters
* Search functionality
* Ordering results
* Pagination support
* Dynamic querysets (`get_queryset`)
* Business logic hooks (`perform_create`)
* Dynamic serializers (`get_serializer_class`)

---

## 📡 API Endpoints

| Method | Endpoint                | Description          | Access              |
| ------ | ----------------------- | -------------------- | ------------------- |
| GET    | `/api/menu-items/`      | List all menu items  | Authenticated users |
| POST   | `/api/menu-items/`      | Create a menu item   | Manager only        |
| GET    | `/api/menu-items/{id}/` | Retrieve a menu item | Authenticated users |
| PUT    | `/api/menu-items/{id}/` | Update a menu item   | Manager only        |
| PATCH  | `/api/menu-items/{id}/` | Partial update       | Manager only        |
| DELETE | `/api/menu-items/{id}/` | Delete a menu item   | Manager only        |

---

## 🔐 Authentication

Authentication is handled using **Token Authentication via Djoser**.

### Obtain Token

```
POST /auth/token/login/
```

Request:

```json
{
  "username": "user",
  "password": "password"
}
```

Response:

```json
{
  "auth_token": "your_token_here"
}
```

### Use Token

Include in request headers:

```
Authorization: Token your_token_here
```

---

## 👥 Roles and Permissions

Custom permission class:

```python
class IsManagerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user.groups.filter(name="manager").exists()
```

| Role          | Access    |
| ------------- | --------- |
| Customer      | Read-only |
| Delivery Crew | Read-only |
| Manager       | Full CRUD |

---

## 🏗️ Project Architecture

```
LittleLemon/
│
├── LittleLemon/
│   ├── settings.py
│   ├── urls.py
│
├── LittleLemonAPI/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│
└── manage.py
```

### Responsibilities

| File           | Responsibility                   |
| -------------- | -------------------------------- |
| models.py      | Database schema                  |
| serializers.py | Data validation & transformation |
| views.py       | API logic                        |
| permissions.py | Access control                   |
| urls.py        | Routing                          |
| settings.py    | Global configuration             |

---

## 🧠 Key Concepts Practiced

* `GenericAPIView`
* DRF Mixins (CRUD behavior)
* Querysets & dynamic filtering
* Serializers & validation
* Authentication (Token-based)
* Custom permissions
* Pagination, search, ordering
* DRF request lifecycle
* Business logic hooks
* Dynamic serializer selection

---

## 💡 Example Code Snippets

### GenericAPIView + Mixins

```python
class MenuItemsView(
    ListModelMixin,
    CreateModelMixin,
    GenericAPIView
):

    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        return MenuItem.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
```

---

### Filtering with Query Params

```python
def get_queryset(self):

    queryset = MenuItem.objects.all()

    featured = self.request.query_params.get("featured")

    if featured:
        queryset = queryset.filter(featured=True)

    return queryset
```

---

### Business Logic Hook

```python
def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)
```

---

## 🔄 DRF Request Lifecycle

```
Client Request
↓
URL Routing
↓
APIView.dispatch()
↓
Authentication
↓
Permissions
↓
View method
↓
Mixin method (list/create/etc.)
↓
Queryset retrieval
↓
Serializer processing
↓
Response
```

---

## 🎯 Learning Objective of This Stage

This stage answers:

👉 How do mixins convert `GenericAPIView` into a working CRUD API?

👉 How does DRF reduce boilerplate using reusable components?

Key insight:

```
GenericAPIView → infrastructure
Mixins → behavior
View → HTTP mapping
```

---

## ⏭️ Next Stage

```
Stage 05 — Concrete Generic Views
```

Examples:

* `ListCreateAPIView`
* `RetrieveUpdateDestroyAPIView`

These eliminate the need for manually defining HTTP methods.

---

## 📝 Author Notes

This project is part of a **progressive DRF learning journey**, where each stage rebuilds the same API using a higher abstraction level.

The focus is not just building APIs, but understanding:

* How DRF works internally
* Why abstractions exist
* When to use each layer

---

⭐ If you're learning DRF, this repository is designed to help you **think like a backend engineer, not just write code**.

```
```
