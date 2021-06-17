data = {0x0103: {1: 'no_compression', 2: 'CCITT',5: 'LZW', 32773: 'PackBits'},
        0x0106: {0: 'WhiteIsZero', 1: 'BlackIsZero', 2: 'RGB', 3: 'PaletteColor'},
        0x0128: {1: 'NoAbsoluteUnit', 2: 'Inch', 3: 'Centimeter'},
        0x0112: {1: 'ORIENTATION_TOPLEFT', 2: 'ORIENTATION_TOPRIGHT', 3: 'ORIENTATION_BOTRIGHT', 4: 'ORIENTATION_BOTLEFT',
                 5: 'ORIENTATION_LEFTTOP', 6: 'ORIENTATION_RIGHTTOP', 7: 'ORIENTATION_RIGHTBOT', 8: 'ORIENTATION_LEFTBOT'}

        }



requiredTagsStrips = {
        'width': 0x0100,
        'length': 0x0101,
        'bits_per_sample': 0x102,
        'compression': 0x0103,
        'photometric_interpretation': 0x0106,
        'strip_offsets': 0x0111,
        'samples_per_pixel': 0x0115,
        'rows_per_strip': 0x0116,
        'strip_byte_counts': 0x117,
        'x_resolution': 0x011A,
        'y_resolution': 0x011B,
        'resolution_unit': 0x0128}

tagsSave = {
        'width': 0x0100,
        'length': 0x0101,
        'bits_per_sample': 0x102,
        'compression': 0x0103,
        'photometric_interpretation': 0x0106,
        'strip_offsets': 0x0111,
        'samples_per_pixel': 0x0115,
        'rows_per_strip': 0x0116,
        'strip_byte_counts': 0x117,
        'x_resolution': 0x011A,
        'y_resolution': 0x011B,
        'resolution_unit': 0x0128,
        # 'planar_configuration': 0x011C
}

tagsValues = {
        'width': -99,
        'length': -99,
        'bits_per_sample': -99,
        'compression': -99,
        'photometric_interpretation': -99,
        'strip_offsets': -99,
        'samples_per_pixel': -99,
        'rows_per_strip': -99,
        'strip_byte_counts': -99,
        'x_resolution': -99,
        'y_resolution': -99,
        'resolution_unit': -99,
        # 'planar_configuration': 1,
}



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
        'y_resolution': 0x011B,
        'resolution_unit': 0x0128
}

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

exifTags = {
        'exif_IFD': 0x8769,
        'GPS_info': 0x8825,
        'interoperability_IFD': 0xA005,
}

tags = {
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
        'resolution_unit': 0x0128,
        'NewSubfileType': 0x00FE,
        'Orientation': 0x0112,
        'PlanarConfiguration': 0x011C,
        'Software': 0x0131,
        'DateTime': 0x0132,
        'ColorSpace': 0xA001,
        'PixelXDimension': 0xA002,
        'PixelYDimension': 0xA003
}




