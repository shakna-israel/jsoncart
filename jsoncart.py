import base64
import zlib
import json
import io
import warnings

import PIL.Image
import PIL.ExifTags
import PIL.TiffImagePlugin

# TODO:
#
# Currently we're just generating a fancy barcode.
# Be nice if we could use some other more resilient recovery methods.
# Like pallette matching, and pattern establishment, etc.

def encode_image(data, image_name):
    # Encode our data
    s = json.dumps(data, sort_keys=True, separators=(',', ':'))
    d = base64.b64encode(zlib.compress(s.encode()))

    # Convert to image data
    x = []
    for i in d:
        # Pack into every channel, to be used as a checksum
        # if available when decoding.
        x.append((i, i, i))

    im = PIL.Image.new(mode = "RGB", size = (len(x), len(x)))

    TAG_DICT = dict(((v, k) for k, v in PIL.ExifTags.TAGS.items()))

    # Build some EXIF data to store our adler checksum
    ifd = PIL.TiffImagePlugin.ImageFileDirectory_v2()
    ifd[TAG_DICT["UserComment"]] = zlib.adler32(d) & 0xffffffff
    exif_out = io.BytesIO()
    ifd.save(exif_out)
    exif = b"Exif\x00\x00" + exif_out.getvalue()

    z = []
    # Record identical rows, for checksumming.
    for y in range(len(x)):
        z.extend(x)

    im.putdata(z)

    im.save(image_name, exif=exif)

def decode_image(filename):
    im = PIL.Image.open(filename, mode='r')

    # Get a checksum from EXIF data if we can (it might have been stripped)
    TAG_DICT = dict(((v, k) for k, v in PIL.ExifTags.TAGS.items()))
    exif = im._getexif()
    try:
        checksum = exif[TAG_DICT['UserComment']]
    except KeyError:
        checksum = False
    
    byte_pack = []

    for i in range(im.width):

        # Collect all copies of a byte
        bits = []
        for ix in range(im.width):
            bit = im.getpixel((i, 0))

            # Only if it passes a "checksum" append it:
            try:
                if bit[0] == bit[1]:
                    bits.append(bit[0])
                elif bit[1] == bit[2]:
                    bits.append(bit[1])
            except TypeError:
                bits.append(bit)

        if len(bits) < 1:
            # TODO
            raise RuntimeError("Image damaged beyond repair at {}/{}.".format(i, im.width))

        # Get the average agreed byte representation.
        bit = max(set(bits), key=bits.count)
        byte_pack.append(bit)

    # Convert back to data
    s = bytes(byte_pack)

    if checksum != False:
        if checksum != zlib.adler32(s) & 0xffffffff:
            # Checksum failed. Data may be corrupt.
            warnings.warn("Checksum failed. Data may be corrupt.")
    else:
        # No adler checksum found.
        warnings.warn("Checksum stripped from data. Verification is best effort.")

    d = zlib.decompress(base64.b64decode(s))
    return json.loads(d)

if __name__ == "__main__":
    import argparse
    import mimetypes

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file (JSON or PNG)")
    parser.add_argument("-o", "--output", help="Output filename (Optional when decoding PNG)")

    args = parser.parse_args()

    if 'image' in mimetypes.guess_type(args.input)[0]:
        # Decoding

        if mimetypes.guess_type(args.input)[0] != 'image/png':
            raise RuntimeError("Only supports PNG input.")

        data = decode_image(args.input)
        if args.output == None:
            # Pretty print
            print(json.dumps(data, sort_keys=True, indent=4))
        else:
            # Write a JSON file.
            with open(args.output, "w") as openFile:
                openFile.write(json.dumps(data, sort_keys=True, separators=(',', ':')))
    else:
        # Encoding
        with open(args.input) as json_file:
            data = json.load(json_file)
        
        if args.output == None:
            raise RuntimeError("Missing output file name.")

        encode_image(data, args.output)
