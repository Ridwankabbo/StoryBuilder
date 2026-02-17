# StoryBuilder

An Collaborative sotry builder Backend application using REST API for multi-user storytelling geme where user add sentence to a shared story in real-time. 

## Features

- JWT authentication
- RESTful API
- Version controll for conflict Prevention
- Multi-User Real-Time Collaboration 

## Tech Stack

- Django
- Django Channels
- Sqlite3
- JWT (Json Web Token)
- WebSocket

## Application urlls structure and path
- ### user
    - registration url : https://127.0.0.1:8000/user/register/

    - otp verification url : https://127.0.0.1:8000/user/verify-otp/
    
    - forgot password url : https://127.0.0.1:8000/user/forgot-password/
    
    - reset password url : https://127.0.0.1:8000/user/reset-password/
    
    -login url : https://127.0.0.1:8000/user/login/api/token
    
    - registration url : https://127.0.0.1:8000/user/api/token/refresh/

- ### Story
    - story list url : https://127.0.0.1:8000/story/story-list/  
    
    - story details url : https://127.0.0.1:8000/story/story-details/
    
    - sentence url : https://127.0.0.1:8000/story/
    sentence/   