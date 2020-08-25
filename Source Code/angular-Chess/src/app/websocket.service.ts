import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as io from 'socket.io-client';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  private url = 'http://localhost:8089'; //change this to whatever URl the backend will be on
  private socket: any;

  constructor() {
    this.socket = io(this.url);
  }

  joinRoom(roomName: string) {
    this.socket.emit('join_room', roomName);
  }
  
  leaveRoom(roomName: string) {
    this.socket.emit('leave_room', roomName)
  }
  
  restartGame(roomName: string) {
    this.socket.emit('restartGame', roomName)
  }

  applyMove(move: any, room: string) {
    // SEND MOVE TO PYTHON
    this.socket.emit('applyMove', move, room);
  }

  getUserName() {
    return Observable.create((observer) => {
      this.socket.on('getUserName', (data) => {
        if (data) {
          observer.next(data);
        } else {
          observer.error('Unable To Reach Server');
        }
      });
      //cleanup Logic
      return () => {
        this.socket.disconnect();
      };
    });
  }

  getRejectedMove() {
    return Observable.create((observer) => {
      this.socket.on('getRejectedMoveResponse', (data) => {
        if (data) {
          observer.next(data);
        } else {
          observer.error('Unable To Reach Server');
        }
      });
      //cleanup Logic
      return () => {
        this.socket.disconnect();
      };
    });
  }

  getUpdatedBoard() {
    // GET NEW BOARD
    return Observable.create((observer) => {
      this.socket.on('getUpdatedBoardResponse', (data) => {
        if (data) {
          observer.next(data);
        } else {
          observer.error('Unable To Reach Server');
        }
      });
      //cleanup Logic
      return () => {
        this.socket.disconnect();
      };
    });
  }

}
