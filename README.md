# Book Review System

## Code Setup
Run the command
```bash
git clone "https://github.com/devbk007/book_review_system.git"
```

## Virtual Environment Setup
Run the following commands after navigating to the project directory to create a conda virtual environment
```bash
conda create --prefix ./env python=3.10.13
conda activate ./env
```

## Installing packages
```bash
pip install -r requirements.txt
```

## How to interact with application?
Run the following command to start the server
```bash
uvicorn main:app --reload
```
then, navigate to http://127.0.0.1:8000/docs to get Swagger UI
