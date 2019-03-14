import logging

from etl.csv_reader import DelimitedSource
from logger import logger

logger.initialise_logger("timestep-names", log_level=logging.INFO)
module_logger = logging.getLogger('timestep-names')

class TimestepNames(object):

    # Name of the field in the CSV file for the timestep
    TIMESTEP_FIELD = "timestep"

    # Name of the field in the CSV file for the name of the timestep
    TIMESTEP_NAME_FIELD = "name"

    def __init__(self):
        """
        Initialise the object to hold the names of the timesteps.
        """
        self.timestep_to_name = {}

    def read_from_file(self, filepath, delimiter, encapsulator, encoding):
        """
        Read the names of the timesteps from a CSV file.

        :param filepath: Location of the timestep data in CSV format.
        :param delimiter: Delimiter used in the CSV file.
        :param encapsulator: Encapsulator used in the CSV file.
        :param encoding: Encoding used.
        """

        # Preconditions
        assert type(filepath) == str
        assert type(delimiter) == str
        assert type(encapsulator) == str
        assert type(encoding) == str

        module_logger.info("Updating the timesteps from file: %s" % filepath)

        # Open the CSV file for reading
        reader = DelimitedSource(filepath=filepath,
                                 delimiter=delimiter,
                                 encapsulator=encapsulator,
                                 encoding=encoding)

        # Walk through each row of data
        num_timesteps_processed = 0
        for line in reader.read():

            # Check the required fields are present
            assert TimestepNames.TIMESTEP_FIELD in line.keys()
            assert TimestepNames.TIMESTEP_NAME_FIELD in line.keys()

            # Extract the timestep and name
            timestep = int(line[TimestepNames.TIMESTEP_FIELD])
            name = line[TimestepNames.TIMESTEP_NAME_FIELD]

            self.timestep_to_name[timestep] = name

            num_timesteps_processed += 1

        module_logger.info("Processed %d timesteps from file" % num_timesteps_processed)
