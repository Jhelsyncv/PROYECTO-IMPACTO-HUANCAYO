import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DonacionComponente } from './donacion-componente';

describe('DonacionComponente', () => {
  let component: DonacionComponente;
  let fixture: ComponentFixture<DonacionComponente>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DonacionComponente],
    }).compileComponents();

    fixture = TestBed.createComponent(DonacionComponente);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
