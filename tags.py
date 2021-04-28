requiredTagsStrips = {
        'width': 0x0100,
        'length': 0x0101,
        'bits_per_sample': 0x102,
        'compression': 0x0103,
        'photometric_interpretation': 0x0106,
        'strip_offsets': 0x111,
        'samples_per_pixel': 0x0115,
        'rows_per_strip': 0x0116,
        'strip_byte_counts': 0x117,
        'x_resolution': 0x011A,
        'y_resolution': 0x11B,
        'resolution_unit': 0x0128}

requiredTagsTailes = {
        'width': 0x0100,
        'length': 0x0101,
        'bits_per_sample': 0x102,
        'compression': 0x0103,
        'photometric_interpretation': 0x0106,
        'tile_width': 0x0142,
        'samples_per_pixel': 0x0115,
        'tile_length': 0x0143,
        'tile_offsets': 0x0144,
        'tile_byte_counts': 0x0145,
        'x_resolution': 0x011A,
        'y_resolution': 0x11B,
        'resolution_unit': 0x0128
}

requiredValues = {'width': 0,
        'length': 0,
        'bits_per_sample': 0,
        'compression': 0,
        'photometric_interpretation': 0,
        'strip_offsets': 0,
        'samples_per_pixel': 0,
        'rows_per_strip': 0,
        'strip_byte_counts': 0,
        'x_resolution': 0,
        'y_resolution': 0,
        'resolution_unit': 0}


dataTypes = {
        'BYTE': 0x0001,
        'ASCII': 0x0002,
        'SHORT': 0x0003,
        'LONG': 0x0004,
        'RATIONAL': 0x0005,
        'SBYTE': 0x0006,
        'UNDEFINE': 0x0007,
        'SSHORT': 0x0008,
        'SLONG': 0x0009,
        'SRATIONAL': 0x000A,
        'FLOAT': 0x000B,
        'DOUBLE': 0x000C
}


moreTags = {

        }
