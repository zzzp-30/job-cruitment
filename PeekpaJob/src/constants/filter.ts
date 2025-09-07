import type { Filter } from "../types/base";

// 公司列表过滤器
export const companylistFilters: Filter[] = [
  {
    title: '公司类型',
    param: 'tag',
    filters: [
      { name: '不限', param: '' },
      { name: '电商平台', param: '电商平台' },
      { name: '短视频', param: '短视频' },
      { name: '金融业', param: '金融业' },
      { name: '区块链', param: '区块链' },
      { name: '社交平台', param: '社交平台' },
      { name: '物流平台', param: '物流平台' },
      { name: '日常生活', param: '日常生活' },
      { name: '影视', param: '影视' },
      { name: '游戏', param: '游戏' },
    ],
  },
  {
    title: '公司规模',
    param: 'size',
    filters: [
      { name: '不限', param: '' },
      { name: '10人以下', param: '10人以下' },
      { name: '10~50人', param: '10~50人' },
      { name: '50~100人', param: '50~100人' },
      { name: '100~500人', param: '100~500人' },
      { name: '500-2000人', param: '500~2000人' },
      { name: '2000~10000人', param: '2000~10000人' },
      { name: '10000人以上', param: '10000人以上' },
    ],
  },
];

// 公司列表排序过滤器
export const companylistOrder: Filter[] = [
  {
    title: '排序方式',
    param: 'order',
    filters: [
      { name: '默认排序', param: '' },
      { name: '职位数量', param: 'job' },
    ],
  },
];
// 职位列表过滤器
export const joblistFilters: Filter[] = [
  {
    title: '工作经验',
    param: 'experience',
    filters: [
      { name: '不限', param: '' },
      { name: '不需要经验', param: '不需要经验' },
      { name: '经验0-2年', param: '经验0-2年' },
      { name: '经验2-5年', param: '经验2-5年' },
      { name: '经验5-10年', param: '经验5-10年' },
      { name: '经验10年以上', param: '经验10年以上' },
    ],
  },
  {
    title: '学历要求',
    param: 'education',
    filters: [
      { name: '不限', param: '' },
      { name: '初中以下', param: '初中以下' },
      { name: '初中', param: '初中' },
      { name: '高中', param: '高中' },
      { name: '大学', param: '大学' },
      { name: '研究生', param: '研究生' },
      { name: '博士', param: '博士' },
    ],
  },
];

// 职位列表排序过滤器
export const joblistOrder: Filter[] = [
  {
    title: '排序方式',
    param: 'order',
    filters: [
      { name: '默认', param: '' },
      { name: '最新', param: 'newest' },
    ],
  },
];