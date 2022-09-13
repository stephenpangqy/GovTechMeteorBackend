# GovTechMeteorBackend
The repository for TAP 2023 Technical Assessment (Q2) - Stephen Pang

## How to Setup
1. Run the load.sql script to setup the MySQL Database
2. Edit the .env file with your DB_USER and DB_PASSWORD
3. If you are on Windows, you can start both microservices by running the start.bat file.
4. For testing of code, you can use the Postman Collections (TAP 2023.postman_collection.json) to run these test cases.

## Architecture
I decided to go for a microservice architecture, as this will decouple the services of interacting with the grant scheme database, as well as the household and family database. The grant information provided in the assessment was placed in a database to simulate the possibility of adding more grants by simply inserting them into the database.

### Grants.py
This microservice controls the grant scheme database, and interacts with the Household microservice to retrieve the necessary household data of those who are eligible for the grant.
### Household.py
This microservice controls the household and family member database, and provides most of the necessary endpoints as specified in the assessment.

## Assumptions
1. Assuming that the date of birth of all family members is provided in a YYYY-MM-DD format.
2. Assuming that the grant scheme criteria only involves the income and age of the household members.
3. Assuming that Unit Numbers are unique, regardless of housing type, as the unit number is the primary key of the database.


