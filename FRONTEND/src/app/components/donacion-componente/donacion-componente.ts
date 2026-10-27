import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DonacionService, Donacion } from '../../services/donacion';

@Component({
  selector: 'app-donaciones',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './donacion-componente.html'
})
export class DonacionComponente implements OnInit {
  private donacionService = inject(DonacionService);

  listaDonaciones: Donacion[] = [];
  nuevaDonacion: Donacion = { item: '', cantidad_kg: 0, comedor: '' };
  
  editandoId: number | null = null;
  mensaje: string | null = null;
  esError: boolean = false;

  ngOnInit(): void {
    this.cargarDonaciones();
  }

  mostrarNotificacion(texto: string, error: boolean = false): void {
    this.mensaje = texto;
    this.esError = error;
    setTimeout(() => {
      this.mensaje = null;
    }, 3000);
  }

  cargarDonaciones(): void {
    this.donacionService.obtenerDonaciones().subscribe({
      next: (data) => (this.listaDonaciones = data),
      error: () => this.mostrarNotificacion('Error al conectar con la base de datos', true)
    });
  }

  guardar(evento: Event): void {
    evento.preventDefault();

    // Validaciones
    if (!this.nuevaDonacion.item.trim() || !this.nuevaDonacion.comedor.trim()) {
      this.mostrarNotificacion('Por favor complete todos los campos de texto', true);
      return;
    }

    if (this.nuevaDonacion.cantidad_kg <= 0) {
      this.mostrarNotificacion('La cantidad en Kg debe ser mayor a 0', true);
      return;
    }

    if (this.editandoId !== null) {
      // Modo Edición
      this.donacionService.actualizarDonacion(this.editandoId, this.nuevaDonacion).subscribe({
        next: () => {
          this.mostrarNotificacion('Donación actualizada correctamente');
          this.limpiarFormulario();
          this.cargarDonaciones();
        },
        error: () => this.mostrarNotificacion('Error al actualizar la donación', true)
      });
    } else {
      // Modo Creación
      this.donacionService.crearDonacion(this.nuevaDonacion).subscribe({
        next: () => {
          this.mostrarNotificacion('Donación registrada correctamente');
          this.limpiarFormulario();
          this.cargarDonaciones();
        },
        error: () => this.mostrarNotificacion('Error al guardar la donación', true)
      });
    }
  }

  seleccionarParaEditar(donacion: Donacion): void {
    if (donacion.id !== undefined) {
      this.editandoId = donacion.id;
      this.nuevaDonacion = { ...donacion };
    }
  }

  eliminar(id?: number): void {
    if (!id) return;
    if (confirm('¿Está seguro de eliminar este registro de donación?')) {
      this.donacionService.eliminarDonacion(id).subscribe({
        next: () => {
          this.mostrarNotificacion('Donación eliminada con éxito');
          this.cargarDonaciones();
        },
        error: () => this.mostrarNotificacion('Error al eliminar el registro', true)
      });
    }
  }

  limpiarFormulario(): void {
    this.editandoId = null;
    this.nuevaDonacion = { item: '', cantidad_kg: 0, comedor: '' };
  }
}