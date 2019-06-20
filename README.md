# Mazegen

[![asciicast](https://asciinema.org/a/wQEqxN04mFwe53rbOKi0rVBjt.svg)](https://asciinema.org/a/wQEqxN04mFwe53rbOKi0rVBjt?autoplay=1&loop=1)

Dumb maze generator and solver, with the intent of being a little terminal toy.

# Requirements

The only requirement is Python 3 - I don't think there's anything required past Python 3.0, but
maybe stick to 3.4+.

## Recommended, but not required:

* Pipenv
* [BearLibTerminal](http://foo.wyrd.name/en:bearlibterminal) for display

# Setup

Clone and `cd`:

```bash
git clone https://github.com/alekratz/mazegen
cd mazegen
```

Optionally install support for bearlibterminal using Pipenv:

```bash
pipenv install
```

# Usage

Basic usage from the root project directory:

`python3 -m mazegen MAZE_WIDTH MAZE_HEIGHT OPTIONS...`

where the width and height are the size of the maze in characters/cells.

For a listing of command line options, run `python3 -m mazegen --help`.

## Examples

Solve exactly one maze and exit:

`python3 -m mazegen 10 10 --cycles 1`

Solve a bigger maze:

`python3 -m mazegen 30 30`

Run using Curses as the display method:

`python3 -m mazegen 10 10 --display curses`

Run with a faster step speed:

`python3 -m mazegen 10 10 --step 0.05`


# Wishlist and TODO

* Support for BearLibTerminal settings (font, window title, etc)
* Smoother animation... somehow?
* Center the Curses window in the terminal
    * Also handle terminal resize if possible
* More display methods?
* Track the path the solver dude follows in the display
