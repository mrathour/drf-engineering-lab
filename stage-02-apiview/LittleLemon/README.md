
# 🍋 Little Lemon Menu API — DRF APIView Stage

## Project Overview

This project implements a **Menu Items REST API** for a restaurant backend using **Django REST Framework (DRF)**.

The API allows authenticated users to **view menu items**, while users with the **Manager role** can perform full CRUD operations.

This project is part of a **progressive Django REST Framework learning roadmap**, where the same API is rebuilt using increasingly powerful DRF abstractions to gain a deep understanding of how the framework works internally.

Current implementation uses **`APIView`**, the foundational class-based view in DRF.

---

# Project Status

🚧 **Learning Stage:** Stage 2 — APIView

Completed stages:

```

1️⃣ Plain Django View
2️⃣ DRF @api_view
3️⃣ APIView (Current Stage)

```

Upcoming stages:

```

4️⃣ GenericAPIView + Mixins
5️⃣ Concrete Generic Views
6️⃣ ViewSets
7️⃣ ModelViewSet
8️⃣ Routers

````

---

# Tech Stack

| Technology | Purpose |
|-----------|--------|
| **Python** | Backend programming language |
| **Django** | Web framework |
| **Django REST Framework** | API development |
| **Djoser** | Authentication endpoints |
| **Token Authentication** | Secure API access |
| **SQLite** | Development database |

---

# Features Implemented

- Menu item **CRUD API**
- Class-based API using **DRF APIView**
- **Token-based authentication**
- **Role-based permissions**
- Input validation using **DRF serializers**
- Clean architecture with **selectors and permissions layers**
- Proper **HTTP status codes**
- RESTful API design

---

# API Endpoints

| Method | Endpoint | Description | Access |
|------|---------|-------------|--------|
| GET | `/api/menu-items` | Retrieve all menu items | Authenticated |
| POST | `/api/menu-items` | Create a menu item | Manager |
| GET | `/api/menu-items/{id}` | Retrieve single menu item | Authenticated |
| PUT | `/api/menu-items/{id}` | Full update | Manager |
| PATCH | `/api/menu-items/{id}` | Partial update | Manager |
| DELETE | `/api/menu-items/{id}` | Delete menu item | Manager |

---

# Authentication

The API uses **Token Authentication** provided by **Djoser**.

Users authenticate by sending a token in the request header.

### Example Request Header

```http
Authorization: Token 123abc456xyz
````

When authenticated successfully, DRF populates:

```python
request.user
```

---

# Roles and Permissions

The API implements **role-based access control** using Django groups.

| Role          | Permissions |
| ------------- | ----------- |
| Manager       | Full CRUD   |
| Customer      | Read-only   |
| Delivery Crew | Read-only   |

Example permission check:

```python
def is_manager(user):
    return user.groups.filter(name="Manager").exists()
```

---

# Project Architecture

```
menu/
│
├── models.py
├── serializers.py
├── selectors.py
├── permissions.py
├── views.py
└── urls.py
```

### File Responsibilities

| File             | Responsibility                    |
| ---------------- | --------------------------------- |
| `models.py`      | Database schema                   |
| `serializers.py` | Data serialization and validation |
| `selectors.py`   | Query logic                       |
| `permissions.py` | Role helper functions             |
| `views.py`       | API request handling              |
| `urls.py`        | Route definitions                 |

This separation follows a **clean architecture pattern** that improves maintainability.

---

# Key Concepts Practiced

This stage focuses on understanding **core DRF API architecture**.

Concepts covered:

* APIView fundamentals
* Class-based API design
* HTTP method mapping
* Serializer validation
* Request parsing (`request.data`)
* Object retrieval patterns
* Token authentication
* Permission checks
* RESTful API responses
* Proper HTTP status codes

---

# Example Code Snippets

### APIView Example

```python
class MenuItemsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        menu_items = get_all_menu_items()
        serializer = MenuItemsSerializer(menu_items, many=True)
        return Response(serializer.data)
```

---

### Serializer Validation

```python
serializer = MenuItemsSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()
```

---

### Update Pattern

```python
serializer = MenuItemsSerializer(
    instance,
    data=request.data
)
```

---

### Partial Update

```python
serializer = MenuItemsSerializer(
    instance,
    data=request.data,
    partial=True
)
```

---

# DRF Request Lifecycle

When a request reaches the API:

```
HTTP Request
   ↓
APIView.dispatch()
   ↓
Authentication
   ↓
Permission checks
   ↓
HTTP method handler (get/post/etc)
   ↓
Serializer processing
   ↓
Response returned
```

This lifecycle is the backbone of how **Django REST Framework processes API requests**.

---

# Learning Objective of This Stage

The purpose of this stage is to understand **how DRF APIs work internally** before using higher-level abstractions.

Key takeaway:

```
APIView = Manual control over API logic
```

This stage helps developers understand:

* request processing
* serializer workflows
* permission handling
* CRUD implementation

---

# Next Stage in the Learning Roadmap

Next step:

### GenericAPIView + Mixins

This stage introduces:

* `GenericAPIView`
* `ListModelMixin`
* `CreateModelMixin`
* `RetrieveModelMixin`
* `UpdateModelMixin`
* `DestroyModelMixin`

These abstractions reduce the **boilerplate code required by APIView**.

Example transformation:

```
APIView implementation → ~70 lines
GenericAPIView version → ~15 lines
```

---

# Author Notes

This project is part of a **deep-dive learning approach to Django REST Framework**.

Instead of jumping directly to high-level abstractions like `ModelViewSet`, the API is rebuilt multiple times using progressively more abstract DRF layers.

Learning progression:

```
Plain Django Views
↓
Function-based DRF Views
↓
APIView
↓
Generic Views
↓
ViewSets
↓
Routers
```

The goal is to develop a **strong conceptual understanding of DRF architecture** rather than relying on framework magic.

---

⭐ If you're also learning DRF, try rebuilding the same API using each abstraction layer — it's one of the fastest ways to master the framework.

```
```
