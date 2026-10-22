# 附录 B 与两篇附录联调 · 2026-10-22

继承 GOSD-PUB-20261020 · 1.2 及附录 A 出版样本。当前任务为完成附录 B，联调两篇附录与全书入口；不重评 870/884 模型样本，不补造第四章 4.2—4.6 的后续研究。

## 内容与来源

附录 B 采用六节同源正文：三类判断、版本材料、四个案例、DPG 认可、公共价值证据、交付与更新。补齐英文全文。两篇附录使用同一阅读样式、章节导航与下载形态，A 正文保持已审定版本。

官方参照核对日期为 2026-10-22。OSI OSAID 1.0 与 DPGA AI 系统要求分别解释；DPGA 对训练、验证和测试数据的开放要求，不由 OSAID 的数据信息要求替代。官方说明和 Registry、评审规则共同支持认可范围及一年有效期。

- https://opensource.org/ai/open-source-ai-definition
- https://www.digitalpublicgoods.net/standard
- https://www.digitalpublicgoods.net/blog/ai-systems-as-dpgs （2025-05-21）
- https://www.digitalpublicgoods.net/blog/navigating-alignment-in-ai-systems-as-dpgs （2026-06-23）
- https://content.digitalpublicgoods.net/A_Practical_Guide_to_the_DPG_Standard_0249fee444.pdf （2026-10，1.0）
- https://www.digitalpublicgoods.net/registry
- https://github.com/DPGAlliance/dpg-resources/blob/main/docs/dpg-review-policy.md

DPG 标准仓库的 standard.md 仍有旧版本表头，故本轮不单独依赖该文件判断 AI 最新适用要求；同时核对官方当前站点、2025 AI 专项说明、2026 说明与 CHANGELOG 1.1.7。案例沿用仓库 cases.json 的 2026-10-17 固定记录，没有重新声称已核验动态页面或授予等级。

## 出版与范围

A4 纵向、正文 11.2 pt / 18.6 pt，表格 9.8 pt。表格尽量整块呈现，两版保留完整正文。B 独立 PDF 与 A＋B 合订 PDF 自动生成；合订版逐页保留原图文，加入分层书签与 A/B 页标签。前置合订版同步范围说明，仍只收录前置篇目与第一章。

全书目录、两篇附录目录、搜索、下载、语言入口、版本记录和仓库说明同步。旧 declaration 路由保持跳转，不恢复第三篇附录。当前范围的正文编排收束与全书 PDF 汇编、英文全译、后续研究分别表述。

## 验收记录

本地执行环境无法建立连接，本轮通过仓库工作流完成构建、检查及渲染，人工再检查渲染结果。

- 分支验收：工作流 39715595467（提交 bd2d22050ab69b3258710e4b04bc24a811b43ec3）全部通过。网站包含 53 页、5,897 个内部链接/资源、400 条搜索记录，90 个 CSV 下载保持原始字节。
- 正文一致性：A/B 中英文网页逐段与各自源稿核对；中文 PDF 包含同源完整正文。原四个固定版本案例、870/884 样本区别、22 条许可差异待复核状态均保留。
- PDF：A 6 页、B 6 页、A＋B 12 页；A4 纵向、字号和文字边界通过。合订版逐页图文与独立版本完全一致，提供 16 个分层书签及 A/B 页标签。前置合订版共 21 页，附带第一章的 12 页保持原图文。
- 浏览器：A/B × 中英文 × 桌面/390 px 窄屏 × 明暗主题，共 16 组通过；另外验证目录键盘操作、减少动态效果设置、禁用 JavaScript 后阅读和下载入口。
- 人工目检：A 全部 6 页、B 全部 6 页；桌面、手机、中文、英文、明暗主题及 B.4 窄屏表格。B 按六节独立分页，避免说明和表格分离；窄屏两列表格自适应宽度。页眉、页码、正文及表格无遮挡。批量预览疑点经单页复看确认正常。

发布提交：ff2b2bb1cd970a0dda47a692386a1c14f08a805b（PR #4）。主站发布工作流 39716203645 构建、部署均成功；实际主站复核工作流 39716352258（任务 119619279512）成功。

线上检查读取 www.x-lab.info 的实际文件，核对 A/B/合订版的 edition、源稿摘要、PDF SHA-256、页数与配套关系；两种语言的下载页与两篇附录互链均返回成功。前置合订版保持 21 页并仅列两篇附录。线上 B 的六幅逐页渲染 PNG 与人工审阅的分支版本逐字节一致，另外目检线上中英文桌面与手机截图。

本次发布的 PDF 摘要如下（对应以上部署与核验运行；以后重新构建以各 edition-manifest.json 为准）：

| 文件 | 页数 | 版本 | SHA-256 |
| --- | --- | --- | --- |
| appendix-a | 6 | 2026-10-22-methods-v3 | bb26dd85942bcce8468af6ba0f3bb0d0364e61380ba0843ede6374ac05b5f5aa |
| appendix-b | 6 | 2026-10-22-openness-v2 | 6e4fd7e8a9f2d8652b70389795c8679b438dea674587a43b2f3eddba89512c1c |
| appendices | 12 | 2026-10-22-appendices-v2 | 344cf228e9d22edb0d316b25d08be25a7fc18ee0c823c155bb77a58055898b6f |

附录与当前约定范围的报告内容已完成本轮收束。全书单一合订 PDF、其他章节的完整英文翻译，以及 4.2—4.6 后续研究仍遵循各自已明示的范围，不据此宣称已全部完成。

