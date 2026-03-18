# DRF Request Lifecycle

Understanding the request lifecycle is essential to understanding how Django REST Framework processes API requests.

This document explains the internal flow of a request through DRF.

---

# High Level Flow

Client Request
↓
URL Routing
↓
View Dispatch
↓
Authentication
↓
Permission Checks
↓
Throttle Checks
↓
View Logic Execution
↓
Serializer Processing
↓
Response Generation

---

# Step 1 — Client Request

A client sends an HTTP request:

Example:

GET /api/menu-items/

The request contains:

* HTTP method
* headers
* query parameters
* request body (for POST/PUT/PATCH)

---

# Step 2 — URL Routing

Django routes the request through:

```
urls.py
```

Example:

```python
path('menu-items/', views.MenuItemsView.as_view())
```

The router determines **which view handles the request**.

---

# Step 3 — View Dispatch

The request enters the DRF view system.

For class-based views:

```
APIView.dispatch()
```

This method:

1. Wraps the Django request
2. Converts it into a DRF `Request` object
3. Determines the HTTP method handler

Example:

```
GET → get()
POST → post()
PUT → put()
```

---

# Step 4 — Authentication

DRF authenticates the user using configured authentication classes.

Example:

```
TokenAuthentication
SessionAuthentication
```

The authenticated user is attached to:

```
request.user
```

---

# Step 5 — Permission Checks

After authentication, DRF checks permissions.

Example:

```
IsAuthenticated
IsAdminUser
Custom permissions
```

If permission fails:

```
403 Forbidden
```

---

# Step 6 — Throttling (Optional)

DRF may apply request throttling.

Example:

```
100 requests per hour
```

This prevents abuse.

---

# Step 7 — View Logic Execution

The view method executes.

Examples:

```
get()
post()
put()
delete()
```

This is where the view:

* retrieves querysets
* validates input
* calls serializers

---

# Step 8 — Serializer Processing

Serializers handle:

* validation
* data transformation
* model conversion

Example:

```
serializer = MenuItemSerializer(data=request.data)
serializer.is_valid()
serializer.save()
```

---

# Step 9 — Response Generation

Finally DRF returns a `Response` object.

Example:

```
return Response(serializer.data)
```

DRF automatically renders the response into:

```
JSON
```

---

# Why This Matters

Understanding this lifecycle helps developers:

* debug APIs effectively
* customize authentication and permissions
* extend DRF behavior
* build scalable APIs
