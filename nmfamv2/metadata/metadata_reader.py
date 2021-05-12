from .metadata_parser import parse_metadata
from nmfamv2.metadata import Metadata


def read_metafile(metafile_path):
    parsed_metadata = parse_metadata(metafile_path)

    # Validator and object creation are combined
    Metadata(parsed_metadata)

# Parser
# Validator
# Object
