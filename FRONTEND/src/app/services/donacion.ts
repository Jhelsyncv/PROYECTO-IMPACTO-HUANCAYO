import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Donacion } from '../interfaces/donacion';

@Injectable({
  providedIn: 'root'
})
export class DonacionService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/donaciones';

  obtenerDonaciones(): Observable<Donacion[]> {
    return this.http.get<Donacion[]>(this.apiUrl);
  }

  crearDonacion(donacion: Donacion): Observable<Donacion> {
    return this.http.post<Donacion>(this.apiUrl, donacion);
  }
}