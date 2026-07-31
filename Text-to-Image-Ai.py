#!/usr/bin/env python3
"""
AI-Powered Text to Image Generator
Free AI APIs Integration - Single Image Generation
Developed by CHOWDHURY-VAI
Version: 3.3 - Single Image Optimized
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import requests
import json
import base64
import os
from datetime import datetime
import threading
from io import BytesIO
import time
import random
import hashlib
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import textwrap

class FreeAIAPIs:
    """Collection of free AI APIs for image generation"""
    
    @staticmethod
    def generate_with_pollinations(text, width=1024, height=1024):
        """AI image generation using Pollinations.ai"""
        try:
            encoded_text = quote(text)
            url = f"https://image.pollinations.ai/prompt/{encoded_text}?width={width}&height={height}&nologo=true&seed={random.randint(1,999999)}"
            
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return image
            return None
        except:
            return None
    
    @staticmethod
    def generate_with_prodia(text, width=1024, height=1024):
        """AI image generation using Prodia API"""
        try:
            url = "https://api.prodia.com/v1/sd/generate"
            
            payload = {
                "model": "sdv1_4.ckpt [7460a6fa]",
                "prompt": text,
                "negative_prompt": "bad quality, blurry, distorted",
                "steps": 25,
                "cfg_scale": 7,
                "seed": random.randint(1, 999999),
                "upscale": False,
                "sampler": "Euler",
                "width": width,
                "height": height
            }
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code == 200:
                job_id = response.json().get('job')
                
                for _ in range(20):
                    time.sleep(2)
                    result_url = f"https://api.prodia.com/v1/job/{job_id}"
                    result = requests.get(result_url, headers=headers)
                    
                    if result.status_code == 200:
                        data = result.json()
                        if data.get('status') == 'succeeded':
                            image_url = data.get('imageUrl')
                            img_response = requests.get(image_url)
                            image = Image.open(BytesIO(img_response.content))
                            return image
            return None
        except:
            return None
    
    @staticmethod
    def generate_with_craiyon(text):
        """AI image generation using Craiyon"""
        try:
            url = "https://api.craiyon.com/v3/generate"
            
            payload = {
                "prompt": text,
                "negative_prompt": "ugly, blurry, low quality",
                "style": "art",
                "model": "art"
            }
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=45)
            if response.status_code == 200:
                data = response.json()
                if 'images' in data and len(data['images']) > 0:
                    image_data = base64.b64decode(data['images'][0])
                    image = Image.open(BytesIO(image_data))
                    return image
            return None
        except:
            return None
    
    @staticmethod
    def generate_with_lexica(text, width=768, height=768):
        """Image generation using Lexica API"""
        try:
            encoded_text = quote(text)
            url = f"https://lexica.art/api/v1/search?q={encoded_text}"
            
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('images') and len(data['images']) > 0:
                    image_url = data['images'][0]['src']
                    img_response = requests.get(image_url)
                    image = Image.open(BytesIO(img_response.content))
                    image = image.resize((width, height), Image.Resampling.LANCZOS)
                    return image
            return None
        except:
            return None

    @staticmethod
    def generate_text_to_image_pil(text, width=1024, height=1024):
        """Generate image from text using PIL with text-based design"""
        seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # Create background based on text analysis
        words = text.lower().split()
        
        # Determine color scheme based on text content
        warm_words = ['sunset', 'sun', 'fire', 'hot', 'warm', 'red', 'orange', 'golden', 'sunrise']
        cool_words = ['ocean', 'water', 'ice', 'cold', 'blue', 'sky', 'night', 'moon', 'space', 'winter']
        nature_words = ['forest', 'tree', 'mountain', 'nature', 'green', 'garden', 'flower', 'river', 'lake']
        urban_words = ['city', 'building', 'street', 'urban', 'night', 'neon', 'cyberpunk', 'modern']
        
        # Analyze text theme
        theme_score = {'warm': 0, 'cool': 0, 'nature': 0, 'urban': 0}
        for word in words:
            if word in warm_words:
                theme_score['warm'] += 1
            if word in cool_words:
                theme_score['cool'] += 1
            if word in nature_words:
                theme_score['nature'] += 1
            if word in urban_words:
                theme_score['urban'] += 1
        
        # Set color palette based on theme
        if theme_score['warm'] > theme_score['cool']:
            bg_colors = [(255, 150, 50), (255, 100, 30), (255, 180, 80), (255, 140, 60)]
            gradient_start = (255, 120, 40)
            gradient_end = (255, 200, 100)
        elif theme_score['cool'] > theme_score['warm']:
            bg_colors = [(50, 100, 200), (30, 80, 180), (80, 130, 220), (60, 110, 200)]
            gradient_start = (20, 50, 150)
            gradient_end = (100, 180, 240)
        elif theme_score['nature'] > 0:
            bg_colors = [(50, 150, 50), (30, 120, 30), (80, 180, 80), (60, 160, 60)]
            gradient_start = (20, 100, 20)
            gradient_end = (100, 200, 100)
        else:
            bg_colors = [(100, 100, 150), (80, 80, 130), (120, 120, 170), (90, 90, 140)]
            gradient_start = (50, 50, 100)
            gradient_end = (150, 150, 200)
        
        # Create gradient background
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        for y in range(height):
            ratio = y / height
            r = int(gradient_start[0] + (gradient_end[0] - gradient_start[0]) * ratio)
            g = int(gradient_start[1] + (gradient_end[1] - gradient_start[1]) * ratio)
            b = int(gradient_start[2] + (gradient_end[2] - gradient_start[2]) * ratio)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        draw = ImageDraw.Draw(image)
        
        # Draw themed elements based on text
        if theme_score['nature'] > 0:
            # Draw mountains
            for i in range(random.randint(3, 6)):
                x1 = random.randint(0, width)
                x2 = random.randint(0, width)
                mountain_height = random.randint(height//3, height//2)
                points = [(x1, height), (x1 + (x2-x1)//2, height - mountain_height), (x2, height)]
                color = (random.randint(30, 80), random.randint(80, 150), random.randint(30, 80))
                draw.polygon(points, fill=color)
            
            # Draw trees
            for i in range(random.randint(5, 15)):
                x = random.randint(0, width)
                y = random.randint(height//2, height - 50)
                size = random.randint(20, 60)
                # Trunk
                draw.rectangle([x-size//8, y-size//2, x+size//8, y], fill=(101, 67, 33))
                # Leaves
                draw.ellipse([x-size//2, y-size, x+size//2, y], fill=(random.randint(20, 80), random.randint(80, 160), random.randint(20, 60)))
        
        elif theme_score['urban'] > 0:
            # Draw buildings
            for i in range(random.randint(5, 10)):
                x = random.randint(0, width - 100)
                building_width = random.randint(60, 150)
                building_height = random.randint(100, height//2)
                y = height - building_height
                color = (random.randint(50, 100), random.randint(50, 100), random.randint(80, 150))
                draw.rectangle([x, y, x + building_width, height], fill=color)
                # Windows
                for wy in range(y + 10, height - 10, 20):
                    for wx in range(x + 10, x + building_width - 10, 15):
                        if random.random() > 0.3:
                            window_color = (255, 255, 150) if random.random() > 0.5 else (100, 100, 120)
                            draw.rectangle([wx, wy, wx+8, wy+12], fill=window_color)
        
        elif theme_score['warm'] > 0:
            # Draw sun
            sun_x = width // 2 + random.randint(-100, 100)
            sun_y = height // 3
            sun_size = random.randint(80, 150)
            draw.ellipse([sun_x - sun_size, sun_y - sun_size, sun_x + sun_size, sun_y + sun_size], 
                        fill=(255, 200, 50))
            # Rays
            for angle in range(0, 360, 30):
                import math
                rad = math.radians(angle)
                x1 = sun_x + int(sun_size * 0.9 * math.cos(rad))
                y1 = sun_y + int(sun_size * 0.9 * math.sin(rad))
                x2 = sun_x + int(sun_size * 1.5 * math.cos(rad))
                y2 = sun_y + int(sun_size * 1.5 * math.sin(rad))
                draw.line([(x1, y1), (x2, y2)], fill=(255, 220, 100), width=3)
        
        elif theme_score['cool'] > 0:
            # Draw stars
            for i in range(random.randint(50, 100)):
                x = random.randint(0, width)
                y = random.randint(0, height//2)
                star_size = random.randint(1, 3)
                draw.ellipse([x, y, x+star_size, y+star_size], fill=(255, 255, 255))
            
            # Draw moon
            moon_x = width * 3 // 4
            moon_y = height // 4
            moon_size = random.randint(50, 100)
            draw.ellipse([moon_x - moon_size, moon_y - moon_size, moon_x + moon_size, moon_y + moon_size], 
                        fill=(240, 240, 250))
        
        # Add floating particles/shapes based on text
        for word in words[:10]:
            for _ in range(5):
                x = random.randint(50, width - 50)
                y = random.randint(50, height - 50)
                size = random.randint(10, 40)
                alpha = random.randint(30, 80)
                color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                
                shape = random.choice(['circle', 'diamond'])
                if shape == 'circle':
                    draw.ellipse([x, y, x+size, y+size], fill=color)
                else:
                    draw.polygon([(x, y-size//2), (x+size//2, y), (x, y+size//2), (x-size//2, y)], fill=color)
        
        # Add main text overlay with styling
        try:
            # Calculate optimal font size
            font_size = min(80, width // 12)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Word wrap the text
        max_chars_per_line = width // (font_size // 2)
        wrapped_text = textwrap.fill(text, width=max_chars_per_line)
        lines = wrapped_text.split('\n')
        
        # Calculate total text height
        total_text_height = 0
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_height = bbox[3] - bbox[1] + 15
            line_heights.append(line_height)
            total_text_height += line_height
        
        # Center text vertically
        start_y = (height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = start_y
            
            # Background box for text readability
            padding = 25
            box_coords = [
                x - padding,
                y - padding,
                x + text_width + padding,
                y + text_height + padding
            ]
            draw.rectangle(box_coords, fill=(0, 0, 0, 180))
            
            # Text shadow
            shadow_offset = max(2, font_size // 30)
            draw.text((x + shadow_offset, y + shadow_offset), line, font=font, fill=(0, 0, 0))
            
            # Main text
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
            
            start_y += line_heights[i]
        
        # Apply effects
        image = image.filter(ImageFilter.SMOOTH)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.15)
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        return image

class AIImageGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Text to Image Generator - By CHOWDHURY-VAI")
        self.root.geometry("1200x750")
        self.root.configure(bg="#0a0a1a")
        self.root.minsize(1100, 700)
        
        self.center_window()
        
        self.apis = FreeAIAPIs()
        self.current_image = None
        self.is_generating = False
        
        self.styles = {
            "Realistic": "photorealistic, 8k, highly detailed, professional photography",
            "Anime": "anime style, manga, studio ghibli, beautiful illustration",
            "Digital Art": "digital art, concept art, trending on artstation, detailed",
            "Oil Painting": "oil painting, masterpiece, classical art, detailed brushstrokes",
            "Watercolor": "watercolor painting, artistic, soft colors, beautiful",
            "3D Render": "3d render, octane render, cinema 4d, realistic lighting",
            "Pixel Art": "pixel art, 8-bit, retro gaming style, pixelated",
            "Cyberpunk": "cyberpunk, neon lights, futuristic, sci-fi, blade runner style",
            "Fantasy": "fantasy art, magical, epic, detailed fantasy illustration",
            "Minimalist": "minimalist, simple, clean lines, modern design",
            "Abstract": "abstract art, modern art, geometric, colorful",
            "Sketch": "pencil sketch, hand-drawn, black and white, detailed sketch"
        }
        
        self.setup_ui()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 1200
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg="#0a0a1a")
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left Panel
        left_panel = tk.Frame(main_container, bg="#0d1117", width=420)
        left_panel.pack(side="left", fill="both", padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # Header
        header_frame = tk.Frame(left_panel, bg="#161b22", height=60)
        header_frame.pack(fill="x", pady=(0, 5))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🤖 AI IMAGE GENERATOR", 
                font=("Arial", 14, "bold"), bg="#161b22", fg="#58a6ff").pack(pady=3)
        tk.Label(header_frame, text="Free AI Powered • No API Key Needed", 
                font=("Arial", 8), bg="#161b22", fg="#8b949e").pack()
        
        # Scrollable content
        canvas = tk.Canvas(left_panel, bg="#0d1117", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0d1117")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=400)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Text Input Section
        input_frame = tk.LabelFrame(scrollable_frame, text="📝 Text Prompt", 
                                   font=("Arial", 10, "bold"), bg="#0d1117", 
                                   fg="#58a6ff", relief="flat", bd=1)
        input_frame.pack(fill="x", padx=8, pady=5)
        
        # Quick suggestions
        suggestions_frame = tk.Frame(input_frame, bg="#0d1117")
        suggestions_frame.pack(fill="x", padx=5, pady=3)
        
        suggestions = ["🌅 Sunset", "🏰 Castle", "🐉 Dragon", "🚀 Space", "🌸 Nature"]
        
        for sug in suggestions:
            tk.Button(suggestions_frame, text=sug, bg="#21262d", fg="#c9d1d9",
                     font=("Arial", 7), relief="flat", padx=6, pady=1,
                     command=lambda s=sug: self.add_suggestion(s)).pack(side="left", padx=1)
        
        self.prompt_text = scrolledtext.ScrolledText(input_frame, height=4, 
                                                     font=("Arial", 10),
                                                     bg="#161b22", fg="#c9d1d9", 
                                                     insertbackground="#58a6ff",
                                                     relief="flat", bd=3, wrap="word")
        self.prompt_text.pack(fill="x", padx=5, pady=3)
        self.prompt_text.insert("1.0", "A beautiful sunset over mountains with golden sky, digital art")
        
        # Negative prompt
        neg_frame = tk.Frame(input_frame, bg="#0d1117")
        neg_frame.pack(fill="x", padx=5, pady=3)
        
        tk.Label(neg_frame, text="Negative Prompt:", bg="#0d1117", fg="#8b949e", 
                font=("Arial", 8)).pack(anchor="w")
        
        self.negative_prompt = tk.Entry(neg_frame, bg="#161b22", fg="#c9d1d9", 
                                       relief="flat", font=("Arial", 9))
        self.negative_prompt.pack(fill="x", pady=1)
        self.negative_prompt.insert(0, "ugly, blurry, low quality, distorted")
        
        # Style Selection
        style_frame = tk.LabelFrame(scrollable_frame, text="🎨 Style Preset", 
                                   font=("Arial", 10, "bold"), bg="#0d1117", 
                                   fg="#58a6ff", relief="flat", bd=1)
        style_frame.pack(fill="x", padx=8, pady=5)
        
        self.style_var = tk.StringVar(value="Digital Art")
        style_combo = ttk.Combobox(style_frame, textvariable=self.style_var, 
                                   values=list(self.styles.keys()), state="readonly",
                                   font=("Arial", 9))
        style_combo.pack(fill="x", padx=8, pady=5)
        style_combo.bind('<<ComboboxSelected>>', self.on_style_change)
        
        # AI Model Selection
        model_frame = tk.LabelFrame(scrollable_frame, text="🤖 AI Model", 
                                   font=("Arial", 10, "bold"), bg="#0d1117", 
                                   fg="#58a6ff", relief="flat", bd=1)
        model_frame.pack(fill="x", padx=8, pady=5)
        
        self.models = {
            "Pollinations AI (Fast & Free)": "pollinations",
            "Prodia AI (High Quality)": "prodia",
            "Craiyon (Creative Art)": "craiyon",
            "Lexica (Artistic Style)": "lexica",
            "Local AI (Text-Based Design)": "local",
            "🌟 Auto (Best Available)": "auto"
        }
        
        self.model_var = tk.StringVar(value="🌟 Auto (Best Available)")
        for model_name in self.models.keys():
            tk.Radiobutton(model_frame, text=model_name, variable=self.model_var, 
                          value=model_name, bg="#0d1117", fg="#c9d1d9", 
                          selectcolor="#0d1117", activebackground="#0d1117",
                          activeforeground="#58a6ff", font=("Arial", 9),
                          anchor="w").pack(fill="x", padx=8, pady=1)
        
        # Image Settings
        settings_frame = tk.LabelFrame(scrollable_frame, text="⚙️ Image Settings", 
                                      font=("Arial", 10, "bold"), bg="#0d1117", 
                                      fg="#58a6ff", relief="flat", bd=1)
        settings_frame.pack(fill="x", padx=8, pady=5)
        
        # Quality selection
        quality_row = tk.Frame(settings_frame, bg="#0d1117")
        quality_row.pack(fill="x", padx=8, pady=3)
        
        tk.Label(quality_row, text="Quality:", bg="#0d1117", fg="#8b949e", 
                font=("Arial", 9), width=8, anchor="w").pack(side="left")
        
        self.quality_var = tk.StringVar(value="HD")
        quality_combo = ttk.Combobox(quality_row, textvariable=self.quality_var,
                                     values=["SD (512px)", "HD (768px)", "Full HD (1024px)", 
                                            "2K (1440px)", "4K (2048px)"], 
                                     state="readonly", font=("Arial", 9), width=18)
        quality_combo.pack(side="left", padx=5)
        
        # Seed
        seed_row = tk.Frame(settings_frame, bg="#0d1117")
        seed_row.pack(fill="x", padx=8, pady=3)
        
        tk.Label(seed_row, text="Seed:", bg="#0d1117", fg="#8b949e", 
                font=("Arial", 9), width=8, anchor="w").pack(side="left")
        
        self.seed_var = tk.StringVar(value="-1 (Random)")
        seed_entry = tk.Entry(seed_row, textvariable=self.seed_var, 
                             bg="#161b22", fg="white", relief="flat",
                             font=("Arial", 9), width=15)
        seed_entry.pack(side="left", padx=5)
        
        # Generate Button
        button_frame = tk.Frame(scrollable_frame, bg="#0d1117")
        button_frame.pack(fill="x", padx=8, pady=10)
        
        self.generate_btn = tk.Button(button_frame, text="🎨 GENERATE IMAGE", 
                                      font=("Arial", 12, "bold"), bg="#238636", 
                                      fg="white", height=2, relief="flat",
                                      command=self.generate_image, cursor="hand2")
        self.generate_btn.pack(fill="x", pady=2)
        
        # Progress and Status
        status_frame = tk.Frame(scrollable_frame, bg="#0d1117")
        status_frame.pack(fill="x", padx=8, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                           maximum=100, mode='determinate', length=380)
        self.progress_bar.pack(fill="x", pady=2)
        
        self.status_label = tk.Label(status_frame, text="✅ Ready to generate...", 
                                    bg="#0d1117", fg="#58a6ff", font=("Arial", 8),
                                    anchor="w")
        self.status_label.pack(fill="x")
        
        # Right Panel - Single Large Preview
        right_panel = tk.Frame(main_container, bg="#0d1117")
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Preview header
        preview_header = tk.Frame(right_panel, bg="#161b22", height=45)
        preview_header.pack(fill="x", pady=(0, 5))
        preview_header.pack_propagate(False)
        
        tk.Label(preview_header, text="🖼️ GENERATED IMAGE", 
                font=("Arial", 12, "bold"), bg="#161b22", fg="#58a6ff").pack(side="left", padx=15)
        
        # Action buttons
        action_frame = tk.Frame(preview_header, bg="#161b22")
        action_frame.pack(side="right", padx=10)
        
        tk.Button(action_frame, text="💾 Save", bg="#238636", fg="white", 
                 relief="flat", font=("Arial", 8), padx=10,
                 command=self.save_image, cursor="hand2").pack(side="left", padx=2)
        tk.Button(action_frame, text="📋 Copy", bg="#21262d", fg="white", 
                 relief="flat", font=("Arial", 8), padx=10,
                 command=self.copy_to_clipboard, cursor="hand2").pack(side="left", padx=2)
        tk.Button(action_frame, text="🔄 Regenerate", bg="#1f6feb", fg="white", 
                 relief="flat", font=("Arial", 8), padx=10,
                 command=self.generate_image, cursor="hand2").pack(side="left", padx=2)
        
        # Single large preview area
        preview_container = tk.Frame(right_panel, bg="#0d1117")
        preview_container.pack(fill="both", expand=True, padx=8, pady=5)
        
        self.preview_frame = tk.Frame(preview_container, bg="#161b22", relief="flat", bd=2)
        self.preview_frame.pack(fill="both", expand=True)
        
        self.preview_label = tk.Label(self.preview_frame, 
                                       text="🤖 AI Generated Image\nWill Appear Here\n\nEnter your prompt and click Generate", 
                                       bg="#161b22", fg="#8b949e", 
                                       font=("Arial", 14, "bold"),
                                       anchor="center")
        self.preview_label.pack(fill="both", expand=True)
        
        # Image info footer
        info_frame = tk.Frame(right_panel, bg="#161b22", height=35)
        info_frame.pack(fill="x", side="bottom")
        info_frame.pack_propagate(False)
        
        self.info_label = tk.Label(info_frame, text="📊 Ready | Developed by CHOWDHURY-VAI", 
                                  bg="#161b22", fg="#8b949e", font=("Arial", 8),
                                  anchor="w", padx=10)
        self.info_label.pack(fill="x")
        
        # Main footer
        footer = tk.Frame(self.root, bg="#0d1117", height=25)
        footer.pack(fill="x", side="bottom")
        
        tk.Label(footer, text="🤖 DEVELOPED BY CHOWDHURY-VAI | AI-Powered Text to Image Generator | 100% FREE", 
                font=("Arial", 8, "bold"), bg="#0d1117", fg="#e94560").pack(expand=True)
    
    def add_suggestion(self, suggestion):
        """Add suggestion to prompt"""
        current = self.prompt_text.get("1.0", tk.END).strip()
        suggestion_text = suggestion.split(' ', 1)[1] if ' ' in suggestion else suggestion
        if current and current != "Enter your prompt here...":
            self.prompt_text.insert(tk.END, f", {suggestion_text}")
        else:
            self.prompt_text.delete("1.0", tk.END)
            self.prompt_text.insert("1.0", suggestion_text)
    
    def on_style_change(self, event=None):
        """Handle style change"""
        style = self.style_var.get()
        style_prompt = self.styles.get(style, "")
        
        if style_prompt:
            current_prompt = self.prompt_text.get("1.0", tk.END).strip()
            if style_prompt not in current_prompt:
                self.prompt_text.insert(tk.END, f", {style_prompt}")
    
    def enhance_prompt(self, text):
        """Enhance prompt with quality keywords"""
        quality_map = {
            "SD (512px)": "",
            "HD (768px)": "high quality, detailed",
            "Full HD (1024px)": "full HD, highly detailed, sharp focus",
            "2K (1440px)": "2K resolution, ultra detailed, professional photography",
            "4K (2048px)": "4K, 8K, ultra high resolution, masterpiece, trending on artstation"
        }
        
        quality = self.quality_var.get()
        quality_text = quality_map.get(quality, "")
        
        enhanced = f"{text}, {quality_text}"
        return enhanced.strip(", ")
    
    def generate_image(self):
        """Generate single AI image"""
        if self.is_generating:
            messagebox.showinfo("Busy", "Already generating image. Please wait...")
            return
        
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt or prompt == "Enter your prompt here...":
            messagebox.showwarning("Empty Prompt", "Please enter a text prompt!")
            return
        
        # Update preview to show loading
        self.preview_label.configure(image="", text="⏳\nGenerating...\nPlease wait...", 
                                      bg="#161b22", fg="#58a6ff")
        
        self.is_generating = True
        self.generate_btn.configure(state="disabled", text="⏳ Generating...")
        self.progress_var.set(0)
        self.status_label.configure(text="🎨 Generating AI image... Please wait...")
        
        thread = threading.Thread(target=self._generate_image_thread, args=(prompt,))
        thread.daemon = True
        thread.start()
    
    def _generate_image_thread(self, prompt):
        """Background image generation"""
        try:
            enhanced_prompt = self.enhance_prompt(prompt)
            
            # Get dimensions
            quality = self.quality_var.get()
            dimensions = {
                "SD (512px)": (512, 512),
                "HD (768px)": (768, 768),
                "Full HD (1024px)": (1024, 1024),
                "2K (1440px)": (1440, 1440),
                "4K (2048px)": (2048, 2048)
            }
            width, height = dimensions.get(quality, (1024, 1024))
            
            model = self.models[self.model_var.get()]
            image = None
            errors = []
            
            self.root.after(0, lambda: self.progress_var.set(20))
            
            # Generate based on selected model
            if model == "auto":
                # Try Pollinations first (fastest)
                self.root.after(0, lambda: self.status_label.configure(text="🎨 Trying Pollinations AI..."))
                image = self.apis.generate_with_pollinations(enhanced_prompt, width, height)
                self.root.after(0, lambda: self.progress_var.set(50))
                
                if image is None:
                    # Try Prodia
                    self.root.after(0, lambda: self.status_label.configure(text="🎨 Trying Prodia AI..."))
                    image = self.apis.generate_with_prodia(enhanced_prompt, width, height)
                    self.root.after(0, lambda: self.progress_var.set(70))
                
                if image is None:
                    # Fallback to text-based design
                    self.root.after(0, lambda: self.status_label.configure(text="🎨 Creating text-based design..."))
                    image = self.apis.generate_text_to_image_pil(enhanced_prompt, width, height)
                
            elif model == "pollinations":
                image = self.apis.generate_with_pollinations(enhanced_prompt, width, height)
            elif model == "prodia":
                image = self.apis.generate_with_prodia(enhanced_prompt, width, height)
            elif model == "craiyon":
                image = self.apis.generate_with_craiyon(enhanced_prompt)
            elif model == "lexica":
                image = self.apis.generate_with_lexica(enhanced_prompt, width, height)
            elif model == "local":
                image = self.apis.generate_text_to_image_pil(enhanced_prompt, width, height)
            
            self.root.after(0, lambda: self.progress_var.set(90))
            
            if image:
                self.current_image = image
                self.root.after(0, lambda: self._update_preview(image))
                self.root.after(0, lambda: self.progress_var.set(100))
                self.root.after(0, lambda: self.status_label.configure(text="✅ Image generated successfully!"))
                self.root.after(0, lambda: self.info_label.configure(
                    text=f"📊 Size: {image.width}×{image.height} | Prompt: {prompt[:50]}..."))
            else:
                # Final fallback
                self.root.after(0, lambda: self.status_label.configure(text="⚠️ Using local generation..."))
                image = self.apis.generate_text_to_image_pil(enhanced_prompt, width, height)
                
                if image:
                    self.current_image = image
                    self.root.after(0, lambda: self._update_preview(image))
                    self.root.after(0, lambda: self.progress_var.set(100))
                    self.root.after(0, lambda: self.status_label.configure(text="✅ Image generated (Local mode)!"))
                else:
                    raise Exception("All generation methods failed")
        
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Generation failed: {str(e)}"))
            self.root.after(0, lambda: self.progress_var.set(0))
            self.root.after(0, lambda: self.preview_label.configure(
                text="❌ Generation Failed\nTry again...", bg="#161b22", fg="#ff6b6b"))
        
        finally:
            self.root.after(0, self._generation_complete)
    
    def _update_preview(self, image):
        """Update preview with generated image"""
        # Get preview frame size
        self.preview_frame.update_idletasks()
        frame_width = self.preview_frame.winfo_width()
        frame_height = self.preview_frame.winfo_height()
        
        if frame_width < 100:
            frame_width = 700
        if frame_height < 100:
            frame_height = 500
        
        # Resize image to fit frame while maintaining aspect ratio
        preview = image.copy()
        preview.thumbnail((frame_width - 20, frame_height - 20), Image.Resampling.LANCZOS)
        
        from PIL import ImageTk
        photo = ImageTk.PhotoImage(preview)
        
        self.preview_label.configure(image=photo, text="", bg="#0d1117")
        self.preview_label.image = photo
    
    def _generation_complete(self):
        """Clean up after generation"""
        self.is_generating = False
        self.generate_btn.configure(state="normal", text="🎨 GENERATE IMAGE")
    
    def save_image(self):
        """Save generated image"""
        if not self.current_image:
            messagebox.showwarning("No Image", "Please generate an image first!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"ai_generated_{timestamp}.png"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ],
            initialfile=default_name
        )
        
        if file_path:
            try:
                if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                    self.current_image.save(file_path, 'JPEG', quality=95)
                else:
                    self.current_image.save(file_path, 'PNG')
                
                messagebox.showinfo("Success", 
                    f"✅ Image saved successfully!\n\n"
                    f"📐 Size: {self.current_image.width}×{self.current_image.height}\n"
                    f"📁 Location: {file_path}\n\n"
                    f"🤖 Generated by CHOWDHURY-VAI AI")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy image to clipboard"""
        if not self.current_image:
            messagebox.showwarning("No Image", "Please generate an image first!")
            return
        
        try:
            from io import BytesIO
            output = BytesIO()
            self.current_image.convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]
            output.close()
            
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                self.status_label.configure(text="✅ Image copied to clipboard!")
                messagebox.showinfo("Success", "Image copied to clipboard!")
            except:
                try:
                    import pyperclip
                    pyperclip.copy(data)
                    self.status_label.configure(text="✅ Image copied to clipboard!")
                    messagebox.showinfo("Success", "Image copied to clipboard!")
                except:
                    raise Exception("Clipboard not supported")
                    
        except Exception as e:
            messagebox.showwarning("Clipboard", f"Cannot copy to clipboard: {str(e)}")

