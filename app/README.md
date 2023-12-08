# This is my implementation of simple web blog  

## Description:
This is a training project firstly to improve FastAPI and Pydantic mastery, 
also to train JWToken authorization

### Additional notes:
consists of two routes: Users and Posts

## Current Status:
Not finished; Check TODO list;
## Requirements:
# Python:
- [Python 3.10.5](https://www.python.org/downloads/)
# DataBase:
- [Postgres](https://www.postgresql.org)
- [SQLAlchemy 2.0.18](https://www.sqlalchemy.org)
# Deployment and testing: 
- [docker 24.0.6](https://docs.docker.com/get-docker/)
- [Postman](https://www.postman.com/downloads/)
# Significant Libraries and Frameworks:
- [fastapi 0.104.1](https://fastapi.tiangolo.com)
- [pytest 7.4.3](https://docs.pytest.org/en/7.4.x/)
- [cryptography 41.0.1](https://cryptography.io/en/latest/)
- [python-jose 3.3.0](https://pypi.org/project/python-jose/)

# Notes on listed dependencies:

# ToDo:

following coroutines: 
- get_all_posts_per_user
- get_post
- delete_post
- add_reaction_to_post
- del_reaction_to_post

authorization logic:
- permissions
- roles logic