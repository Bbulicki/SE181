# Filename: GameManager.py
# Description: Back-End to Chess Game Term Project
# Created: 8/17/2020
# Updated: 8/24/2020
# SE181 - Group 19

####################################################################################################################################

# Import Packages
from aiohttp import web
import socketio
import asyncio
import copy
import json

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*', logger=True, engineio_logger=True)

app = web.Application()
sio.attach(app)

# Global var to keep track of users connected to Server
connectionCount = 0
# hardcoded Game Room name, change if neccesary
# just to make sure Server knows what room to emit to when sending to both players
gameRoom = "gameRoom"
player1SID = ''
player2SID = ''

winner = 'none'
playerTurn = 'none'
gameboard = ''

# Event: Join_Room
# Description: Gets a request from client and adds client to server room
# Message: join_room
@sio.on('join_room')
async def handle_message(sid, room):
    sio.enter_room(sid, room=room)
    global player1SID
    global player2SID
    global connectionCount 
    connectionCount = connectionCount + 1
    userName = ""
    response = {
        "userName": "",
        "isWhite:": ""
    }
    if (connectionCount == 1):
        response["userName"] = "Player 1"
        response["isWhite"] = "white"
        player1SID = sid
    elif (connectionCount == 2):
        response["userName"] = "Player 2"
        response["isWhite"] = "black"
        player2SID = sid
    else:
        response["userName"] = "Spectator"
        response["isWhite"] = ""
    await sio.emit('getUserName', response, room=sid)

    # have to wait for player 2 to know who he is first before we can do a proper game
    if (connectionCount == 2):
        await createGame()

# Event: Leave_Room
# Description: Gets a request from client and removes client from server room
# Message: leave_room
@sio.on('leave_room')
def handle_message(sid, room):
    sio.leave_room(sid, room=room)
    global connectionCount 
    connectionCount = connectionCount - 1

# Event: RestartGame
# Description: Gets a request from client and creates a new game
# Message: restartGame 
@sio.on('restartGame')
async def handle_message(sid, room):
    global connectionCount 
    if (connectionCount == 2):
        await createGame()

# Event: ApplyMove
# Description: Communicates with clients to progress game and update board
# Message: applyMove 
@sio.on('applyMove')
async def handle_message(sid, moveJson, game_room):
    global gameboard
    global playerTurn
    vMove = False
    move = (moveJson) #moveJson should be in format {"curX": int, "curY": int, "newX": int, "promotion": char}
    print(move)
    curX=int(move["curX"])
    curY=int(move["curY"])
    newX=int(move["newX"])
    newY=int(move["newY"])
    print(curX, curY, newX, newY)
    # Check if Move Valid
    if (moveValidation(gameboard,curX,curY,newX,newY,playerTurn) == True):
        gameboard = makeMove(gameboard, curX, curY, newX, newY)
        vMove = True
        #Handle Castling
        if (gameboard[newX][newY][0] in ('k')):
            if curX == 0 and curY == 4 and newX == 0:
                if newY == 2:
                    #Castle Queen's Side
                    gameboard = makeMove(gameboard, 0, 0, 0, 3)
                elif newY == 6:
                    #Castle King Side
                    gameboard = makeMove(gameboard, 0, 7, 0, 5)
        elif (gameboard[newX][newY][0] in ('K')):
            if curX == 7 and curY == 4 and newX == 7:
                if newY == 2:
                    #Castle Queen's Side
                    gameboard = makeMove(gameboard, 7, 0, 7, 3)
                elif newY == 6:
                    #Castle King Side
                    gameboard = makeMove(gameboard, 7, 7, 7, 5)
    
        #Check if Pawn Promotion
        for c in range(8):
            if (gameboard[0][c] == ['P',1]):
                newPiece = move["promotion"]
                gameboard=pawnPromotion(gameboard,0,c,newPiece,'w')
        for c in range(8):
            if (gameboard[7][c] == ['p',1]):
                newPiece = move["promotion"]
                gameboard=pawnPromotion(gameboard,7,c,newPiece,'b')

        sboard = simpleBoard(gameboard, 'w')
        #data to send down to Client
        gamedata = {
            "gameBoard": sboard,
            "playerTurn": "",
            "check": "none",
            "winner": "none"
        }

        #Check for Check/CheckMate
        if playerTurn == 'w':
            if (isCheck(gameboard, 'b')):
                if (isCheckMate(gameboard, 'b')):
                    winner = 'Player 1'
                    gamedata["winner"] = winner
                else:
                    gamedata["check"] = "Player 2"
        elif playerTurn == 'b':
            if (isCheck(gameboard, 'w')):
                if (isCheckMate(gameboard, 'w')):
                    winner = 'Player 2'
                    gamedata["winner"] = winner
                else:
                    gamedata["check"] = "Player 1"

        # Change Player Turn
        if playerTurn == 'w':
            playerTurn = 'b'
        else:
            playerTurn = 'w'
        gamedata["playerTurn"] = playerTurn

        await sio.emit('getUpdatedBoardResponse', gamedata, room=gameRoom)
    else:
        await sio.emit('getRejectedMoveResponse', "Move Rejected", room=sid)

