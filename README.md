# jsoncart

Convert JSON to and from PNG with Python.

---

This tool can be used as a commandline program, or as a Python library.

It can encode JSON into a PNG file, with a large amount of recoverability that should survive most compression, so long as the _resolution_ remains intact.

I have successfully decoded files converted via imagemagick like so:

> convert -quality 1 help.png testbad.png

That's a 1% original quality conversion.

---

## Library

TODO

---

## CLI

TODO

---

## License

See the `LICENSE` file for the binding legal text.

CC 0 as of writing.
