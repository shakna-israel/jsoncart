# jsoncart

Convert JSON to and from PNG with Python.

---

This tool can be used as a commandline program, or as a Python library.

It can encode JSON into a PNG file, with a large amount of recoverability that should survive most compression, so long as the _resolution_ remains intact. (Technically speaking, the width must remain intact.)

I have successfully decoded files converted via imagemagick like so:

> convert -quality 1 help.png testbad.png

That's a 1% original quality conversion.

---

## Example

![Example JSON file](https://git.sr.ht/~shakna/jsoncart/blob/master/test.png)

The above image is the same as [test.json](https://git.sr.ht/~shakna/jsoncart/blob/master/test.json).

---

## Library

### encode_image(data, image_name)

Take a Python `dict` and write it to `image_name`.

If `image_name` does not end in `.png`, will result in Undefined Behaviour.

### decode_image(filename)

Takes a `filename`, and if it can be read, returns a Python `dict`.

As with all Python, expect it can raise all sorts of Exceptions. (I/O, memory, ValueError, etc.)

---

## CLI

usage: jsoncart.py [-h] [-i INPUT] [-o OUTPUT]

optional arguments:

> -h, --help

show this help message and exit

> -i INPUT, --input INPUT

Input file (JSON or PNG)

> -o OUTPUT, --output OUTPUT

Output filename (Optional when decoding PNG)

---

## License

See the `LICENSE` file for the binding legal text.

CC 0 as of writing.
