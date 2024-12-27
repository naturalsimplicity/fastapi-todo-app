# FastAPI ToDo app

FastAPI ToDo App for Mentors Seminar Course

## Features

Service work on a paradigm that everyone can see all the tasks
but only authenticated users can create and edit tasks.

To read tasks you can use:
1. `GET /api/v1/items` — returns list of all tasks
2. `GET /api/v1/items/{item_id}` — returns specific item
3. `GET /api/v1/users/{login}/items` — returns all items of specific user

If you want to create or edit a task:
1. `POST /api/v1/users/register` — register with your name and login and get authentication token (you need to pass Authorization header with your request hereinafter)
2. `POST /api/v1/items` — create new item 
3. `PUT /api/v1/items/{item_id}` — edit existing task (you can edit only yours)
4. `DELETE /api/v1/` — delete existing task (you can edit only yours)

## Application startup

Create an image from Dockerfile:

    docker build -t todo-app .

Create volume for the app data:

    docker volume create todo_data

Start container with the app:
    
    docker run --name todo-app-fastapi -d -p 8000:80 -v todo_data:/app/data todo-app
