# Obsidian Knowledge Map | Obsidian 语义知识地图

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## English

**Obsidian Knowledge Map** is a specialized skill for Gemini CLI that transforms your Obsidian vault into an artistic semantic landscape. By combining state-of-the-art AI embeddings with classical and contemporary aesthetics, it allows you to "see" the shape of your knowledge.

### ✨ Features

-   **AI-Powered Clustering**: Uses `jina-embeddings-v2` to process note content and UMAP for high-dimensional to 2D projection.
-   **Semantic Synthesis**: A unique three-phase workflow where the AI autonomously summarizes category names for each knowledge "peak" based on your real note content.
-   **Dual Artistic Styles**:
    -   🖋️ **Da Vinci**: Parchment texture, sepia ink, and delicate quill-like contour lines.
    -   🌌 **Contemporary**: Dark gallery theme, glowing electric contours, and minimalist typography.
-   **Interactive Navigation**: Generates a full-screen interactive HTML map where every "star" (note) is clickable and opens directly in your Obsidian vault via URI. Now supports both **Da Vinci** and **Contemporary** styles.

### 🚀 How it Works (v1.3 Workflow)

1.  **Spatial Computation**: The script calculates text embeddings locally using ONNX and identifies 6 key semantic clusters (peaks).
2.  **Semantic Synthesis**: The AI Agent reads the titles of notes near each peak and synthesizes a high-level category name (e.g., "AI Engineering", "Financial Wisdom").
3.  **Artistic Rendering**: The final map is rendered as a PNG with smooth contours.
4.  **Interactive Enhancement**: Optionally generates a Plotly-based HTML map with synchronized styles and deep-linking.

### 🛠️ Installation

1.  Clone this repository into your Gemini CLI skills directory:
    `git clone https://github.com/fengyukongzhou/obsidian-knowledge-map .gemini/skills/obsidian-knowledge-map`
2.  Ensure you have the required dependencies:
    `pip install onnxruntime umap-learn tokenizers matplotlib scipy numpy PyYAML plotly`

---

<a name="chinese"></a>

## 中文

**Obsidian 语义知识地图** 是为 Gemini CLI 设计的专项技能，它能将您的 Obsidian 笔记库转化为极具艺术感的语义地貌图。通过将前沿的 AI 嵌入技术与古典/现代审美相结合，让您可以直观地“看见”知识的形状。

### ✨ 核心特性

-   **AI 驱动聚类**：采用 `jina-embeddings-v2` 模型处理笔记内容，并通过 UMAP 算法实现高维向 2D 坐标的精准投影。
-   **语义自动归纳**：独创的三阶段工作流，由 AI 根据您真实的笔记内容，自主总结每个知识“山峰”的分类名称。
-   **双重艺术风格**：
    -   🖋️ **达·芬奇手稿**：羊皮纸质感、深褐色铁胆墨水、羽毛笔触感的等高线。
    -   🌌 **当代艺术**：深色画廊风格、电光等高线、极简无衬线字体。
-   **全屏交互联动**：生成交互式 HTML 地图，点击地图上的“星点”即可通过 `obsidian://` 协议直接唤起 Obsidian 并定位到笔记。HTML 现在同步支持 **达·芬奇** 与 **当代艺术** 两种风格切换。

### 🚀 运行逻辑 (v1.3 工作流)

1.  **空间计算**：脚本在本地通过 ONNX 运行嵌入模型，识别出 6 个核心语义聚类中心。
2.  **语义合成**：AI Agent 读取山峰附近的笔记标题，提炼出高度概括的领域标签（如“量化交易”、“数字化生存”）。
3.  **艺术渲染**：生成带有精准标注和细腻等高线的 PNG 静态地图。
4.  **交互增强**：可选项，基于 Plotly 生成具备同步审美风格且可点击跳转的 HTML 交互地图。

### 🛠️ 安装方法

1.  将本仓库克隆至您的 Gemini CLI skills 目录：
    `git clone https://github.com/fengyukongzhou/obsidian-knowledge-map .gemini/skills/obsidian-knowledge-map`
2.  安装必要依赖：
    `pip install onnxruntime umap-learn tokenizers matplotlib scipy numpy PyYAML plotly`

---

**Created with ❤️ by Gemini CLI.**
