# Task Management API

A Flask-based RESTful API for managing tasks with features like filtering, sorting, and CRUD operations.

## Features

- Create, Read, Update, and Delete tasks
- Filter tasks by category, priority, and deadline range
- Sort tasks by various fields (created_at, priority, etc.)
- SQLite database for data persistence
- Marshmallow schema validation
- RESTful API design

## Tech Stack

- Python 3.11
- Flask 3.1.1
- SQLAlchemy 2.0.41
- SQLite

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd software_engineer_test_fy25
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python run.py or flask run
```

The server will start at `http://127.0.0.1:5000`

## API Endpoints

### Create a Task
- **POST** `/tasks`
```json
{
    "title": "Complete Project",
    "description": "Finish the task management API",
    "category": "Work",
    "priority": "High",
    "deadline": "2024-03-20T15:00:00"
}
```

### Get All Tasks
- **GET** `/tasks`
  - Optional query parameters:
    - `category`: Filter by category
    - `priority`: Filter by priority
    - `deadline_from`: Filter by deadline start date
    - `deadline_to`: Filter by deadline end date
    - `sort_by`: Field to sort by (default: created_at)
    - `order`: Sort order (asc/desc, default: desc)

Example queries:
- Filter by category and priority: `/tasks?category=Work&priority=High`
- Filter by deadline range: `/tasks?deadline_from=2023-01-01&deadline_to=2023-12-31`
- Sort by priority ascending: `/tasks?sort_by=priority&order=asc`

### Get Task by ID
- **GET** `/tasks/<id>`

### Update Task
- **PUT** `/tasks/<id>`
```json
{
    "title": "Updated Title",
    "priority": "Medium"
}
```

### Delete Task
- **DELETE** `/tasks/<id>`

## Data Model

### Task
- `id`: Integer (Primary Key)
- `title`: String (100 chars, required)
- `description`: Text (optional)
- `category`: String (50 chars, required)
- `priority`: String (10 chars, required)
- `deadline`: DateTime (required)
- `created_at`: DateTime (auto-set)
- `updated_at`: DateTime (auto-updated)

## Testing

Run the test suite using pytest:
```bash
python -m pytest
```

## Error Handling

The API includes proper error handling for:
- Invalid input data
- Missing resources
- Validation errors
- Bad requests

## Development

The application uses SQLite for development. The database file is located at `instance/tasks.db` and is automatically created when the application starts. 


Collection Name: FY25_API_DOCS [Postman Documentation link]([https://web.postman.co/workspace/My-Workspace~837b6c03-d97c-453c-8048-98fc17a06315/collection/36790923-3c1ba8ad-2874-45af-9779-b208994895c1?action=share&source=copy-link&creator=36790923](https://www.postman.com/descent-module-operator-17907072/workspace/software-engineer-fy25/collection/36790923-3c1ba8ad-2874-45af-9779-b208994895c1?))
