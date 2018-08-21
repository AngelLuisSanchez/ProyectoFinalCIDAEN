import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from '../../services/api-service.service';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-celebrities',
  templateUrl: './celebrities.component.html',
  styleUrls: ['./celebrities.component.css']
})
export class CelebritiesComponent implements OnInit {
  celebrities = [];
  urlImagen = '';
  firstSearch = false;
  barChart = [];

  constructor(private _apiService: ApiServiceService) { }

  ngOnInit() {
    this._apiService.getCountCelebrities().subscribe(
      resp => {
        resp = resp.json();
        console.log(resp);

        this.barChart = new Chart('barChart', {
          type: 'bar',
          data: {
            labels: ['ABC', 'El Mundo', 'Diarioes', 'El País'],
            datasets: [{
              label: '# of celebrities',
              data: [resp.counts.abc, resp.counts.elmundo, resp.counts.diarioes, resp.counts.elpais],
              backgroundColor: [
                'rgba(255, 132, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            title: {
              text: 'Celebrities by Newspaper',
              display: true
            },
            scales: {
              yAxes: [{
                ticks: {
                  beginAtZero: true
                }
              }]
            }
          }
        });

      }
    );
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
