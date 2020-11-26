# Ssh update

This API has two endpoints for updating and viewing information on a router.

## Setup

Clone repository.

```bash
git clone https://github.com/LuisG93/router_test.git
```

Create a virtualenv:

```bash
virtualenv apienv --python=python3
```

Activate it.

Install python libraries

```bash
pip install -r requirements.txt
```

## Runserver

```bash
flask run
```

## update_router endpoint

You can enter to the endpoint <http://localhost:5000/update_router/> using post method. You need to pass the following arguments:

- routers: This param is a list of diccionaries. Each of them contain the information about a router and must contain this fields:
  - ip: A string with the ip for the router
  - port: A integer with the port number
  - user: A string with the ssh username
  - password: A string with the ssh password
  - interface: A string with the name of the interface to update
- bandwidh: A integer with the new bandwith for all the routers(Kbps)

## get_router endpoint

You can enter to the endpoint <http://localhost:5000/get_router/> using post method. You need to pass the following arguments:

- routers: This param is a list of diccionaries. Each of them contain the information about a router and must contain this fields:
  - ip: A string with the ip for the router
  - port: A integer with the port number
  - user: A string with the ssh username
  - password: A string with the ssh password
  - interface: A string with the name of the interface to update
- info: An array of strings. You can send "bandwidth" and "address".
