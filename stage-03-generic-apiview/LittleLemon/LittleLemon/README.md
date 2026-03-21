# DRF Engineering Lab — Stage 03: GenericAPIView

> Part of a progressive Django REST Framework learning roadmap, built stage by stage with increasing abstraction.

---

## Project Overview

A fully functional **Menu Items CRUD REST API** built with Django REST Framework using `GenericAPIView` as the base view class.

This stage focuses on understanding what `GenericAPIView` provides on top of `APIView` — before introducing mixins — by implementing all HTTP methods manually while leveraging DRF's built-in infrastructure for queryset management, serialization, pagination, filtering, search, and ordering.

---

## Project Status

| Learning Stage | Status |
|---|---|
| Stage 01 — `@api_view` | ✅ Complete |
| Stage 02 — `APIView` | ✅ Complete |
| **Stage 03 — `GenericAPIView`** | ✅ **Current Stage** |
| Stage 04 — `GenericAPIView` + Mixins | 🔜 Next |
| Stage 05 — Concrete Generic Views | 🔜 Upcoming |
| Stage 06 — ViewSets | 🔜 Upcoming |
| Stage 07 — ModelViewSet | 🔜 Upcoming |
| Stage 08 — Routers | 🔜 Upcoming |

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Language |
| Django 6.x | Web framework |
| Django REST Framework | API framework |
| Djoser | Token-based authentication |
| django-filter | Field-level filtering |
| SQLite | Development database |

---

## Features Implemented

- Full CRUD for Menu Items across six endpoints
- Token authentication using Djoser
- Role-based permissions — Managers get full CRUD, all other authenticated users get read-only access
- Pagination using `PageNumberPagination`
- Exact field filtering on `featured`
- Text search on `title`
- Ordering by `price` and `inventory`
- Clean permission architecture using `BasePermission`

---

## API Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/menu-items/` | List all menu items | Authenticated |
| `POST` | `/api/menu-items/` | Create a new menu item | Manager only |
| `GET` | `/api/menu-items/{id}/` | Retrieve a single menu item | Authenticated |
| `PUT` | `/api/menu-items/{id}/` | Full update of a menu item | Manager only |
| `PATCH` | `/api/menu-items/{id}/` | Partial update of a menu item | Manager only |
| `DELETE` | `/api/menu-items/{id}/` | Delete a menu item | Manager only |

### Query Parameters — `GET /api/menu-items/`

| Parameter | Type | Example |
|---|---|---|
| `page` | Pagination | `?page=2` |
| `search` | Text search on title | `?search=burger` |
| `ordering` | Sort by field | `?ordering=price` or `?ordering=-price` |
| `featured` | Exact filter | `?featured=true` |

---

## Authentication

This API uses **Token Authentication**. Every request must include a valid token in the `Authorization` header.

```http
Authorization: Token <your_token_here>
```

Tokens are obtained via Djoser:

```http
POST /auth/token/login/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

---

## Roles and Permissions

| Role | Group Name | Access Level |
|---|---|---|
| Manager | `Manager` | Full CRUD — GET, POST, PUT, PATCH, DELETE |
| Customer | *(no group)* | Read only — GET only |
| Delivery Crew | `Delivery Crew` | Read only — GET only |

Permissions are enforced via a `BasePermission` class using DRF's `SAFE_METHODS` constant — no manual `if` checks inside view methods.

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
LittleLemonAPI/
├── models.py         # MenuItem model definition
├── serializers.py    # ModelSerializer for MenuItem
├── permissions.py    # IsManagerOrReadOnly permission class
├── views.py          # MenuItemsView and MenuItemDetailView
└── urls.py           # Endpoint routing
```

| File | Responsibility |
|---|---|
| `models.py` | Defines the `MenuItem` database schema |
| `serializers.py` | Handles serialization, deserialization, and validation |
| `permissions.py` | Defines role-based access control |
| `views.py` | Handles all API request logic using `GenericAPIView` |
| `urls.py` | Maps URL patterns to view classes |

---

## Key Concepts Practiced

