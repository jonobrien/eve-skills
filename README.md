eve-skills
==========

Create a simple HTML skill overview by supplying logging into your account. Uses the SDE for skill information.

## skillsheet

```
python app.py
```
navigate to localhost:1337/login

get redirected to login, and back to your skills


## skillcheck

Generates an html page showing skills missing from character that the csv file contains

csv file in root directory called test.csv

```
python app.py
```
navigate to localhost:1337/login

get redirected to login, then back to your skills

then click the skillcheck button

requires a csv file with `<skill group, name, required level>` to compare against api:

```
Gunnery,Gunnery,5
"Planet Management","Advanced Planetology",5
Drones,"Medium Drone Operation",1
"Spaceship Command","Caldari Strategic Cruiser",5
```