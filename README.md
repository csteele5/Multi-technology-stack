# Multi Technology Stack

## Summary

This repository contains details of all the components of this web/database stack. The purpose of this system is to showcase different technologies integrated together for the purposes of managing the following data:

- Code Snippets for use in different development projects
- Simple Poll Results
- To-do / Issue Tracking

## Stack Technologies

The primary philosophy during the build of this system is to host all distinct elements in individual Docker containers to be hosted on AWS, and keep all changes updated through a CI/CD pipeline.  Technologies and primary purpose are as follows:

| Technology | Purpose |
| ----------- | ----------- |
| Docker | Container technology used to house individual technologies that interact to perform as a single system with multiple input/output pathways |
| Django | Backend Framework, defining classes, managing data structure |
|Django REST Framework | Extends Django to provide a secure and stable API for CRUD operations |
| Python | Backend coding language, controlling all functions in the Django Framework and the APIs through the Django REST Framework and Flask REST Framework |
| PostgreSQL | Primary SQL database for all relational data |
| MongoDB | NoSQL database for transactional history and active data collections |

Additional technologies in planning stages: 

- React
- React Native
- Node.js
- PHP
- Laravel
- CodeIgniter


## System Functionality

## System Diagram

![very scientific diagram goes here](assets/sysDiagram.jpg)

## Task List

The task list will be incorporated into the Django backend and a link will be provided.  Initially, the task list will appear below:

### Set Up Project
- [x] Sketch out high level design
- [x] Create local repository for development
- [x] Initialize README.md with plan for project
- [ ] Create Git Repo and perform initial push
- [ ] Initialize framework for multiple container environment

### Build System Back End
- [ ] Deploy Django out-of-box on Docker
- [ ] Deploy Postgres in separate container
- [ ] Initialize Postgres as data source for Django
- [ ] Verify basic Django/Postgres functionality with persistent data store while in development environment before moving forward

### Build Django System Front End

**Build Function #1 - Code Snippet Catalog**
- [ ] Create data structure
- [ ] Create simple Django form
- [ ] Build user login
- [ ] Apply user login
*The primary CRUD access to this snippet catalog will be through the admin pages, React, PHP*

**Build Function #2 - Simple Poll**
- [ ] Create data structure
- [ ] Create simple Django form - No user login
- [ ] Add basic CSS styling
*Django will provide basic anonymous submit functionality.  Results visualization TBD*

**Build Function #3 - Task / Issue Tracker**
- [x] Design data structure
- [ ] Create data structure
- [ ] Create simple Django form
- [ ] Apply user login
*The primary CRUD access to this snippet catalog will be through the admin pages, React, PHP*

### Build REST API Capability

Set up Django REST Framework, Flask/Python framework with token authentication.  Allow all CRUD capabilities for the Code Snippet Catalog and Task / Issue Tracker.  Allow Create and Read capability for the Simple Poll.

### Build React Application to Consume REST API

Have Node talk to the API or React will directly interact with the API. 

### Additional Functionality/Technologies

- MongoDB (log transactions, what technology performed the work, user, etc)
- Possible transition of a function from SQL to NoSQL
- PHP
- React Native (mobile)
- Data Visualization capability

## References

This is a list of the primary resources used to put these technologies together.