# Function: CreateGame
# Description: Begins Game with 2 Players
# Arguements:
# Return:    
async def createGame(): 
    global playerTurn
    global gameboard
    playerTurn = 'w'
    gameboard = startGame()
    sboard = simpleBoard(gameboard, 'w')
    
    #data to send down to Client
    gamedata = {
        "gameBoard": sboard,
        "playerTurn": playerTurn,
        "check": "none",
        "winner": "none"
    }
    await sio.emit('getUpdatedBoardResponse', gamedata, room=gameRoom)

# Function: StartGame
# Description: Initializes Chess Board with starting positions
# Arguements:
# Return: moves[]
def startGame():
    startingBoard=[]
    #STANDARD BOARD
    #Square Structure -> [<piece>,<Moved Yet>] (0- not moved, 1- moved, 2- no piece)
    startingBoard.append([["r",0],["n",0],["b",0],["q",0],["k",0],["b",0],["n",0],["r",0]])
    startingBoard.append([["p",0],["p",0],["p",0],["p",0],["p",0],["p",0],["p",0],["p",0]])
    for n in range(4):
       startingBoard.append([[".",2],[".",2],[".",2],[".",2],[".",2],[".",2],[".",2],[".",2]])
    startingBoard.append([["P",0],["P",0],["P",0],["P",0],["P",0],["P",0],["P",0],["P",0]])
    startingBoard.append([["R",0],["N",0],["B",0],["Q",0],["K",0],["B",0],["N",0],["R",0]])
    return(startingBoard)

