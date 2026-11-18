export interface Donacion {
  id?: number;
  item: string;
  cantidad_kg: number;
  comedor: string;
  categoria?: string;
  donante?: string;
  fecha_registro?: string;
}
