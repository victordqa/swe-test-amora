# FastAPI Poetry Project Setup Guide

This is a Software Engineer TEST project.

## Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```sh
git clone https://github.com/victordqa/swe-test-amora.git
cd swe-test-amora
```

### 2. Install Poetry

Poetry is used to manage dependencies. Install Poetry if you haven't already:

-follow the [Poetry installation instructions](https://python-poetry.org/docs/#installation).

### 3. Create/Enter Virtual Environment

```bash
poetry shell
```

### 4. Install Dependencies

Use Poetry to install the project dependencies:

```bash
poetry install
```

### 4. Set Up PostgreSQL

Ensure PostgreSQL is installed and running on your local machine. You can install PostgreSQL directly from the [official website](https://www.postgresql.org/download/) or use a package manager like `brew` on macOS or `apt` on Ubuntu.
Create a your database.

### 5. Set Up Environment Variables

Create a `.env` file in the root directory with your database credentials:

```env
# .env file
POSTGRES_PASSWORD=yourpass
POSTGRES_USER=user
POSTGRES_DB=amora_dev
SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://user:yourpass@localhost:5431/amora_dev
```

### 6. Run Database Migrations

Use Alembic to run the database migrations:

```bash
alembic upgrade head
```

### 7. Start the Application

Start the FastAPI application:

```bash
uvicorn main:app
```

### 8. Access the Application

Open your browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to access the API documentation.
