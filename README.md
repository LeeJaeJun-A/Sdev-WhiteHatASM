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
``` .env
# JWT (JSON Web Token) Configuration
JWT_SECRET_KEY="your_generated_secret_key_here"  # Replace with a strong secret key
JWT_ALGORITHM="HS256"  # Algorithm used for encoding and decoding JWTs
JWT_ACCESS_TOKEN_EXPIRE_SECONDS=3600  # Access token expiry time in seconds (1 hour)
JWT_REFRESH_TOKEN_EXPIRE_SECONDS=86400  # Refresh token expiry time in seconds (24 hours)

# Database Configuration
AUTH_MODULE_DB_PATH="sqlite:///./auth.db"  # Replace with your actual database URL or path

# Account Settings for the Service Web Application
DEFAULT_ROOT_ACCOUNT_ID="root"  # Replace with a secure root account ID
DEFAULT_ROOT_ACCOUNT_PASSWORD="root1234"  # Replace with a secure root account password

# Account Lockout Settings
MAX_FAILURES=5  # Adjust based on your security policy
LOCK_TIME_MINUTES=5  # Adjust based on your security policy

# FastAPI URL Configuration
VITE_FASTAPI_URL="http://127.0.0.1:8000"  # Replace with your production FastAPI URL

# Password Rehashing Configuration
REHASH_COUNT_STANDARD=10  # Adjust based on your security requirements
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
2. Run the Frontend Development Server:
```bash
npm run dev
```