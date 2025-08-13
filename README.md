# Emergent Labs Portfolio Website

A professional portfolio website showcasing Emergent Labs' AI-powered application development platform. Built with React frontend, FastAPI backend, and MongoDB database.

## 🌐 Live Demo

The application is currently deployed and accessible at:
https://72b1c11c-42ac-479c-9780-24857d108336.preview.emergentagent.com

## 📋 Prerequisites

Before setting up the project locally, ensure you have the following installed:

### Required Software
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **MongoDB** (v4.4 or higher) - [Download here](https://www.mongodb.com/try/download/community)
- **Yarn** (recommended package manager) - Install with `npm install -g yarn`

### Verify Installation
```bash
node --version    # Should be v16+
python --version  # Should be v3.8+
mongod --version  # Should be v4.4+
yarn --version    # Should be installed
```

## 🚀 Local Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd emergent-labs-portfolio
```

### 2. Database Setup

#### Start MongoDB
```bash
# On macOS with Homebrew
brew services start mongodb-community

# On Ubuntu/Debian
sudo systemctl start mongod

# On Windows
# Start MongoDB service from Services app or run:
mongod
```

#### Verify MongoDB is Running
```bash
# Connect to MongoDB to verify it's running
mongosh
# You should see MongoDB shell prompt
```

### 3. Backend Setup

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Install Backend Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables
```bash
# The .env file should already exist with these settings:
# MONGO_URL="mongodb://localhost:27017"
# DB_NAME="test_database"
# CORS_ORIGINS="*"

# Verify .env file exists and has correct content
cat .env
```

#### Start Backend Server
```bash
# Run the FastAPI server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

The backend will be available at: `http://localhost:8001`

### 4. Frontend Setup

#### Open New Terminal and Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Frontend Dependencies
```bash
yarn install
```

#### Configure Frontend Environment Variables
```bash
# Update .env file with local backend URL
echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env
echo "WDS_SOCKET_PORT=443" >> .env
```

#### Start Frontend Development Server
```bash
yarn start
```

The frontend will be available at: `http://localhost:3000`

## 📁 Project Structure

```
emergent-labs-portfolio/
├── backend/                    # FastAPI backend
│   ├── server.py              # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   └── venv/                  # Python virtual environment
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styling
│   │   └── index.js          # Entry point
│   ├── public/               # Static assets
│   ├── package.json          # Node dependencies
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   └── .env                  # Environment variables
├── tests/                    # Test files
├── README.md                 # This file
└── backend_test.py           # API testing script
```

## 🔌 API Endpoints

The backend provides the following API endpoints:

### Portfolio Endpoints
- `GET /api/` - Root endpoint
- `GET /api/portfolio` - Get all portfolio sections
- `GET /api/portfolio/{section_id}` - Get specific portfolio section

### Contact Endpoints
- `POST /api/contact` - Submit contact form
- `GET /api/contact` - Get contact submissions

### Status Endpoints
- `POST /api/status` - Create status check
- `GET /api/status` - Get status checks

### Example API Usage
```bash
# Get all portfolio data
curl http://localhost:8001/api/portfolio

# Submit contact form
curl -X POST http://localhost:8001/api/contact \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "message": "Hello!"}'
```

## 🧪 Testing

### Backend API Testing
Run the comprehensive API test suite:
```bash
python backend_test.py
```

### Manual Testing
1. **Frontend**: Open `http://localhost:3000` and verify all sections load
2. **Navigation**: Test smooth scrolling between sections
3. **Contact Form**: Submit a test message and verify it's saved
4. **API**: Use the endpoints listed above to test backend functionality

## 🛠️ Development

### Available Scripts

#### Backend
```bash
# Start development server with auto-reload
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Run with custom host/port
uvicorn server:app --host 127.0.0.1 --port 8000 --reload
```

#### Frontend
```bash
# Start development server
yarn start

# Build for production
yarn build

# Run tests
yarn test
```

### Hot Reload
Both frontend and backend support hot reload:
- **Frontend**: Automatically reloads when you save React files
- **Backend**: Automatically reloads when you save Python files (with `--reload` flag)

## 🎨 Features

### Frontend Features
- ✅ **Hero Section**: Company overview with key features
- ✅ **Services Section**: Core services and offerings
- ✅ **Target Users**: Information about who we serve
- ✅ **Differentiators**: What makes Emergent Labs unique
- ✅ **Technical Capabilities**: Technology stack details
- ✅ **Platform Features**: Complete development environment
- ✅ **Contact Form**: Lead generation with backend integration
- ✅ **Responsive Navigation**: Smooth scrolling with mobile menu
- ✅ **Professional Design**: Dark theme with AI-focused imagery

### Backend Features
- ✅ **Portfolio API**: Comprehensive company information
- ✅ **Contact Management**: Form submissions with MongoDB storage
- ✅ **Status Monitoring**: Health check endpoints
- ✅ **CORS Support**: Cross-origin resource sharing
- ✅ **Data Validation**: Pydantic models with validation
- ✅ **Error Handling**: Proper HTTP status codes and error responses

## 🌍 Environment Variables

### Backend (.env)
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
CORS_ORIGINS="*"
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=443
```

## 🔧 Troubleshooting

### Common Issues

#### MongoDB Connection Error
```bash
# Check if MongoDB is running
brew services list | grep mongodb  # macOS
sudo systemctl status mongod       # Linux

# Start MongoDB if not running
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

#### Port Already in Use
```bash
# Find process using port 8001
lsof -i :8001

# Kill process if needed
kill -9 <PID>

# Or use different port
uvicorn server:app --host 0.0.0.0 --port 8002 --reload
```

#### Frontend Build Issues
```bash
# Clear cache and reinstall
rm -rf node_modules yarn.lock
yarn install

# Update browserslist
npx update-browserslist-db@latest
```

#### Python Dependencies Issues
```bash
# Upgrade pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Getting Help

If you encounter issues:
1. Check the console logs for error messages
2. Verify all prerequisites are installed correctly
3. Ensure MongoDB is running and accessible
4. Check that all environment variables are set correctly
5. Review the API endpoints section for correct usage

## 📝 Development Notes

- The application uses **MongoDB with UUID primary keys** instead of ObjectId for better JSON serialization
- **Tailwind CSS** is used for styling with a professional dark theme
- **AI-generated images** from Unsplash and Pexels provide visual appeal
- **FastAPI** provides automatic API documentation at `http://localhost:8001/docs`
- **React Router** handles client-side routing
- **Axios** manages API communication between frontend and backend

## 📄 License

This project is part of the Emergent Labs portfolio and showcases the company's AI-powered development capabilities.

---

**Built with ❤️ by Emergent Labs - The AI-Powered Application Development Platform**
