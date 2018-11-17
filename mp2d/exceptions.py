"""
Exceptions for mp2d.
"""

class DataUnavailableError(Exception):
    """Error when dataset incomplete and otherwise valid query can't be fulfilled."""

    def __init__(self, dataset, atom):
        self.message = 'Dataset ({}) missing value for key ({})'.format(dataset, atom)
