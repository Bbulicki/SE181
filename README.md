# SE181
Introduction to Software Engineering and Development

Description of Course:
Introduces advanced software development fundamentals including memory management, typing and scoping,
 datastores, software testing, and security, as well as user-centric design and user experience.
  This course will be taught using a specified programming language of instruction.

Project: Chess Game
Team Members: Armaan Bhasin, Brandin Bulicki, Aparna Mishra, Tumaresi Yalikun, Briana Schuetz

------------------------------------------------------------------------------------------------------------
## Requirements:
     @angular/cli
         @angular-devkit
    
    Python v3.8.5
        socketio
            v0.2.1
        asyncio
            v3.4.3
        aiohttp
            v3.6.2
    
## Building Game:
     1. From Command line open ../SE181/Server
        Start Server:
            python GameManager.py
     2. From Command Line open ../SE181/angular-Chess
        Start Client1: (Player 1)
            ng serve --port <PORT1> --host <IPADDRESS>
            (PORT1 => Open Port on machine) (--host <IPADDRESS> => Not Required: Defaults to Localhost)
     3. From Command Line open ../SE181/angular-Chess
        Start Client2: (Player 2)
            ng serve --port <PORT2> --host <IPADDRESS>
            (PORT1 => Open Port on machine) (--host <IPADDRESS> => Not Required: Defaults to Localhost)
     4. Open Player 1:
        Navigate to <IPADDRESS>:<PORT1>
     5. Open Player 2:
        Navigate to <IPADDRESS>:<PORT2>
     6. Play Chess

------------------------------------------------------------------------------------------------------------
## Release Notes:

#### 1.0.0 Initial Version with Board Specifications
     - 1.0.1 Board Format was updated.
     - 1.0.2 Function descriptions and specifications were added.
     - 1.0.3 Move validation for each chess piece was completed.
#### 1.1.0 Event and Moves Handling
     - 1.1.1 Found attacks for a given piece.
     - 1.1.2 Check/Checkmate events are handled. 
     - 1.1.3 Moves for each chess piece were completed.
#### 1.2.0 Bug Fixes for Events
     - 1.2.1 Ensured that the king was capable of moving out of check.
     - 1.2.2 Bugs under the checkmate feature were fixed.
#### 1.3.0 Chess Board Visualization
     - 1.3.1 Functionality to Flip Board was added.
     - 1.3.2 Reformatted the chess board visualization for the back-end. 
#### 1.4.0 Bug fixes for Piece Movements
     - 1.4.1 Bishop’s movement was fixed.
     - 1.4.2 Fixed the pawn’s attack moves.
#### 1.5.0 User Interface Initialization
     - 1.5.1 Board and Chess Piece Initialization
     - 1.5.2 Initialization of Socket
#### 1.6.0 Bug fixes for Socket Communication
     - 1.6.1 Corrected Socket Message Communication Between Client and Server
     - 1.6.2 Fixed duplicate attributes for screen and player.
#### 1.7.0 Pop Up and Viewpoint Creation
     - 1.7.1 Creation of notification pop ups.
     - 1.7.2 Creation of a Second Viewpoint for each player
#### 1.8.0 Re-Design Chess Board
     - 1.8.1 Locked Player from taking opponent’s turn
     - 1.8.2 Reformatted the chess board visualization for the front-end. 	
#### 1.9.0 Bug Fixes for Pawn Promotion & Castling
     - 1.9.1 Corrected Handling of Pawn Promotion on the UI
     - 1.9.2 Fixed rook’s move when castling.
#### 2.0.0 Course Submission Version
     - 2.0.1  Added New Game Button for continuous play

------------------------------------------------------------------------------------------------------------

## Functionalities:

    - Board and Chess Piece Initialization:
        The chess game displays a chess board with 64 unique squares, 8 unique rows (with 8 squares each), and 8 unique columns with 8 squares each. Each player has 8 pawns, 2 rooks, 2 knights, 2 bishops, 1 king and 1 queen.

    - Movements of Chess Pieces:
        The game ensures that each chess piece (pawn, rook, knight, bishop, queen, king) moves according to rules of the game.

    - Castling Move:
        The game recognizes castling when the king and the rook have not moved from their starting squares, all spaces between the king and the rook are empty and the king is not in check.

    - Pawn Promotion:
        The game recognizes pawn promotion when a player’s pawn successfully reaches the 8th rank. A pawn promotion notification appears and the player can select if they would like the pawn to be promoted to a bishop, knight, rook or queen.

    - Check Recognition:
        The game recognizes when a player is in check and displays a check notification for both players.

    - Checkmate Recognition:
        The game recognizes when a player is in checkmate, checkmate notification pops up and the winner is announced.

    - Checkmate Enforcement:
        The game recognizes when a player is in checkmate, checkmate notification pops up, the winner is announced and the game ends.

------------------------------------------------------------------------------------------------------------
## Functionalities that have not been implemented for this chess game :

    - Move Timer Enforcement :
        Appearance of a time limit notification and the passing of current turn to the opponent.

    - En Passant:
        Recognition of En Passant where the player captures an enemy pawn that makes a move of two squares from its starting square.

    - Stalemate Enforcement:
        Appearance of a draw notification for both players with an option to end the game.

    - Insufficient Material Enforcement:
        Appearance of an insufficient material notification for both players and an option to end the game.

    - 50 Move Rule Enforcement:
        Recognition of  the 50 move rule where no pawn has moved or no capture has occurred for the last 50 moves ; appearance of a draw notification. 

    - Threefold Repetition Enforcement:
        Recognition of the threefold repetition where the player continues to repeat the same move as other moves puts them at a disadvantage; appearance of a draw notification. 

------------------------------------------------------------------------------------------------------------
## Known Bugs:	
    Removing Player from Server Not Properly Implemented
        Severity Level: 3
        Reasoning: If a player breaks their connection to the server, the server must be restarted before another match can begin
    Spectator (Third Connection) Does Not Show Game
        Severity Level: 1
        Reasoning: The game of chess does not require spectators.
