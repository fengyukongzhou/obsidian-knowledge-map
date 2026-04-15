import os
import re
import yaml
import json
import numpy as np
import onnxruntime
import umap
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
from tokenizers import Tokenizer
from scipy.stats import gaussian_kde
from scipy.ndimage import maximum_filter
from scipy.spatial.distance import cdist
import sys
import argparse

class MapGenerator:
    def __init__(self, vault_path, model_dir, output_dir, style='davinci'):
        self.vault_path = Path(vault_path)
        self.model_dir = Path(model_dir)
        self.output_dir = Path(output_dir)
        self.style = style
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Tokenizer & ONNX Session initialization
        self.tokenizer = Tokenizer.from_file(str(self.model_dir / "tokenizer.json"))
        self.tokenizer.enable_padding(direction='right', pad_id=1, pad_type_id=0, pad_token='<pad>')
        self.tokenizer.enable_truncation(max_length=1024)
        self.onnx_path = str(self.model_dir / "onnx/model_quantized.onnx")
        self._init_session()

    def _init_session(self):
        import onnxruntime as ort
        import gc
        if hasattr(self, 'session'):
            del self.session
            gc.collect()
        options = ort.SessionOptions()
        options.enable_cpu_mem_arena = False # Memory safety for large vaults
        options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        options.intra_op_num_threads = 2
        self.session = ort.InferenceSession(self.onnx_path, options, providers=['CPUExecutionProvider'])

    def scan_notes(self):
        """Universal vault scanner: only skips system/attachment folders starting with '_'"""
        notes = []
        for root, dirs, files in os.walk(self.vault_path):
            # Skip hidden/attachment folders like _attachments or .obsidian
            dirs[:] = [d for d in dirs if not d.startswith(('_', '.'))]
            for file in files:
                if file.endswith('.md'):
                    path = Path(root) / file
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except: continue
                    
                    # Generic Frontmatter Parsing
                    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                    fm = {}
                    if fm_match:
                        try: fm = yaml.safe_load(fm_match.group(1)) or {}
                        except: fm = {}
                    body = content[fm_match.end():] if fm_match else content
                    
                    # Basic noise filter: skip very short notes
                    if len(body) < 100: continue
                    
                    notes.append({
                        'title': fm.get('title', path.stem),
                        'rel_path': str(path.relative_to(self.vault_path)),
                        'content': body[:2000], 
                        'folder': path.parent.name if path.parent != self.vault_path else "Root"
                    })
        return notes

    def encode(self, texts):
        all_embs = []
        total = (len(texts) + 3) // 4
        for i in range(0, len(texts), 4):
            batch_idx = i // 4 + 1
            if batch_idx % 10 == 0 or batch_idx == 1 or batch_idx == total:
                print(f"  Progress: Batch {batch_idx}/{total}...")
            
            # Auto-recycling to prevent memory leaks
            if batch_idx % 50 == 0:
                self._init_session()
                
            batch = texts[i:i+4]
            enc = self.tokenizer.encode_batch(batch)
            ids = np.array([e.ids for e in enc], dtype=np.int64)
            mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
            out = self.session.run(None, {"input_ids": ids, "attention_mask": mask})[0]
            
            # Mean Pooling & Normalization
            mask_exp = np.expand_dims(mask, -1).astype(float)
            emb = np.sum(out * mask_exp, 1) / np.maximum(mask_exp.sum(1), 1e-9)
            emb /= np.maximum(np.linalg.norm(emb, axis=1, keepdims=True), 1e-9)
            all_embs.append(emb)
        return np.vstack(all_embs)

    def analyze_geography(self):
        emb_cache = self.output_dir / "embeddings.npy"
        coord_cache = self.output_dir / "coords.npy"
        notes = self.scan_notes()
        num_notes = len(notes)
        
        if emb_cache.exists():
            embs = np.load(emb_cache)
        else:
            embs = self.encode([n['content'] for n in notes])
            np.save(emb_cache, embs)
            
        if coord_cache.exists():
            coords = np.load(coord_cache)
        else:
            # Adaptive UMAP Parameters
            n_neighbors = int(np.clip(np.sqrt(num_notes) * 2, 15, 100))
            min_dist = 0.1 if num_notes < 500 else 0.05
            reducer = umap.UMAP(n_components=2, metric='cosine', n_neighbors=n_neighbors, min_dist=min_dist, random_state=42)
            coords = reducer.fit_transform(embs)
            coords = (coords - coords.min(axis=0)) / (coords.max(axis=0) - coords.min(axis=0))
            np.save(coord_cache, coords)
        
        # KDE Density estimation
        kde = gaussian_kde(coords.T)
        X, Y = np.meshgrid(np.linspace(0, 1, 300), np.linspace(0, 1, 300))
        Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(300, 300)
        Z = (Z - Z.min()) / (Z.max() - Z.min())
        
        # Peak Detection
        data_max = maximum_filter(Z, size=15, mode='constant')
        mask = (Z == data_max) & (Z > 0.1)
        peak_pts = np.column_stack(np.where(mask))
        peaks = sorted([{'val': Z[r,c], 'x': X[r,c], 'y': Y[r,c]} for r, c in peak_pts], key=lambda x: x['val'], reverse=True)
        
        # Dynamic Peak Merging
        merge_dist = 0.12 if num_notes < 500 else 0.08
        max_p = 6 if num_notes < 1000 else 10
        merged = []
        for p in peaks:
            if not any(np.sqrt((p['x']-mp['x'])**2 + (p['y']-mp['y'])**2) < merge_dist for mp in merged):
                merged.append(p)
                if len(merged) >= max_p: break
        
        # Extract cluster neighbors for Agent to summarize
        peak_neighbor_titles = []
        for p in merged:
            dists = cdist(np.array([[p['x'], p['y']]]), coords).flatten()
            nearest = [notes[j]['title'] for j in np.argsort(dists)[:15]]
            peak_neighbor_titles.append(nearest)
            
        state = {'notes': notes, 'coords': coords.tolist(), 'Z': Z.tolist(), 'peaks': merged}
        with open(self.output_dir / "map_state.json", 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False)
        return peak_neighbor_titles

    def render(self, themes):
        with open(self.output_dir / "map_state.json", 'r', encoding='utf-8') as f:
            state = json.load(f)
        Z = np.array(state['Z'])
        coords = np.array(state['coords'])
        X, Y = np.meshgrid(np.linspace(0, 1, 300), np.linspace(0, 1, 300))
        
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        fig, ax = plt.subplots(figsize=(14, 14), dpi=150)
        
        # Styling based on user choice
        paper_color = '#f4ecd8' if self.style == 'davinci' else '#050505'
        ink_color = '#4e342e' if self.style == 'davinci' else '#FFFFFF'
        fig.patch.set_facecolor(paper_color)
        ax.set_facecolor(paper_color)
        cmap = mcolors.LinearSegmentedColormap.from_list('map', 
            ['#d0d0e6', '#e6d096', '#966432'] if self.style == 'davinci' else ['#0a0a0a', '#007aff', '#00ffff'])
        
        ax.contourf(X, Y, Z, levels=20, cmap=cmap, alpha=0.6)
        ax.contour(X, Y, Z, levels=20, colors=ink_color, linewidths=0.5, alpha=0.3)
        
        # Universal Categorical Coloring
        folders = [n['folder'] for n in state['notes']]
        unique_f = sorted(list(set(folders)))
        # Use a high-quality categorical color map (tab20)
        color_palette = plt.cm.get_cmap('tab20').colors
        for i, f in enumerate(unique_f):
            m = np.array([n == f for n in folders])
            if any(m):
                # Add a thin edge for better visibility on dark backgrounds
                edge_color = 'white' if self.style == 'contemporary' else 'none'
                ax.scatter(coords[m, 0], coords[m, 1], s=20, 
                           c=[color_palette[i % 20]], alpha=0.7, label=f, 
                           edgecolors=edge_color, linewidths=0.2)
        
        # Peak Annotations
        roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
        for i, (p, t) in enumerate(zip(state['peaks'], themes)):
            ax.add_artist(plt.Circle((p['x'], p['y']), 0.02, color=ink_color, fill=False, alpha=0.8))
            ax.text(p['x'], p['y'], roman[i], ha='center', va='center', color=ink_color, fontweight='bold')
            ax.text(p['x']+0.03, p['y']+0.01, t, color=ink_color, fontsize=10, 
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=paper_color, edgecolor=ink_color, alpha=0.6))
        
        ax.set_title("OBSIDIAN KNOWLEDGE MAP", fontsize=32, color=ink_color, pad=40, fontfamily='serif')
        # Limit legend size if too many folders
        leg = ax.legend(loc='lower left', frameon=True, facecolor=paper_color, edgecolor=ink_color, fontsize=8, ncol=2 if len(unique_f)>10 else 1)
        plt.setp(leg.get_texts(), color=ink_color) # Explicitly set text color
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(self.output_dir / "knowledge_map.png")
        plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=['analyze', 'render'])
    parser.add_argument("--vault"); parser.add_argument("--model"); parser.add_argument("--output")
    parser.add_argument("--style", default='davinci'); parser.add_argument("--themes")
    args = parser.parse_args()
    
    gen = MapGenerator(args.vault, args.model, args.output, args.style)
    if args.mode == 'analyze':
        print(json.dumps(gen.analyze_geography(), ensure_ascii=False))
    elif args.mode == 'render':
        if args.themes:
            themes = json.loads(args.themes)
        else:
            with open(gen.output_dir / "themes.json", 'r', encoding='utf-8') as f:
                themes = json.load(f)
        gen.render(themes)
