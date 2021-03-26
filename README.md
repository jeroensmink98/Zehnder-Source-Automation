# Zehnder-Source-Automation
The offical repo of the Zehnder Source Automation project

## How to run
1. Clone the project to the target machine
2. Create a copy of the ``env.example`` file and name it ``.env``
3. Configure the ``.env`` file to your needs
4. Run ```docker-compose up`` to startup the environment


## Adding libraries
To add packages to the build include them in the ``requirements.txt``. After that you will need to rebuild the image with ``docker compose build``.

Make sure you either push the new container to the Docker hub or include the local container in the ```docker-compose.yml`` file.
