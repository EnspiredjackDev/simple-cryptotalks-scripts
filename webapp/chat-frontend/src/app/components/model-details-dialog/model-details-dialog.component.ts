import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-model-details-dialog',
  templateUrl: './model-details-dialog.component.html',
  styleUrls: ['./model-details-dialog.component.css']
})
export class ModelDetailsDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) { }
}
