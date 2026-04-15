---
name: obsidian-knowledge-map
version: 1.2
description: 根据 Obsidian 笔记库内容，使用本地 ONNX 嵌入模型生成具有 AI 语义分类功能的知识地图（PNG）。支持达·芬奇手稿风格与当代艺术风格。触发词包括“生成知识地图”、“Knowledge Map”、“绘制笔记地形图”。
---

# Obsidian Knowledge Map Generator

该 Skill 通过“空间计算 - 语义归纳 - 艺术渲染”三阶段流水线，将笔记库转化为可视化的语义地貌图。

## 环境定位 (Context Awareness)
- **路径探测**：Agent 应优先通过 `glob("**/obsidian-knowledge-map/scripts/generator.py")` 确定脚本位置。
- **默认路径 (Fallback)**: `E:\OBVault\Nexus\.gemini\skills\obsidian-knowledge-map`

## 核心流程

### 0. 预检与环境验证 (Pre-check)
在启动任何阶段前，必须验证：
1. **依赖检查**：执行 `python -c "import onnxruntime, umap, tokenizers, matplotlib, scipy, numpy, yaml"`。
2. **主动修复**：若报错，**立即向用户提供安装指令**：`pip install onnxruntime umap-learn tokenizers matplotlib scipy numpy PyYAML`。
3. **路径验证**：确认 `vault_path` 和 `model_path` 目录存在。

### 1. 初始化与参数确认
启动前，通过 `ask_user` 获取：`vault_path`, `model_path`, `output_dir`, `style` (`davinci` 或 `contemporary`)。

### 2. 空间分析阶段 (Phase 1)
执行降维与聚类：
```powershell
python "{SCRIPT_PATH}" --mode analyze --vault "{vault_path}" --model "{model_path}" --output "{output_dir}" --style "{style}"
```
**关键检查点**：
- 确认脚本返回 6 组标题列表。
- 验证 `map_state.json` 是否生成。

### 3. AI 语义归纳阶段 (Phase 2)
- 为 6 组标题总结**名词短语**分类标签。
- 转换为 JSON 数组：`'["标签1", "标签2", ...]'`。

### 4. 艺术渲染阶段 (Phase 3)
执行绘图：
```powershell
python "{SCRIPT_PATH}" --mode render --vault "{vault_path}" --model "{model_path}" --output "{output_dir}" --style "{style}" --themes '{themes_json}'
```
**渲染后自检 (Accessibility Audit)**：
- **对比度检查**：若 `style` 为 `contemporary`，确保图例文字为白色 (`#FFFFFF`)。
- **散点可见性**：确保在深色背景下散点有浅色描边。

## 故障排除 (Troubleshooting)
- **文字模糊/看不清**：检查脚本中 `ink_color` 与 `paper_color` 的赋值逻辑。
- **路径包含中文**：在 Windows PowerShell 中，变量传参时请确保使用 `UTF-8` 编码或双引号包裹。

## 注意事项
- **总结准则**：分类名称应直接使用名词短语，确保 6 个分类在语义上有明显区隔。
