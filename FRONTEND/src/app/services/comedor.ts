import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Comedor } from '../interfaces/comedor';

export type { Comedor };

@Injectable({
  providedIn: 'root'
})
export class ComedorService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/comedores';

  private obtenerHeaders(): HttpHeaders {
    const token = typeof window !== 'undefined' && typeof localStorage !== 'undefined'
      ? localStorage.getItem('token')
      : null;

    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  obtenerComedores(): Observable<Comedor[]> {
    return this.http.get<Comedor[]>(this.apiUrl);
  }

  crearComedor(comedor: Comedor): Observable<Comedor> {
    return this.http.post<Comedor>(this.apiUrl, comedor, { headers: this.obtenerHeaders() });
  }
}
