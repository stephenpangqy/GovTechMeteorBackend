# GovTechMeteorBackend
The repository for TAP 2023 Technical Assessment (Q2)

## How to Setup
1. Run the load.sql script to setup the MySQL Database
2. Edit the .env file with your DB_USER and DB_PASSWORD
3. If you are on Windows, you can start both microservices by running the start.bat file.
4. For testing of code, you can use the Postman Collections (TAP 2023.postman_collection.json) to run these test cases.

## Architecture
I decided to go for a microservice architecture, as this will decouple the services of interacting with the grant scheme database, as well as the household and family database.
