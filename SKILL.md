---
name: obsidian-knowledge-map
version: 1.3
description: 根据 Obsidian 笔记库内容，使用本地 ONNX 嵌入模型生成具有 AI 语义分类功能的知识地图（PNG/HTML）。支持交互式 HTML 地图（带点击跳转功能）。触发词包括“生成知识地图”、“Knowledge Map”、“绘制笔记地形图”。
---

# Obsidian Knowledge Map Generator

该 Skill 通过“空间计算 - 语义归纳 - 艺术渲染 - 交互增强”四阶段流水线，将笔记库转化为可视化的语义地貌图。

## 环境定位 (Context Awareness)
- **路径探测**：Agent 应优先通过 `glob("**/obsidian-knowledge-map/scripts/generator.py")` 确定脚本位置。
- **默认路径 (Fallback)**: `E:\OBVault\Nexus\.gemini\skills\obsidian-knowledge-map`

## 核心流程

### 0. 预检与环境验证 (Pre-check)
在启动前，必须验证依赖：
1. **依赖检查**：执行 `python -c "import onnxruntime, umap, tokenizers, matplotlib, scipy, numpy, yaml, plotly"`。
2. **主动修复**：若报错，提供安装指令：`pip install onnxruntime umap-learn tokenizers matplotlib scipy numpy PyYAML plotly`。
3. **路径验证**：确认 `vault_path` 和 `model_path` 目录存在。

### 1. 初始化与参数确认
通过 `ask_user` 获取：`vault_path`, `model_path`, `output_dir`, `style` (`davinci` 或 `contemporary`)。

### 2. 空间分析阶段 (Phase 1)
执行降维与聚类：
```powershell
python "{SCRIPT_PATH}" --mode analyze --vault "{vault_path}" --model "{model_path}" --output "{output_dir}" --style "{style}"
```
**关键检查点**：确认生成了 `map_state.json`。

### 3. AI 语义归纳阶段 (Phase 2)
- 为 6 组标题总结**名词短语**分类标签。
- 转换为 JSON 数组：`'["标签1", "标签2", ...]'`。

### 4. 艺术渲染阶段 (Phase 3)
执行绘图 (PNG)：
```powershell
python "{SCRIPT_PATH}" --mode render --vault "{vault_path}" --model "{model_path}" --output "{output_dir}" --style "{style}" --themes '{themes_json}'
```

### 5. 交互增强阶段 (Phase 4 - 可选)
询问用户：“是否生成支持点击跳转的交互式 HTML 地图？”
若用户同意，执行：
```powershell
python "{SKILL_DIR}\scripts\html_generator.py" --output "{output_dir}" --vault_name "{vault_name}" --themes '{themes_json}'
```
**渲染后操作**：
- 询问用户并使用 `run_shell_command` 打开生成的 `.png` 或 `.html` 文件。

## 注意事项
- **HTML 联动**：HTML 地图支持点击节点通过 `obsidian://` 协议直接打开笔记，需确保库名 (`vault_name`) 准确。
- **渲染质量**：针对 `contemporary` 风格，已自动优化图例颜色与对比度。
