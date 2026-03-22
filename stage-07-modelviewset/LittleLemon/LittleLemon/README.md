# DRF Engineering Lab — Stage 07: ModelViewSet

> Part of a progressive DRF abstraction ladder built to master Django REST Framework from the ground up.

---

## Project Overview

A fully functional **Menu Items REST API** built with Django REST Framework, refactored at each stage to use a higher level of abstraction. This stage implements the API using `ModelViewSet` — DRF's most complete ViewSet class — which composes all CRUD mixins into a single, declarative class.

The project is part of an **8-stage DRF learning roadmap**, progressing from raw `@api_view` decorators all the way to Router-based URL generation.

---

## Project Status

| Roadmap Stage | Abstraction Used | Status |
|---|---|---|
| Stage 01 | `@api_view` | ✅ Complete |
| Stage 02 | `APIView` | ✅ Complete |
| Stage 03 | `GenericAPIView` | ✅ Complete |
| Stage 04 | `GenericAPIView + Mixins` | ✅ Complete |
| Stage 05 | Concrete Generic Views | ✅ Complete |
| Stage 06 | `GenericViewSet` | ✅ Complete |
| **Stage 07** | **`ModelViewSet`** | ✅ **Current** |
| Stage 08 | Routers | 🔜 Next |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Framework | Django 4.x |
| API Layer | Django REST Framework |
| Authentication | Djoser + DRF Token Authentication |
| Filtering | `django-filter` |
| Database | SQLite (development) |

---

## Features Implemented

- ✅ Full CRUD for Menu Items (list, create, retrieve, update, partial update, delete)
- ✅ Token-based authentication via Djoser
- ✅ Role-based permissions — Manager (full access) vs Customer (read-only)
- ✅ Search by item title (`?search=burger`)
- ✅ Filter by featured status (`?featured=true`)
- ✅ Ordering by price (`?ordering=price`)
- ✅ Pagination — 2 items per page (`?page=2`)
- ✅ All endpoints wired manually using `.as_view()` (no Routers yet)

---

## API Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/menu-items/` | List all menu items | Authenticated |
| `POST` | `/api/menu-items/` | Create a new menu item | Manager only |
| `GET` | `/api/menu-items/{id}/` | Retrieve a single item | Authenticated |
| `PUT` | `/api/menu-items/{id}/` | Full update of an item | Manager only |
| `PATCH` | `/api/menu-items/{id}/` | Partial update of an item | Manager only |
| `DELETE` | `/api/menu-items/{id}/` | Delete an item | Manager only |

### Query Parameters

| Parameter | Example | Description |
|---|---|---|
| `search` | `?search=pizza` | Filter items by title |
| `featured` | `?featured=true` | Filter by featured status |
| `ordering` | `?ordering=price` | Order results by price |
| `page` | `?page=2` | Navigate paginated results |

---

## Authentication

This project uses **Djoser** with DRF's built-in `TokenAuthentication`.

**Obtain a token:**
```
POST /auth/token/login/
Body: { "username": "...", "password": "..." }
```

**Use the token in all requests:**
```
Authorization: Token <your_token_here>
```

Requests without a valid token receive a `401 Unauthorized` response before any permission checks run.

---

## Roles and Permissions

| Role | Group | Access Level |
|---|---|---|
| **Manager** | `Manager` Django group | Full CRUD on all endpoints |
| **Customer** | No group assigned | Read-only (GET requests only) |
| **Unauthenticated** | — | 401 Unauthorized |

Permissions are enforced via a custom `IsManagerOrReadOnly` permission class:

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
stage_07/
│
├── views.py          # MenuItemViewSet — ModelViewSet with declarative config
├── urls.py           # Manual .as_view() URL patterns (no Router)
├── serializers.py    # MenuItemSerializer
├── models.py         # MenuItem model
├── permissions.py    # IsManagerOrReadOnly custom permission
└── paginations.py    # MenuItemPagination (page_size = 2)
```

### File Responsibilities

| File | Responsibility |
|---|---|
| `views.py` | ViewSet with queryset, serializer, permissions, filtering, pagination |
| `urls.py` | Maps HTTP methods to ViewSet actions via `.as_view()` |
| `serializers.py` | Validates and serializes `MenuItem` model data |
| `models.py` | Defines `MenuItem` database schema |
| `permissions.py` | Custom role-based access control logic |
| `paginations.py` | Isolated pagination config — `page_size = 2` |

---

## Key Concepts Practiced

- **ModelViewSet composition** — understanding it as `GenericViewSet` + all 5 mixins
- **Declarative ViewSet configuration** — zero hand-written action methods
- **Layered permission enforcement** — `IsAuthenticated` → `IsManagerOrReadOnly`
- **Filter backend chaining** — `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`
- **Per-resource pagination** — custom subclass instead of global `settings.py`
- **Manual URL routing** — `.as_view({...})` without Routers
- **Project structure** — isolating concerns across `permissions.py`, `paginations.py`

---

## Example Code Snippets

### The Complete ViewSet

```python
class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['featured']
    ordering_fields = ['price']
    pagination_class = MenuItemPagination
```

### URL Wiring Without Routers

```python
urlpatterns = [
    path('menu-items/', views.MenuItemViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('menu-items/<int:pk>/', views.MenuItemViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
]
```

### Custom Pagination

```python
class MenuItemPagination(PageNumberPagination):
    page_size = 2
```

---

## DRF Request Lifecycle

```
HTTP Request
    │
    ▼
Authentication     → TokenAuthentication verifies token
    │
    ▼
Permissions        → IsAuthenticated → IsManagerOrReadOnly
    │
    ▼
Filter Backends    → DjangoFilter → SearchFilter → OrderingFilter
    │
    ▼
ViewSet Action     → list / create / retrieve / update / destroy
    │
    ▼
Serializer         → Validates input / Serializes output
    │
    ▼
Pagination         → MenuItemPagination slices queryset
    │
    ▼
HTTP Response
```

---

## Learning Objective of This Stage

> **Why is `ModelViewSet` the most commonly used DRF abstraction?**

`ModelViewSet` composes all five CRUD mixins into a single class. Declaring `queryset` and `serializer_class` is sufficient to activate all six endpoints automatically. Every other behaviour — permissions, filtering, pagination — is added declaratively, not procedurally.

**The result:** zero hand-written action methods, full CRUD coverage, and complete customization control through attribute declarations and optional method overrides.


## Next Stage — Stage 08: Routers

Currently, URL wiring requires two manual `path()` entries per resource:

```python
path('menu-items/', ...as_view({'get': 'list', 'post': 'create'})),
path('menu-items/<int:pk>/', ...as_view({...})),
```

**Stage 08 replaces both lines with:**

```python
router = DefaultRouter()
router.register('menu-items', MenuItemViewSet)
urlpatterns = router.urls
```

Routers introspect the ViewSet and generate all URL patterns automatically.

---

## Author Notes

This project is a **learning artifact**, not a production application. Each stage is intentionally isolated to highlight the abstraction being practiced. Code is kept minimal to keep the learning signal clean.

The progressive refactor approach — rewriting the same API at each abstraction level — is deliberate: it makes the value of each layer tangible rather than theoretical.

---

*DRF Engineering Lab — Built stage by stage to understand DRF from the inside out.*