import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Donacion } from '../../interfaces/donacion';
import { DonacionService } from '../../services/donacion';

@Component({
  selector: 'app-donacion-componente',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './donacion-componente.html',
  styleUrl: './donacion-componente.css'
})
export class DonacionComponente implements OnInit {
  private donacionService = inject(DonacionService);

  listaDonaciones: Donacion[] = [];
  nuevaDonacion: Donacion = {
    item: '',
    cantidad_kg: 0,
    comedor: ''
  };

  ngOnInit(): void {
    this.cargarDonaciones();
  }

  cargarDonaciones(): void {
    this.donacionService.obtenerDonaciones().subscribe({
      next: (data) => (this.listaDonaciones = data),
      error: (err) => console.error('Error al cargar donaciones', err)
    });
  }

  guardar(evento: Event): void {
    evento.preventDefault();
    if (!this.nuevaDonacion.item || !this.nuevaDonacion.comedor) return;

    this.donacionService.crearDonacion(this.nuevaDonacion).subscribe({
      next: (donacionGuardada) => {
        this.listaDonaciones.push(donacionGuardada);
        this.nuevaDonacion = { item: '', cantidad_kg: 0, comedor: '' };
      },
      error: (err) => console.error('Error al guardar', err)
    });
  }
}