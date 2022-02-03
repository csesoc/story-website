# story-website

A website for story-driven programming competitions.

## How to build

1. Download Docker Desktop and follow the instructions [here](https://docs.docker.com/desktop/windows/wsl/#download).
2. Create the `config/.env` file containing all environment variables.
3. In the main folder, run `docker-compose --env-file="./config/.env" up --build` to make your Docker images for the first time. `--build` is not necessary when you update code later on.
4. Profit
