# Bitlog

A blogging platform made in django. _(This is a hobby project, **not** production-ready.)_

A full-featured blogging platform built with `Django`. This project is a _hobby project_ showcasing a variety of common social blogging features, designed to demonstrate full-stack web development skills in Python and Django.

## Features

-   **Posts:** Create, Read, Update, Delete (CRUD)
-   **User Authentication:** Sign up, login, logout
-   **Profiles:** Edit profile, add banner images
-   **Social Interactions:** Follow/unfollow users, like/unlike posts, comment, save posts
-   **Browsing & Discovery:** Search, sort, filter by category or tag, pagination
-   **Extras:** Reading history, clean user-friendly UI

## Technologies Used

-   **Backend:** Django
-   **Frontend:** HTML, CSS, Javascript
-   **Database:** SQLite (for development)
-   **Environment Management:** UV

## Setup Instructions

#### 1. Clone the repository

```sh
git clone https://github.com/Anas-Shakeel/bitlog.git
cd bitlog/
```

#### 2. Create a virtual environment

```sh
python -m venv .venv
# Activate it:
# On macOS/Linux: source .venv/bin/activate
# On Windows: .venv\Scripts\activate
```

#### 3. Install dependencies

```sh
pip install -r requirements.txt
```

#### 4. Configure environment variables

Create a `.env` file in the root directory and add this in the file:

```sh
SECRET_KEY=any_random_secret_key
DEBUG=True
```

#### 5. Apply migrations

```sh
python manage.py migrate
```

#### 7. Run the development server

```sh
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to explore the app.

## License

This project is open-source and available under the `MIT` License.

## Assets and Credits

-   All icons used in this project belong to [icons8.com](https://icons8.com/)
-   Hero image used in `home.html` template was taken from [freepik.com](https://www.freepik.com/free-vector/hand-drawn-essay-illustration_40478844.htm)
