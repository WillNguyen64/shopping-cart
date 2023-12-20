# Design Details

This document lists the design decisions that were made during the course of this project.

# Areas of Improvement

This section describes items that could be improved on:

* Feature Limitations
  * The shopping cart API does not support multiple users
    * For this project, I assumed there was only one user who had one cart.
    * In reality, we should extend the API to allow adding multiple users, each having their own cart.
  * The shopping cart API does not consolidate multiple instances of the same item in the cart.
    * If the same item is added multiple times to a cart, each instance is treated separate from the others, with each one mapped to a different reservation.
    * When a client gets the items in a cart, they may see multiple items with the same name. 
    * Would it be easier for a client if we multiple items were consolidated into the one?

* Fault Tolerance
  * If a call to the reservation API fails, we should time out and retry up to a certain number of times.
    * For this project, if the API call fails, we log the error.
  * If the shopping cart API crashes, there's no way to recover in-flight reservation attempts.
    * To do this, we need a way to correlate an item ID that was added to a cart with a reservation ID.
    * For this project, I modified the reservation API to take an item ID for correlation purposes.
    * To recover from a crash, we use the item ID (as a correlation ID) to look up the matching reservation IDs from the reservation API service. This would require a API to do this lookup.

* Deployment
  * Add Dockerfile to build a container image for deployment

* Database Setup
  * Use a DB migration tool
    * To simplify things, the DB tables are created on-the-fly in an in-memory SQLite DB during service startup.
    * For production, we should use a DB migration tool (e.g., Alembic) to properly manange and version schema changes to the DB server (e.g., PostgreSQL)

* Code Quality
  * Automate static analysis (e.g., mypy)
    * We need to add missing static types for classes and methods/functions.
  * Automate code coverage tool (e.g., Coverage.py)
  * Automate code formatting (e.g., black)

* Testing
  * The test case that validates what happens when an item reservation takes a very long time doesn't work as expected.
    * Currently, the POST request to /items blocks waiting for the reservation to complete when it should just return right away.
    * This may be due to a bug/limitation in the Starlette TestClient. This needs more investigation.
  * When doing ad-hoc tests thru the Swagger UI, the POST requests to /items will fail because there is no Reservation API to test against.
    * We can use a mock API server (e.g., Prism) to mock the responses from the Reservation API.

# Rationale behind Framework Choices

* Package management
  * pipenv was used to manage virtual environment to install package dependencies
  * It was chosen for its simplicity and ease-of-use. Since it's similar to Poetry, we could have gone either way. If this turns out to be larger project with many dependencies, then maybe Poetry would be better for performance reasons.

* API framework
  * FastAPI was used to implement the Shopping cart API service.
  * It was chosen over something like Flask because it provides a full integrated set of out-of-box tools (e.g., Pydantic, etc.) for quickly building an API, instead of integrating different projects yourself.  Also, the documentation is excellent.

* ORM framework
  * SQLAlchemy was used to read/write to the DB.
  * It was chosen to help us to quickly write DB-related code instead of writing raw SQL.

* Background tasks
  * The FastAPI Background tasks feature was used to run the long-running reservations task.
  * Since these tasks are I/O bound, we can take advantage of Python asyncio library to run a large number of tasks that FastAPI can switch between without blocking the main thread.
  * If the tasks were CPU bound, we would have to run the tasks in separate processes or else they would block the main thread, which requires a different framework like Celery.

* Configuration Settings
  * pydantic-settings was used to manage the configuration files for different deployoment environments
  * This tool was chosen for its simplicity, flexibility, and ease-of-use.