# Function: FindMoves
# Description: Determines all the legal moves that can be made for a given piece (Follows Piece Movement, Does Not Attack Own Piece)
# Arguements: board, currentPosX, currentPosY
# Return: moves[]
def findMoves(board, currentPosX, currentPosY):
    moves=[]

    if (board[currentPosX][currentPosY][0]) in ('p'):
        if (board[currentPosX+1][currentPosY][0] == '.'):
            moves.append([currentPosX+1,currentPosY])
        if (board[currentPosX][currentPosY][1] == 0 and board[currentPosX+2][currentPosY][0] == '.'):   #If in Starting Position
            moves.append([currentPosX+2,currentPosY])
        if (currentPosY < 7 and board[currentPosX+1][currentPosY+1][0] != "."): #If attacking to left
            moves.append([currentPosX+1,currentPosY+1])
        if (currentPosY > 0 and board[currentPosX+1][currentPosY-1][0] != "."): #If attacking to Right
            moves.append([currentPosX+1,currentPosY-1])
    elif (board[currentPosX][currentPosY][0]) in ('P'):
        if (board[currentPosX-1][currentPosY][0] == '.'):
            moves.append([currentPosX-1,currentPosY])
        if (board[currentPosX][currentPosY][1] == 0 and board[currentPosX-2][currentPosY][0] == '.'):   #If in Starting Position
            moves.append([currentPosX-2,currentPosY])
        if (currentPosY < 7 and board[currentPosX-1][currentPosY+1][0] != "."): #If attacking to Right
            moves.append([currentPosX-1,currentPosY+1])
        if (currentPosY > 0 and board[currentPosX-1][currentPosY-1][0] != "."): #If attacking to left
            moves.append([currentPosX-1,currentPosY-1])
    elif (board[currentPosX][currentPosY][0]) in ('r', 'R'):
        #Move Along X
        i=currentPosX
        while (i < 7):
            if (board[i+1][currentPosY][0] == "."):
                moves.append([i+1,currentPosY])
                i += 1
            else:
                moves.append([i+1,currentPosY])
                break
        i=currentPosX
        while (i > 0):
            if (board[i-1][currentPosY][0] == "."):
                moves.append([i-1,currentPosY])
                i -= 1
            else:
                moves.append([i-1,currentPosY])
                break
        #Move Along Y
        i=currentPosY
        while (i < 7):
            if (board[currentPosX][i+1][0] == "."):
                moves.append([currentPosX,i+1])
                i += 1
            else:
                moves.append([currentPosX,i+1])
                break
        i=currentPosY
        while (i > 0):
            if (board[currentPosX][i-1][0] == "."):
                moves.append([currentPosX,i-1])
                i -= 1
            else:
                moves.append([currentPosX,i-1])
                break
    elif (board[currentPosX][currentPosY][0]) in ('n', 'N'):
        if ( currentPosX < 7 ):
            if ( currentPosY < 6 ):
                moves.append([currentPosX+1,currentPosY+2])
            if ( currentPosY > 1 ):
                moves.append([currentPosX+1,currentPosY-2])
        if ( currentPosX < 6 ):
            if ( currentPosY < 7 ):
                moves.append([currentPosX+2,currentPosY+1])
            if ( currentPosY > 0 ):
                moves.append([currentPosX+2,currentPosY-1])
        if ( currentPosX > 0):
            if ( currentPosY < 6 ):
                moves.append([currentPosX-1,currentPosY+2])
            if ( currentPosY > 1 ):
                moves.append([currentPosX-1,currentPosY-2])
        if ( currentPosX > 1 ):
            if ( currentPosY < 7 ):
                moves.append([currentPosX-2,currentPosY+1])
            if ( currentPosY > 0 ):
                moves.append([currentPosX-2,currentPosY-1])
    elif (board[currentPosX][currentPosY][0]) in ('b', 'B'):
        i=0
        while (0 <= currentPosX + i < 7 and 0 <= currentPosY + i < 7):
            if (board[currentPosX + i +1][currentPosY + i + 1][0] == "."):
                moves.append([currentPosX + i + 1,currentPosY + i + 1])
                i += 1
            else:
                moves.append([currentPosX + i + 1,currentPosY + i + 1])
                break
        i=0
        while (0 < currentPosX - i <= 7 and 0 <= currentPosY + i < 7):
            if (board[currentPosX - i - 1][currentPosY + i + 1][0] == "."):
                moves.append([currentPosX - i - 1,currentPosY + i + 1])
                i += 1
            else:
                moves.append([currentPosX - i - 1,currentPosY + i + 1])
                break
        i=0
        while (0 <= currentPosX + i < 7 and 0 < currentPosY - i <= 7):
            if (board[currentPosX + i + 1][currentPosY - i - 1][0] == "."):
                moves.append([currentPosX + i + 1,currentPosY - i - 1])
                i += 1
            else:
                moves.append([currentPosX + i + 1,currentPosY - i - 1])
                break
        i=0
        while (0 < currentPosX - i <= 7 and 0 < currentPosY - i <= 7):
            if (board[currentPosX - i - 1][currentPosY - i - 1][0] == "."):
                moves.append([currentPosX - i - 1,currentPosY - i - 1])
                i += 1
            else:
                moves.append([currentPosX - i - 1,currentPosY - i - 1])
                break
    elif (board[currentPosX][currentPosY][0]) in ('q', 'Q'):
        i=0
        while (0 <= currentPosX + i < 7 and 0 <= currentPosY + i < 7):
            if (board[currentPosX + i +1][currentPosY + i + 1][0] == "."):
                moves.append([currentPosX + i + 1,currentPosY + i + 1])
                i += 1
            else:
                moves.append([currentPosX + i + 1,currentPosY + i + 1])
                break
        i=0
        while (0 < currentPosX - i <= 7 and 0 <= currentPosY + i < 7):
            if (board[currentPosX - i - 1][currentPosY + i + 1][0] == "."):
                moves.append([currentPosX - i - 1,currentPosY + i + 1])
                i += 1
            else:
                moves.append([currentPosX - i - 1,currentPosY + i + 1])
                break
        i=0
        while (0 <= currentPosX + i < 7 and 0 < currentPosY - i <= 7):
            if (board[currentPosX + i + 1][currentPosY - i - 1][0] == "."):
                moves.append([currentPosX + i + 1,currentPosY - i - 1])
                i += 1
            else:
                moves.append([currentPosX + i + 1,currentPosY - i - 1])
                break
        i=0
        while (0 < currentPosX - i <= 7 and 0 < currentPosY - i <= 7):
            if (board[currentPosX - i - 1][currentPosY - i - 1][0] == "."):
                moves.append([currentPosX - i - 1,currentPosY - i - 1])
                i += 1
            else:
                moves.append([currentPosX - i - 1,currentPosY - i - 1])
                break
        #Move Forward/Backward
        i=currentPosX
        while (i < 7):
            if (board[i+1][currentPosY][0] == "."):
                moves.append([i+1,currentPosY])
                i += 1
            else:
                moves.append([i+1,currentPosY])
                break
        i=currentPosX
        while (i > 0):
            if (board[i-1][currentPosY][0] == "."):
                moves.append([i-1,currentPosY])
                i -= 1
            else:
                moves.append([i-1,currentPosY])
                break
        #Move Left/Right
        i=currentPosY
        while (i < 7):
            if (board[currentPosX][i+1][0] == "."):
                moves.append([currentPosX,i+1])
                i += 1
            else:
                moves.append([currentPosX,i+1])
                break
        i=currentPosY
        while (i > 0):
            if (board[currentPosX][i-1][0] == "."):
                moves.append([currentPosX,i-1])
                i -= 1
            else:
                moves.append([currentPosX,i-1])
                break
    elif (board[currentPosX][currentPosY][0]) in ('k', 'K'):
        if (currentPosX > 0):
            moves.append([currentPosX - 1,currentPosY])
            if (currentPosY > 0):
                moves.append([currentPosX - 1,currentPosY - 1])
            if (currentPosY < 7):
                moves.append([currentPosX - 1,currentPosY + 1])
        if (currentPosX < 7):
            moves.append([currentPosX + 1,currentPosY])
            if (currentPosY > 0):
                moves.append([currentPosX + 1,currentPosY - 1])
            if (currentPosY < 7):
                moves.append([currentPosX + 1,currentPosY + 1])
        if (currentPosY > 0):
            moves.append([currentPosX,currentPosY - 1])
        if (currentPosY < 7):
            moves.append([currentPosX ,currentPosY + 1])
        #Castling
        if (board[currentPosX][currentPosY][1] == 0):
            if(board[currentPosX][5][0] == '.' and board[currentPosX][6][0] == '.' and board[currentPosX][7][1] == 0): #add [curx,5] and [curX,6] cannot put king in check
                moves.append([currentPosX,6])
            if (board[currentPosX][3][0] == '.' and board[currentPosX][2][0] == '.' and board[currentPosX][1][0] == '.' and board[currentPosX][0][1] == 0): #add [curx,3] and [curX,2] cannot put king in check
                moves.append([currentPosX,2])
    return(moves)

