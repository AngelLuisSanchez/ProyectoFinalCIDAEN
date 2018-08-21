import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Observable } from '../../../node_modules/rxjs';

@Injectable({
  providedIn: 'root'
})

export class ApiServiceService {

  endpointangel = 'https://i4hwmlikwl.execute-api.eu-west-1.amazonaws.com/dev/';
  endpointalberto = 'XXXXXXXX';

  constructor(private http: Http) { }

  getCelebrities(date: string): Observable<any> {
    const url = this.endpointangel + 'celebrities/' + date;

    return this.http.get(url);
  }

  getCloudTags(): Observable<any> {
    const url = this.endpointangel + 'cloudtags';

    return this.http.get(url);
  }

  getS3Url(key: string): Observable<any> {
    const url = this.endpointangel + 'key/' + key;

    return this.http.get(url);
  }

  getCountCelebrities(): Observable<any> {
    const url = this.endpointangel + 'countCelebrities'

    return this.http.get(url);
  }

}
