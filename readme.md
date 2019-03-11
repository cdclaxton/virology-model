# Virological Model

## Introduction

## Configuration

The configuration for reading the data and running the inference engine is expressed in a JSON file. This enables
the software to be run against different data sets more quickly than if the configuration was stored as parameters
in the code.

* `paths`:
    * `individuals` -- folder containing the data on individuals for each time step.
    * `infections` -- folder containing the infection data for each time step.
    * `locations` -- CSV file containing all geographic locations (except `unknown` and `dead`, which are added 
    automatically).
    
### Individuals

The Individuals folder contains a file per time step of the form `individual_xxxx.csv` where `xxxx` is a number, e.g.
`individuals_0056.csv`.

Each CSV file must contain the individual's identifier (`individual_id`), their name (`name`), date of birth (`dob`),
date of death (`dod`), caused by the infection or otherwise, and any required attributes.

| individual_id | name           | dob        | dod         | height | weight |
|---------------|----------------|------------|-------------|--------|--------|
| 0001          | Stan Smith     | 01/03/1970 | None        | 178    | 72     |
| 0002          | Francine Smith | 26/04/1973 | None        | 167    | 66     |
| 0003          | Klaus Heissler | 25/08/2010 | 14/02/2017  | 4      | 0.1    |

The date must be in the UK format of DD/MM/YYYY. For an individual who is alive, set their `dod` to `None`.

### Infections    

The Infections folder contains a file per time step of the form `infection_xxxx.csv` where `xxxx` is a number, e.g.
`infection_0132.csv`.

Each CSV file must be of the form:

| individual_id | infected |
|---------------|----------|
| 1267          | True     |
| 7273          | False    |
| 9837          | True     |

If an individual does not appear in the file, but they are known by the system, they are assumed to have their 
previous state. If they have not been seen before, then they are assumed not to be infected.

### Locations
    
The Locations data contains a complete list of all geographic locations over all time steps. An example of the 
structure of the data is:

| location_id | name    |
|------------|---------|
| s1         | Germany |
| s2         | France  |
| s3         | Italy   |

Note that the identifier must be unique as this is used by the Individuals data.

## Particle filter examples

This Python project contains a `particle_filtering_examples` module that holds small scripts that were used to help 
learn how particle filters work. The code isn't relevant for the main the solution, but could be useful for learning 
or tutorials.
 