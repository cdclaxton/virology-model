# Virological Model

## Introduction

This software models how infections are transmitted between sub-populations with a temporal dependence. Due to the
non-linear nature of the model, a Particle Filter is employed.

The purpose of the sub-populations aspect is to restrict the complexity of the model. At each time step, it is assumed 
that the sub-population to which an individual belongs is known. Some of the attributes of an individual are used by 
the model to determine the probability of transmission of an infection. 

## Configuration and input data

The configuration for reading the data and running the inference engine is expressed in a JSON file. This enables
the software to be run against different data sets more quickly than if the configuration was stored as parameters
in the code.

* `paths`:
    * `individuals` -- folder containing the data on individuals for each time step.
    * `infections` -- folder containing the infection data for each time step.
    * `timestep_names` -- file containing a name for each timestep for plotting and logging purposes
    
### Individuals

The Individuals folder contains a file per time step of the form `individual_xxxx.csv` where `xxxx` is a number, e.g.
`individuals_0056.csv`.

Each CSV file must contain the individual's unique identifier (`individual_id`) and their attributes. The model
currently uses the attributes:

- name (`name`)
- date of birth (`dob`)
- date of death (`dod`) caused by the infection or otherwise
- location (`location`) -- the locations `dead` and `unknown` are treated differently in that the transmission of 
  infections is not considered

An example of the input CSV data is:

| individual_id | name           | dob        | dod         | location |
|---------------|----------------|------------|-------------|----------|
| 0001          | Stan Smith     | 01/03/1970 | None        | Germany  |
| 0002          | Francine Smith | 26/04/1973 | None        | Germany  |
| 0003          | Klaus Heissler | 25/08/2010 | 14/02/2017  | Dead     |

The date must be in the UK format of DD/MM/YYYY. For an individual who is alive, set their `dod` to `None`.

It is expected that the attributes will update over time. At each time step, only the latest attributes are retained.

The converters to parse the attributes are specified in the JSON configuration file.

### Infections    

The Infections folder contains a file per time step of the form `infection_xxxx.csv` where `xxxx` is a number, e.g.
`infection_0132.csv`. The individual ID and infection strain are both treated as strings.

Each CSV file must be of the form:

| individual_id | infection_strain |
|---------------|------------------|
| 0001          | c-1              |
| 0002          | c-2              |
| 0003          | None             |

If an individual does not appear in the file, but they are known by the system, they are assumed to have their 
previous state. If they have not been seen before, then they are assumed not to be infected.

### Timestep names

For plotting and logging purposes, a more meaningful name can be associated with each timestep. A CSV file is used
to hold the `timestep` (e.g. `2`) and a name (e.g. `May 2019`). Note that the timestep is treated as an integer and 
the name is a string.

An example of the file is:

| timestep | name       |
|----------|------------|
| 0        | March 2019 |
| 1        | April 2019 |
| 2        | May 2019   |

Note that if a timestep does not have associated name, the index will simply be used instead for plotting and logging.

## Particle filter examples

This Python project contains a `particle_filtering_examples` module that holds small scripts that were used to help 
learn how particle filters work. The code isn't relevant for the main the solution, but could be useful for learning 
or tutorials.
 