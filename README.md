<div align="center">

# 🤖 CodeReview AI

### AI-Powered Intelligent Code Review Assistant

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[Features](#-key-features) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

CodeReview AI is a production-ready, AI-powered code review assistant that provides comprehensive analysis of your code including quality assessment, security vulnerability detection, performance optimization suggestions, and best practices validation.

### Why CodeReview AI?

- 🚀 **Fast & Efficient**: Async architecture for high-performance analysis
- 🔒 **Security First**: Detect vulnerabilities before they reach production
- 🎨 **Multi-Language**: Support for 8+ programming languages
- 🤖 **AI-Powered**: GPT-4 integration for intelligent, context-aware suggestions
- 📊 **Comprehensive Metrics**: Detailed code quality and complexity analysis
- 🔗 **GitHub Integration**: Automated pull request reviews
- 🎯 **Actionable Insights**: Clear, practical suggestions for improvement

## 🌟 Key Features

### Code Analysis
- **Static Analysis**: AST-based code inspection
- **Security Scanning**: Detect SQL injection, XSS, and other vulnerabilities  
- **Code Quality**: Cyclomatic complexity, maintainability index
- **Style Checking**: PEP8, ESLint, and language-specific style guides
- **Best Practices**: Design patterns and anti-pattern detection

### Supported Languages
```
Python  •  JavaScript  •  TypeScript  •  Java  •  Go  •  Rust  •  C++  •  C#
```

### Integration
- REST API for easy integration
- GitHub PR automation
- CI/CD pipeline support
- Webhook notifications

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/SURENDER294/CodeReview-AI---Intelligent-Code-Review-Assistant.git
cd CodeReview-AI---Intelligent-Code-Review-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys

# Run the application
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 🚀 Usage

### Basic Code Review

```python
import requests

code = """
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price']
    return total
"""

response = requests.post(
    "http://localhost:8000/review",
    json={
        "code": code,
        "language": "python",
        "context": "E-commerce checkout function"
    }
)

print(response.json())
```

### Pull Request Review

```python
response = requests.post(
    "http://localhost:8000/review-pr",
    json={
        "repo_url": "https://github.com/username/repo",
        "pr_number": 42,
        "include_tests": True
    }
)

print(response.json())
```

## 📚 API Documentation

### Endpoints

#### `GET /`
API information and health status

#### `GET /health`
Health check endpoint for monitoring

#### `POST /review`
Analyze a code snippet

**Request Body:**
```json
{
  "code": "string",
  "language": "python",
  "context": "optional string",
  "severity_threshold": "medium"
}
```

**Response:**
```json
{
  "status": "success",
  "summary": "Found 3 issues. Consider addressing them for better code quality.",
  "issues": [
    {
      "title": "High Cyclomatic Complexity",
      "description": "Function 'process_data' has complexity of 15",
      "severity": "medium",
      "category": "quality",
      "line_number": 42,
      "suggestion": "Consider breaking down into smaller functions"
    }
  ],
  "metrics": {
    "total_lines": 150,
    "code_lines": 120,
    "blank_lines": 30
  },
  "review_id": "uuid-string"
}
```

#### `POST /review-pr`
Review an entire GitHub pull request

For complete API documentation, visit: `http://localhost:8000/docs` (Swagger UI)

## 🏗️ Architecture

```
CodeReview-AI/
├── app/
│   ├── __init__.py              # Application initialization
│   ├── main.py                  # FastAPI application & routes
│   ├── config.py                # Configuration management
│   ├── services/
│   │   ├── __init__.py
│   │   ├── code_analyzer.py     # Core analysis engine (350+ lines)
│   │   ├── pr_reviewer.py       # GitHub PR integration
│   │   └── ai_provider.py       # AI model integration
│   ├── models/                  # Pydantic data models
│   └── utils/                   # Utility functions
├── tests/                       # Test suite
├── examples/                    # Usage examples
├── docs/                        # Additional documentation  
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Configuration

Create a `.env` file in the project root:

```env
# API Configuration
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# GitHub Integration
GITHUB_TOKEN=your_github_token_here

# Application Settings
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run linting
flake8 app/
black app/ --check
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- OpenAI for GPT-4 API
- The open-source community for inspiration

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/SURENDER294/CodeReview-AI---Intelligent-Code-Review-Assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SURENDER294/CodeReview-AI---Intelligent-Code-Review-Assistant/discussions)

## 🗺️ Roadmap

- [ ] Real-time code review during typing
- [ ] IDE plugins (VS Code, JetBrains)
- [ ] Custom rule definitions
- [ ] Machine learning model training
- [ ] Code quality trends dashboard
- [ ] Multi-repository analysis
- [ ] Team collaboration features

---

<div align="center">

**[⬆ back to top](#-codereview-ai)**

Made with ❤️ by [SURENDER294](https://github.com/SURENDER294)

⭐ Star this repository if you find it helpful!

</div>
