# story-website

A website for story-driven programming competitions.

## Architecture

### Backend

The backend itself is written in Python (with Flask), and is made up of a couple of sections:

- The "Advent of Code" stuff itself (in `/backend/advent`): where all of our puzzles are located.
- Authentication (in `/backend/auth` and `/backend/routes/auth.py`): where our login/registration/logout stuff is located.
- API (in `/backend/routes`): the main point of access between the frontend and backend.

Features we want to implement:
[] Email verification (i.e. when we register an account, an email gets sent to the account name)
[] A decent puzzle architecture

### Database

The database is written in PostgreSQL, and the backend uses `psycopg2` in order to interact with it (so if you've done COMP3311,
this should be pretty familiar). The creation of tables can be found in `/database/setup.sql`.

### Frontend

The frontend is written in React, and we plan to have the following features:
[] Cleaned-up login/register/logout pages
[] Profile page
[] Leaderboard

## How to build

1. Download Docker Desktop and follow the instructions [here](https://docs.docker.com/desktop/windows/wsl/#download). (Assumes Windows - if you're using something else then follow instructions there)
2. Create the `config` folder, and put all `.env` files there.
3. In the main folder, run `docker-compose up --build` to make your Docker images for the first time. `--build` is not necessary when you update code later on.
4. If you need to add a package that doesn't already exist to the frontend, make sure to do `docker-compose down -v` first, and then do `docker-compose up --build`.
5. Profit
