# 山海漫游 · Roam Notes

国内外旅游景点图鉴 H5，基于 Vue 3 + Vite。收录六大洲 25 处目的地，提供大洲、国家、省州、城市联动分类，以及自然风光、历史古迹、人文风情主题筛选。

## 本地启动

```sh
cd roam-notes
npm install
npm run dev
```

浏览器打开终端显示的地址，默认 `http://localhost:5173/`。已有 `node_modules` 时可直接启动。已使用 Node.js 22.11.0 验证。

项目自带景点数据和本地实景照片，启动时无需重新采集，也不依赖外部图片或字体服务。

```sh
npm run check     # 校验景点、分类、署名、本地素材和搜索筛选逻辑
npm run build     # 生成 dist/
npm run preview   # 预览构建产物，默认端口 4173
```

## 功能与边界

- 搜索中英文景点名称、国家、省市及标签；按地区和主题组合筛选。
- 查看景点招牌照片、中文介绍、观察建议和资料来源。
- 收藏目的地；旅行手记支持新增、编辑、删除及 JSON 备份导入导出。
- 手机底部导航、桌面网格布局、键盘操作与系统减少动态效果偏好支持。

收藏和手记仅保存在当前浏览器的 localStorage，不会自动上传或跨设备同步。更换浏览器、域名或端口会进入独立的存储空间；清除网站数据会丢失记录，建议定期导出备份。备份采用合并导入，同 ID 手记保留已有版本。当前没有用户账号、后端接口、实时门票或开放时间。

## 数据和图片

景点文字依据 UNESCO 世界遗产中心资料进行中文整理，保留来源链接及 CC BY-SA 3.0 IGO 标识；观察建议为编辑内容。照片来自 Wikimedia Commons，逐条记录摄影者、许可及原始文件页，保存在 `public/images/`。照片使用等比显示与裁切，各自遵循详情页标注的许可。

```sh
npm run collect                    # 断点续采，跳过已保存素材
python3 scripts/collect.py --refresh # 重新采集全部素材，需要联网
```

采集需要 Python 3 和系统 curl，无需 API 密钥或第三方 Python 包。使用 curl 的系统证书验证，保留 TLS 校验。Commons 限流或网络故障可能导致采集中断；成功条目会立即保存，下次可续采。已人工核对当前照片与景点的匹配关系；刷新后仍应复核结果。

- `src/data/seed.json`：景点编辑内容与搜索词；可用 `photoFile` 固定 Commons 文件名。
- `src/data/places.json`：页面使用的数据及每张照片的署名、许可、下载地址。
- `sources/commons/`：采集时的官方 API 原始响应。
- `sources/unesco-research-*.txt`：文字资料核对记录。
- `src/App.vue`、`src/PlaceCard.vue`：页面和景点卡片。
- `src/lib.js`：筛选与浏览器存储辅助逻辑。
- `src/style.css`：桌面及手机样式。

本项目为独立的前端项目，无需后端服务即可本地运行。
