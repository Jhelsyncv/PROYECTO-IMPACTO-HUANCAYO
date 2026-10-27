import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Donacion {
  id?: number;
  item: string;
  cantidad_kg: number;
  comedor: string;
}

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

  actualizarDonacion(id: number, donacion: Donacion): Observable<Donacion> {
    return this.http.put<Donacion>(`${this.apiUrl}/${id}`, donacion);
  }

  eliminarDonacion(id: number): Observable<{ mensaje: string }> {
    return this.http.delete<{ mensaje: string }>(`${this.apiUrl}/${id}`);
  }
}