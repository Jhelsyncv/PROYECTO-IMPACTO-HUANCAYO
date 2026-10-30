import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Donacion {
  id?: number;
  item: string;
  cantidad_kg: number;
  comedor: string;
  categoria?: string;
  donante?: string;
  fecha_registro?: string;
}

@Injectable({
  providedIn: 'root'
})
export class DonacionService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/donaciones';

  private obtenerHeaders(): HttpHeaders {
    const token = typeof window !== 'undefined' && typeof localStorage !== 'undefined'
      ? localStorage.getItem('token')
      : null;

    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  obtenerDonaciones(): Observable<Donacion[]> {
    return this.http.get<Donacion[]>(this.apiUrl);
  }

  crearDonacion(donacion: Donacion): Observable<Donacion> {
    return this.http.post<Donacion>(this.apiUrl, donacion, { headers: this.obtenerHeaders() });
  }

  actualizarDonacion(id: number, donacion: Donacion): Observable<Donacion> {
    return this.http.put<Donacion>(`${this.apiUrl}/${id}`, donacion, { headers: this.obtenerHeaders() });
  }

  eliminarDonacion(id: number): Observable<{ mensaje: string }> {
    return this.http.delete<{ mensaje: string }>(`${this.apiUrl}/${id}`, { headers: this.obtenerHeaders() });
  }
}