# Function: FindAttacks
# Description: Determines all the legal attacks that can be made for a given piece on a board
# Arguements: board, currentPosX, currentPosY
# Return: attacks[]
def findAttacks(board, currentPosX, currentPosY):
    attacks=[]

    if (board[currentPosX][currentPosY][0]) in ('p'):
        if (currentPosY < 7 and board[currentPosX+1][currentPosY+1][0] != "."): #If attacking to left
            attacks.append([currentPosX+1,currentPosY+1])
        if (currentPosY > 0 and board[currentPosX+1][currentPosY-1][0] != "."): #If attacking to Right
            attacks.append([currentPosX+1,currentPosY-1])
    elif (board[currentPosX][currentPosY][0]) in ('P'):
        if (currentPosY < 7 and board[currentPosX-1][currentPosY+1] != "."): #If attacking to Right
            attacks.append([currentPosX-1,currentPosY+1])
        if (currentPosY > 0 and board[currentPosX-1][currentPosY-1] != "."): #If attacking to left
            attacks.append([currentPosX-1,currentPosY-1])
    elif (board[currentPosX][currentPosY][0]) in ('r', 'R'):
        #Move Along X
        i=currentPosX
        while (i < 7):
            if (board[i+1][currentPosY][0] == "."):
                attacks.append([i+1,currentPosY])
                i += 1
            else:
                attacks.append([i+1,currentPosY])
                break
        i=currentPosX
        while (i > 0):
            if (board[i-1][currentPosY][0] == "."):
                attacks.append([i-1,currentPosY])
                i -= 1
            else:
                attacks.append([i-1,currentPosY])
                break
        #Move Along Y
        i=currentPosY
        while (i < 7):
            if (board[currentPosX][i+1][0] == "."):
                attacks.append([currentPosX,i+1])
                i += 1
            else:
                attacks.append([currentPosX,i+1])
                break
        i=currentPosY
        while (i > 0):
            if (board[currentPosX][i-1][0] == "."):
                attacks.append([currentPosX,i-1])
                i -= 1
            else:
                attacks.append([currentPosX,i-1])
                break
    elif (board[currentPosX][currentPosY][0]) in ('n', 'N'):
        if ( currentPosX < 7 ):
            if ( currentPosY < 6 ):
                attacks.append([currentPosX+1,currentPosY+2])
            if ( currentPosY > 1 ):
                attacks.append([currentPosX+1,currentPosY-2])
        if ( currentPosX < 6 ):
            if ( currentPosY < 7 ):
                attacks.append([currentPosX+2,currentPosY+1])
            if ( currentPosY > 0 ):
                attacks.append([currentPosX+2,currentPosY-1])
        if ( currentPosX > 0):
            if ( currentPosY < 6 ):
                attacks.append([currentPosX-1,currentPosY+2])
            if ( currentPosY > 1 ):
                attacks.append([currentPosX-1,currentPosY-2])
        if ( currentPosX > 1 ):
            if ( currentPosY < 7 ):
                attacks.append([currentPosX-2,currentPosY+1])
            if ( currentPosY > 0 ):
                attacks.append([currentPosX-2,currentPosY-1])
    elif (board[currentPosX][currentPosY][0]) in ('b', 'B'):
        i=0
        while (0 <= currentPosX + i < 7 and 0 <= currentPosY + i < 7):
            if (board[currentPosX + i +1][currentPosY + i + 1][0] == "."):
                attacks.append([currentPosX + i + 1,currentPosY + i + 1])
                i += 1
            else:
                attacks.append([currentPosX + i + 1,currentPosY + i + 1])
                break
        i=0
        while (0 < currentPosX - i <= 7 and 0 <= currentPosY + i < 7):
            if (board[currentPosX - i - 1][currentPosY + i + 1][0] == "."):
                attacks.append([currentPosX - i - 1,currentPosY + i + 1])
                i += 1
            else:
                attacks.append([currentPosX - i - 1,currentPosY + i + 1])
                break
        i=0
        while (0 <= currentPosX + i < 7 and 0 < currentPosY - i <= 7):
            if (board[currentPosX + i + 1][currentPosY - i - 1][0] == "."):
                attacks.append([currentPosX + i + 1,currentPosY - i - 1])
                i += 1
            else:
                attacks.append([currentPosX + i + 1,currentPosY - i - 1])
                break
        i=0
        while (0 < currentPosX - i <= 7 and 0 < currentPosY - i <= 7):
            if (board[currentPosX - i - 1][currentPosY - i - 1][0] == "."):
                attacks.append([currentPosX - i - 1,currentPosY - i - 1])
                i += 1
            else:
                attacks.append([currentPosX - i - 1,currentPosY - i - 1])
                break
    elif (board[currentPosX][currentPosY][0]) in ('q', 'Q'):
        i=0
        while (0 <= currentPosX + i < 7 and 0 <= currentPosY + i < 7):
            if (board[currentPosX + i +1][currentPosY + i + 1][0] == "."):
                attacks.append([currentPosX + i + 1,currentPosY + i + 1])
                i += 1
            else:
                attacks.append([currentPosX + i + 1,currentPosY + i + 1])
                break
        i=0
        while (0 < currentPosX - i <= 7 and 0 <= currentPosY + i < 7):
            if (board[currentPosX - i - 1][currentPosY + i + 1][0] == "."):
                attacks.append([currentPosX - i - 1,currentPosY + i + 1])
                i += 1
            else:
                attacks.append([currentPosX - i - 1,currentPosY + i + 1])
                break
        i=0
        while (0 <= currentPosX + i < 7 and 0 < currentPosY - i <= 7):
            if (board[currentPosX + i + 1][currentPosY - i - 1][0] == "."):
                attacks.append([currentPosX + i + 1,currentPosY - i - 1])
                i += 1
            else:
                attacks.append([currentPosX + i + 1,currentPosY - i - 1])
                break
        i=0
        while (0 < currentPosX - i <= 7 and 0 < currentPosY - i <= 7):
            if (board[currentPosX - i - 1][currentPosY - i - 1][0] == "."):
                attacks.append([currentPosX - i - 1,currentPosY - i - 1])
                i += 1
            else:
                attacks.append([currentPosX - i - 1,currentPosY - i - 1])
                break
        #Move Forward/Backward
        i=currentPosX
        while (i < 7):
            if (board[i+1][currentPosY][0] == "."):
                attacks.append([i+1,currentPosY])
                i += 1
            else:
                attacks.append([i+1,currentPosY])
                break
        i=currentPosX
        while (i > 0):
            if (board[i-1][currentPosY][0] == "."):
                attacks.append([i-1,currentPosY])
                i -= 1
            else:
                attacks.append([i-1,currentPosY])
                break
        #Move Left/Right
        i=currentPosY
        while (i < 7):
            if (board[currentPosX][i+1][0] == "."):
                attacks.append([currentPosX,i+1])
                i += 1
            else:
                attacks.append([currentPosX,i+1])
                break
        i=currentPosY
        while (i > 0):
            if (board[currentPosX][i-1][0] == "."):
                attacks.append([currentPosX,i-1])
                i -= 1
            else:
                attacks.append([currentPosX,i-1])
                break
    elif (board[currentPosX][currentPosY][0]) in ('k', 'K'):
        if (currentPosX > 0):
            attacks.append([currentPosX - 1,currentPosY])
            if (currentPosY > 0):
                attacks.append([currentPosX - 1,currentPosY - 1])
            if (currentPosY < 7):
                attacks.append([currentPosX - 1,currentPosY + 1])
        if (currentPosX < 7):
            attacks.append([currentPosX + 1,currentPosY])
            if (currentPosY > 0):
                attacks.append([currentPosX + 1,currentPosY - 1])
            if (currentPosY < 7):
                attacks.append([currentPosX + 1,currentPosY + 1])
        if (currentPosY > 0):
            attacks.append([currentPosX,currentPosY - 1])
        if (currentPosY < 7):
            attacks.append([currentPosX ,currentPosY + 1])
    return(attacks)

