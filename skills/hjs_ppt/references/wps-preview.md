# WPS 制作中预览

用户要求边做边看时，在第一版可读页面保存后就打开 WPS，之后每完成一页或一组有意义的修改，保存完整 PPTX，再调用预览脚本。最终交付文件也打开检查。默认不等到整份成片才首次展示。

这是**保存节点预览**：每次打开已完整保存的快照，不是字符级实时协作，也不承诺 WPS 会自动刷新已打开文件。当前实现不常驻监听、不定时抢焦点、不关闭用户窗口。

## 使用

只探测环境，不打开应用、不创建副本：

```powershell
powershell -NoProfile -File "<skill-dir>/scripts/preview_wps.ps1" -InputFile "draft.pptx" -CheckOnly
```

打开当前保存版本：

```powershell
powershell -NoProfile -File "<skill-dir>/scripts/preview_wps.ps1" -InputFile "draft.pptx" -PreviewDirectory "<task>/wps-preview"
```

自定义安装位置：

```powershell
powershell -NoProfile -File "<skill-dir>/scripts/preview_wps.ps1" -InputFile "draft.pptx" -WpsPath "<WPS 安装目录>/office6/wpp.exe"
```

脚本从 PATH、Windows App Paths 注册表和常见安装目录查找 `wpp.exe`，也支持显式路径。复制为带时间和随机后缀的只读快照，校验源/副本 SHA-256 一致，才请求 WPS 打开。源文件不修改，快照不覆盖，WPS 已打开的其他文稿不关闭。快照目录是任务产物，不随 skill 发布。

每次会打开新的预览文稿/标签；编辑应继续作用于制作源文件。若用户在预览中另存或修改，先把它作为新输入对齐，不能忽略用户修改。旧预览可由用户关闭，禁止批量杀掉 WPS 进程以“刷新”。

## 能力与验收边界

- 没装 WPS：报告缺少应用；继续完成素材与排版。只有用户要求安装时才另行安装。可用现有 PowerPoint 展示，但需先说明这不是 WPS 验证。
- `launch_requested` 仅表示启动请求已提交，不代表文件已经显示正常。用可用的桌面截图/窗口工具确认文件名、页面、字体、图片、MathType 显示及修复提示。
- 检查一页不代表全稿验收；最终仍需全部页面的渲染和视觉检查。
- MathType 显示正确不等于可编辑。严格按 [MathType 规则](mathtype.md) 在保存后的最终文件逐条验证；WPS 当前版本不支持所需 OLE 编辑时，保留对象并明确该兼容性限制。
- 没有桌面控制工具时提供已生成快照路径，明确“未目视确认 WPS 打开”。

开发本功能时，本机未安装 WPS。已验证探测、复制、只读快照和启动参数的本地测试；真实 WPS 打开/字体/MathType 兼容性需在安装后验证，不能把模拟启动测试写成 WPS 实测通过。
