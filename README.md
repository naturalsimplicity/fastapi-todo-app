# fastapi-services
FastAPI services for Mentors Seminar Course

Create own image from Dockerfile:

    docker build -t todo-app .

Create volume for the app data:

    docker volume create todo_data

Start container with the app:
    
    docker run --name todo-app-fastapi -d -p 8000:80 -v todo_data:/app/data todo-app