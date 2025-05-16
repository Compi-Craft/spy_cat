export interface Cat {
    id: number;
    name: string;
    years_experience: number;
    breed: string;
    salary: number;
  }
  
export interface NewCat {
  name: string;
  years_experience: number | '';
  breed: string;
  salary: number | '';
}

  