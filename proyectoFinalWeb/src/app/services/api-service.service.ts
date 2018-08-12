import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Observable } from '../../../node_modules/rxjs';

@Injectable({
  providedIn: 'root'
})

export class ApiServiceService {

  endpointangel = 'https://2j7xoa1ww9.execute-api.eu-west-1.amazonaws.com/dev/';
  endpointalberto = 'XXXXXXXX';

  constructor(private http: Http) { }

  getCelebrities(): Observable<any> {
    const url = this.endpointangel + 'celebrities';

    return this.http.get(url);
  }

  getCloudTagss(): Observable<any> {
    const url = this.endpointangel + 'cloudtags';

    return this.http.get(url);
  }

}
