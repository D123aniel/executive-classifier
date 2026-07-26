import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { AboutPage } from './about-page';

describe('AboutPage', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AboutPage],
      providers: [provideRouter([])]
    }).compileComponents();
  });

  it('should render the research narrative and major sections', () => {
    const fixture = TestBed.createComponent(AboutPage);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;

    expect(compiled.querySelector('h1')?.textContent).toContain(
      'Signal through the noise'
    );
    expect(compiled.querySelector('#methodology')).toBeTruthy();
    expect(compiled.querySelector('#results')).toBeTruthy();
    expect(compiled.querySelector('#limitations')).toBeTruthy();
    expect(compiled.textContent).not.toContain('Documentation in progress');
  });

  it('should link table-of-contents entries to page sections', () => {
    const fixture = TestBed.createComponent(AboutPage);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const sectionLinks = Array.from(
      compiled.querySelectorAll<HTMLAnchorElement>('.page-nav a')
    );

    expect(sectionLinks.map((link) => link.getAttribute('href'))).toEqual([
      '#research',
      '#framework',
      '#methodology',
      '#results',
      '#limitations',
      '#deployment'
    ]);
  });

  it('should protect links that open external sites', () => {
    const fixture = TestBed.createComponent(AboutPage);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const externalLinks = Array.from(
      compiled.querySelectorAll<HTMLAnchorElement>('a[target="_blank"]')
    );

    expect(externalLinks.length).toBeGreaterThan(0);
    expect(
      externalLinks.every((link) => link.rel === 'noopener noreferrer')
    ).toBe(true);
  });
});
