export interface UpdateForm {
  [key: string]: number | string | boolean | JSON | UpdateForm;
}
export interface BasePaginationResult {
  count: number;
  next: string | null;
  previous: string | null;
}
// 过滤器单个按钮
export interface FilterItem {
  name: string; // 显示内容
  param: string; // 搜索参数
  active?: boolean; // 是否高亮显示
}

// 过滤器数组
export interface Filter {
  title: string; // 组标题
  param: string; // 组参数
  filters: FilterItem[]; // 子按钮列表
}
// 轮播图
export interface Banner {
  img_url: string; // 图片URL
  link_url: string; // 落地页跳转URL
}
// 推荐列表类型
export enum RecommendType {
  JOB = 'job', // 职位推荐列表卡片
  COMPANY = 'company', // 公司推荐列表卡片
}
// 推荐列表
export interface RecommendList<T> {
  // 推荐数据组标题
  name: RecommendType;
  // 推荐数据列表
  data_list: T[];
}