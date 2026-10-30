import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/auth';

  private esNavegador(): boolean {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }

  login(credenciales: FormData): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, credenciales).pipe(
      tap(res => {
        if (res.access_token && this.esNavegador()) {
          localStorage.setItem('token', res.access_token);
          localStorage.setItem('usuario', JSON.stringify(res.usuario));
        }
      })
    );
  }

  logout(): void {
    if (this.esNavegador()) {
      localStorage.removeItem('token');
      localStorage.removeItem('usuario');
    }
  }

  estaAutenticado(): boolean {
    if (!this.esNavegador()) return false;
    return !!localStorage.getItem('token');
  }

  obtenerToken(): string | null {
    if (!this.esNavegador()) return null;
    return localStorage.getItem('token');
  }

  obtenerUsuario(): any {
    if (!this.esNavegador()) return null;
    const user = localStorage.getItem('usuario');
    return user ? JSON.parse(user) : null;
  }
}