| Concept | Description |
|---|---|
| `queryset` as class attribute | Lazy QuerySet declaration — no SQL until iteration |
| `get_queryset()` | Returns the declared queryset — overridable for dynamic logic |
| `get_object()` | Fetches single object by `pk`, raises 404, checks object permissions |
| `get_serializer()` | Instantiates the serializer with correct context |
| `filter_queryset()` | Applies all declared `filter_backends` to the queryset |
| `paginate_queryset()` | Slices queryset for the current page |
| `get_paginated_response()` | Returns a `Response` with pagination metadata |
| `BasePermission` | Reusable, declarative permission logic |
| `filter_backends` | Pluggable filtering, search, and ordering backends |

---

## Example Code Snippets

### View — List with Filtering and Pagination

```python
class MenuItemsView(GenericAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["featured"]
    search_fields = ["title"]
    ordering_fields = ["price", "inventory"]

    def get(self, request):
        menu_items = self.get_queryset()
        menu_items = self.filter_queryset(menu_items)   # must be called explicitly
        page = self.paginate_queryset(menu_items)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
```

### View — Detail with `get_object()`

```python
class MenuItemDetailView(GenericAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        menu_item = self.get_object()           # reads pk from URL, raises 404 if missing
        serializer = self.get_serializer(menu_item)
        return Response(serializer.data)

    def patch(self, request, pk):
        menu_item = self.get_object()
        serializer = self.get_serializer(menu_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        menu_item = self.get_object()
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

---

## DRF Request Lifecycle

```
Request
  → Authentication       (TokenAuthentication identifies the user)
  → Permission checks    (IsAuthenticated + IsManagerOrReadOnly)
  → View method called
  → get_queryset()       (returns queryset blueprint)
  → filter_queryset()    (applies filter_backends)
  → paginate_queryset()  (slices for current page)
  → get_serializer()     (serializes the data)
  → get_paginated_response() (wraps in Response with metadata)
  → Response returned
```

For detail views, `filter_queryset()` and `paginate_queryset()` are replaced by `get_object()`, which handles `pk` lookup and object-level permission checks.

---

## Learning Objective of This Stage

This stage exists to make one concept clear before mixins are introduced:

> `GenericAPIView` separates **declaration** from **execution**. You declare `queryset`, `serializer_class`, `pagination_class`, and `filter_backends` at the class level. DRF provides methods that wire them together.

The distinction between `APIView` and `GenericAPIView`:

| Concern | `APIView` | `GenericAPIView` |
|---|---|---|
| Queryset | Written manually per method | Declared once, accessed via `get_queryset()` |
| Object lookup | `get_object_or_404()` manually | `self.get_object()` — automatic |
| Serializer | Direct class instantiation | `self.get_serializer()` — context-aware |
| Pagination | Not provided | Built-in infrastructure |
| Filtering | Not provided | Built-in infrastructure |

---

## Next Stage in the Learning Roadmap

**Stage 04 — `GenericAPIView` + Mixins**

In Stage 4, the methods written manually here (`get()`, `post()`, `put()`, `patch()`, `delete()`) will be replaced by DRF Mixins:

| Mixin | Provides |
|---|---|
| `ListModelMixin` | `list()` — wraps the `get()` pattern from this stage |
| `CreateModelMixin` | `create()` — wraps the `post()` pattern |
| `RetrieveModelMixin` | `retrieve()` — wraps the detail `get()` |
| `UpdateModelMixin` | `update()` / `partial_update()` — wraps `put()` / `patch()` |
| `DestroyModelMixin` | `destroy()` — wraps `delete()` |

Stage 3 was written manually so that Stage 4 feels earned — the mixin source code will be immediately recognizable.

---

## Author Notes

This project is part of a self-directed DRF engineering lab following a strict **progressive abstraction ladder**. Each stage isolates one layer of DRF's view hierarchy and implements it fully before moving up.

The goal is not to replicate DRF internals — it is to understand each abstraction layer well enough to use it with intent in production-grade code, knowing which class to reach for and why.