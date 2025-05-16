# 🐾 Spy Cat Agency – Backend

This is the backend component of the **Spy Cat Agency** test assessment. It provides a REST API built with **FastAPI** and connected to a SQL database via SQLAlchemy. It enables the agency to manage spy cats, missions, and their associated targets.

---

## 🚀 Features

* ✅ CRUD operations for **Spy Cats**
* ✅ Create **Missions** along with embedded **Targets**
* ✅ Assign cats to missions
* ✅ Update target notes, mark as completed
* ✅ Business rules validation (e.g., frozen notes, mission completion)
* ✅ Breed validation via [TheCatAPI](https://api.thecatapi.com/v1/breeds)

---

## 🧱 Tech Stack

* Python 3.12
* FastAPI
* SQLAlchemy
* SQLite (default)
* Pydantic
* Uvicorn

---

## 🛠️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Compi-Craft/spy_cat.git
cd spy-cat-agency-backend
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the application

```bash
uvicorn main:app --reload
```

---

## 📫 Postman Collection

Postman collection with all available endpoints:

[Postman Collection](./docs/postman.json).

---

# 🐾 Spy Cat Agency - Frontend

This is the frontend application for the Spy Cat Agency (SCA) management system. It provides a simple dashboard to manage spy cats with CRUD operations.

## 🚀 Features

* List all spy cats retrieved from the backend API
* Add a new spy cat (Name, Years of Experience, Breed, Salary)
* Edit a spy cat’s salary
* Delete a spy cat
* Graceful handling of API errors

## 🧱 Tech Stack

* Next.js (React framework)
* Tailwind CSS (for styling, optional — you can replace it with any UI library)
* Axios (for HTTP requests)

## 🛠️ Getting Started

### Prerequisites

* Node.js (>=16.x recommended)
* npm or yarn

### Installation

1. Install dependencies

```bash
npm install
# or
yarn install
```

### Running the development server

```bash
npm run dev
# or
yarn dev
```

Open your browser and go to [http://localhost:3000/cats](http://localhost:3000/cats) to see the app.

### Building for production

```bash
npm run build
npm start
```

## API

The frontend interacts with the backend API under the path `/api/spy_cats` for spy cat management.

Example endpoints:

* GET `/` - List all spy cats
* POST `/` - Create a spy cat
* PUT `/{id}` - Update salary
* DELETE `/{id}` - Delete a spy cat

## Notes

* Breed validation is performed on the backend using TheCatAPI.
* Error messages from the backend are shown on the UI.
* Styling is minimal but functional.
