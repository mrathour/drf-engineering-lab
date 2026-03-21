# 🍋 LittleLemon Menu API — Stage 05: Concrete Generic Views

![Django](https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django)
![DRF](https://img.shields.io/badge/DRF-3.x-red?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Status](https://img.shields.io/badge/Stage-05%20of%2008-orange?style=flat-square)

---

## Project Overview

LittleLemon Menu API is a RESTful backend built with **Django REST Framework**, providing full CRUD operations on a restaurant menu. This project is part of a structured **DRF Engineering Lab** — an 8-stage progressive learning roadmap designed to master DRF from first principles to production-grade abstractions.

Each stage refactors the same API using a higher level of abstraction, building deep understanding of what DRF provides and why.

---

## Project Status

| Stage | Abstraction | Status |
|---|---|---|
| 01 | `@api_view` | ✅ Complete |
| 02 | `APIView` | ✅ Complete |
| 03 | `GenericAPIView` (manual HTTP methods) | ✅ Complete |
| 04 | `GenericAPIView + Mixins` | ✅ Complete |
| **05** | **Concrete Generic Views** | ✅ **Current Stage** |
| 06 | ViewSets | ⏳ Upcoming |
| 07 | ModelViewSet | ⏳ Upcoming |
| 08 | Routers | ⏳ Upcoming |

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Django 6.0 | Web framework and ORM |
| Django REST Framework | API layer |
| Djoser | Token-based auth endpoints |
| django-filter | Queryset filtering |
| SQLite | Development database |

---

## Features Implemented

- ✅ Full CRUD on Menu Items (`list`, `create`, `retrieve`, `update`, `partial update`, `delete`)
- ✅ Token Authentication via Djoser
- ✅ Role-based permissions (`Manager` write access, authenticated read access)
- ✅ Queryset filtering by `featured` field
- ✅ Search by `title`
- ✅ Ordering by `price` and `inventory`
- ✅ Paginated responses (page size: 4)

---

## API Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/menu-items/` | List all menu items | Authenticated |
| `POST` | `/api/menu-items/` | Create a menu item | Manager only |
| `GET` | `/api/menu-items/{id}/` | Retrieve a single item | Authenticated |
| `PUT` | `/api/menu-items/{id}/` | Full update of an item | Manager only |
| `PATCH` | `/api/menu-items/{id}/` | Partial update of an item | Manager only |
| `DELETE` | `/api/menu-items/{id}/` | Delete a menu item | Manager only |

### Query Parameters

| Parameter | Example | Description |
|---|---|---|
| `search` | `?search=pizza` | Search by title |
| `featured` | `?featured=true` | Filter by featured status |
| `ordering` | `?ordering=price` | Order by price or inventory |
| `page` | `?page=2` | Paginate results |

---

## Authentication

This API uses **Token Authentication**. Obtain a token via Djoser and include it in every request header.

**Obtain Token:**
```http
POST /auth/token/login/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Use Token in Requests:**
```http
GET /api/menu-items/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## Roles and Permissions

| Role | Access |
|---|---|
| **Manager** | Full read and write access to all endpoints |
| **Authenticated User** | Read-only access (`GET` requests) |
| **Unauthenticated User** | No access — `401 Unauthorized` |

Roles are managed via Django's built-in `Groups` system. Add a user to the `Manager` group to grant write access.

**Custom Permission Class:**
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
LittleLemon/
├── LittleLemon/
│   ├── settings.py          # Global DRF config: auth, pagination
│   └── urls.py              # Root URL routing
└── LittleLemonAPI/
    ├── models.py            # MenuItem model definition
    ├── serializers.py       # ModelSerializer for MenuItem
    ├── permissions.py       # Custom IsManagerOrReadOnly permission
    ├── views.py             # Concrete Generic Views (Stage 05 core)
    └── urls.py              # App-level URL patterns
```

| File | Responsibility |
|---|---|
| `settings.py` | Configures global authentication class and pagination defaults |
| `models.py` | Defines the `MenuItem` database schema |
| `serializers.py` | Handles serialization, deserialization, and field validation |
| `permissions.py` | Implements role-based write restrictions |
| `views.py` | Two view classes using `ListCreateAPIView` and `RetrieveUpdateDestroyAPIView` |
| `urls.py` | Maps URL patterns to view classes |

---

## Key Concepts Practiced

- **Concrete Generic Views** — Pre-composed DRF classes that combine `GenericAPIView` + Mixins + pre-wired HTTP method handlers
- **Mixin internals** — Understanding what `ListCreateAPIView` contains vs what Stage 4 required manually
- **`pagination_class` vs `permission_classes`** — Single class vs list; understanding why they differ
- **Filter backends** — Composing `DjangoFilterBackend`, `SearchFilter`, and `OrderingFilter`
- **Global vs per-view configuration** — What belongs in `settings.py` vs on the view class

---

## Example Code Snippets

### Stage 05 Core Views

```python
class MenuItemsView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['featured']
    ordering_fields = ['price', 'inventory']


class MenuItemDetailView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    authentication_classes = [TokenAuthentication]
```

### What DRF Eliminated (vs Stage 04)

Stage 04 required this wiring — Stage 05 removes it entirely:

```python
# Stage 04 — written manually, every time
def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)
```

### What ListCreateAPIView Contains Internally

```python
# Real DRF source code — this is what you no longer write
class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

---

## DRF Request Lifecycle

```
HTTP Request
    ↓
URL Router → matched view class
    ↓
.as_view() → dispatches to correct HTTP method handler
    ↓
Authentication (TokenAuthentication)
    ↓
Permission check (IsAuthenticated → IsManagerOrReadOnly)
    ↓
.get() calls self.list()  ←  pre-wired inside ListCreateAPIView
    ↓
get_queryset() → filter backends applied → pagination applied
    ↓
MenuItemSerializer(queryset, many=True) → serializer.data
    ↓
Response(serializer.data) → HTTP 200 JSON
```

---

## Learning Objective of This Stage

> **Why do Concrete Generic Views exist if Mixins already exist?**

Mixins provide behavior (`list()`, `create()`, etc.) but do not connect that behavior to HTTP verbs. The developer had to manually write `def get() → self.list()` every time. Concrete Generic Views pre-wire this connection. The only remaining responsibility is declaring class attributes — no method handlers needed.

**Boilerplate eliminated:** 6 HTTP method handler functions removed across both views.

---

## Next Stage in the Learning Roadmap

**Stage 06 — ViewSets**

Stage 05 introduces a structural observation: both `MenuItemsView` and `MenuItemDetailView` share identical `queryset`, `serializer_class`, `permission_classes`, and `authentication_classes`. At 2 views this is manageable. At 15 views it becomes a maintenance problem.

ViewSets resolve this by grouping related views into a single class, so shared configuration is declared once.

---

## Author Notes

This project is intentionally built in progressive stages rather than jumping straight to `ModelViewSet + Routers`. Each stage isolates one abstraction, making it possible to clearly understand what DRF provides vs what the developer was previously writing manually.

The goal is not just to use DRF — it is to understand every layer it abstracts away.

---

*Part of the DRF Engineering Lab — an 8-stage backend learning roadmap.*