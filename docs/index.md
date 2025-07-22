# Battle Results Flask Documentation

Welcome to the Battle Results Flask application documentation. This documentation provides detailed information about the project, its structure, and how to use it.

## Table of Contents

1. [Setup Guide](setup.md)
   - Instructions for setting up the development environment
   - Running the application locally

2. [API Documentation](api.md)
   - Endpoint descriptions
   - Request and response formats
   - Example usage

3. [Deployment Guide](deployment.md)
   - Options for deploying the application
   - Considerations for production environments
   - Docker deployment

4. [Best Practices](best_practices.md)
   - Code organization
   - Development workflows
   - Security considerations
   - Database management

5. [Troubleshooting](git_venv_windows_fix.md)
   - Fixing Git issues on Windows
   - Virtual environment troubleshooting

## Interactive API Documentation

When the application is running, you can access the interactive Swagger UI API documentation at:

```
http://localhost:8080/api/docs
```

## Project Overview

The Battle Results Flask application is a RESTful API service for managing game battle results. It provides endpoints for creating, reading, updating, and deleting battle entries. The application uses SQLite as its database and SQLAlchemy as the ORM.

### Key Features

- RESTful API for managing battle results
- Web interface for viewing battle entries
- Swagger UI for API documentation
- SQLite database for data storage
- Modular architecture for easy extension
