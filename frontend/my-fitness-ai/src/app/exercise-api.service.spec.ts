import { TestBed } from '@angular/core/testing';

import { ExerciseApiService } from './exercise-api.service';

describe('ExerciseApiService', () => {
  let service: ExerciseApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ExerciseApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
