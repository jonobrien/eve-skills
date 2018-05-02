eve-skills
==========

Create a simple HTML skill overview by supplying an EVE Online API key.  Uses the soon-deprecated xml api for character/api access. Uses the SDE for skill information.

## charsheet

```
python charsheet.py <apikey> <vCode> > <output.html>
```





## skillcheck

Generates an html page showing skills missing from character that the csv file contains

```
python skillcheck.py <csv-file> <apikey> <vCode> > <output.html>
```


csv file with `<skill group, name, required level>` to compare against api:

```
Gunnery,Gunnery,5
"Planet Management","Advanced Planetology",5
Drones,"Medium Drone Operation",1
"Spaceship Command","Caldari Strategic Cruiser",5
```