# Function: FriendlyFire
# Description: Determines if an attack is being made against a player's own piece
# Arguements: board, currentPosX, currentPosY, possibleMoves
# Return: moves[]
def friendlyFire(board, currentPosX, currentPosY, possibleMoves):
    moves = []
    for n in possibleMoves:
        if (board[n[0]][n[1]][0] == '.' or board[currentPosX][currentPosY][0].isupper() != board[n[0]][n[1]][0].isupper()):
            moves.append(n)
    return (moves)

# Function: MoveValidation
# Description: Checks for Legal Move (Follows Piece Movement, Does Not Attack Own Piece)
# Arguements: board, currentPosX, currentPosY, newPositionX, newPositionY
# Return: True/False
def moveValidation(board, currentPosX, currentPosY, newPositionX,  newPositionY, player):
    #Make sure you are moving your piece
    if player == 'w':
        if board[currentPosX][currentPosY][0] in ('p','r','n','b','q','k','.'):
            return (False)

    if player == 'b':
        if board[currentPosX][currentPosY][0] in ('P','R','N','B','Q','K','.'):
            return (False)

    #Find Possible Moves/Attacks
    possibleMoves = findMoves(board, currentPosX, currentPosY)

    #Remove Attacks Against Own Pieces
    legalMoves = friendlyFire(board, currentPosX, currentPosY, possibleMoves)

    #Remove Spots that would put in check
    testCheckboard = makeMove(board, currentPosX, currentPosY, newPositionX, newPositionY)
    if (board[currentPosX][currentPosY][0].isupper()):
        if (isCheck(testCheckboard, 'w')):
            return(False)
    else:
        if (isCheck(testCheckboard, 'b')):
            return(False)

    #Checks if New Position is Valid
    for n in legalMoves:
        if (newPositionX == n[0] and newPositionY == n[1]):
            return(True) #Move Accepted
    #Move Illegal
    return(False)

