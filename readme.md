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



### Infections    

The Infections folder contains a file per time step of the form `infection_xxxx.csv` where `xxxx` is a number, e.g.
`infection_0132.csv`.

Each CSV file must be of the form:

| individual_id | infected |
|---------------|----------|
| 1267e         | True     |
| 7273f         | False    |

If an individual does not appear in the file, but they are known by the system, they are assumed to have their 
previous state. If they have not been seen before, then they are assumed not to be infected.

### Locations
    
The Locations data contains a complete list of all geographic locations over all time steps. An example of the 
structure of the data is:

| identifier | name    |
|------------|---------|
| s1         | Germany |
| s2         | France  |

Note that the identifier must be unique as this is used by the Individuals data.

## Particle filter examples

This Python project contains a `particle_filtering_examples` module that holds small scripts that were used to help 
learn how particle filters work. The code isn't relevant for the main the solution, but could be useful for learning 
or tutorials.
 