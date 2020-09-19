# `TBGlobalist Covid-19`

This repository is collection of python scripts used by [tbglobalist.com](https://www.tbglobalist.com) for its publications.

The original intend is to create a list of scripts to regularly update the [tbglobalist.com](https://www.tbglobalist.com) 
site with articles on Covid-19.

Any files of this repository, along with articles on Covid-19 published on [tbglobalist.com](https://www.tbglobalist.com), 
are released under [GNU license]().
The aim is to encourage worldwide programmers and the scientific community to contribute with their expertise, in order 
to make general improvements to the researches and propose new ones.

Countries whom Freedom of Speach index is not at satisfactory level are excluded from the researches. 

The Covid-19 data is extracted from [Our World in Data](https://ourworldindata.org/coronavirus) datasets, which are 
updated daily.

At the moment are available the following scripts: 

#### `covid19_over65.py`
~~~~
It contains logic to make relation beetwen Covid deaths and the population of over 65 years old. It produces each day an
article update based on this index. 
Ex: https://www.tbglobalist.com/2020/09/15/covid-19-deaths-against-population-of-65-years-and-over-updated-to-15-september-2020/
The script makes use of world_pop_2020.csv, a dataset which contains world population data by age classes (data comes 
from the United Nations: https://population.un.org/wpp/Download/Standard/Population/).

**SCRIPT USAGE**
The script can be invoked in another python script, once the CovidData class has been imported. This is the case of 
TBGlobalist, which use the script to generate its articles. At the end of the file there is an example usage of the 
class.

~~~~


