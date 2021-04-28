# Zehnder Source Automation
This is the official repo for the Zehnder Source Automation project lead by Sjoerd Kwakkel and executed by students from Hogeschool Windesheim in 2021.

## Authors
- [Jeroen Smink](https://github.com/jeroensmink98)
- Wolter van Donk
- Diana Truta
- Manar Baouane

## Before running
Make sure you have the following programs installed on your machine
- [Anaconda Navigator](https://www.anaconda.com/products/individual)

## Configure the environment
### Step 1
In this repo you will find a file called ``environment.yml`` import this file in Anaconda Navigator as a environment. Go to the environments tab in Anaconda Navigator and in the bottom select <b>import</b> from here select the ``environment.yml`` file and give the environment a name.

The Python environment will be imported and all modules are already installed and ready to use. 

### Step 2
Next you will have to configure the ``config.ini`` file. Here you will have to select both the full path location of the ``run_all_scripts.bat`` file in the file system and specify an output path for the ``.csv`` files that will be exported when executing the scripts.

Make sure the user who is runnig/executing the scripts has enough rights to write to the target location in the ``config.ini`` file. Otherwise the scripts will throw an exception.


## Run the scripts
Now there are two ways of running the scripts. Inside of Qlik Sense you can target the functionality called ``ZSAs.RunScripts`` This method will cause all python scripts to run inside of the ``scripts`` directory. 

You can also manualy launch the scripts by running ``python run.py`` from the CLI of your Anaconda environment.


## Adding packages to the environment
If you need to add new packages to the Anaconda Environment either trough the Anaconda tool or trough Pip you can do it as following:

1. Go to the environment tab in Anaconda Navigator.
2. Open your specific environment by pressing the arrow button and then choose terminal.
3. Now just install your pip packages as normal
4. When done installing the packages you can create an export of your environment by typing ``conda env export > environment.yml --name zsa`` the ``environment.yml`` file can then again be imported as a seperate environment or be added to version control when a package is updated etc..
5. WARNING: For some reason the outputted file ``environment.yml`` gets a UTF-16 encoding. This has to do with the fact we use ``>`` in the command. Therefore you have to open the file first in a text-editor and change the encoding to UTF-8 otherwise Anaconda will not import the file. If you know how to fix this.. please let [Jeroen Smink](https://github.com/jeroensmink98) know or update the documentation.

## Using the configuration file
You can add new variables to the configuration file by using a key value pair. then in your python scripts you will only have to import the module that takes care of the ``ini`` file and you good to go!

```py
from configparser import ConfigParser

# Create instance of configParser
config = ConfigParser()

# Import ini file
config.read("config.ini")

my_var = config.get("main", "KEY")
```



