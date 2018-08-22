import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from '../../services/api-service.service';
import { Chart } from 'chart.js';

declare var $: any;

@Component({
  selector: 'app-celebrities',
  templateUrl: './celebrities.component.html',
  styleUrls: ['./celebrities.component.css']
})

export class CelebritiesComponent implements OnInit {
  celebrities = [];
  urlImagen = '';
  firstSearch = true;
  barChart = [];
  barChartByDate = [];
  celebrityName = '';

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
              text: 'Celebrities by Newspaper (All)',
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

  getS3Url(key: string, name: string) {
    key = key.replace('/', '%2F');
    this._apiService.getS3Url(key).subscribe(
      resp => {
        resp = resp.json();
        console.log(resp);
        this.urlImagen = resp.url;
        this.celebrityName = name;
        (<any>$('#imageModal')).modal({ backdrop: 'static', keyboard: false });
      },
      error => {
        console.log(error);
      }
    );
  }

  searchCelebrities(date: string) {
    this.urlImagen = '';
    this._apiService.getCelebrities(date).subscribe(resp => {
        resp = resp.json();
        console.log(resp.obj);
        this.celebrities = resp.obj.celebrities;
        this.firstSearch = false;

        const countsByDate = resp.obj.countsByDate;

        this.barChartByDate = new Chart('barChartByDate', {
          type: 'bar',
          data: {
            labels: ['ABC', 'El Mundo', 'Diarioes', 'El País'],
            datasets: [{
              label: '# of celebrities',
              data: [countsByDate.abc, countsByDate.elmundo, countsByDate.diarioes, countsByDate.elpais],
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
              text: `Celebrities by Newspaper (${date})`,
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
      }, error => {
        console.error(error);
      });
  }
}
