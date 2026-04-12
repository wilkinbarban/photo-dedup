import json
import os
from pathlib import Path

def update_i18n():
    with open('src/modules/config/i18n.py', 'r', encoding='utf-8') as f:
        content = f.read()

    new_en = """        "lbl_summary_groups": "{tot_groups} duplicate groups  •  {tot_photos} involved photos",
        
        "msg_load_ai": "Loading AI model...",
        "msg_search_img": "Searching for images...",
        "msg_analyzing": "Analyzing {total} images (Multi-Processing)...",
        "msg_analyzed": "Analyzed {n} images",
        "msg_comparing": "Comparing images...",
        "msg_comparing_n": "Comparing image {i}/{n}...",
        "msg_found_groups": "Found {n} duplicate groups"
    },"""

    new_es = """        "lbl_summary_groups": "{tot_groups} grupos duplicados  •  {tot_photos} fotos implicadas",
        
        "msg_load_ai": "Cargando modelo de IA...",
        "msg_search_img": "Buscando imágenes...",
        "msg_analyzing": "Analizando {total} imágenes (Multi-Procesamiento)...",
        "msg_analyzed": "Analizadas {n} imágenes",
        "msg_comparing": "Comparando imágenes...",
        "msg_comparing_n": "Comparando imagen {i}/{n}...",
        "msg_found_groups": "Encontrados {n} grupos duplicados"
    },"""

    new_pt = """        "lbl_summary_groups": "{tot_groups} grupos duplicados  •  {tot_photos} fotos envolvidas",
        
        "msg_load_ai": "Carregando modelo de IA...",
        "msg_search_img": "Procurando imagens...",
        "msg_analyzing": "Analisando {total} imagens (Multiprocessamento)...",
        "msg_analyzed": "Analisadas {n} imagens",
        "msg_comparing": "Comparando imagens...",
        "msg_comparing_n": "Comparando imagem {i}/{n}...",
        "msg_found_groups": "Encontrados {n} grupos duplicados"
    }"""
    
    content = content.replace('        "lbl_summary_groups": "{tot_groups} duplicate groups  •  {tot_photos} involved photos"\n    },', new_en)
    content = content.replace('        "lbl_summary_groups": "{tot_groups} grupos duplicados  •  {tot_photos} fotos implicadas"\n    },', new_es)
    content = content.replace('        "lbl_summary_groups": "{tot_groups} grupos duplicados  •  {tot_photos} fotos envolvidas"\n    }', new_pt)

    with open('src/modules/config/i18n.py', 'w', encoding='utf-8') as f:
        f.write(content)

def update_analyzer():
    with open('src/modules/services/analyzer.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add import
    if "from src.modules.config.i18n import get_text" not in content:
        content = content.replace("import multiprocessing", "import multiprocessing\nfrom src.modules.config.i18n import get_text")
        
    replacements = [
        ('self.progress.emit(0, "Cargando modelo de IA...")', 'self.progress.emit(0, get_text("msg_load_ai"))'),
        ('self.progress.emit(0, "Searching for images...")', 'self.progress.emit(0, get_text("msg_search_img"))'),
        ('self.progress.emit(5, f"Analyzing {total} images (Multi-Processing)...")', 'self.progress.emit(5, get_text("msg_analyzing").format(total=total))'),
        ('self.progress.emit(60, f"Analyzed {len(photos)} images")', 'self.progress.emit(60, get_text("msg_analyzed").format(n=len(photos)))'),
        ('self.progress.emit(60, "Comparing images...")', 'self.progress.emit(60, get_text("msg_comparing"))'),
        ('self.progress.emit(95, f"Found {len(groups)} duplicate groups")', 'self.progress.emit(95, get_text("msg_found_groups").format(n=len(groups)))'),
        ('self.progress.emit(pct, f"Comparing image {i+1}/{n}...")', 'self.progress.emit(pct, get_text("msg_comparing_n").format(i=i+1, n=n))')
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open('src/modules/services/analyzer.py', 'w', encoding='utf-8') as f:
        f.write(content)

update_i18n()
update_analyzer()
