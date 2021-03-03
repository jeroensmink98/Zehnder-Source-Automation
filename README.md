# Zehnder-Source-Automation
The offical repo of the Zehnder Source Automation project

## How to run
To run the local version of the development environment just build the docker container and start it

To build the docker container run ``docker compose build`` after that run ``docker compose up`` Don't include the ``-d`` flag since we want our Notebook URL to be displayed in the terminal

## Adding libraries
To add packages to the build include them in the ``requirements.txt``. After that you will need to rebuild the image with ``docker compose build``.
