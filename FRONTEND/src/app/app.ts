import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { DonacionComponente } from './components/donacion-componente/donacion-componente';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, DonacionComponente],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  title = 'FRONTEND';
}