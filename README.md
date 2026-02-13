# CodeReview AI

AI-powered intelligent code review assistant.

## Setup

1. Clone repo
2. Create virtual env
3. Install dependencies

pip install -r requirements.txt

4. Copy .env.example to .env
5. Add your API keys

## Run

uvicorn app.main:app --reload

## Endpoints

POST /review
{
  "code": "print('hello')",
  "language": "python"
}

POST /review-pr
{
  "repo_url": "https://github.com/user/repo",
  "pr_number": 1
}

