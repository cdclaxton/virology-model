import logging

from etl.csv_reader import DelimitedSource
from logger import logger

logger.initialise_logger("infections", log_level=logging.INFO)
module_logger = logging.getLogger('infections')


class Infections(object):

    # Name of the field in the CSV file for the individual's ID
    INDIVIDUAL_ID_FIELD_NAME = 'individual_id'

    # Name of the field in the CSV file for whether the individual is infected
    INFECTION_STRAIN_FIELD_NAME = 'infection_strain'

    # Value for no infection
    NO_INFECTION = 'None'

    def __init__(self):
        """
        Initialise the object that holds the infections for a given timestep.
        """

        # Timestep for the data
        self.timestep = None

        # Dictionary of individual ID (key) to whether they are infected or not (value)
        self.individual_to_infection = {}

    def update_infection(self, individual_id, infection_strain):
        """
        Update the information about an individual's infection.

        :param individual_id: Unique identifier for the individual.
        :param infection_strain: Infection strain (or None if not infected).
        """

        # Preconditions
        assert infection_strain is None or type(infection_strain) == str

        # Update the individual's infection details
        self.individual_to_infection[individual_id] = infection_strain

    def update_from_file(self, timestep, filepath, delimiter, encapsulator, encoding):
        """
        Update the infection data from a CSV file.

        :param timestep: Timestep of the infection data.
        :param filepath: Location of the infection data in CSV format.
        :param delimiter: Delimiter used in the CSV file.
        :param encapsulator: Encapsulator used in the CSV file.
        :param encoding: Encoding used.
        """

        # Preconditions
        assert type(timestep) == int
        assert type(filepath) == str
        assert type(delimiter) == str
        assert type(encapsulator) == str
        assert type(encoding) == str

        module_logger.info("Updating the infections at timestep %d from file: %s" % (timestep, filepath))

        # Open the CSV file for reading
        reader = DelimitedSource(filepath=filepath,
                                 delimiter=delimiter,
                                 encapsulator=encapsulator,
                                 encoding=encoding)

        # Walk through each row of data
        num_infections_processed = 0
        for line in reader.read():

            # Ensure the data is correct
            assert Infections.INDIVIDUAL_ID_FIELD_NAME in line.keys()
            assert Infections.INFECTION_STRAIN_FIELD_NAME in line.keys()

            # Extract the parameters
            individual_id = line[Infections.INDIVIDUAL_ID_FIELD_NAME]
            strain = line[Infections.INFECTION_STRAIN_FIELD_NAME]

            if strain == Infections.NO_INFECTION:
                strain = None

            # Update the individual
            self.update_infection(individual_id, strain)

            num_infections_processed += 1

        module_logger.info("Processed %d infections from file" % num_infections_processed)
