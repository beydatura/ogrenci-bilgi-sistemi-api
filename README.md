# Student Information System API

A REST API project built with Django and Django REST Framework (DRF) that manages a university's student, teacher, course, and enrollment operations.

🇬🇧 English | [🇹🇷 Türkçe](README.tr.md)

## Table of Contents

- [Purpose](#purpose)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Database Models](#database-models)
- [Model Relationships](#model-relationships)
- [Endpoint List](#endpoint-list)
- [Filtering, Search, Ordering, Pagination](#filtering-search-ordering-pagination)
- [Example Requests and Responses](#example-requests-and-responses)
- [Validation Rules](#validation-rules)
- [HTTP Status Codes](#http-status-codes)
- [API Testing](#api-testing)
- [Postman Collection](#postman-collection)

---

## Purpose

This project provides a **REST API** representing a university's student information system. A frontend (React, Vue, Angular, Android, iOS, or any other client) never connects to the database directly; all operations go through this API via HTTP requests:

```
Frontend / Mobile App → HTTP Request → Django REST Framework API → Django ORM → Database
```

The API supports standard CRUD (Create/Read/Update/Delete) operations on Department, Student, Teacher, Course, and Enrollment resources, along with filtering, search, ordering, and pagination.

## Tech Stack

- **Python 3**
- **Django** — web framework, ORM
- **Django REST Framework (DRF)** — API layer (serializers, views, routers)
- **django-filter** — field-based filtering
- **SQLite** — development database
- **Postman** — API testing tool

## Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd obs_project

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install django djangorestframework django-filter

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser (for admin panel access)
python manage.py createsuperuser
```

## Running the Project

```bash
python manage.py runserver
```

- API root: `http://127.0.0.1:8000/api/`
- Admin panel: `http://127.0.0.1:8000/admin/`

## Database Models

### Department
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | CharField | Department name |
| description | TextField | Department description |
| created_at | DateTimeField | Creation date (auto) |

### Student
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| first_name | CharField | First name |
| last_name | CharField | Last name |
| email | EmailField | Email address |
| student_number | CharField | Student number (unique) |
| enrollment_date | DateField | Enrollment date (auto) |
| department | ForeignKey → Department | The student's department |

### Teacher
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| first_name | CharField | First name |
| last_name | CharField | Last name |
| email | EmailField | Email address |
| specialization | CharField | Area of expertise |
| department | ForeignKey → Department | The teacher's department |

### Course
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | CharField | Course name |
| code | CharField | Course code (unique) |
| credit | IntegerField | Credit value |
| department | ForeignKey → Department | The course's department |
| teacher | ForeignKey → Teacher | Instructor teaching the course |

### Enrollment
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| student | ForeignKey → Student | The enrolled student |
| course | ForeignKey → Course | The course enrolled in |
| enrollment_date | DateField | Enrollment date (auto) |
| grade | FloatField | Grade (0-100, nullable) |

`unique_together = ('student', 'course')` — the same student cannot be enrolled in the same course more than once.

## Model Relationships

```
Department (1) ─── (N) Student
Department (1) ─── (N) Teacher
Department (1) ─── (N) Course
Teacher    (1) ─── (N) Course

Student (N) ─── (N) Course   [via the Enrollment through-model]
```

- A department can have multiple students, teachers, and courses; each student/teacher/course belongs to exactly one department.
- A teacher can teach multiple courses; each course has exactly one teacher.
- A student can enroll in multiple courses, and a course can have multiple enrolled students — this many-to-many relationship is implemented via the `Enrollment` through-model because it carries extra data (grade, enrollment date).

## Endpoint List

Standard CRUD endpoints for each resource (Department, Student, Teacher, Course, Enrollment):

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/departments/` | List all departments |
| POST | `/api/departments/` | Create a new department |
| GET | `/api/departments/{id}/` | Retrieve a single department |
| PUT | `/api/departments/{id}/` | Fully update a department |
| PATCH | `/api/departments/{id}/` | Partially update a department |
| DELETE | `/api/departments/{id}/` | Delete a department |
| GET | `/api/students/` | List all students |
| POST | `/api/students/` | Create a new student |
| GET | `/api/students/{id}/` | Retrieve a single student |
| PUT | `/api/students/{id}/` | Fully update a student |
| PATCH | `/api/students/{id}/` | Partially update a student |
| DELETE | `/api/students/{id}/` | Delete a student |
| GET | `/api/teachers/` | List all teachers |
| POST | `/api/teachers/` | Create a new teacher |
| GET | `/api/teachers/{id}/` | Retrieve a single teacher |
| PUT | `/api/teachers/{id}/` | Fully update a teacher |
| PATCH | `/api/teachers/{id}/` | Partially update a teacher |
| DELETE | `/api/teachers/{id}/` | Delete a teacher |
| GET | `/api/courses/` | List all courses |
| POST | `/api/courses/` | Create a new course |
| GET | `/api/courses/{id}/` | Retrieve a single course |
| PUT | `/api/courses/{id}/` | Fully update a course |
| PATCH | `/api/courses/{id}/` | Partially update a course |
| DELETE | `/api/courses/{id}/` | Delete a course |
| GET | `/api/enrollments/` | List all enrollments |
| POST | `/api/enrollments/` | Enroll a student in a course |
| GET | `/api/enrollments/{id}/` | Retrieve a single enrollment |
| PUT | `/api/enrollments/{id}/` | Fully update an enrollment |
| PATCH | `/api/enrollments/{id}/` | Partially update an enrollment |
| DELETE | `/api/enrollments/{id}/` | Delete an enrollment |

## Filtering, Search, Ordering, Pagination

| Feature | Example | Description |
|---|---|---|
| Filtering | `GET /api/students/?department=1` | Returns students belonging to a given department |
| Filtering | `GET /api/courses/?teacher=2` | Returns courses taught by a given teacher |
| Search | `GET /api/students/?search=Ahmet` | Searches within first name/last name/email |
| Ordering | `GET /api/students/?ordering=first_name` | Sorts ascending by name |
| Ordering | `GET /api/students/?ordering=-enrollment_date` | Sorts descending by enrollment date |
| Pagination | `GET /api/students/?page=2` | Returns page 2 (5 records per page) |

These parameters can be combined, e.g. `GET /api/courses/?department=1&ordering=name&search=Python`

## Example Requests and Responses

### Creating a new student

**Request:**
```
POST /api/students/
Content-Type: application/json

{
    "first_name": "Zeynep",
    "last_name": "Kaya",
    "email": "zeynep@example.com",
    "student_number": "20260099",
    "department": 1
}
```

**Response (201 Created):**
```json
{
    "id": 6,
    "first_name": "Zeynep",
    "last_name": "Kaya",
    "email": "zeynep@example.com",
    "student_number": "20260099",
    "enrollment_date": "2026-09-05",
    "department": 1
}
```

### Viewing student details (with related data)

**Request:**
```
GET /api/students/1/
```

**Response (200 OK):**
```json
{
    "id": 1,
    "first_name": "Ali",
    "last_name": "Çelik",
    "email": "ali.celik@ogrenci.edu.tr",
    "student_number": "20260001",
    "enrollment_date": "2026-09-05",
    "department": {
        "id": 1,
        "name": "Bilgisayar Mühendisliği",
        "description": "",
        "created_at": "2026-09-05T15:04:53.920169Z"
    },
    "enrollments": [
        {
            "id": 1,
            "course": {
                "id": 1,
                "name": "Python Programlama",
                "code": "CENG101",
                "credit": 4
            },
            "enrollment_date": "2026-09-05",
            "grade": 85.5
        }
    ]
}
```

### Validation error example

**Request:**
```
POST /api/students/
Content-Type: application/json

{
    "first_name": "",
    "student_number": "20260001",
    "department": 999
}
```

**Response (400 Bad Request):**
```json
{
    "first_name": ["This field may not be blank."],
    "email": ["This field is required."],
    "student_number": ["student with this student number already exists."],
    "department": ["Invalid pk \"999\" - object does not exist."]
}
```

### Not found example

**Request:**
```
GET /api/students/9999/
```

**Response (404 Not Found):**
```json
{
    "detail": "Not found."
}
```

## Validation Rules

- First/last name fields cannot be blank
- Email must be in a valid format
- Student number and course code must be unique
- A non-existent department/teacher/student/course cannot be referenced
- The same student cannot be enrolled in the same course twice
- Grade values cannot fall outside the 0-100 range

## HTTP Status Codes

| Code | Usage |
|---|---|
| 200 OK | Successful GET, PUT, PATCH |
| 201 Created | Successful POST |
| 204 No Content | Successful DELETE |
| 400 Bad Request | Invalid/missing data |
| 404 Not Found | Resource not found |

## API Testing

All endpoints were tested with Postman, covering both successful and error scenarios:
- Full CRUD flow (create → list → view → update → delete)
- Uniqueness violations (duplicate student number / course code)
- Invalid relationship references (non-existent department/teacher/student/course)
- Out-of-range grade values
- Duplicate enrollment attempts (same student–course pair)
- Access to non-existent records (404 scenario)
- Combinations of filtering, search, ordering, and pagination parameters

## Postman Collection

A ready-to-use Postman collection covering all of the API's endpoints is available at
`postman/Öğrenci Bilgi Sistemi API.postman_collection.json`.

### How to use it
1. Open Postman
2. Click **Import** in the top left
3. Select `postman/Öğrenci Bilgi Sistemi API.postman_collection.json`
4. The collection will load with all endpoints (Departments, Students, Teachers, Courses, Enrollments) organized into folders