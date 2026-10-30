import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DonacionService, Donacion } from '../../services/donacion';
import { AuthService } from '../../services/auth';

declare var XLSX: any;
declare var jspdf: any;
declare var Chart: any;

@Component({
  selector: 'app-donaciones',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './donacion-componente.html'
})
export class DonacionComponente implements OnInit {
  private donacionService = inject(DonacionService);
  private authService = inject(AuthService);

  // Variables de Autenticación
  loginEmail = '';
  loginPassword = '';

  // Lista y Formulario de Donaciones
  listaDonaciones: Donacion[] = [];
  categorias: string[] = ['Granos y Cereales', 'Lácteos', 'Cárnicos', 'Verduras y Frutas', 'Abarrotes', 'Otros'];
  
  nuevaDonacion: Donacion = { 
    item: '', 
    cantidad_kg: 0, 
    comedor: '', 
    categoria: 'Granos y Cereales', 
    donante: '' 
  };
  
  // Filtros y Estados
  busqueda: string = '';
  fechaInicio: string = '';
  fechaFin: string = '';
  cargando: boolean = false;
  
  // Paginación
  paginaActual: number = 1;
  elementosPorPagina: number = 5;

  editandoId: number | null = null;
  mensaje: string | null = null;
  esError: boolean = false;
  idParaEliminar: number | null = null;

  chartCategoriasInstance: any;
  chartComedoresInstance: any;

  ngOnInit(): void {
    this.cargarDonaciones();
  }

  // --- MÉTODOS DE AUTENTICACIÓN ---
  get usuarioActual() {
    return this.authService.obtenerUsuario();
  }

  estaAutenticado(): boolean {
    return this.authService.estaAutenticado();
  }

  iniciarSesion(evento: Event): void {
    evento.preventDefault();
    const formData = new FormData();
    formData.append('username', this.loginEmail);
    formData.append('password', this.loginPassword);

    this.authService.login(formData).subscribe({
      next: () => {
        this.mostrarNotificacion('Sesión iniciada con éxito');
        this.loginEmail = '';
        this.loginPassword = '';
      },
      error: () => this.mostrarNotificacion('Correo o contraseña incorrectos', true)
    });
  }

  cerrarSesion(): void {
    this.authService.logout();
    this.mostrarNotificacion('Sesión cerrada correctamente');
  }

  // --- MÉTODOS DE NEGOCIO ---
  get donacionesFiltradas(): Donacion[] {
    return this.listaDonaciones.filter(d => {
      const termino = this.busqueda.toLowerCase().trim();
      const coincideTexto = !termino || 
        d.item.toLowerCase().includes(termino) || 
        d.comedor.toLowerCase().includes(termino) ||
        (d.categoria && d.categoria.toLowerCase().includes(termino)) ||
        (d.donante && d.donante.toLowerCase().includes(termino));

      let coincideFecha = true;
      if (d.fecha_registro) {
        const fechaReg = new Date(d.fecha_registro).setHours(0,0,0,0);
        if (this.fechaInicio) {
          const inicio = new Date(this.fechaInicio).setHours(0,0,0,0);
          coincideFecha = coincideFecha && (fechaReg >= inicio);
        }
        if (this.fechaFin) {
          const fin = new Date(this.fechaFin).setHours(23,59,59,999);
          coincideFecha = coincideFecha && (fechaReg <= fin);
        }
      }

      return coincideTexto && coincideFecha;
    });
  }

  get donacionesPaginadas(): Donacion[] {
    const inicio = (this.paginaActual - 1) * this.elementosPorPagina;
    return this.donacionesFiltradas.slice(inicio, inicio + this.elementosPorPagina);
  }

  get totalPaginas(): number {
    return Math.ceil(this.donacionesFiltradas.length / this.elementosPorPagina) || 1;
  }

  get totalKg(): number {
    return this.listaDonaciones.reduce((acc, curr) => acc + (Number(curr.cantidad_kg) || 0), 0);
  }

  cambiarPagina(nuevaPagina: number): void {
    if (nuevaPagina >= 1 && nuevaPagina <= this.totalPaginas) {
      this.paginaActual = nuevaPagina;
    }
  }

  limpiarFiltros(): void {
    this.busqueda = '';
    this.fechaInicio = '';
    this.fechaFin = '';
    this.paginaActual = 1;
  }

  mostrarNotificacion(texto: string, error: boolean = false): void {
    this.mensaje = texto;
    this.esError = error;
    setTimeout(() => {
      this.mensaje = null;
    }, 3500);
  }

  cargarDonaciones(): void {
    this.cargando = true;
    this.donacionService.obtenerDonaciones().subscribe({
      next: (data) => {
        this.listaDonaciones = data;
        this.cargando = false;
        setTimeout(() => this.actualizarGraficos(), 100);
      },
      error: () => {
        this.cargando = false;
        this.mostrarNotificacion('Error al conectar con la base de datos', true);
      }
    });
  }

