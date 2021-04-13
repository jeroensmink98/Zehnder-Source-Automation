# Zehnder-Source-Automation
The offical repo of the Zehnder Source Automation project

## Build Container from scratch
If you want to build the docker container from scratch you can find a ``.Dockerfile`` in the ``/docker`` folder. You can open the file with a text editor.

When you are done making changes build a new version of the image by going into the directory and run ``docker build . `` or when you want to upload it to a registery run ``docker build -t <USERNAME>/<REPO>:TAG .`` It will build a version that you can push to the registery.

If you want to use your own image you just builded yourself edit the ``docker.compose.yml`` file. and change the value of ``image:`` into the name of your container.


## How to run
1. Clone the project to the target machine
2. Create a copy of the ``env.example`` file and name it ``.env``
3. Configure the ``.env`` file to your needs
4. Run ``docker-compose up`` to startup the environment
5. In the output of the console you can find a url that will lead to the notebook environment, including a cookie to login


## Adding libraries
To add packages to the build include them in the ``requirements.txt``. After that you will need to rebuild the image with ``docker compose build``.

Make sure you either push the new container to the Docker hub or include the local container in the ``docker-compose.yml`` file.
