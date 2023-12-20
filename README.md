# Shopping Cart API
This is a shopping cart API that reserves items once they are put into a cart.
The design details are covered [here](docs/design.md).

# Prerequisites
* Git
* Python 3.9+

# Setup

## Clone repository
```bash
git clone https://github.com/WillNguyen64/shopping-cart.git
cd shopping-cart
```

## Install pipenv
```bash
# Install pipenv
$ pip install pipenv --user

# Add pipenv to your PATH
# The steps below assume you're using Bash. If you're using a different shell, replace
# .profile with the appropriate file for your shell.
$ cp ~/.profile ~/.profile.BAK
$ echo "export PATH=\$PATH:$(python -m site --user-base)/bin" >> ~/.profile
$ source ~/.profile
```

## Install project dependencies
```bash
# Install dependencies to a local virtual environment
$ pipenv install
```

# Run API service
```bash
$ pipenv run uvicorn shopping_cart.main:app --host 0.0.0.0 --port 8282 --reload
```

When the service is started, you can access the Swagger UI at http://127.0.0.1:8282/docs to run some ad-hoc tests.

# Run Tests for API service
```bash
$ pipenv run pytest ./tests
```
