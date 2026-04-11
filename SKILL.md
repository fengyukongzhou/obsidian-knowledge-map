---
name: obsidian-knowledge-map
description: 根据 Obsidian 笔记库内容，使用本地 ONNX 嵌入模型生成具有 AI 语义分类功能的知识地图（PNG）。支持达·芬奇手稿风格与当代艺术风格。触发词包括“生成知识地图”、“Knowledge Map”、“绘制笔记地形图”。
---

# Obsidian Knowledge Map Generator

该 Skill 通过“空间计算 - 语义归纳 - 艺术渲染”三阶段流水线，将笔记库转化为可视化的语义地貌图。

## 核心流程

### 1. 初始化与参数确认
启动前，必须通过 `ask_user` 获取：
- `vault_path`: Obsidian 库根目录。
- `model_path`: 本地 Jina/ONNX 模型目录（snapshots 下的哈希目录）。
- `output_dir`: 图片保存位置（推荐：桌面）。
- `style`: 风格选择 (`davinci` 或 `contemporary`)。

### 2. 空间分析阶段 (Phase 1)
执行脚本进行 UMAP 降维与聚类中心（峰值）提取：
```powershell
python "scripts/generator.py" --mode analyze --vault "{vault_path}" --model "{model_path}" --output "{output_dir}" --style "{style}"
```
**输出**：脚本会打印出 6 组最邻近山峰的笔记标题列表。

### 3. AI 语义归纳阶段 (Phase 2)
读取 Phase 1 输出的标题组，Agent（我）需执行：
- 为每一组标题（共 6 组）总结出一个**高度概括、精准且不带修饰词**的分类名称。
- 将总结出的 6 个标签转换为 JSON 列表字符串，例如：`'["金融投资", "AI技术", "生活感悟", ...]'`。

### 4. 艺术渲染阶段 (Phase 3)
将 AI 生成的标签回传至脚本，完成最终绘图：
```powershell
python "scripts/generator.py" --mode render --vault "{vault_path}" --model "{model_path}" --output "{output_dir}" --style "{style}" --themes '{themes_json}'
```

## 依赖要求
确保系统环境已安装：`onnxruntime`, `umap-learn`, `tokenizers`, `matplotlib`, `scipy`, `numpy`, `PyYAML`。

## 注意事项
- **路径处理**：在 Windows 环境下，调用 Python 时请务必使用双引号包裹路径。
- **总结准则**：分类名称应直接使用名词短语，确保 6 个分类在语义上有明显区隔。
- **状态文件**：Phase 1 会生成 `map_state.json` 用于 Phase 3 读取，请确保两次操作在同一输出目录下。
