import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModelDetailsDialogComponent } from './model-details-dialog.component';

describe('ModelDetailsDialogComponent', () => {
  let component: ModelDetailsDialogComponent;
  let fixture: ComponentFixture<ModelDetailsDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ModelDetailsDialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModelDetailsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