# Function: MakeMove
# Description: Moves the Piece(s) From One Location on the Board to Another
# Arguements:
# Return: updateBoard
def makeMove (board, currentPosX, currentPosY, newPositionX,  newPositionY):
    updateBoard = copy.deepcopy(board)
    tmpPiece = updateBoard[currentPosX][currentPosY][0]
    updateBoard[currentPosX][currentPosY] = ['.',2]
    updateBoard[newPositionX][newPositionY] = [tmpPiece, 1]
    return(updateBoard)

# Function: IsCheck
# Description: Determine if a player is in Check
# Arguements: board, player
# Return: True/False
def isCheck(board, player):
    checkSquares=[]
    row=0
    col=0
    # Find if White in Check
    if player == 'w':
        while row < 8:
            while col < 8:
                if (board[row][col][0] in ['p','r','n','b','q']):
                    checkSquares.append(findAttacks(board, row, col ))
                col+=1
            row+=1
            col=0
        for check in checkSquares:
            for c in check:
                if (board[c[0]][c[1]][0] == 'K'):
                    return(True) #Is in Check
        return(False) #Is not in Check
    # Find if Black in Check
    if player == 'b':
        while row < 8:
            while col < 8:
                if (board[row][col][0] in ['P','R','N','B','Q']):
                    checkSquares.append(findAttacks(board, row, col))
                col+=1
            row+=1
            col=0
        for check in checkSquares:
            for c in check:
                if (board[c[0]][c[1]][0] == 'k'):
                    return(True) #Is in Check
        return(False) #Is not in Check

