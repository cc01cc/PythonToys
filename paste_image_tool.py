"""
Copyright 2025 Yihong Zheng(zeo, github/cc01cc)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import datetime
from PIL import ImageGrab, Image
import pyperclip
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog

# 默认配置（相对路径根目录）
DEFAULT_ROOT_DIR = os.getcwd()  # 默认当前工作目录
DEFAULT_SAVE_DIR = os.path.join(DEFAULT_ROOT_DIR, "zeoimg")  # 默认保存目录
FILE_PREFIX = "zeoimg_01-"

class ClipboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片粘贴处理器")
        self.root.geometry("500x360")  # 增加高度以容纳新控件
        
        # 初始化目录变量（使用绝对路径）
        self.save_dir = tk.StringVar(value=DEFAULT_SAVE_DIR)
        self.root_dir = tk.StringVar(value=DEFAULT_ROOT_DIR)
        self.file_prefix = FILE_PREFIX
        
        self.create_widgets()
        
        # 绑定快捷键（窗口获得焦点时触发）
        self.root.bind("<Control-v>", self.handle_shortcut)
        self.root.bind("<Command-v>", self.handle_shortcut)

    def create_widgets(self):
        # 创建主框架容器
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 目录设置区域
        dir_frame = ttk.LabelFrame(main_frame, text="路径设置", padding=5)
        dir_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 保存目录选择
        self._create_dir_selector(dir_frame, "保存目录：", self.save_dir, 0)
        
        # 根目录选择
        self._create_dir_selector(dir_frame, "相对路径根目录：", self.root_dir, 1)

        # 状态显示区域
        self.status_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=60,
            height=10,
            font=("Consolas", 10)
        )
        self.status_text.pack(pady=5, expand=True, fill=tk.BOTH)

        # 操作说明
        ttk.Label(
            main_frame,
            text="提示：聚焦本窗口后按 Ctrl+V (Windows) 或 Cmd+V (macOS) 粘贴图片",
            foreground="gray"
        ).pack(pady=(0, 5))

    def _create_dir_selector(self, parent, label_text, var, row):
        """创建目录选择控件组"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame, text=label_text).pack(side=tk.LEFT)
        
        entry = ttk.Entry(frame, textvariable=var)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 5))
        
        ttk.Button(
            frame, 
            text="浏览...", 
            command=lambda: self.browse_directory(var)
        ).pack(side=tk.LEFT)

    def browse_directory(self, var):
        """浏览并选择目录"""
        current_path = var.get()
        initial_dir = current_path if os.path.exists(current_path) else DEFAULT_ROOT_DIR
        
        selected_dir = filedialog.askdirectory(
            title=f"选择{var._name.split('_')[-1]}",
            initialdir=initial_dir
        )
        if selected_dir:
            var.set(os.path.abspath(selected_dir))  # 确保存储绝对路径
            self.log(f"[OK] 已更新目录：{selected_dir}")

    def log(self, message):
        """状态日志输出"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)

    def process_clipboard_image(self):
        """核心逻辑：从剪贴板获取图片 → 保存 → 生成Markdown链接"""
        try:
            # 1. 从剪贴板获取图片
            img = ImageGrab.grabclipboard()
            if not img or not isinstance(img, Image.Image):
                self.log("[!] 剪贴板内容不是图片")
                return
            
            # 2. 生成文件名（时间戳防重复）
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.file_prefix}{timestamp}.png"
            
            # 3. 保存图片
            save_dir = os.path.abspath(self.save_dir.get())
            os.makedirs(save_dir, exist_ok=True)  # 确保目录存在
            save_path = os.path.join(save_dir, filename)
            img.save(save_path)
            self.log(f"[OK] 图片已保存：{save_path}")
            
            # 4. 生成Markdown链接（基于根目录的相对路径）
            root_dir = os.path.abspath(self.root_dir.get())
            try:
                # 计算相对路径
                rel_path = os.path.relpath(save_path, start=root_dir)
                # if rel_path.startswith(".."):
                #     # 警告：保存路径不在根目录下
                #     self.log(f"[WARN] 保存路径不在根目录下，使用绝对路径代替")
                #     rel_path = save_path
            except ValueError:
                # Windows下跨盘符时抛出异常
                self.log(f"[WARN] 跨盘符路径，使用绝对路径代替")
                rel_path = save_path
                
            md_path = rel_path.replace("\\", "/")
            md_link = f"![{filename}]({md_path})"
            
            # 5. 将链接复制回剪贴板
            pyperclip.copy(md_link)
            self.log(f"[CLP] Markdown链接已复制：{md_link}")
            
        except Exception as e:
            self.log(f"[ERR] 处理失败：{e}")

    def handle_shortcut(self, event=None):
        """快捷键事件处理"""
        self.log("[ACT] 检测到快捷键，开始处理图片...")
        self.process_clipboard_image()
        return "break"  # 阻止事件传递

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardApp(root)
    root.mainloop()