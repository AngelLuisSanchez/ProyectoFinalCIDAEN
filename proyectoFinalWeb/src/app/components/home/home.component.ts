import { Component } from '@angular/core';
import { ApiServiceService } from '../../services/api-service.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent {

  celebrities = [];

  constructor(private apiService: ApiServiceService) {
    this.apiService.getCelebrities().subscribe(
      resp => {
        resp = resp.json();
        console.log(resp);
        for (const celebrity of resp) {
          this.celebrities.push(celebrity);
        }
      },
      error => {
        console.log(error);
      }
    )
  }

}
