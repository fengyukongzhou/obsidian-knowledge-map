# Obsidian Knowledge Map | Obsidian 语义知识地图

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## English

**Obsidian Knowledge Map** is a specialized skill for Gemini CLI that visualizes your Obsidian vault as a semantic landscape. By combining AI embeddings with customizable aesthetics, it provides a spatial representation of your knowledge base.

### ✨ Features

-   **Embedding-Based Clustering**: Utilizes `jina-embeddings-v2` to process note content and UMAP for projecting high-dimensional data onto a 2D plane.
-   **Semantic Summarization**: A multi-phase workflow where the AI summarizes category names for identified knowledge "peaks" based on local note content.
-   **Artistic Styles**:
    -   🖋️ **Da Vinci**: Parchment texture, sepia ink, and delicate contour lines.
    -   🌌 **Contemporary**: Dark gallery theme, glowing contours, and minimalist typography.
-   **Interactive Navigation**: Generates a full-screen interactive HTML map (Plotly-based) where notes are clickable and open directly in Obsidian via URI. Supports both **Da Vinci** and **Contemporary** styles.

### 🚀 How it Works (v1.3 Workflow)

1.  **Spatial Computation**: Calculates text embeddings locally using ONNX and identifies semantic clusters (peaks).
2.  **Semantic Synthesis**: The AI Agent reviews note titles near each peak to generate representative category names.
3.  **Artistic Rendering**: Generates a static PNG map with smooth contours and Roman numeral annotations.
4.  **Interactive Enhancement**: Optionally generates a deep-linked HTML map with synchronized visual styles.

### 🛠️ Installation

1.  Clone this repository into your Gemini CLI skills directory:
    `git clone https://github.com/fengyukongzhou/obsidian-knowledge-map .gemini/skills/obsidian-knowledge-map`
2.  Install the required dependencies:
    `pip install onnxruntime umap-learn tokenizers matplotlib scipy numpy PyYAML plotly`

---

<a name="chinese"></a>

## 中文

**Obsidian 语义知识地图** 是为 Gemini CLI 设计的专项技能，它能将您的 Obsidian 笔记库转化为可视化的语义地貌图。通过将 AI 嵌入技术与自定义审美相结合，为您的知识库提供空间化呈现。

### ✨ 核心特性

-   **基于嵌入的聚类**：采用 `jina-embeddings-v2` 模型处理笔记内容，并通过 UMAP 算法实现高维坐标向 2D 平面的投影。
-   **语义归纳**：多阶段工作流，由 AI 根据真实的笔记内容，为识别出的知识“山峰”总结分类名称。
-   **双重艺术风格**：
    -   🖋️ **达·芬奇手稿**：羊皮纸质感、深褐色墨水、细腻的等高线。
    -   🌌 **当代艺术**：深色画廊风格、电光等高线、极简无衬线字体。
-   **全屏交互联动**：生成交互式 HTML 地图（基于 Plotly），点击地图上的节点可通过 `obsidian://` 协议直接打开笔记。HTML 地图同步支持 **达·芬奇** 与 **当代艺术** 风格。

### 🚀 运行逻辑 (v1.3 工作流)

1.  **空间计算**：在本地通过 ONNX 运行嵌入模型，识别核心语义聚类中心。
2.  **语义合成**：AI Agent 读取山峰附近的笔记标题，提炼出代表性的领域标签。
3.  **艺术渲染**：生成带有标注和等高线的 PNG 静态地图。
4.  **交互增强**：（可选）基于 Plotly 生成具备同步视觉风格且可点击跳转的 HTML 交互地图。

### 🛠️ 安装方法

1.  将本仓库克隆至您的 Gemini CLI skills 目录：
    `git clone https://github.com/fengyukongzhou/obsidian-knowledge-map .gemini/skills/obsidian-knowledge-map`
2.  安装必要依赖：
    `pip install onnxruntime umap-learn tokenizers matplotlib scipy numpy PyYAML plotly`

---

**Created with ❤️ by Gemini CLI.**
