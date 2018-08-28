import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from '../../services/api-service.service';
import { Chart } from 'chart.js';
import { CounterCelebrities } from '../../interfaces/counter-celebrities';
import { ListCelebrities } from '../../interfaces/list-celebrities';

declare var $: any;

@Component({
  selector: 'app-celebrities',
  templateUrl: './celebrities.component.html',
  styleUrls: ['./celebrities.component.css']
})

export class CelebritiesComponent implements OnInit {
  listCelebrities: ListCelebrities[] = [];
  counterCelebritiesByDate: CounterCelebrities;
  counterCelebrities: CounterCelebrities;
  urlImagen = '';
  firstSearch = true;
  barChart: Chart;
  barChartByDate: Chart;
  celebrityName = '';

  constructor(private _apiService: ApiServiceService) { }

  ngOnInit() {
    this._apiService.getCountCelebrities().subscribe(
      resp => {
        this.counterCelebrities = resp;

        this.barChart = new Chart('barChart', {
          type: 'bar',
          data: {
            labels: ['ABC', 'El Mundo', 'Diarioes', 'El País'],
            datasets: [{
              label: '# of celebrities',
              data: [
                this.counterCelebrities.abcCounter,
                this.counterCelebrities.mundoCounter,
                this.counterCelebrities.paisCounter,
                this.counterCelebrities.diarioesCounter
              ],
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
        this.urlImagen = resp;
        this.celebrityName = name;
        (<any>$('#imageModal')).modal({ backdrop: 'static', keyboard: false });
      },
      error => {
        console.log(error);
      }
    );
  }

  searchCelebrities(date: string) {
    this._apiService.getCelebrities(date).subscribe(
      celebrities => {
        this.listCelebrities = celebrities.listCelebrities;
        this.counterCelebritiesByDate = celebrities.counterCelebrities;

        if (!this.firstSearch) {
          this.barChartByDate.destroy();
        } else {
          this.firstSearch = false;
        }

        this.barChartByDate = new Chart('barChartByDate', {
          type: 'bar',
          data: {
            labels: ['ABC', 'El Mundo', 'Diarioes', 'El País'],
            datasets: [{
              label: '# of celebrities',
              data: [
                this.counterCelebritiesByDate.abcCounter,
                this.counterCelebritiesByDate.mundoCounter,
                this.counterCelebritiesByDate.diarioesCounter,
                this.counterCelebritiesByDate.paisCounter
              ],
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
