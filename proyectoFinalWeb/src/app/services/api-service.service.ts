import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Celebrities } from '../interfaces/celebrities';
import { HttpClient } from '@angular/common/http';
import { CounterCelebrities } from '../interfaces/counter-celebrities';
import { map } from 'rxjs/operators';
import { CloudTags } from '../interfaces/cloud-tags';
import { Http } from '@angular/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})

export class ApiServiceService {

  enpointgateway = environment.ENDPOINT;

  constructor(private httpClient: HttpClient) { }

  getCelebrities(date: string): Observable <Celebrities> {
    const endpoint = this.enpointgateway + 'celebrities/' + date;

    return this.httpClient.get(endpoint, {
      headers: {'x-api-key': environment.APIKEY}
    })
      .pipe(
        map((celebrities: any) => {
          return <Celebrities> celebrities.celebrities;
        })
      );
  }

  getCloudTags(): Observable<CloudTags> {
    const endpoint = this.enpointgateway + 'cloudtags';

    return this.httpClient.get(endpoint, {
      headers: {'x-api-key': environment.APIKEY}
    })
      .pipe(
        map((cloudTags: any) => {
          return <CloudTags> cloudTags.cloudTags;
        })
      );
  }

  getS3Url(key: string): Observable<string> {
    const endpoint = this.enpointgateway + 'key/' + key;

    return this.httpClient.get(endpoint, {
      headers: {'x-api-key': environment.APIKEY}
    })
      .pipe(
        map((url: any) => {
          return <string> url.url;
        })
      );
  }

  getCountCelebrities(): Observable<CounterCelebrities> {
    const endpoint = this.enpointgateway + 'countCelebrities';

    return this.httpClient.get(endpoint, {
      headers: {'x-api-key': environment.APIKEY}
    })
    .pipe(
      map((counterCelebrities: any) => {
        return <CounterCelebrities>counterCelebrities.counterCelebrities;
      })
    );
  }

}
