from MetadataParser import parse_metadata


def read_metafile(metafile_path):
    parsed_metadata = parse_metadata(metafile_path)

    # Validator and object creation are combined
    Metadata(parsed_metadata)

# Parser
# Validator
# Object
