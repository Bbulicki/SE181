import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import {MatDialog, MatDialogConfig } from '@angular/material/dialog';

@Component({
  selector: 'app-pawn-promotion-dialog',
  templateUrl: './pawn-promotion-dialog.component.html',
  styleUrls: ['./pawn-promotion-dialog.component.css']
})
export class PawnPromotionDialogComponent implements OnInit {

  promotionForm: FormGroup;
  promotionOptions: string[] = ['Queen', 'Rook', 'Bishop', 'Knight'];
  promotionSelection: string;

  constructor(public dialogRef: MatDialogRef<PawnPromotionDialogComponent>) { }

  ngOnInit() {
    this.promotionForm = new FormGroup({
      promotion: new FormControl('', Validators.required),
    });
  }

  closeDialog() {
    if (this.promotionForm.valid) {
      this.dialogRef.close({
        promotedPiece: this.promotionForm.value.promotion,
      });
    }
  }

}
