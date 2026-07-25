import { Routes } from '@angular/router';

import { AboutPage } from './about/about-page';
import { ClassifierPage } from './classifier/classifier-page';

export const routes: Routes = [
  {
    path: '',
    component: ClassifierPage,
    title: 'Executive Evasiveness Classifier'
  },
  {
    path: 'about',
    component: AboutPage,
    title: 'About | Executive Classifier'
  },
  {
    path: '**',
    redirectTo: ''
  }
];