  actualizarGraficos(): void {
    if (typeof window === 'undefined' || typeof document === 'undefined') return;

    const resumenCategoria: { [key: string]: number } = {};
    this.listaDonaciones.forEach(d => {
      const cat = d.categoria || 'Otros';
      resumenCategoria[cat] = (resumenCategoria[cat] || 0) + Number(d.cantidad_kg);
    });

    const resumenComedor: { [key: string]: number } = {};
    this.listaDonaciones.forEach(d => {
      const com = d.comedor || 'Sin Comedor';
      resumenComedor[com] = (resumenComedor[com] || 0) + Number(d.cantidad_kg);
    });

    const ctxCat = document.getElementById('chartCategorias') as HTMLCanvasElement;
    if (ctxCat) {
      if (this.chartCategoriasInstance) this.chartCategoriasInstance.destroy();
      this.chartCategoriasInstance = new Chart(ctxCat, {
        type: 'bar',
        data: {
          labels: Object.keys(resumenCategoria),
          datasets: [{
            label: 'Kilogramos (Kg)',
            data: Object.values(resumenCategoria),
            backgroundColor: 'rgba(13, 110, 253, 0.7)',
            borderColor: 'rgb(13, 110, 253)',
            borderWidth: 1
          }]
        },
        options: { responsive: true, plugins: { legend: { display: false } } }
      });
    }

    const ctxCom = document.getElementById('chartComedores') as HTMLCanvasElement;
    if (ctxCom) {
      if (this.chartComedoresInstance) this.chartComedoresInstance.destroy();
      this.chartComedoresInstance = new Chart(ctxCom, {
        type: 'doughnut',
        data: {
          labels: Object.keys(resumenComedor),
          datasets: [{
            data: Object.values(resumenComedor),
            backgroundColor: ['#0d6efd', '#20c997', '#ffc107', '#dc3545', '#6f42c1', '#fd7e14']
          }]
        },
        options: { responsive: true }
      });
    }
  }

  guardar(evento: Event): void {
    evento.preventDefault();

    if (!this.nuevaDonacion.item.trim() || !this.nuevaDonacion.comedor.trim()) {
      this.mostrarNotificacion('Por favor complete el alimento y el comedor', true);
      return;
    }

    if (this.nuevaDonacion.cantidad_kg <= 0) {
      this.mostrarNotificacion('La cantidad en Kg debe ser mayor a 0', true);
      return;
    }

    if (this.editandoId !== null) {
      this.donacionService.actualizarDonacion(this.editandoId, this.nuevaDonacion).subscribe({
        next: () => {
          this.mostrarNotificacion('Donación actualizada correctamente');
          this.limpiarFormulario();
          this.cargarDonaciones();
        },
        error: () => this.mostrarNotificacion('Error al actualizar la donación. Requiere iniciar sesión.', true)
      });
    } else {
      this.donacionService.crearDonacion(this.nuevaDonacion).subscribe({
        next: () => {
          this.mostrarNotificacion('Donación registrada con éxito');
          this.limpiarFormulario();
          this.cargarDonaciones();
        },
        error: () => this.mostrarNotificacion('Error al guardar la donación. Requiere iniciar sesión.', true)
      });
    }
  }

  seleccionarParaEditar(donacion: Donacion): void {
    if (donacion.id !== undefined) {
      this.editandoId = donacion.id;
      this.nuevaDonacion = { ...donacion };
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  prepararEliminar(id?: number): void {
    if (id) this.idParaEliminar = id;
  }

  confirmarEliminacion(): void {
    if (!this.idParaEliminar) return;
    this.donacionService.eliminarDonacion(this.idParaEliminar).subscribe({
      next: () => {
        this.mostrarNotificacion('Registro eliminado con éxito');
        this.idParaEliminar = null;
        this.cargarDonaciones();
      },
      error: () => this.mostrarNotificacion('Error al eliminar el registro. Requiere iniciar sesión.', true)
    });
  }

  limpiarFormulario(): void {
    this.editandoId = null;
    this.nuevaDonacion = { 
      item: '', 
      cantidad_kg: 0, 
      comedor: '', 
      categoria: 'Granos y Cereales', 
      donante: '' 
    };
  }

  exportarExcel(): void {
    const datosExcel = this.donacionesFiltradas.map((d, index) => ({
      '#': index + 1,
      'Artículo / Alimento': d.item,
      'Categoría': d.categoria || 'Otros',
      'Cantidad (Kg)': d.cantidad_kg,
      'Comedor Destino': d.comedor,
      'Donante': d.donante || 'Anónimo',
      'Fecha': d.fecha_registro ? new Date(d.fecha_registro).toLocaleDateString('es-PE') : '-'
    }));

    const hoja = XLSX.utils.json_to_sheet(datosExcel);
    const libro = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(libro, hoja, 'Donaciones');
    XLSX.writeFile(libro, 'Reporte_Donaciones_Huancayo.xlsx');
  }

  exportarPDF(): void {
    const doc = new jspdf.jsPDF();
    doc.setFontSize(16);
    doc.text('Reporte General de Donaciones - Comedores Huancayo', 14, 20);
    doc.setFontSize(10);
    doc.text(`Fecha de emisión: ${new Date().toLocaleDateString('es-PE')}`, 14, 28);

    const filas = this.donacionesFiltradas.map((d, index) => [
      index + 1,
      d.item,
      d.categoria || 'Otros',
      `${d.cantidad_kg} kg`,
      d.comedor,
      d.donante || 'Anónimo'
    ]);

    (doc as any).autoTable({
      head: [['#', 'Artículo', 'Categoría', 'Cantidad', 'Comedor', 'Donante']],
      body: filas,
      startY: 35,
      theme: 'striped',
      headStyles: { fillColor: [13, 110, 253] }
    });

    doc.save('Reporte_Donaciones_Huancayo.pdf');
  }
}