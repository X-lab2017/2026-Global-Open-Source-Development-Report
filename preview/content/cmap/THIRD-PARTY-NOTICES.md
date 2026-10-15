# 3D 协作地球：来源与许可

- 视觉与场景实现参考：[janarosmonaliev/github-globe](https://github.com/janarosmonaliev/github-globe)，作者 Zhanarbek Osmonaliev。参考其 Three.js 场景、球面连线与 OrbitControls 交互思路；本报告另行实现数据、球面表面、关系示意、选择行为及单屏阅读布局，未复用作者的航班数据。
- 渲染依赖：Three.js **0.170.0** 与同版本 OrbitControls，随站点本地发布；许可见 `vendor/THREE-LICENSE.txt`。OrbitControls 唯一导入路径改为本地 Three.js 文件。
- 球面陆地与边界：复用已接受的 OpenShare `world.json`。二维地图仍保持原平台地图形态；三维地球用同一地理数据映射至球面。台湾省随中国地域呈现。
- 协作示意：96 位虚构开发者、18 个共享项目与 384 条参与关系；双向光点、历史延续和衰减用于解释原理，未运行 OpenRank 算法。
- 贡献点：报告2026的中、美、印国家值与 GitHub2025的236地域分布可切换；不拆分组别或补算缺失国家。
- 来源线：20条报告原表关系；可选金色虚线为未列来源的条件估算。完整方法与边界见 `flow-method.md`，数值与类别见 `flows.csv`。

## github-globe — MIT License

Copyright (c) 2021 Zhanarbek Osmonaliev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
