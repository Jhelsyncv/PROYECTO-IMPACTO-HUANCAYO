import { Component } from '@angular/core';
import { DonacionComponente } from './components/donacion-componente/donacion-componente';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [DonacionComponente],
  template: `<app-donacion-componente></app-donacion-componente>`
})
export class App {
  title = 'frontend';
}
