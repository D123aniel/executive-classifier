import { DecimalPipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize } from 'rxjs';

import { ClassifierApiService } from '../core/classifier-api.service';
import {
  EvasivenessLabel,
  PredictionResponse
} from '../core/prediction.model';

interface ScoreRow {
  label: EvasivenessLabel;
  score: number;
  tone: string;
}

@Component({
  selector: 'app-classifier-page',
  imports: [DecimalPipe, ReactiveFormsModule],
  templateUrl: './classifier-page.html',
  styleUrl: './classifier-page.scss'
})
export class ClassifierPage {
  private readonly formBuilder = inject(FormBuilder);
  private readonly api = inject(ClassifierApiService);

  protected readonly form = this.formBuilder.nonNullable.group({
    question: ['', [Validators.required, Validators.maxLength(12_000)]],
    response: ['', [Validators.required, Validators.maxLength(12_000)]]
  });
  protected readonly prediction = signal<PredictionResponse | null>(null);
  protected readonly loading = signal(false);
  protected readonly errorMessage = signal('');
  protected readonly scoreRows = computed<ScoreRow[]>(() => {
    const result = this.prediction();
    if (!result) {
      return [];
    }

    return [
      { label: 'Direct', score: result.scores.Direct, tone: 'direct' },
      {
        label: 'Partially Evasive',
        score: result.scores['Partially Evasive'],
        tone: 'partial'
      },
      {
        label: 'Fully Evasive',
        score: result.scores['Fully Evasive'],
        tone: 'evasive'
      }
    ];
  });

  protected analyze(): void {
    this.errorMessage.set('');
    this.prediction.set(null);
    this.form.markAllAsTouched();

    const question = this.form.controls.question.value.trim();
    const response = this.form.controls.response.value.trim();
    if (this.form.invalid || !question || !response) {
      this.errorMessage.set('Enter both an analyst question and an executive response.');
      return;
    }

    this.loading.set(true);
    this.api
      .predict({ question, response })
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (prediction) => this.prediction.set(prediction),
        error: (error: HttpErrorResponse) => {
          const isUnavailable = error.status === 0 || error.status === 503;
          this.errorMessage.set(
            isUnavailable
              ? 'The model is unavailable or still waking up. Please try again shortly.'
              : 'We could not analyze this response. Please try again.'
          );
        }
      });
  }

  protected loadExample(type: 'direct' | 'partial' | 'evasive'): void {
    const examples = {
      direct: {
        question: 'What drove the margin decline this quarter?',
        response:
          'Raw material costs increased by 12%, freight costs rose, and we recorded a one-time inventory write-down.'
      },
      partial: {
        question: 'What caused customer churn to increase this quarter?',
        response:
          'We continue to invest in customer experience and believe our long-term retention strategy remains strong.'
      },
      evasive: {
        question: 'Why did operating expenses increase significantly?',
        response:
          'Our team remains focused on innovation and delivering long-term value for shareholders.'
      }
    };

    this.form.setValue(examples[type]);
    this.prediction.set(null);
    this.errorMessage.set('');
  }

  protected reset(): void {
    this.form.reset();
    this.prediction.set(null);
    this.errorMessage.set('');
  }

  protected resultClass(label: EvasivenessLabel): string {
    if (label === 'Direct') {
      return 'direct';
    }
    if (label === 'Partially Evasive') {
      return 'partial';
    }
    return 'evasive';
  }
}
