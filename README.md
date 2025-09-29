# FastAPI Product Search With Filters Project

## A fully functional project written in Python showing how to build a FastAPI REST API with product filters and search!

This project is an example that demonstrates how to create a product search API using FastAPI, 
Beanie ODM, and MongoDB. Every part of this project is sample code which shows how to do the 
following:

- **Define flexible filters with nested logical operators (AND/OR)**
- **Store and manage filters in MongoDB with Beanie ODM**
- **Create and query products using dynamic filter conditions**
- **Write tests for filters, products, and product search endpoints**
- **Support pagination for search results**

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