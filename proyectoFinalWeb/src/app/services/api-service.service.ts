import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Observable } from '../../../node_modules/rxjs';

@Injectable({
  providedIn: 'root'
})

export class ApiServiceService {

  endpointangel = 'XXXXXXXX';
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
