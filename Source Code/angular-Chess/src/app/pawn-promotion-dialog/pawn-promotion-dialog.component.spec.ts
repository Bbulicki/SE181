import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PawnPromotionDialogComponent } from './pawn-promotion-dialog.component';

describe('PawnPromotionDialogComponent', () => {
  let component: PawnPromotionDialogComponent;
  let fixture: ComponentFixture<PawnPromotionDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PawnPromotionDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PawnPromotionDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
