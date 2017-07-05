# Hackpad Migrations Email Parser

## Requirements
- Python 3
- Python Virtual Env

## Setup Environment
- Run `./bin/bootstrap.sh` to setup a Python Virtual Env inside the project root.
- Add gmail OAUTH2 client secret inside `.credentials/client_secret.json`
- Obtain OAuth 2.0 Credentials: run `./bin/fetch_credentials.sh` 

## Run (once)
- Edit (or copy and edit) the `./config/config.yml` file
- Set the `download_directory` using a **full path** to the destination directory.
- Run `./bin/run.sh [path-to-config-file]` (default path-to-config-file is `./config/config.yml`)