def main():
    root = tk.Tk()
    
    try:
        root.iconbitmap('ai_icon.ico')
    except:
        pass
    
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground="#161b22", background="#21262d", 
                   foreground="white", arrowcolor="white")
    style.configure("TProgressbar", background="#58a6ff", troughcolor="#161b22")
    style.configure("Vertical.TScrollbar", background="#21262d", arrowcolor="white")
    
    app = AIImageGenerator(root)
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     🤖 AI-POWERED TEXT TO IMAGE GENERATOR v3.3         ║
    ║     DEVELOPED BY CHOWDHURY-VAI                         ║
    ║                                                          ║
    ║     ✨ Features:                                        ║
    ║     ✓ Single Image Generation                          ║
    ║     ✓ Prompt-Based Accurate Images                     ║
    ║     ✓ 100% FREE - No API Key Required                  ║
    ║     ✓ Multiple AI Models                               ║
    ║     ✓ Style Presets (12 Styles)                        ║
    ║     ✓ Up to 4K Quality                                 ║
    ║     ✓ Text-Analysis Based Design                       ║
    ║     ✓ Large Single Preview                             ║
    ║                                                          ║
    ║     📡 Free APIs:                                       ║
    ║     • Pollinations.ai (Fastest)                        ║
    ║     • Prodia AI (High Quality)                         ║
    ║     • Craiyon (Creative)                               ║
    ║     • Lexica (Artistic)                                ║
    ║     • Local AI (Text-Based Smart Design)               ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    root.mainloop()

if __name__ == "__main__":
    main()
