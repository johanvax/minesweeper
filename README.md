# Minesweeper clone

Made in python by Johan just for fun when I should be studying...

## If you download the release...

1. Navigate to where the file is located
2. Check for permissions: `ls -l | grep minesweeper-johan`. To make it work, the should be an `x` visible somewhere. If not...
3. Add permission by doing `chmod +x minesweeper-johan`.
4. Run with `./minesweeper-johan <rows> <cols>` from the terminal.

## How to play by getting the source code

```
# without command line arguments gets you a grid with dimensions 30x40
python3 main.py

# ...or you can specify row and col dim
python3 main.py <rows> <cols> # <rows> and <cols> as positive ints
```

```
# for max fun in the terminal, add this to your .bashrc or .zshrc (don't know what to do on windows)
alias minesweeper='python3 path/to/code/main.py'
```
