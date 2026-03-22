# DRF Engineering Lab — Stage 06: ViewSets

![Django](https://img.shields.io/badge/Django-4.x-green)
![DRF](https://img.shields.io/badge/DRF-3.x-red)
![Status](https://img.shields.io/badge/Stage-06%20ViewSets-blue)
![Auth](https://img.shields.io/badge/Auth-Djoser%20Token-orange)

---

## Project Overview

A progressively built **Menu Items REST API** using Django REST Framework, refactored at each stage to use a higher level of DRF abstraction. This repository is a structured DRF learning lab — every stage solves the same problem with a cleaner, more idiomatic approach.

**Stage 06** refactors the Menu Items CRUD API from two separate Concrete Generic Views into a **single ViewSet class**, demonstrating how DRF groups all resource actions under one class and how HTTP methods are bound to actions at URL registration time.

---

## Project Status

| Roadmap Stage | Pattern | Status |
|---|---|---|
| Stage 01 | `@api_view` | ✅ Complete |
| Stage 02 | `APIView` | ✅ Complete |
| Stage 03 | `GenericAPIView` | ✅ Complete |
| Stage 04 | `GenericAPIView` + Mixins | ✅ Complete |
| Stage 05 | Concrete Generic Views | ✅ Complete |
| **Stage 06** | **ViewSets** | ✅ **Current** |
| Stage 07 | `ModelViewSet` | 🔜 Upcoming |
| Stage 08 | Routers | 🔜 Upcoming |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 4.x |
| API Layer | Django REST Framework 3.x |
| Authentication | Djoser + DRF Token Authentication |
| Filtering | `django-filter`, DRF `SearchFilter`, `OrderingFilter` |
| Pagination | DRF `PageNumberPagination` |
| Database | SQLite (development) |

---

## Features Implemented

- Full **CRUD** for Menu Items via a single `MenuItemViewSet`
- **Token-based authentication** enforced on all endpoints
- **Role-based permissions** — Managers can write, others are read-only
- **Search** by item title
- **Filtering** by featured status
- **Ordering** by price and inventory
- **Pagination** on list endpoint
- Manual URL-to-action binding via `.as_view()` dict — no Router used (intentionally)

---

## API Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/menu-items/` | List all menu items (paginated) | Authenticated |
| `POST` | `/api/menu-items/` | Create a new menu item | Manager only |
| `GET` | `/api/menu-items/{id}/` | Retrieve a single menu item | Authenticated |
| `PUT` | `/api/menu-items/{id}/` | Full update of a menu item | Manager only |
| `PATCH` | `/api/menu-items/{id}/` | Partial update of a menu item | Manager only |
| `DELETE` | `/api/menu-items/{id}/` | Delete a menu item | Manager only |

### Query Parameters (on `GET /api/menu-items/`)

| Parameter | Type | Example |
|---|---|---|
| `search` | string | `?search=pizza` |
| `featured` | boolean | `?featured=true` |
| `ordering` | field name | `?ordering=price` or `?ordering=-price` |

---

## Authentication

All endpoints require a valid **Token** in the request header. Tokens are issued via Djoser's auth endpoints.

### Obtain a Token

```http
POST /auth/token/login/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Use the Token

Include the token in every subsequent request:

```http
Authorization: Token <your_token_here>
```

Requests without a valid token receive `401 Unauthorized`.

---

## Roles and Permissions

| Role | Group | Permissions |
|---|---|---|
| **Manager** | `Manager` Django group | Full CRUD access |
| **Customer** | No group assigned | Read-only (`GET` only) |
| **Unauthenticated** | — | `401 Unauthorized` |

Permission logic is handled by a custom `IsManagerOrReadOnly` permission class:

```python
class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Manager').exists()
```

---

## Project Architecture

```
restaurant_api/
├── menu/
│   ├── models.py          # MenuItem model definition
│   ├── serializers.py     # MenuItemSerializer
│   ├── views.py           # MenuItemViewSet (Stage 06)
│   ├── urls.py            # Manual action-map URL wiring
│   └── permissions.py     # IsManagerOrReadOnly
├── config/
│   ├── settings.py        # DRF, Djoser, filter config
│   └── urls.py            # Root URL configuration
└── manage.py
```

| File | Responsibility |
|---|---|
| `models.py` | Defines `MenuItem` with `title`, `price`, `inventory`, `featured` fields |
| `serializers.py` | Validates and serializes `MenuItem` data |
| `views.py` | Single `MenuItemViewSet` — all CRUD actions in one class |
| `urls.py` | Binds HTTP methods to ViewSet actions via `.as_view()` |
| `permissions.py` | Custom permission — write access for Managers only |

---

## Key Concepts Practiced

| Concept | Description |
|---|---|
| `GenericViewSet` | Combines `GenericAPIView` infrastructure with ViewSet routing |
| Action methods | Named actions (`list`, `create`, `retrieve`, etc.) replace HTTP method handlers |
| Manual URL binding | `.as_view({'get': 'list'})` maps HTTP verbs to actions explicitly |
| `get_object()` | Automatic pk-based lookup with 404 handling and object-level permissions |
| `get_queryset()` | Centralized queryset access used by all actions |
| `filter_queryset()` | Applies all registered filter backends in one call |
| `paginate_queryset()` | Handles page slicing for list responses |

---

## Example Code Snippets

### ViewSet Definition

```python
from rest_framework.viewsets import GenericViewSet

class MenuItemViewSet(GenericViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['featured']
    ordering_fields = ['price', 'inventory']
    pagination_class = PageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        menu_item = self.get_object()
        serializer = self.get_serializer(menu_item)
        return Response(serializer.data)

    def update(self, request, pk):
        menu_item = self.get_object()
        serializer = self.get_serializer(menu_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        menu_item = self.get_object()
        serializer = self.get_serializer(menu_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        menu_item = self.get_object()
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### Manual URL-to-Action Binding

```python
# urls.py — This is what a Router generates automatically in Stage 08
from django.urls import path
from . import views

urlpatterns = [
    path(
        'menu-items/',
        views.MenuItemViewSet.as_view({'get': 'list', 'post': 'create'})
    ),
    path(
        'menu-items/<int:pk>/',
        views.MenuItemViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        })
    ),
]
```

---

## DRF Request Lifecycle (Stage 06)

```
HTTP Request
    │
    ▼
urls.py — .as_view({'get': 'list'})
    │       Maps HTTP verb → action name at registration time
    ▼
ViewSet.initialize_request()
    │       Wraps request, runs authentication
    ▼
ViewSet.initial()
    │       Runs permission checks
    ▼
Action method — list() / create() / retrieve() / etc.
    │       Executes business logic using GenericAPIView tools
    ▼
Response
```

---

## Learning Objective of This Stage

> **How does DRF map URLs to actions in a ViewSet, and why is ViewSet a better abstraction for larger APIs?**

Stage 06 answers this by:

1. Replacing two view classes with **one ViewSet class** per resource
2. Replacing HTTP method names with **semantic action names**
3. Writing the HTTP→action binding **manually** in `urls.py` — exactly what Routers automate in Stage 08

The key insight: a ViewSet has **no knowledge of HTTP verbs**. The binding is declared externally at URL registration. This separation is what makes Routers possible.

---

## Next Stage: Stage 07 — ModelViewSet

Stage 07 will demonstrate that every action written manually in Stage 06 can be replaced by inheriting from `ModelViewSet`:

```python
# All six actions — for free
class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
```

Stage 06 was written by hand precisely so that Stage 07's automation is fully understood — not taken for granted.

---

## Author Notes

This project follows a **strict progressive abstraction ladder**. Each stage solves an identical problem at a higher level of DRF abstraction. No stage skips ahead — every automation is understood before it is used.

The goal is not to build fast, but to understand deeply. By Stage 08, the same API will be fully functional with a fraction of the code — and every line of that code will be understood from first principles.