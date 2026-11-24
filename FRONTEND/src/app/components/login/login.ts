import { Component, EventEmitter, Output, OnInit, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class LoginComponent implements OnInit {
  private authService = inject(AuthService);
  private cdr = inject(ChangeDetectorRef);

  @Output() loginExitoso = new EventEmitter<void>();

  // Estado de vista: 'login' o 'registro'
  modo: 'login' | 'registro' = 'login';

  // Campos de Inicio de Sesión
  loginEmail: string = '';
  loginPassword: string = '';
  recordarme: boolean = true;
  mostrarPasswordLogin: boolean = false;

  // Manejo de errores y UX de Login
  errorLogin: boolean = false;
  intentosFallidos: number = 0;
  bloqMayusActivo: boolean = false;

  // Campos de Registro de Usuario
  registroNombre: string = '';
  registroEmail: string = '';
  registroPassword: string = '';
  registroConfirmarPassword: string = '';
  registroAceptaTerminos: boolean = true;
  mostrarPasswordRegistro: boolean = false;
  mostrarConfirmarPasswordRegistro: boolean = false;

  // Medidor de seguridad de contraseña
  fuerzaPasswordNivel: number = 0; // 0 a 3
  fuerzaPasswordTexto: string = '';

  // Estados visuales y notificaciones
  cargando: boolean = false;
  mensaje: string | null = null;
  esError: boolean = false;
  mostrarModalOlvido: boolean = false;

  // Recuperación segura de contraseña
  recuperarEmail: string = '';
  recuperacionEnviada: boolean = false;
  cargandoRecuperacion: boolean = false;
  mensajeRecuperacion: string | null = null;
  errorRecuperacion: boolean = false;

  ngOnInit(): void {
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      const emailRecordado = localStorage.getItem('alimentahuancayo_email');
      if (emailRecordado) {
        this.loginEmail = emailRecordado;
        this.recordarme = true;
      }
    }
  }

  cambiarModo(nuevoModo: 'login' | 'registro'): void {
    this.modo = nuevoModo;
    this.mensaje = null;
    this.errorLogin = false;
    this.cdr.markForCheck();
  }

  togglePasswordLogin(): void {
    this.mostrarPasswordLogin = !this.mostrarPasswordLogin;
    this.cdr.markForCheck();
  }

  togglePasswordRegistro(): void {
    this.mostrarPasswordRegistro = !this.mostrarPasswordRegistro;
    this.cdr.markForCheck();
  }

  toggleConfirmarPasswordRegistro(): void {
    this.mostrarConfirmarPasswordRegistro = !this.mostrarConfirmarPasswordRegistro;
    this.cdr.markForCheck();
  }

  mostrarAlerta(texto: string, error: boolean = false): void {
    this.mensaje = texto;
    this.esError = error;
    this.cdr.markForCheck();
  }

  cerrarAlerta(): void {
    this.mensaje = null;
    this.errorLogin = false;
    this.cdr.markForCheck();
  }

  onInputModificado(): void {
    if (this.errorLogin) {
      this.errorLogin = false;
      this.mensaje = null;
      this.cdr.markForCheck();
    }
  }

  verificarBloqMayus(event: KeyboardEvent): void {
    if (event.getModifierState) {
      this.bloqMayusActivo = event.getModifierState('CapsLock');
      this.cdr.markForCheck();
    }
  }

  evaluarFuerzaPassword(): void {
    const pass = this.registroPassword;
    if (!pass) {
      this.fuerzaPasswordNivel = 0;
      this.fuerzaPasswordTexto = '';
      return;
    }

    let nivel = 0;
    if (pass.length >= 6) nivel++;
    if (pass.length >= 8 && /[A-Z]/.test(pass) && /[0-9]/.test(pass)) nivel++;
    if (pass.length >= 10 && /[^A-Za-z0-9]/.test(pass)) nivel++;

    this.fuerzaPasswordNivel = Math.max(1, nivel);
    if (this.fuerzaPasswordNivel === 1) this.fuerzaPasswordTexto = 'Débil';
    else if (this.fuerzaPasswordNivel === 2) this.fuerzaPasswordTexto = 'Media';
    else this.fuerzaPasswordTexto = 'Fuerte';

    this.cdr.markForCheck();
  }

  iniciarSesion(evento?: Event): void {
    if (evento) evento.preventDefault();

    if (!this.loginEmail.trim() || !this.loginPassword.trim()) {
      this.errorLogin = true;
      this.mostrarAlerta('Por favor ingrese su correo electrónico y contraseña', true);
      return;
    }

    this.cargando = true;
    this.mensaje = null;
    this.errorLogin = false;
    this.cdr.markForCheck();

    const formData = new FormData();
    formData.append('username', this.loginEmail.trim());
    formData.append('password', this.loginPassword.trim());

    this.authService.login(formData).subscribe({
      next: (res) => {
        this.cargando = false;
        this.errorLogin = false;
        this.intentosFallidos = 0;

        // Guardar o borrar correo según la opción "Recordarme"
        if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
          if (this.recordarme) {
            localStorage.setItem('alimentahuancayo_email', this.loginEmail.trim());
          } else {
            localStorage.removeItem('alimentahuancayo_email');
          }
        }

        this.mostrarAlerta(`¡Bienvenido(a), ${res.usuario?.nombre || 'Usuario'}!`, false);
        this.cdr.markForCheck();

        setTimeout(() => {
          this.loginExitoso.emit();
        }, 350);
      },
      error: (err) => {
        this.cargando = false;
        this.errorLogin = true;
        this.intentosFallidos++;
        this.loginPassword = ''; // Limpiar contraseña incorrecta para permitir reingreso rápido

        if (this.intentosFallidos >= 3) {
          this.mostrarAlerta(
            `Contraseña incorrecta (${this.intentosFallidos} intentos). Si olvidaste tu acceso, usa "¿Olvidaste tu contraseña?".`,
            true
          );
        } else {
          this.mostrarAlerta(err.message || 'Correo electrónico o contraseña incorrectos. Verifique sus datos.', true);
        }

        this.cdr.markForCheck();

        // Auto-enfocar el campo de contraseña inmediatamente
        if (typeof document !== 'undefined') {
          setTimeout(() => {
            const passElem = document.getElementById('loginPassField') as HTMLInputElement;
            if (passElem) passElem.focus();
          }, 80);
        }
      }
    });
  }

  registrarUsuario(evento?: Event): void {
    if (evento) evento.preventDefault();

    if (!this.registroNombre.trim() || !this.registroEmail.trim() || !this.registroPassword.trim()) {
      this.mostrarAlerta('Por favor complete todos los campos obligatorios', true);
      return;
    }

    if (this.registroPassword.length < 6) {
      this.mostrarAlerta('La contraseña debe tener como mínimo 6 caracteres', true);
      return;
    }

    if (this.registroPassword !== this.registroConfirmarPassword) {
      this.mostrarAlerta('Las contraseñas no coinciden', true);
      return;
    }

    if (!this.registroAceptaTerminos) {
      this.mostrarAlerta('Debe aceptar los términos de la plataforma para continuar', true);
      return;
    }

    this.cargando = true;
    this.mensaje = null;
    this.cdr.markForCheck();

    const datos = {
      nombre: this.registroNombre.trim(),
      email: this.registroEmail.trim(),
      password: this.registroPassword.trim()
    };

    this.authService.registro(datos).subscribe({
      next: (res) => {
        this.cargando = false;
        this.mostrarAlerta('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión', false);
        // Pre-llenar formulario de login
        this.loginEmail = datos.email;
        this.loginPassword = '';
        this.cdr.markForCheck();

        setTimeout(() => {
          this.modo = 'login';
          this.cdr.markForCheck();
        }, 1000);
      },
      error: (err) => {
        this.cargando = false;
        this.mostrarAlerta(err.message || 'Error al registrar el usuario', true);
        this.cdr.markForCheck();
      }
    });
  }

  abrirModalOlvido(): void {
    this.mostrarModalOlvido = true;
    this.recuperacionEnviada = false;
    this.recuperarEmail = this.loginEmail || '';
    this.mensajeRecuperacion = null;
    this.errorRecuperacion = false;
    this.cdr.markForCheck();
  }

  cerrarModalOlvido(): void {
    this.mostrarModalOlvido = false;
    this.recuperacionEnviada = false;
    this.recuperarEmail = '';
    this.mensajeRecuperacion = null;
    this.errorRecuperacion = false;
    this.cdr.markForCheck();
  }

  enviarRecuperacion(evento?: Event): void {
    if (evento) evento.preventDefault();

    if (!this.recuperarEmail.trim()) {
      this.mensajeRecuperacion = 'Por favor ingrese su correo electrónico';
      this.errorRecuperacion = true;
      this.cdr.markForCheck();
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.recuperarEmail.trim())) {
      this.mensajeRecuperacion = 'Por favor ingrese un formato de correo electrónico válido';
      this.errorRecuperacion = true;
      this.cdr.markForCheck();
      return;
    }

    this.cargandoRecuperacion = true;
    this.mensajeRecuperacion = null;
    this.cdr.markForCheck();

    this.authService.recuperarPassword(this.recuperarEmail.trim()).subscribe({
      next: () => {
        this.cargandoRecuperacion = false;
        this.recuperacionEnviada = true;
        this.cdr.markForCheck();
      },
      error: () => {
        this.cargandoRecuperacion = false;
        this.recuperacionEnviada = true;
        this.cdr.markForCheck();
      }
    });
  }
}
