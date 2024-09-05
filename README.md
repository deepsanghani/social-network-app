# Social Network App

This is a social network application built with Django. The application uses PostgreSQL as the database.

## Installation

### Setting Up the Project

1. **Clone the repository**:

    ```bash
    git clone https://github.com/deepsanghani/social-network-app.git
    cd social-network-app
    ```

2. **Create a `.env` file**:

    Create a `.env` file in the root directory of the project and add the following environment variables:

    ```env
    DB_NAME=social_network
    DB_USERNAME=postgres
    DB_PASS=root
    DB_HOST=localhost
    DB_PORT=5432
    ENV=Development
    ```

3. **Install Python dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    Run the following command to apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. **Run the development server**:

    Start the Django development server with:

    ```bash
    python manage.py runserver 5000
    ```

6. **Access the API**:

    The API will be available at `http://localhost:5000`.

