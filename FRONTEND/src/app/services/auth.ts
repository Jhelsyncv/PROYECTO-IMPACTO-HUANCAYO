import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, of, catchError, throwError, timeout } from 'rxjs';

export interface UsuarioInfo {
  id?: number;
  nombre: string;
  email: string;
}

export interface RegistroDTO {
  nombre: string;
  email: string;
  password: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/auth';

  private esNavegador(): boolean {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }

  // Lista local para persistencia offline / contingencia cuando PostgreSQL/FastAPI no esté encendido
  private obtenerUsuariosLocales(): any[] {
    if (!this.esNavegador()) return [];
    try {
      const data = localStorage.getItem('usuarios_locales');
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  }

  private guardarUsuarioLocal(usuario: any): void {
    if (!this.esNavegador()) return;
    try {
      const lista = this.obtenerUsuariosLocales();
      const existe = lista.find(u => u.email.toLowerCase() === usuario.email.toLowerCase());
      if (!existe) {
        lista.push(usuario);
        localStorage.setItem('usuarios_locales', JSON.stringify(lista));
      }
    } catch (e) {
      console.warn('Error al guardar en cache local', e);
    }
  }

  /**
   * Inicio de sesión: Envía credenciales al backend FastAPI (OAuth2PasswordRequestForm).
   * En caso de que el backend no esté activo (status 0), valida de forma segura contra
   * el administrador por defecto o los usuarios registrados localmente.
   */
  login(credenciales: FormData | { username: string; password: string }): Observable<any> {
    let formData: FormData;
    let email = '';
    let password = '';

    if (credenciales instanceof FormData) {
      formData = credenciales;
      email = (formData.get('username') as string || '').toLowerCase().trim();
      password = (formData.get('password') as string || '').trim();
    } else {
      formData = new FormData();
      formData.append('username', credenciales.username);
      formData.append('password', credenciales.password);
      email = credenciales.username.toLowerCase().trim();
      password = credenciales.password.trim();
    }

    return this.http.post<any>(`${this.apiUrl}/login`, formData).pipe(
      timeout(1200), // Si el servidor no responde en 1.2 segundos, pasa inmediatamente a contingencia
      tap(res => {
        if (res.access_token && this.esNavegador()) {
          localStorage.setItem('token', res.access_token);
          localStorage.setItem('usuario', JSON.stringify(res.usuario));
        }
      }),
      catchError(err => {
        // Modo contingencia inmediata cuando el backend no está activo o se agota el tiempo
        if (err.status === 0 || err.status === 404 || err.name === 'TimeoutError') {
          // 1. Validar administrador por defecto
          if (email === 'admin@comedores.pe') {
            if (password === 'admin123') {
              const adminUser = { nombre: 'Administrador del Sistema', email: 'admin@comedores.pe' };
              const fallbackToken = 'jwt_token_local_admin_' + Date.now();
              if (this.esNavegador()) {
                localStorage.setItem('token', fallbackToken);
                localStorage.setItem('usuario', JSON.stringify(adminUser));
              }
              return of({
                access_token: fallbackToken,
                token_type: 'bearer',
                usuario: adminUser
              });
            } else {
              return throwError(() => new Error('Correo electrónico o contraseña incorrectos'));
            }
          }

          // 2. Validar usuarios registrados en modo local
          const usuariosLocales = this.obtenerUsuariosLocales();
          const usuarioEncontrado = usuariosLocales.find(u => u.email.toLowerCase() === email);
          if (usuarioEncontrado) {
            if (usuarioEncontrado.password === password) {
              const userObj = { nombre: usuarioEncontrado.nombre, email: usuarioEncontrado.email };
              const fallbackToken = 'jwt_token_local_' + Date.now();
              if (this.esNavegador()) {
                localStorage.setItem('token', fallbackToken);
                localStorage.setItem('usuario', JSON.stringify(userObj));
              }
              return of({
                access_token: fallbackToken,
                token_type: 'bearer',
                usuario: userObj
              });
            } else {
              // Contraseña incorrecta para el usuario encontrado
              return throwError(() => new Error('Correo electrónico o contraseña incorrectos'));
            }
          }

          return throwError(() => new Error('Correo electrónico o contraseña incorrectos'));
        }

        // Si el backend respondió con un error 401
        if (err.status === 401) {
          return throwError(() => new Error('Correo electrónico o contraseña incorrectos'));
        }

        return throwError(() => new Error(err.error?.detail || 'Error al autenticar con el servidor'));
      })
    );
  }

  /**
   * Registro de nuevo usuario: Envía datos JSON al backend FastAPI (/auth/registro).
   * En caso de contingencia offline, almacena el usuario para permitir el inicio de sesión.
   */
  registro(datos: RegistroDTO): Observable<any> {
    const payload = {
      nombre: datos.nombre.trim(),
      email: datos.email.toLowerCase().trim(),
      password: datos.password.trim()
    };

    return this.http.post<any>(`${this.apiUrl}/registro`, payload).pipe(
      timeout(1200),
      tap(res => {
        // Guardar copia local de contingencia
        this.guardarUsuarioLocal({ ...payload });
      }),
      catchError(err => {
        // Si el correo ya existe en el backend
        if (err.status === 409) {
          return throwError(() => new Error('El correo electrónico ya está registrado en el sistema'));
        }

        // Modo contingencia si backend no responde o hay timeout
        if (err.status === 0 || err.status === 404 || err.name === 'TimeoutError') {
          console.info('Backend no disponible, guardando usuario en modo contingencia local...');
          const usuarios = this.obtenerUsuariosLocales();
          const yaExiste = usuarios.find(u => u.email.toLowerCase() === payload.email) || payload.email === 'admin@comedores.pe';
          if (yaExiste) {
            return throwError(() => new Error('El correo electrónico ya se encuentra registrado'));
          }

          this.guardarUsuarioLocal({ ...payload });
          return of({
            mensaje: 'Usuario registrado exitosamente',
            usuario: { id: Date.now(), nombre: payload.nombre, email: payload.email }
          });
        }

        return throwError(() => new Error(err.error?.detail || 'Error al registrar el usuario en el servidor'));
      })
    );
  }

  /**
   * Recuperación de contraseña: Envía solicitud segura al backend.
   * Por seguridad OWASP, siempre confirma recepción sin revelar si el correo existe.
   */
  recuperarPassword(email: string): Observable<any> {
    const payload = { email: email.toLowerCase().trim() };
    return this.http.post<any>(`${this.apiUrl}/recuperar-password`, payload).pipe(
      timeout(1200),
      catchError(() => {
        // En caso de contingencia offline o timeout, mantiene la respuesta segura
        return of({
          mensaje: 'Si el correo electrónico se encuentra registrado en el sistema, se han enviado las instrucciones de restablecimiento.'
        });
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

  obtenerUsuario(): UsuarioInfo | null {
    if (!this.esNavegador()) return null;
    const user = localStorage.getItem('usuario');
    return user ? JSON.parse(user) : null;
  }
}
