# Minesweeper clone

Made in python by Johan just for fun when I should be studying...

Provide arguments like this:
- `<[--easy, --medium, --hard]>`, or
- `<rows> <cols>`, or
- `<rows> <cols> <[--easy, --medium, --hard]>`

Examples:
- `./minesweeper-johan --easy` --> Starts up a game with standard board of 20x15 with 10% bombs
- `./minesweeper-johan 20 20` --> Starts up a game with 20x20 board with 15% bombs
- `./minesweeper-johan 20 20 --hard` --> Starts up a game with 20x20 board with 20% bombs

### How to play
- Left click to flip a tile
- Right click to flag a tile
- You win if you have flipped or flagged everything and not died :)
