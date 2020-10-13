<div align="center">

# flick

`flick = flask + click`<br>
**Time for some Pizza!**

---

</div>

## :ledger: Contents
- [About](#beginner-about)
  - [Technologies Used](#technologies-used)
  - [Team](#team)
- [Development Setup](#electric_plug-development-setup)
  - [Running the webserver](#running-the-webserver)
  - [Setting up/Installing the CLI client](#setting-upinstalling-the-cli-client)
- [Usage](#zap-usage)
  - [Commands](#commands)

## :beginner: About
Tired from working a lot on your terminal? Feeling hungry?<br>
Now you can order a Pizza on the fly, directly through your command line using `flick`!<br>
`flick` is the combination of a CLI application that interacts with a webserver with information about various pizza joints and their menu. Your Pizza is just a command away.<br>
(Note: This is just a mock-up for now, and doesn't actually order a pizza)

#### Technologies Used
- [`flask`](https://github.com/pallets/flask): Powers the webserver that serves the joints' info, their data and receives orders
- [`$ click_`](https://github.com/pallets/click): Heart of the Command-Line client that the user interacts with

#### Team
- [Aksh](https://github.com/akshgpt7)
- [Grace](https://github.com/gracewgao)
- [Brandon](https://github.com/bepotts)


## :electric_plug: Development Setup

- Clone this repository by running `git clone https://github.com/akshgpt7/flick` and cd into it.
- Make sure you have pipenv installed on your system. If not, do it by `pip install pipenv`.
- To activate a virtual environment for the project, run `pipenv shell`. After this, you'll be inside the virtual environment.
- Install the dependencies by running `pipenv install`.

### Running the webserver
- cd into the webserver directory using `cd src/webserver`.
- Run the command `flask run`.
- The server will now be up and running.

### Setting up/Installing the CLI client
***Note: This can be done system wide (outside the pipenv) if you just want to use the client, but it's highly recommended to do it inside the virtual env for development.***
- In a new terminal window, cd into the cli directory by `cd src/cli`.
- Run the following command:
  - **Linux**: `python3 -m pip install --editable .`
  - **Windows**: `pip install -e .`
- Use any `flick` [command](#commands) now!

## :zap: Usage
Type `flick --help` to see a help message, and a list of commands you can use.<br>
***Type `flick [command-name] --help` to see help for a particular command.***

#### Commands:
- `joint-info`   View information about a specific pizza joint
- `order`        Place your order for pizza :)
- `rate`         Send a review for a pizza joint!
- `show-joints`  View all available pizza joints
- `show-menu`    Show menu items for joint specified
