import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { DonacionComponente } from './components/donacion-componente/donacion-componente';
import { LoginComponent } from './components/login/login';
import { AuthService } from './services/auth';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, DonacionComponente, LoginComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  title = 'AlimentaHuancayo';
  private authService = inject(AuthService);

  get estaAutenticado(): boolean {
    return this.authService.estaAutenticado();
  }

  onLoginExitoso(): void {
    // Al autenticarse, Angular actualiza reactivamente el flujo
  }

  onCerrarSesion(): void {
    // Al cerrar sesión, el getter estaAutenticado devuelve false y redirige al Login
  }
}