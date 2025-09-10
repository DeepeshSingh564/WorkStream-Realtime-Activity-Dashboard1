# Django Activity Tracker

## Overview

This is a Django-based activity tracking application that allows users to log and monitor their activities in real-time. The system features user authentication, activity logging with duration tracking, and live updates through WebSocket connections. Users can sign up, log in, create activity entries, and view their activity history through a web dashboard with real-time updates.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Django 5.2.6** with Django REST Framework for API endpoints
- **Django Channels** with Redis backend for WebSocket support and real-time communication
- **Token-based authentication** using Django's built-in token system
- **SQLite database** (default Django setup) for data persistence

### Application Structure
- **accounts app**: Handles user registration, login, and authentication
- **activity app**: Manages activity logging, dashboard views, and real-time updates
- **RESTful API design** with separate endpoints for web pages and API operations

### Authentication & Authorization
- Token-based authentication for API access
- Session authentication for web interface
- Per-user activity isolation (users only see their own activities)
- CSRF protection for form submissions

### Real-time Communication
- **WebSocket consumers** for live activity updates
- **Per-user channel groups** to ensure users only receive their own activity updates
- **Redis channel layer** for message passing between Django instances
- Automatic WebSocket connection on dashboard load

### Database Schema
- **User model**: Django's built-in User model for authentication
- **ActivityLog model**: Stores activity entries with user foreign key, activity name, duration (in minutes), and timestamp
- **Token model**: Django's built-in token model for API authentication

### API Endpoints
- `POST /api/signup/`: User registration
- `POST /api/login/`: User authentication
- `POST /api/logout/`: User logout
- `GET/POST /api/activities/`: List user activities and create new entries
- `GET/PUT/DELETE /api/activities/<id>/`: Individual activity operations

### Frontend Integration
- Server-side rendered templates with vanilla JavaScript
- AJAX forms for seamless user interaction
- WebSocket client for real-time dashboard updates
- Token storage in localStorage for API authentication

## External Dependencies

### Core Framework Dependencies
- **Django 5.2.6**: Main web framework
- **Django REST Framework 3.16.1**: API development and serialization
- **Django Channels 4.3.1**: WebSocket and async support

### Real-time Communication
- **channels-redis 4.3.0**: Redis channel layer for Django Channels
- **redis 6.4.0**: Redis client library
- **Twisted 25.5.0**: Async networking framework (Channels dependency)

### WebSocket & Async Support
- **autobahn 24.4.2**: WebSocket protocol implementation
- **daphne 4.2.1**: ASGI server for Django Channels
- **Twisted** and related libraries for async operations

### Security & Cryptography
- **cryptography 45.0.7**: Cryptographic operations
- **pyOpenSSL 25.1.0**: SSL/TLS support

### Deployment
- **Replit hosting environment**: Configured for Replit's domain structure
- Environment-based ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS configuration