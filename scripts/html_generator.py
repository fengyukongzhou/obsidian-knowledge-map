import json
import numpy as np
import plotly.graph_objects as go
import os
import urllib.parse
from pathlib import Path

def generate_immersive_html(output_dir, vault_name, themes, style='davinci'):
    output_dir = Path(output_dir)
    state_path = output_dir / "map_state.json"
    
    if not state_path.exists():
        print(f"Error: map_state.json not found in {output_dir}")
        return
        
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    notes = state['notes']
    coords = np.array(state['coords'])
    Z = np.array(state['Z'])
    peaks = state['peaks']
    
    # Palette definition based on style
    if style == 'davinci':
        bg_color = '#f4ecd8' # Parchment
        ink_color = '#4e342e' # Deep Sepia
        text_alpha = 'rgba(78, 52, 46, 0.4)'
        contour_colors = [
            [0, 'rgba(244, 236, 216, 0)'],
            [0.1, 'rgba(208, 208, 230, 0.2)'],
            [0.3, 'rgba(230, 208, 150, 0.4)'],
            [0.6, 'rgba(150, 100, 50, 0.5)'],
            [1, 'rgba(78, 52, 46, 0.7)']
        ]
        line_color = 'rgba(78, 52, 46, 0.15)'
        grid_color = 'rgba(78, 52, 46, 0.05)'
        legend_bg = 'rgba(244, 236, 216, 0.7)'
        hover_bg = 'rgba(255, 255, 255, 0.95)'
        hover_text = '#4e342e'
    else: # contemporary
        bg_color = '#050505'
        ink_color = '#FFFFFF'
        text_alpha = 'rgba(255, 255, 255, 0.25)'
        contour_colors = [
            [0, 'rgba(0,0,0,0)'],
            [0.1, 'rgba(30,50,100,0.15)'],
            [0.3, 'rgba(50,100,200,0.3)'],
            [0.6, 'rgba(0,150,255,0.5)'],
            [1, 'rgba(0,255,255,0.7)']
        ]
        line_color = 'rgba(255,255,255,0.06)'
        grid_color = 'rgba(255,255,255,0.02)'
        legend_bg = 'rgba(20,20,20,0.4)'
        hover_bg = 'rgba(10,10,10,0.95)'
        hover_text = '#FFFFFF'
    
    # 1. Base Figure
    fig = go.Figure()

    # 2. Immersive Terrain (80 layers)
    x_range = np.linspace(0, 1, Z.shape[1])
    y_range = np.linspace(0, 1, Z.shape[0])
    fig.add_trace(go.Contour(
        z=Z, x=x_range, y=y_range,
        colorscale=contour_colors,
        showscale=False,
        contours=dict(coloring='heatmap', showlines=True),
        line=dict(width=0.4, color=line_color),
        ncontours=80,
        hoverinfo='skip'
    ))

    # 3. Dynamic Clusters
    folders = [n['folder'] for n in notes]
    unique_f = sorted(list(set(folders)))
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    color_palette = plt.cm.get_cmap('tab20').colors
    
    for i, f in enumerate(unique_f):
        indices = [j for j, val in enumerate(folders) if val == f]
        if not indices: continue
        
        folder_notes = [notes[j] for j in indices]
        x = coords[indices, 0]
        y = coords[indices, 1]
        titles = [n['title'] for n in folder_notes]
        urls = [f"obsidian://open?vault={urllib.parse.quote(vault_name)}&file={urllib.parse.quote(n['rel_path'])}" for n in folder_notes]
        
        edge_color = 'rgba(255,255,255,0.3)' if style == 'contemporary' else 'rgba(0,0,0,0.1)'
        
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='markers',
            marker=dict(
                size=6, 
                color=mcolors.to_hex(color_palette[i % 20]), 
                opacity=0.9,
                line=dict(width=0.5, color=edge_color)
            ),
            name=f,
            text=titles,
            customdata=urls,
            hovertemplate="<b>%{text}</b><br><span style='font-size:10px; color:#888;'>CLICK TO OPEN</span><extra></extra>"
        ))

    # 4. AI Peak Labels
    for i, (p, t) in enumerate(zip(peaks, themes)):
        fig.add_trace(go.Scatter(
            x=[p['x']], y=[p['y']],
            mode='text',
            text=[f"<span style='color:{text_alpha}; letter-spacing:4px; font-weight:100;'>{t.upper()}</span>"],
            textposition="top center",
            hoverinfo='skip',
            showlegend=False
        ))

    # 5. Full Screen Layout
    fig.update_layout(
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        showlegend=True,
        legend=dict(
            font=dict(color=ink_color, size=10, family="serif" if style == 'davinci' else "sans-serif"),
            bgcolor=legend_bg,
            bordercolor=line_color,
            borderwidth=1,
            orientation='h',
            yanchor='bottom',
            y=0.03,
            xanchor='center',
            x=0.5,
            itemsizing='constant'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        clickmode='event',
        dragmode=False,
        hoverlabel=dict(
            bgcolor=hover_bg, 
            bordercolor=line_color,
            font=dict(color=hover_text, size=12, family="sans-serif")
        ),
        autosize=True
    )

    html_content = fig.to_html(
        include_plotlyjs='cdn', 
        full_html=False, 
        config={'displayModeBar': False, 'responsive': True}
    )
    
    brand_font = "'Times New Roman', serif" if style == 'davinci' else "'Inter', sans-serif"
    
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{vault_name} | Knowledge Contour</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;400&display=swap" rel="stylesheet">
        <style>
            body, html {{ margin: 0; padding: 0; width: 100vw; height: 100vh; background-color: {bg_color}; overflow: hidden; }}
            #main-stage {{ width: 100vw; height: 100vh; display: block; }}
            .plotly-graph-div {{ width: 100vw !important; height: 100vh !important; }}
            #brand {{
                position: absolute; top: 40px; left: 50px;
                color: {text_alpha};
                font-family: {brand_font};
                font-weight: 100; font-size: 14px;
                letter-spacing: 12px;
                pointer-events: none; z-index: 100;
            }}
        </style>
    </head>
    <body>
        <div id="brand">{vault_name.upper()} CONTOUR</div>
        <div id="main-stage">{html_content}</div>
        <script>
            window.addEventListener('load', function() {{
                var plot = document.getElementsByClassName('plotly-graph-div')[0];
                plot.on('plotly_click', function(data){{
                    if(data.points[0].customdata){{
                        window.location.href = data.points[0].customdata;
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    html_path = output_dir / "knowledge_map.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Interactive HTML ({style} style) saved to {html_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--vault_name")
    parser.add_argument("--themes")
    parser.add_argument("--style", default='davinci')
    args = parser.parse_args()
    
    if args.themes:
        themes = json.loads(args.themes)
    else:
        with open(Path(args.output) / "themes.json", 'r', encoding='utf-8') as f:
            themes = json.load(f)
            
    generate_immersive_html(args.output, args.vault_name, themes, args.style)
