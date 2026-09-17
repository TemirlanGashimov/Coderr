# Coderr Backend

Coderr is a Django REST Framework backend for a service marketplace. Users can register as customers or business users, business users can publish offers, customers can place orders and write reviews, and authenticated clients can retrieve dashboard statistics.

## Features

- Token-based registration and login
- Customer and business user profiles
- Offer creation, filtering, searching, updating, and deletion
- Order creation and status management
- Business reviews with rating validation and ownership permissions
- Dashboard statistics for reviews, ratings, business profiles, and offers
- Paginated offer listing for the offers endpoint only

## Technology

- Python
- Django
- Django REST Framework
- SQLite for local development
- Token authentication

## Project Structure

```text
core/                 Django project configuration and root URL routing
users_app/            Registration, login, profiles, and user permissions
offers_app/            Offers, offer details, serializers, and permissions
orders_app/            Orders, order counts, serializers, and permissions
reviews_app/           Reviews, validation, serializers, and permissions
dashboard_app/        Dashboard summary endpoint
manage.py              Django administration entry point
requirements.txt      Python dependencies
.env.template         Environment variable template
```

Each feature app keeps its API implementation in an `api/` package containing serializers, views, URLs, and permissions where required.

## Requirements

- Python 3.12 or newer
- A virtual environment

Install the dependencies:

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Windows CMD:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

macOS and Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a local `.env` file from `.env.template`. The copy command creates the
file; then replace the placeholder with your own secret key.

Windows CMD:

```bat
copy .env.template .env
```

macOS and Linux:

```bash
cp .env.template .env
```

The resulting `.env` file should contain:

```env
SECRET_KEY=replace-this-with-a-local-secret
```

Generate a secure Django secret key and replace the placeholder after the
equals sign. The command is the same on Windows, macOS, and Linux:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Never commit the `.env` file or share its secret key.

Apply migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

Create an administrator for the Django admin panel:

```bash
python manage.py createsuperuser
```

The admin panel is available at `http://127.0.0.1:8000/admin/` and requires
the credentials of a staff user with admin permissions.

The API is available at `http://127.0.0.1:8000/api/`.

## Pagination

Pagination is enabled only for `GET /api/offers/`. The endpoint returns up to 10 offers per page by default and supports the `page` and `page_size` query parameters. The maximum page size is 100.

Order, review, and profile list endpoints return regular JSON lists and are not globally paginated.

## Authentication

Registration and login are public. Both endpoints return a token. Send that token with protected requests:

```http
Authorization: Token <your-token>
```

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

Offer listings support `creator_id`, `min_price`, and `max_delivery_time` filters as well as ordering and search parameters supported by Django REST Framework. Review listings support `business_user_id`, `reviewer_id`, and ordering.

## Response Status Codes

- `200 OK`: The request was successful.
- `201 Created`: A resource was created successfully.
- `204 No Content`: A resource was deleted successfully.
- `400 Bad Request`: The submitted data failed validation.
- `401 Unauthorized`: Authentication is required or the token is invalid.
- `403 Forbidden`: The authenticated user does not have permission.
- `404 Not Found`: The requested resource does not exist.

## Testing and Checks

Run Django's system checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test
```

The tests cover registration, login, profiles, offers, orders, reviews, and dashboard behavior.

To measure test coverage, install the coverage tool and run:

```bash
pip install coverage
coverage run manage.py test
coverage report
```

The project excludes local coverage output from version control.

## Development Notes

- The local SQLite database is intentionally excluded from version control.
- Keep secrets in `.env`; do not commit the file.
- API routes are grouped by app and included centrally by `core/urls.py`.
- Serializers expose explicit fields and permissions are declared at the API view level.
