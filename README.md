# WebForge.ai - AI-Powered Web App Generator

> Describe your app, get a complete GitHub repository in minutes

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

## 🚀 Features

- **AI-Powered Generation**: Leverages Google Gemini Flash 2.5 for intelligent code generation
- **Multi-Framework Support**: React, Vue, Angular, Next.js, Django, Node.js, and more
- **Real-Time Progress**: WebSocket-based live updates during generation
- **GitHub Integration**: Automatic repository creation and code commits
- **Live Preview**: Interactive preview of generated applications
- **Code Quality**: Automated validation, testing, and security scanning
- **Subscription Tiers**: Free, Pro, and Enterprise plans with Paddle integration

## 📋 Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.11+
- **PostgreSQL** 15+
- **Redis** 7+
- **Docker** (optional, for containerized deployment)
- **GitHub Account** (for OAuth and repository creation)
- **Google Gemini API Key**
- **Paddle Account** (for payment processing)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/webforge-ai.git
cd webforge-ai
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Edit .env with your credentials:
# - SECRET_KEY
# - DATABASE_URL
# - GEMINI_API_KEY
# - GITHUB_CLIENT_ID
# - GITHUB_CLIENT_SECRET
# - PADDLE_API_KEY
# - REDIS_HOST

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Edit .env with:
# VITE_API_URL=http://localhost:8000/api
# VITE_WS_URL=ws://localhost:8000

# Start development server
npm run dev
```

### 4. Start Redis (Required for WebSocket and Celery)

```bash
# Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or install locally
# macOS: brew install redis && redis-server
# Ubuntu: sudo apt install redis-server && redis-server
```

### 5. Start Celery Worker (For Background Tasks)

```bash
cd backend
celery -A webforge worker -l info
```

### 6. Initialize Pattern Database

```bash
cd backend
python manage.py shell

>>> from pipeline.pipeline import PatternPipeline
>>> pipeline = PatternPipeline()
>>> pipeline.initialize_database()
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=webforge.settings.development

# Database
DB_NAME=webforge
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_HOST=localhost

# AI
GEMINI_API_KEY=your-gemini-api-key

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_CALLBACK_URL=http://localhost:8000/auth/github/callback/

# Paddle Payments
PADDLE_VENDOR_ID=your-paddle-vendor-id
PADDLE_API_KEY=your-paddle-api-key
PADDLE_PUBLIC_KEY=your-paddle-public-key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

#### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000
```

## 📂 Project Structure

```
webforge-ai/
├── frontend/                 # Vue.js frontend
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── views/           # Page views
│   │   ├── stores/          # Pinia stores
│   │   ├── services/        # API & WebSocket services
│   │   └── router/          # Vue Router config
│   └── public/              # Static assets
│
├── backend/                  # Django backend
│   ├── apps/
│   │   ├── authentication/  # User auth
│   │   ├── generator/       # Code generation
│   │   ├── projects/        # Project management
│   │   └── payments/        # Paddle integration
│   ├── ai_engine/           # AI components
│   │   ├── gemini_planner.py
│   │   ├── pattern_retriever.py
│   │   ├── code_generator.py
│   │   └── quality_validator.py
│   └── pipeline/            # Pattern database pipeline
│
├── docker/                   # Docker configurations
└── docs/                     # Documentation
```

## 🚦 Usage

### 1. Access the Application

Open your browser to `http://localhost:5173`

### 2. Authentication

Click "Sign Up or Login with GitHub" to authenticate via GitHub OAuth

### 3. Create Your First App

1. Click "Get Started" or "Start Building"
2. Describe your app in natural language
3. Select desired features
4. Choose your tech stack
5. Configure style preferences
6. Review and generate

### 4. Monitor Progress

Watch real-time progress updates as your app is generated:
- Requirements analysis
- Architecture planning
- Code generation
- Quality validation
- GitHub repository creation

### 5. Access Results

- View generated code
- Preview the live application
- Access GitHub repository
- Download as ZIP file

## 🧪 Testing

### Backend Tests

```bash
cd backend
python manage.py test
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## 🐳 Docker Deployment

### Build and Run with Docker Compose

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🌐 Production Deployment

### Frontend (Cloudflare Pages)

```bash
cd frontend
npm run build

# Deploy dist/ folder to Cloudflare Pages
```

### Backend (Fly.io)

```bash
cd backend

# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy
flyctl deploy
```

### Database (Neon PostgreSQL)

1. Create account at [neon.tech](https://neon.tech)
2. Create new project
3. Copy connection string to `DATABASE_URL`

## 📊 Subscription Tiers

| Feature | Free | Pro ($30/mo) | Enterprise ($150/mo) |
|---------|------|--------------|----------------------|
| Monthly Generations | 3 | 10 | 20 |
| Daily Requests | 5 | 20 | 50 |
| GitHub Integration | ✅ | ✅ | ✅ |
| Live Preview | ✅ | ✅ | ✅ |
| Priority Support | ❌ | ✅ | ✅ |
| Debug Existing Repos | ❌ | ❌ | ✅ |

## 🔐 Security

- All user sessions are encrypted
- OAuth tokens securely stored
- Generated code scanned for vulnerabilities with Bandit
- CSRF protection enabled
- Rate limiting implemented
- SQL injection prevention
- XSS protection

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- ChromaDB for vector storage
- Anthropic Claude for architecture inspiration
- Open source community

## 📧 Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/yourusername/webforge-ai/issues)
- Email: support@webforge.ai

## 🗺️ Roadmap

- [ ] Support for more frameworks (Svelte, Solid.js)
- [ ] AI-powered debugging
- [ ] Collaborative editing
- [ ] Version control integration
- [ ] Automated testing generation
- [ ] CI/CD pipeline generation
- [ ] Mobile app support (React Native, Flutter)

---

**Made with ❤️ by the WebForge.ai Team**

**Powered by Google Gemini Flash 2.5**
