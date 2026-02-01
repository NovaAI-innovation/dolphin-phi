---
title: Dolphin Phi
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
short_description: FastAPI wrapper for Qwen2.5-Coder model with automated deployment
---

# Dolphin Phi - AI Coding Assistant API

Dolphin Phi is a FastAPI wrapper for the Qwen2.5-Coder model that provides a REST API interface for AI-powered coding assistance.

## Features

- FastAPI-based REST API
- Authentication via Bearer tokens
- Pre-configured Docker deployment
- Automated testing and deployment with GitHub Actions
- Support for multiple deployment targets (Render, Docker Hub, GitHub Container Registry)

## Local Development

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/dolphin-phi.git
cd dolphin-phi
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export API_TOKEN="your-secret-token-here"
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:10000`.

## API Usage

### Authentication

All API calls require a Bearer token in the Authorization header:

```
Authorization: Bearer YOUR_API_TOKEN
```

### Endpoints

#### GET /

Health check endpoint.

```bash
curl -X GET http://localhost:10000/
```

#### POST /chat

Send a chat prompt to the model.

```bash
curl -X POST http://localhost:10000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"prompt": "Write a Python function to calculate factorial"}'
```

## Deployment

### Automated Deployment with GitHub Actions

The repository includes a GitHub Actions workflow that automatically:

1. Runs tests on pull requests and pushes to main
2. Builds and pushes Docker images to GitHub Container Registry
3. Deploys to Render (if configured)
4. Pushes Docker images to Docker Hub (if configured)

### Environment Variables

For deployment, you'll need to set the following secrets in your GitHub repository:

- `API_TOKEN`: The authentication token for the API
- `RENDER_DEPLOY_HOOK_URL`: Webhook URL for Render deployment (optional)
- `DOCKERHUB_USERNAME`: Docker Hub username (optional)
- `DOCKERHUB_TOKEN`: Docker Hub access token (optional)

### Manual Docker Deployment

Build and run the Docker container locally:

```bash
docker build -t dolphin-phi .
docker run -p 10000:10000 -e API_TOKEN="your-secret-token" dolphin-phi
```

## Testing

Run the test suite:

```bash
pip install -r requirements-test.txt
python -m pytest test_app.py -v
```

## Architecture

- **app.py**: Main FastAPI application with model integration
- **Dockerfile**: Multi-stage Dockerfile for optimized builds
- **requirements.txt**: Production dependencies
- **requirements-test.txt**: Dependencies for testing
- **test_app.py**: Unit tests with mocking for external dependencies
- **.github/workflows/test-and-deploy.yml**: GitHub Actions workflow for CI/CD

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
