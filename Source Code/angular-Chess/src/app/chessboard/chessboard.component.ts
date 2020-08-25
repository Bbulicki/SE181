import { Component, OnInit } from '@angular/core';
import { WebsocketService } from '../websocket.service';
import { PawnPromotionDialogComponent } from '../pawn-promotion-dialog/pawn-promotion-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-chessboard',
  templateUrl: './chessboard.component.html',
  styleUrls: ['./chessboard.component.css']
})
export class ChessboardComponent implements OnInit {

  // constants
  Columns: string[] = ["A", "B", "C", "D", "E", "F", "G", "H"];
  Rows: number[] = [1, 2, 3, 4, 5, 6, 7, 8];
  gameRoom: string = "gameRoom";

  // variables
  ChessBoard: Board = new Board();
  isPieceChosen: boolean = false;
  pieceChosen: Square = null;
  isLocationChosen: boolean = false;
  locationChosen: Square = null;

  constructor(private websocketservice: WebsocketService, public promotiondialog: MatDialog, public gameoverdialog: MatDialog) { }

  ngOnInit(): void {
    this.getRejectedMove();
    this.getUpdatedBoard();
    this.getUserName();
    this.websocketservice.joinRoom(this.gameRoom);
  }

  startGame() {
    this.websocketservice.restartGame(this.gameRoom);
  }

  // SEND MOVE TO WEBSOCKET SERVICE
  async applyMove(move: Move) {
    move.promotedPiece = await this.checkForPawnPromotion(move);
    var coords = {
      "curX": move.currentPosition.coordinates[0],
      "curY": move.currentPosition.coordinates[1],
      "newX": move.newPosition.coordinates[0],
      "newY": move.newPosition.coordinates[1],
      "promotion": move.promotedPiece
    };
    this.websocketservice.applyMove(coords, this.gameRoom);

    return true;
  }

  async checkForPawnPromotion(move: Move) {
    if ((move.currentPosition.piece.toLowerCase() == 'p') && !this.ChessBoard.isWhitePlayer && (move.newPosition.coordinates[0] == 7)) {  // white pawn promotion
      // continue
    } else if ((move.currentPosition.piece.toLowerCase() == 'p') && this.ChessBoard.isWhitePlayer && (move.newPosition.coordinates[0] == 0)) {  // black pawn promotion
      // continue
    } else {
      return "none";
    }

    const dialogRef = this.promotiondialog.open(PawnPromotionDialogComponent, {
      width: '300px',
    });
    return dialogRef.afterClosed().toPromise().then(response => {
      var result = "none";
      if (response) {
        // alert("promoting pawn to " + response.promotedPiece);
        console.log(response.promotedPiece)
        result=response.promotedPiece;
      } else {
        console.error('Error! No response object recieved from PawnPromotion Dialog!');
      }
      return Promise.resolve(result);
    });
    
  }

  // GET REJECTED MOVE FROM WEBSOCKET SERVICE
  getRejectedMove() {
    this.websocketservice.getRejectedMove().subscribe(response => {
      if (response) {
        alert("Move is not valid. Please try again.");
      }
    },
    err => console.error('Observer for getting Username got an error: ' + err),
    () => console.log('Observer for getting Username got a complete notification'));
  }

  // GET OBSERVABLE TO GET NEW BOARD FROM WEBSOCKET SERVICE
  getUpdatedBoard() {
    var updatedBoard: string[][];
    var playerTurn: string;
    var player: string;
    var winner: string;
    this.websocketservice.getUpdatedBoard().subscribe(response => {
      if (response) {
        console.log(JSON.stringify(response));
        updatedBoard = response.gameBoard;
        playerTurn = response.playerTurn;
        player = response.check;
        winner = response.winner;
        
        console.log(response.winner)
        if (winner != "none") {
          // alert("GAME OVER. " + winner + " has won.");
          this.ChessBoard.endGame(winner);
        } else {
          // UPDATE BOARD & WHOSE TURN
          this.ChessBoard.updateBoard(updatedBoard, playerTurn);
        }
      }
    },
    err => console.error('Observer for getting Board got an error: ' + err),
    () => console.log('Observer for getting Board got a complete notification'));
    
  }

  // GET USERNAME FROM WEBSOCKET SERVICE 
  getUserName() {
    this.websocketservice.getUserName().subscribe(response => {
      if (response) {
        console.log("SENDING USER TO BOARD: ", response.userName, response.isWhite);
        // SETTING LOCAL USER & ISWHITE
        this.ChessBoard.setLocalUser(response.userName, response.isWhite);
      }
    },
    err => console.error('Observer for getting Username got an error: ' + err),
    () => console.log('Observer for getting Username got a complete notification'));

  }