# Function: IsCheckMate
# Description: Determine if a player is in Checkmate given a board that has a player in check
# Arguements: board, player
# Return: True/False
def isCheckMate(board, player):
    possibleMoves = []
    legalMoves=[]
    currentBoard = copy.deepcopy(board)
    if (player == 'w'):
        # Can King move out of Check?
        row=0
        col=0
        while row < 8 and col < 8:
            if (board[row][col][0] in ['K']):
                possibleMoves = (findMoves(board, row, col ))
                legalMoves = friendlyFire(board, row, col, possibleMoves)
                break
            else:
                col+=1
            if col == 8 and row < 8:
                row+=1
                col=0
        #legalMoves = friendlyFire(board, row, col, possibleMoves)
        testBoard = copy.deepcopy(currentBoard)
        for m in legalMoves:
            testMove = makeMove(testBoard, row, col, m[0], m[1])
            if (isCheck(testMove, player)):
                testBoard = copy.deepcopy(currentBoard)
            else:
                return(False) #Is not in Checkmate
        # Can Other Piece move out of Check?
        row=0
        col=0
        possibleMoves = []
        legalMoves = []
        allies=[]
        while row < 8 and col < 8:
            if (board[row][col][0] in ['R','N','B','Q','P']):
                allies.append([row, col]) #Get location of Piece
                possibleMoves = (findMoves(board, row, col )) #Get Moves for that Piece
                legalMoves.append(friendlyFire(board, row, col, possibleMoves))
            col+=1
            if col == 8 and row < 8:
                row+=1
                col=0
        testBoard = copy.deepcopy(currentBoard)
        i = 0
        while i < len(allies):
            for m in legalMoves[i]:
                testMove = makeMove(testBoard, allies[i][0], allies[i][1], m[0], m[1])
                if (isCheck(testMove, player)):
                    testBoard = copy.deepcopy(currentBoard)
                else:
                    return(False) #Is not in Checkmate
            i+=1
         #Is in Checkmate
        return(True)

    if (player == 'b'):
        # Can King move out of Check?
        row=0
        col=0
        while row < 8 and col < 8:
            if (board[row][col][0] in ['k']):
                possibleMoves = (findMoves(board, row, col ))
                legalMoves = friendlyFire(board, row, col, possibleMoves)
                break
            else:
                col+=1
            if col == 8 and row < 8:
                row+=1
                col=0
        #legalMoves = friendlyFire(board, row, col, possibleMoves)
        testBoard = copy.deepcopy(currentBoard)
        for m in legalMoves:
            testMove = makeMove(testBoard, row, col, m[0], m[1])
            if (isCheck(testMove, player)):
                testBoard = copy.deepcopy(currentBoard)
            else:
                return(False) #Is not in Checkmate
        # Can Other Piece move out of Check?
        row=0
        col=0
        possibleMoves = []
        legalMoves = []
        allies=[]
        while row < 8 and col < 8:
            if (board[row][col][0] in ['r','n','b','q','p']):
                allies.append([row, col]) #Get location of Piece
                possibleMoves = (findMoves(board, row, col )) #Get Moves for that Piece
                legalMoves.append(friendlyFire(board, row, col, possibleMoves))
            col+=1
            if col == 8 and row < 8:
                row+=1
                col=0
        testBoard = copy.deepcopy(currentBoard)
        i = 0
        while i < len(allies):
            for m in legalMoves[i]:
                testMove = makeMove(testBoard, allies[i][0], allies[i][1], m[0], m[1])
                if (isCheck(testMove, player)):
                    testBoard = copy.deepcopy(currentBoard)
                else:
                    return(False) #Is not in Checkmate
            i+=1
         #Is in Checkmate
        return(True)

