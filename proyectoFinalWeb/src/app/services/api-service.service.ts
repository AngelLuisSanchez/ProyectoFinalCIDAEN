import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Celebrities } from '../interfaces/celebrities';
import { HttpClient } from '@angular/common/http';
import { CounterCelebrities } from '../interfaces/counter-celebrities';
import { map } from 'rxjs/operators';
import { CloudTags } from '../interfaces/cloud-tags';

@Injectable({
  providedIn: 'root'
})

export class ApiServiceService {

  endpointangel = 'XXXXXXXXXX';
  endpointalberto = 'XXXXXXXX';

  constructor(private httpClient: HttpClient) { }

  getCelebrities(date: string): Observable <Celebrities> {
    const endpoint = this.endpointangel + 'celebrities/' + date;

    return this.httpClient.get(endpoint)
      .pipe(
        map(celebrities => {
          return <Celebrities> celebrities.celebrities;
        })
      );
  }

  getCloudTags(): Observable<any> {
    const endpoint = this.endpointangel + 'cloudtags';

    return this.httpClient.get(endpoint)
      .pipe(
        map(cloudTags => {
          return <CloudTags> cloudTags.cloudTags;
        })
      );
  }

  getS3Url(key: string): Observable<string> {
    const endpoint = this.endpointangel + 'key/' + key;

    return this.httpClient.get(endpoint)
      .pipe(
        map(url => {
          return <string> url.url;
        })
      );
  }

  getCountCelebrities(): Observable<CounterCelebrities> {
    const endpoint = this.endpointangel + 'countCelebrities';

    return this.httpClient.get(endpoint)
    .pipe(
      map(counterCelebrities => {
        return <CounterCelebrities>counterCelebrities.counterCelebrities;
      })
    );
  }

}
