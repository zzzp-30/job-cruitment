import type{ Company } from "./Company";
import type { Job } from "./Job";
import type { Banner, Filter, RecommendList } from "./base";

// 首页接口数据
export interface IndexResponse {
  category: Filter[];
  banner: Banner[];
  recommend_jobs: RecommendList<Job>[];
  recommend_companies: RecommendList<Company>[];
}