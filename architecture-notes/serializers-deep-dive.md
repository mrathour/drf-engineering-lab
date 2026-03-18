# DRF Serializers — Deep Dive

Serializers are one of the core components of Django REST Framework.
They are responsible for converting complex data types such as Django models into JSON and validating incoming request data.

---

# What a Serializer Does

A serializer performs three major tasks:

1. **Serialization**
2. **Deserialization**
3. **Validation**

Example workflow:

```
Model Instance
↓
Serializer
↓
JSON Response
```

And the reverse:

```
JSON Request
↓
Serializer Validation
↓
Model Instance
```

---

# Basic Serializer Example

```python
class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = '__all__'
```

This serializer automatically maps model fields into API fields.

---

# Serialization Example

```python
menu_item = MenuItem.objects.get(id=1)
serializer = MenuItemSerializer(menu_item)

serializer.data
```

Output:

```json
{
  "id": 1,
  "title": "Pizza",
  "price": 12.5
}
```

---

# Deserialization Example

```python
serializer = MenuItemSerializer(data=request.data)

if serializer.is_valid():
    serializer.save()
```

The serializer:

1. validates input
2. converts JSON into a model instance
3. saves it to the database

---

# Validation

DRF provides multiple validation layers:

### Field validation

```python
price = serializers.DecimalField(max_digits=6, decimal_places=2)
```

### Custom field validation

```python
def validate_price(self, value):
    if value < 0:
        raise serializers.ValidationError("Price cannot be negative")
    return value
```

### Object-level validation

```python
def validate(self, data):
    if data["price"] < 1:
        raise serializers.ValidationError("Invalid price")
    return data
```

---

# Why Serializers Are Powerful

Serializers:

* replace manual JSON parsing
* validate incoming data
* enforce schema consistency
* decouple API representation from models

They are the **bridge between Django models and API responses**.
