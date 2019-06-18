# Mazegen

Dumb maze generator with the intent of being a little terminal toy.

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

There are additionally other options for running from the terminal. To use BearLibTerm as your
display, pass `--display blt` as an option on the command line.