# Function: PawnPromotion
# Description: Promote Pawn When Reaching Other Side Of Board
# Arguements: board, pawnPosX, pawnPosY, newPiece
# Return: updateBoard
def pawnPromotion(board, pawnPosX, pawnPosY, newPiece, player):
    swap =''

    if (player == 'w'):
        if newPiece == "Queen":
            swap = 'Q'
        elif newPiece == "Bishop":
            swap = 'B'
        elif newPiece == "Rook":
            swap = 'R'
        elif newPiece == "Knight":
            swap = 'N'
    else:
        if newPiece == "Queen":
            swap = 'q'
        elif newPiece == "Bishop":
            swap = 'b'
        elif newPiece == "Rook":
            swap = 'r'
        elif newPiece == "Knight":
            swap = 'n'

    updateBoard = board
    updateBoard[pawnPosX][pawnPosY] = [swap,1]
    return(updateBoard)

# Function: simpleBoard
# Description: Given Board[row][column][square] simplify to Board[row][column] and print
# Arguements: board
# Return: simpleBoard
def simpleBoard(board,player):
    simpleB = []
    r = 0
    c = 0
    while r < 8:
        simpleR=[]
        while c < 8:
            if player == 'w':
                simpleR.append(board[r][c][0])
            elif player == 'b':
                simpleR.append(board[7-r][c][0])
            c+=1
        c=0
        r+=1
        simpleB.append(simpleR)

    #for row in simpleB:
    #    print(row)
    return(simpleB)

############################################################################
if __name__ == '__main__':
    web.run_app(app, port=8089)