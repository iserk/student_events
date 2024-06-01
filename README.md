# Student Academic Management System

## 0. Introduction

This project is a simple student academic management system.
It is a web application that allows teachers to manage their courses and students to enroll in courses. 

## 1. Features
- Students can enroll and unenroll in courses.
- Teachers can view the list of students enrolled in their courses.
- Students can view the list of courses they are enrolled in.
- Teachers can manage the courses they teach.
- Courses can be marked as active or inactive. Inactive courses will not available for enrollment.
- Courses can be marked as public or private. Private courses will not be visible to students but can still be enrolled in by students.

## 2. Technologies
- Python 3.12+
- Django 5+
- SQLite (for development)
- PostgreSQL (for production)
- Bootstrap 5
- Redis (for caching and session storage)
- Nginx (for serving static files and reverse proxy)

## 3. Installation

First of all, clone the repository:
```bash
git clone https://github.com/iserk/student_events.git
```

### 3.1 Docker

The project can be installed using Docker Compose (make sure you have Docker and Docker Compose installed on your system).

Before starting the project, please update the environment variables in the `.env` file if needed.
The most important environment variables are the following:
```conf
# Django
# Please replace 'your_secret_key' with a random string
# You can generate it with django.core.management.utils.get_random_secret_key()
DJANGO_SECRET_KEY=your_secret_key

# Nginx (used only in production)
NGINX_HOST_PORT=127.0.0.1:8081
```

#### 3.1.1 Development Environment
Use the following command to start the project in development mode:
You don't need to configure anything. Feel free to skip to the section 4.1.

#### 3.1.2 Production Environment
In production, the project is intended to be run behind an Nginx reverse proxy,
which can also be used as a TLS termination point.

In case you already have an Nginx server running on your server, this setup can use two instances of Nginx:
- One is containerized and used for serving static files and reverse proxying to the Django application.
- The other one is the existing Nginx server that will be used as a TLS termination point, reverse proxying to the containerized Nginx.

Below is an example configuration of an external Nginx server that will be used as a TLS termination point:

```nginx

server {
    listen 443 ssl;
    server_name your_domain_name.com;
    keepalive_timeout 5;
    charset utf-8;

    access_log /var/log/nginx/your_domain_name.access.log;
    error_log /var/log/nginx/your_domain_name.error.log;

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_redirect off;

        if (!-f $request_filename) {
            # Host and port of the containerized Nginx server.
            # Change '127.0.0.1:8081' here to your host:port; must match the NGINX_HOST_PORT in the .env file:
            proxy_pass http://127.0.0.1:8081;
            break;
        }
    }

    ssl_certificate /etc/letsencrypt/live/your_domain_name.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain_name.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

# Optional: Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your_domain_name.com;
    return 301 https://your_domain_name.com$request_uri;
}
```

## 4. Running the project

### 4.1 Development Environment

```bash
docker-compose up
```


### 4.2 Production Environment

```bash
docker-compose -f production.yml up
```

## 5. Accessing the application

### 5.1 Development Environment
After starting the project, you can access the application at `http://localhost:8000/`.

### 5.2 Production Environment
After starting the project, you can access the application at `https://your_domain_name.com/`.

