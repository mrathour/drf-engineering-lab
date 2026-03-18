# DRF Engineering Lab

This repository documents a structured learning journey through **Django REST Framework (DRF)** by rebuilding the same API using progressively higher-level abstractions.

Instead of learning DRF concepts in isolation, this project demonstrates how the framework evolves from low-level function-based views to highly abstracted router-driven APIs.

The goal is to deeply understand **how DRF abstractions build on top of each other**.

---

# The DRF Abstraction Ladder

Each stage in this repository rebuilds the same API using a different DRF abstraction level.

1. Stage 01 — `@api_view`
2. Stage 02 — `APIView`
3. Stage 03 — `GenericAPIView`
4. Stage 04 — `Mixins`
5. Stage 05 — `Concrete Generic Views`
6. Stage 06 — `ViewSets`
7. Stage 07 — `ModelViewSet`
8. Stage 08 — `Routers`

Each stage introduces a new level of abstraction while maintaining the same API functionality.

---

# Project API Domain

The API models a simplified **restaurant ordering system** similar to the Little Lemon project.

Core domains include:

* Menu Items
* Cart
* Orders
* Authentication
* User Roles

---

# Repository Structure

drf-engineering-lab/

architecture-notes/
stage-01-api-view/
stage-02-apiview/
stage-03-generic-apiview/
stage-04-mixins/
stage-05-concrete-generic-views/
stage-06-viewsets/
stage-07-modelviewset/
stage-08-routers/

---

# Learning Goal

The objective of this repository is to understand:

* How DRF request handling works
* How serializers translate models into APIs
* How DRF abstractions reduce boilerplate
* How scalable APIs are structured in Django

This repository is designed as an **engineering lab**, where the same system is rebuilt multiple times to understand the framework deeply.