  // GET ICONS FOR PIECE
  getIcon(piece: string) {
    var icon: string = null;
    switch(piece) { 
      case "K": { 
         icon = "assets/Chess_klt45.svg";
         break; 
      } case "k": { 
        icon = "assets/Chess_kdt45.svg";
         break; 
      } case "Q": { 
        icon = "assets/Chess_qlt45.svg";
         break; 
      } case "q": { 
        icon = "assets/Chess_qdt45.svg";
         break; 
      } case "R": { 
        icon = "assets/Chess_rlt45.svg";
         break; 
      } case "r": { 
        icon = "assets/Chess_rdt45.svg";
         break; 
      } case "B": { 
        icon = "assets/Chess_blt45.svg";
         break; 
      } case "b": { 
        icon = "assets/Chess_bdt45.svg";
         break; 
      } case "N": { 
        icon = "assets/Chess_nlt45.svg";
         break; 
      } case "n": { 
        icon = "assets/Chess_ndt45.svg";
         break; 
      } case "P": { 
        icon = "assets/Chess_plt45.svg";
         break; 
      } case "p": { 
        icon = "assets/Chess_pdt45.svg";
         break; 
      }
      default: { 
        icon = "assets/BLANK_ICON.png";
         break; 
      } 
   }
   return icon;
  }

  // MAKING A MOVE
  selectSquare(sq: Square) {
    if (!this.ChessBoard.isWhitePlayer && (this.ChessBoard.whoseTurn == "w")) {
      alert("It is not your turn. Please wait.");
      return;
    } else if (this.ChessBoard.isWhitePlayer && (this.ChessBoard.whoseTurn == "b")) {
      alert("It is not your turn. Please wait.");
      return;
    } else if (this.ChessBoard.whoseTurn == "none") {
      alert("Game over. Please start a new game.");
      return;
    }

    if (!this.isPieceChosen) {
      this.isPieceChosen = true;
      sq.isSelected = true;
      this.pieceChosen = sq;
    } else {
      sq.isSelected = true;
      this.isLocationChosen = true;
      this.locationChosen = sq;

      var newMove: Move = new Move(this.pieceChosen, this.locationChosen, "none");
      this.applyMove(newMove); // VALIDATE & ATTEMPT MOVE

      // deselecting
      this.pieceChosen.isSelected = false;
      this.isPieceChosen = false;
      this.pieceChosen = null;
      this.locationChosen.isSelected = false;
      this.isLocationChosen = false;
      this.locationChosen = null;
    }
  }

}

class Square {
  coordinates: number[] = null;
  oddSquare: boolean = true;
  piece: string = null;
  isOccupied: boolean = false;
  isSelected: boolean = false;
}

class Move {
  currentPosition: Square = null;
  newPosition: Square = null;
  promotedPiece: string;

  constructor(currpos: Square, newpos: Square, promoted: string) {
    this.currentPosition = currpos;
    this.newPosition = newpos;
    this.promotedPiece = promoted;
  }

}

class Board {
  Rows = ["1", "2", "3", "4", "5", "6", "7", "8"];
  Columns = ["a", "b", "c", "d", "e", "f", "g", "h"];
  BoardMatrix: Square[][] = EmptyBoard.createEmptyBoard(this.Rows, this.Columns);
  localUser: string;
  isWhitePlayer: boolean;
  whoseTurn: string;
  displayTurn: string;
  opposingUser: string;
  
  setLocalUser(username: string, isWhite: string) {
    this.localUser = username;
    if (isWhite == 'white') {
      this.isWhitePlayer = true;
    } else {
      this.isWhitePlayer = false;
    }
    if (username == 'Player 1') {
      this.opposingUser = 'Player 2';
    } else if (username == 'Player 2') {
      this.opposingUser = 'Player 1';
      this.BoardMatrix = EmptyBoard.createEmptyBoard(this.Rows, this.Columns);
    }
    console.log("LOCAL USER: ", this.localUser, this.isWhitePlayer);
  }

  updateBoard(newBoard: string[][], playerTurn: string) {
    this.whoseTurn = playerTurn;
    if (playerTurn == 'w') {
      this.displayTurn = "Player 1 (White)";
    } else if (playerTurn == 'b') {
      this.displayTurn = "Player 2 (Black)";
    }
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 8; j++) {
        if (newBoard[i][j] != this.BoardMatrix[i][j].piece) {
          this.BoardMatrix[i][j].piece = newBoard[i][j];
          if(newBoard[i][j] != '.') {
            this.BoardMatrix[i][j].isOccupied = true;
          }
        }
      }
    }
  }

  endGame(winner: string) {
    alert("GAME OVER. " + winner + " has won.");
    this.whoseTurn = "none";
  }
  
}

class EmptyBoard {
  static createEmptyBoard(rows: string[], columns: string[]) {
    var Squares: Square[][] = new Array<Square[]>(8);
    var isOddSquare: boolean = false;
    for (let i = 0; i < 8; i++) {
      Squares[i] = new Array<Square>(8);
      for (let j = 0; j < 8; j++) {
        Squares[i][j] = {
          // coordinates: rows[i] + columns[j],
          coordinates: [i, j],
          oddSquare: isOddSquare,
          piece: '.',
          isOccupied: false,
          isSelected: false
        };
        isOddSquare = !isOddSquare;
      }
      isOddSquare = !isOddSquare;
    }
    return Squares;
  }
}