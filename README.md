# Interview Helper Server

This project provides a Flask server for managing interview questions and interacting with OpenAI's GPT-4o.

## Setup

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Set environment variables:
    ```sh
    export OPENAI_API_KEY='your-openai-api-key'
    export SECRET_KEY='your-secret-key'
    ```

3. Run the server:
    ```sh
    python server.py
    ```

## Endpoints

- `POST /add-question`
- `GET /questions/type/<type_name>`
- `GET /questions/company/<company_name>`
- `GET /questions/difficulty/<int:difficulty_score>`
- `POST /reset-db`
- `POST /query`
- `GET /stream-questions`
- `GET /search-questions`
