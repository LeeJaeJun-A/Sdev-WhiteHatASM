# AI assisted white hat ASM

![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)
![Python](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![MongoDB](https://img.shields.io/badge/mongodb-%2347A248.svg?style=for-the-badge&logo=mongodb&logoColor=white)


## Requirements
- Python 3.9 or higher
- Node.js 16.x or higher
- pip (Python package manager)
- npm or yarn (JavaScript package managers)

## Installation and Setup
### 1. Clone this repository or download it, and place it where you want to.

### 2. Set Up the FastAPI Backend
1. Install Backend Dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Configure .env File:
``` backend/.env
# JWT (JSON Web Token) Configuration
# Change this to a secure key in production. This is just a test key.
JWT_SECRET_KEY="SERVER_BY_ENKI_LEEJAEJUN"  # Secret key used for generating and verifying JWTs. Replace with a strong key in production.
JWT_ALGORITHM="HS256"  # Algorithm used for encoding and decoding JWTs.
JWT_ACCESS_TOKEN_EXPIRE_SECONDS=3600  # Expiration time for access tokens (in seconds). Default is set to 1 hour.
JWT_REFRESH_TOKEN_EXPIRE_SECONDS=86400  # Expiration time for refresh tokens (in seconds). Default is set to 24 hours.

# Database Configuration
# The path to the SQLite3 database file. Change this to your production database path if different.
AUTH_MODULE_DB_PATH="sqlite:///./auth.db"  # Path to the SQLite3 database file. Replace with your actual database path in production.

# MongoDB Configuration
# URI settings for MongoDB in local and Docker environments.
MONGODB_LOCAL_URI="mongodb://localhost:27017"  # URI for connecting to MongoDB in a local environment.
MONGODB_DOCKER_URI="mongodb://mongo:27017"  # URI for connecting to MongoDB in a Docker environment.
MONGODB_DATABASE_NAME="shinnam"  # The name of the MongoDB database to be used.

# Default Root Account Configuration
# Default root account credentials. Change these to secure credentials in production.
DEFAULT_ROOT_ACCOUNT_ID="root"  # Default root account ID.
DEFAULT_ROOT_ACCOUNT_PASSWORD="root1234"  # Default root account password.

# Account Lockout Settings
# Settings for account lockout.
MAX_FAILURES=5  # Maximum number of allowed login failures before the account is locked.
LOCK_TIME_MINUTES=5  # Time (in minutes) for which the account is locked after reaching the maximum number of failures.

# Password Rehashing Configuration
# Settings for password rehashing.
REHASH_COUNT_STANDARD=10  # Number of successful requests after which the user's password should be rehashed. Adjust according to your security requirements.

```

3. Run the Backend Server:
```
uvicorn backend.main:app --reload
```

### 3. Set Up the SvelteKit Frontend
1. Install Frontend Dependencies:
```bash
cd frontend
npm install
```

2. Configure .env File:
``` frontend/.env
# FastAPI URL Configuration
# URL for the FastAPI application. Change this to the production URL.  # Replace with your production FastAPI URL
VITE_FASTAPI_URL="http://127.0.0.1:8000"
```

3. Run the Frontend Development Server:
```bash
npm run dev
```

## Running with Docker Compose
If you prefer to run the entire application using Docker Compose, follow these steps:
1. Ensure you have Docker and Docker Compose installed on your system.

2. In the root directory of the project (where docker-compose.yml is located), run the following command:
```bash
docker-compose up --build
```
This command will:
- Build the Docker images for both the backend and frontend services.
- Start the MongoDB service, backend FastAPI server, and frontend SvelteKit server.
- Mongo Express will also be available at http://localhost:8081 to manage your MongoDB data.

3. Access the application:
- Frontend: Visit http://localhost:4173 in your web browser to view the frontend application.
- Backend: The FastAPI backend will be running at http://localhost:8000.
- Mongo Express: You can access Mongo Express at http://localhost:8081 to interact with the MongoDB database.

To stop the application, press CTRL + C in the terminal where Docker Compose is running, or use:
```bash
docker-compose down
```
This command will stop and remove the containers, but your data will persist in the Docker volumes.