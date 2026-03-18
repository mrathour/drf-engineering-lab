# DRF View Abstractions

Django REST Framework provides multiple layers of abstractions for building APIs.

Each abstraction reduces boilerplate while increasing automation.

---

# DRF Abstraction Ladder

The DRF view system evolves through the following layers:

```
Function Based Views
↓
APIView
↓
GenericAPIView
↓
Mixins
↓
Concrete Generic Views
↓
ViewSets
↓
ModelViewSet
↓
Routers
```

Each layer builds on top of the previous one.

---

# APIView

`APIView` is the foundation of DRF class-based views.

Example:

```python
class MenuItemsView(APIView):

    def get(self, request):
        ...

    def post(self, request):
        ...
```

It provides:

* request parsing
* authentication
* permission checks
* response rendering

---

# GenericAPIView

`GenericAPIView` extends APIView and adds:

* queryset support
* serializer support
* pagination
* filtering

Example:

```python
class MenuItemsView(GenericAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
```

---

# Mixins

Mixins provide reusable CRUD behavior.

Examples:

```
ListModelMixin
CreateModelMixin
RetrieveModelMixin
UpdateModelMixin
DestroyModelMixin
```

Example:

```python
class MenuItemsView(
    ListModelMixin,
    CreateModelMixin,
    GenericAPIView
):
```

---

# Concrete Generic Views

DRF provides prebuilt generic views combining mixins.

Examples:

```
ListCreateAPIView
RetrieveUpdateDestroyAPIView
```

These remove most boilerplate code.

---

# ViewSets

ViewSets combine multiple view behaviors into a single class.

Example:

```python
class MenuItemViewSet(ModelViewSet):
```

Routers automatically generate URL routes.

---

# Why These Abstractions Exist

DRF abstractions:

* reduce repetitive code
* standardize API patterns
* improve maintainability
* speed up development

Understanding the abstraction ladder helps developers choose the **right level of control vs automation**.
