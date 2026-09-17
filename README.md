# Coderr Backend

Coderr is a Django REST Framework backend for a service marketplace. Users can register as customers or business users. Business users can publish and manage offers, while customers can place orders and write reviews. The API also provides profile management, authentication, filtering, search, order management, and dashboard statistics.

## Table of Contents

- [Features](#features)
- [Technology](#technology)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Pagination](#pagination)
- [Response Status Codes](#response-status-codes)
- [Testing and Checks](#testing-and-checks)
- [Development Notes](#development-notes)
- [Contributing](#contributing)
- [License](#license)

## Features

- Token-based registration and login
- Customer and business user profiles
- Offer creation, filtering, searching, updating, and deletion
- Order creation and status management
- Business reviews with rating validation and ownership permissions
- Dashboard statistics for reviews, ratings, business profiles, and offers
- Paginated offer listing for the offers endpoint

## Technology

- Python
- Django
- Django REST Framework
- SQLite for local development
- Token authentication

## Prerequisites

Before setting up the project, make sure the following requirements are available:

- Python 3.12 or newer
- `pip`
- Python virtual environment support

## Quickstart

### 1. Create and activate a virtual environment

#### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows CMD

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

#### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a local `.env` file from `.env.template`.

#### Windows CMD

```bat
copy .env.template .env
```

#### macOS and Linux

```bash
cp .env.template .env
```

The resulting `.env` file should contain:

```env
SECRET_KEY=replace-this-with-a-local-secret
```

A Django secret key can be generated with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Replace the placeholder value in `.env` with the generated key.

Never commit the `.env` file or share its secret key.

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

The API is then available at:

```text
http://127.0.0.1:8000/api/
```

### 6. Optional: Create an administrator

```bash
python manage.py createsuperuser
```

The Django admin panel is available at:

```text
http://127.0.0.1:8000/admin/
```

## Usage

Register a customer or business account using:

```text
POST /api/registration/
```

Log in using:

```text
POST /api/login/
```

The login response provides an authentication token. Use this token for protected API requests.

Business users can create and manage offers. Customers can create orders from offer details and submit reviews for business users.

Offer listings support filtering, ordering, searching, and pagination.

## Project Structure

```text
core/                   Django project configuration and root URL routing
users_app/              Registration, login, profiles, and user permissions
offers_app/             Offers, offer details, serializers, filters, and permissions
orders_app/             Orders, order counts, serializers, filters, and permissions
reviews_app/            Reviews, validation, filters, serializers, and permissions
dashboard_app/          Dashboard summary endpoint
manage.py               Django administration entry point
requirements.txt        Python dependencies
.env.template           Environment variable template
```

Each feature app keeps its API implementation in an `api/` package containing serializers, views, URLs, permissions, and filters where required.

## Authentication

Coderr uses token authentication.

Registration and login are public. Protected endpoints require the token to be sent in the `Authorization` header:

```http
Authorization: Token <your-token>
```

Permissions depend on the endpoint and the user's profile type. Some operations are restricted to customers, business users, resource owners, or administrators.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/registration/` | Register a customer or business user |
| POST | `/api/login/` | Log in and receive an authentication token |
| GET, PATCH | `/api/profile/<user_id>/` | Read or update a user profile |
| GET | `/api/profiles/business/` | List business profiles |
| GET | `/api/profiles/customer/` | List customer profiles |
| GET, POST | `/api/offers/` | List or create offers |
| GET, PATCH, DELETE | `/api/offers/<offer_id>/` | Read, update, or delete an offer |
| GET | `/api/offerdetails/<detail_id>/` | Read one offer detail |
| GET, POST | `/api/orders/` | List or create orders |
| GET, PATCH, DELETE | `/api/orders/<order_id>/` | Read, update, or delete an order |
| GET | `/api/order-count/<business_user_id>/` | Count in-progress orders |
| GET | `/api/completed-order-count/<business_user_id>/` | Count completed orders |
| GET, POST | `/api/reviews/` | List or create reviews |
| GET, PATCH, DELETE | `/api/reviews/<review_id>/` | Read, update, or delete a review |
| GET | `/api/base-info/` | Read dashboard summary statistics |

### Offer Query Parameters

`GET /api/offers/` supports:

- `creator_id`
- `min_price`
- `max_delivery_time`
- `ordering`
- `search`
- `page`
- `page_size`

Invalid values for `max_delivery_time` return `400 Bad Request`.

### Review Query Parameters

`GET /api/reviews/` supports:

- `business_user_id`
- `reviewer_id`
- `ordering`

Reviews can be ordered by `updated_at` and `rating`.

## Pagination

Pagination is enabled only for:

```text
GET /api/offers/
```

The endpoint returns up to 10 offers per page by default and supports:

```text
?page=<page_number>
?page_size=<number>
```

The maximum page size is 100.

Order, review, and profile list endpoints return regular JSON lists and are not globally paginated.

## Response Status Codes

| Status | Meaning |
| --- | --- |
| `200 OK` | The request was successful |
| `201 Created` | A resource was created successfully |
| `204 No Content` | A resource was deleted successfully |
| `400 Bad Request` | Submitted data or query parameters failed validation |
| `401 Unauthorized` | Authentication is required or the token is invalid |
| `403 Forbidden` | The authenticated user does not have permission |
| `404 Not Found` | The requested resource does not exist |

## Testing and Checks

Run Django's system checks:

```bash
python manage.py check
```

Run the complete test suite:

```bash
python manage.py test
```

The tests cover:

- Registration and login
- User profiles
- Offers and offer details
- Orders
- Reviews
- Dashboard statistics
- Authentication and permissions
- Validation and error responses

### Test Coverage

Install Coverage.py if it is not already installed:

```bash
pip install coverage
```

Run the tests with coverage:

```bash
coverage run manage.py test
```

Display the coverage report:

```bash
coverage report
```

Coverage output generated locally should not be committed to version control.

## Development Notes

- SQLite is used for local development.
- The local database is intentionally excluded from version control.
- Secrets are stored in `.env` and must not be committed.
- API routes are grouped by app and included centrally through `core/urls.py`.
- API implementations are separated into feature-specific Django apps.
- Serializers expose explicit fields.
- Permissions are defined at the API view level.
- Offer listings use pagination, while order, review, and profile lists return regular JSON lists.
- Orders store a snapshot of the selected offer detail when they are created.

## Contributing

Contributions should follow the existing project structure and coding conventions.

Before submitting changes:

1. Create a separate branch for the change.
2. Keep changes focused on a single feature or fix.
3. Run the Django system checks.
4. Run the complete test suite.
5. Verify that existing API behavior is not broken.
6. Do not commit local databases, environment files, secrets, or coverage output.

## License

No separate license has been specified for this project.