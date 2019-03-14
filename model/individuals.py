import logging

from etl.csv_reader import DelimitedSource
from logger import logger

logger.initialise_logger("individuals", log_level=logging.INFO)
module_logger = logging.getLogger('individuals')


class Individuals(object):

    # Name of the field used for an individual's unique identifier
    ID_FIELD_NAME = 'id'

    def __init__(self):
        """
        Initialise the object that holds the individuals.
        """

        # Timestep for the data
        self.timestep = None

        # Dictionary of individuals
        self.individual_to_attributes = {}

        # Set of expected attributes for each individual
        self.expected_attributes = set()

    def update_individual(self, individual):
        """
        Update an individual.

        :param individual: Representation of an individual as a dict.
        """

        # Preconditions
        assert type(individual) == dict
        assert Individuals.ID_FIELD_NAME in individual.keys()
        assert len(individual[Individuals.ID_FIELD_NAME]) > 0

        # Split the ID of the individual from its attributes
        individual_id = individual[Individuals.ID_FIELD_NAME]
        keys_without_id = set(individual.keys())
        keys_without_id.remove(Individuals.ID_FIELD_NAME)

        # If this is the first individual, then update the expected attributes, otherwise check the attributes
        if len(self.individual_to_attributes) > 0:
            module_logger.debug("Updating individual with ID: %s" % individual_id)
            assert keys_without_id == self.expected_attributes
        else:
            module_logger.info("First individual found with ID: %s" % individual_id)
            module_logger.info("Expected attributes of an individual: %s" % str(keys_without_id))
            self.expected_attributes = keys_without_id

        # Update the individual
        individual_without_id = individual.copy()
        del individual_without_id[Individuals.ID_FIELD_NAME]
        self.individual_to_attributes[individual_id] = individual_without_id

    def update_from_file(self, timestep, filepath, delimiter, encapsulator, encoding, converters={}):
        """
        Update (or add) the individuals based on data in a file.

        :param timestep: Timestep to which the data corresponds.
        :param filepath: Location of the CSV data.
        :param delimiter: Delimiter used within the file.
        :param encapsulator: Encapsulator used within the file.
        :param encoding: Encoding of the file.
        :param converters: Dict of functions (attribute name -> function) to convert the data to the required type.
        """

        # Preconditions
        assert type(timestep) == int
        assert type(filepath) == str
        assert type(delimiter) == str
        assert type(encapsulator) == str
        assert type(encoding) == str

        module_logger.info("Updating the individuals at timestep %d from file: %s" % (timestep, filepath))

        # Open the CSV file for reading
        reader = DelimitedSource(filepath=filepath,
                                 delimiter=delimiter,
                                 encapsulator=encapsulator,
                                 encoding=encoding)

        # Walk through each row of data
        num_individuals_processed = 0
        for line in reader.read():

            # The individuals data must contain a unique identifier
            assert Individuals.ID_FIELD_NAME in line

            # Apply the required conversions
            for key in converters.keys():

                # Check that the converter has the required data from the file
                assert key in line.keys()

                # Apply the conversion
                line[key] = converters[key](line[key])

            # Update the individual
            self.update_individual(line)

            num_individuals_processed += 1

        module_logger.info("Processed %d individuals" % num_individuals_processed)
