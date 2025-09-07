export interface BasePaginationResult {
  count: number;
  next: string | null;
  previous: string | null;
}

export interface UpdateForm {
  [key: string]: number | string | boolean | JSON;
}