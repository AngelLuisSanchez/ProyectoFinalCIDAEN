import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from '../../services/api-service.service';

@Component({
  selector: 'app-celebrities',
  templateUrl: './celebrities.component.html',
  styleUrls: ['./celebrities.component.css']
})
export class CelebritiesComponent implements OnInit {
  celebrities = [];
  urlImagen = '';
  firstSearch = false;

  constructor(private _apiService: ApiServiceService) { }

  ngOnInit() {
  }

  getS3Url(key: string) {
    key = key.replace('/', '%2F');
    this._apiService.getS3Url(key).subscribe(
      resp => {
        resp = resp.json();
        console.log(resp);
        this.urlImagen = resp.url;
      },
      error => {
        console.log(error);
      }
    );
  }

  searchCelebrities(dateAux: string) {
    this.urlImagen = '';
    this._apiService.getCelebrities(dateAux).subscribe(resp => {
        resp = resp.json();
        console.log(resp.datos);
        this.celebrities = resp.datos;
        this.firstSearch = true;
      }, error => {
        console.error(error);
      });
  }

}
