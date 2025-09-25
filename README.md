# Product Catalog API Service 🛒

## Description
Product Catalog API Service is a web-based platform that allows users to manage and search products via saved filters. Built with FastAPI and MongoDB (Beanie + Motor), this system provides a scalable and extensible API for product and filter management. It supports CRUD operations for products and filters, as well as searching products using saved filters. The entire system is containerized with Docker for easy deployment.

## Project Features
- **📦 Product Management:**
  - Create, read, update, and delete products
  - Paginated product listing with configurable `page` and `per_page`
  - Unique name validation to prevent duplicates
- **🔖 Filter Management:**
  - Create, read, update, and delete filters
  - Each filter consists of multiple conditions with operators
  - Supports complex logical operators (AND/OR)
  - Filter engine designed for easy extension: adding new operators requires minimal changes
- **🔍 Product Search via Filters:**
  - Retrieve products filtered by saved filters
  - Paginated results with previous/next page links
  - Returns HTTP 404 if no products or filters are found
- **⚡ Scalable & Extensible:**
  - Asynchronous operations via FastAPI + Motor
  - MongoDB used for flexible document storage
  - Designed to handle growing data sets efficiently
- **🐳 Containerized Deployment:**
  - Fully dockerized with `docker-compose`
  - Separate services for web and database
  - Persistent MongoDB storage via Docker volumes

## Installation and Setup
To get started with the Product Catalog API Service, follow these steps:

### Step 1: Clone the Repository
```bash
git clone https://github.com/rezehor/product-catalog.git
```
### Step 2: Environment Variables
Copy the sample .env file
```bash
cp .env.sample .env (Linux / macOS)
copy .env.sample .env (Windows)
```
### Step 3: Run with Docker
```bash
docker-compose up --build
```
## Service URLs
Docs (Swagger API documentation)
```bash
http://localhost:8000/docs
```
Redoc (Redoc API documentation)
```bash
http://localhost:8000/redoc
```
MongoDB Compass (MongoDB management GUI)
```bash
http://localhost:27018
```