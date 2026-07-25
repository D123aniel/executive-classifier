import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { PredictionRequest, PredictionResponse } from './prediction.model';

@Injectable({ providedIn: 'root' })
export class ClassifierApiService {
  private readonly http = inject(HttpClient);

  predict(request: PredictionRequest): Observable<PredictionResponse> {
    return this.http.post<PredictionResponse>('/api/predict', request);
  }
}
