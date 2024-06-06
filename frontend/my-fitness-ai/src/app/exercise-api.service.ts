import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ExerciseApiService {
  private apiKey = '4623|B0oWv01vaf4fCpyzvGYwrHiWQI1Jh1fy60FbgBrh';
  private backendUrl = environment.backendUrl;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.apiKey}`
    });
  }

  getListOfBodyParts(): Observable<any> {
    const url = `${this.backendUrl}/api/392/exercise+database+api/309/list+of+body+parts`;
    return this.http.get<any>(url, { headers: this.getHeaders() });
  }

  getExercisesByBodyPart(bodyPart: string): Observable<any> {
    const url = `${this.backendUrl}/api/392/exercise+database+api/310/list+exercise+by+body+part`;
    const params = { bodyPart };
    return this.http.get<any>(url, { headers: this.getHeaders(), params });
  }

  getListOfTargetMuscles(): Observable<any> {
    const url = `${this.backendUrl}/api/392/exercise+database+api/311/list+of+target+muscles`;
    return this.http.get<any>(url, { headers: this.getHeaders() });
  }

  getExercisesByTargetMuscle(target: string): Observable<any> {
    const url = `${this.backendUrl}/api/392/exercise+database+api/312/list+by+target+muscle`;
    const params = { target };
    return this.http.get<any>(url, { headers: this.getHeaders(), params });
  }

  getExerciseById(id: string): Observable<any> {
    const url = `${this.backendUrl}/api/392/exercise+database+api/1004/exercise+by+id`;
    const params = { id };
    return this.http.get<any>(url, { headers: this.getHeaders(), params });
  }

  getListOfEquipment(): Observable<any> {
    const url = `${this.backendUrl}/api/392/exercise+database+api/2082/list+of+equipment`;
    return this.http.get<any>(url, { headers: this.getHeaders() });
  }

  getExercisesByEquipment(equipment: string): Observable<any> {
    const url = `${this.backendUrl}/api/392/exercise+database+api/2083/list+by+equipment`;
    const params = { equipment };
    return this.http.get<any>(url, { headers: this.getHeaders(), params });
  }

  getAiWorkoutPlanner(target: string, gender: string, weight: number, goal: string): Observable<any> {
    const url = `${this.backendUrl}/api/392/exercise+database+api/4824/ai+workout+planner`;
    const params = { target, gender, weight, goal };
    return this.http.get<any>(url, { headers: this.getHeaders(), params });
  }

  getCaloriesBurned(age: number, gender: string, weight: number, exerciseId: string, reps: number, liftedWeight?: number, minutes?: number): Observable<any> {
    const url = `${this.backendUrl}/api/392/exercise+database+api/4825/calories+burned`;
    let params = new HttpParams()
      .set('age', age.toString())
      .set('gender', gender)
      .set('weight', weight.toString())
      .set('exercise_id', exerciseId)
      .set('reps', reps.toString());

    if (liftedWeight) {
      params = params.set('lifted_weight', liftedWeight.toString());
    }

    if (minutes) {
      params = params.set('minutes', minutes.toString());
    }

    return this.http.get<any>(url, { headers: this.getHeaders(), params });
  }
}

