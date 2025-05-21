import argparse
import os
import sys
import shutil
from PIL import Image
import tkinter as tk
from tkinter import ttk, filedialog
import certifi
import requests
from urllib.parse import urlencode


def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False


def process_images(input_dir, output_transparent, output_opaque):
    os.makedirs(output_transparent, exist_ok=True)
    os.makedirs(output_opaque, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            filepath = os.path.join(input_dir, filename)
            try:
                with Image.open(filepath) as img:
                    if has_transparency(img):
                        shutil.copy2(filepath, output_transparent)
                    else:
                        shutil.copy2(filepath, output_opaque)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")


class ImageClassifierGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PNG透明度分类工具")
        self._create_widgets()

    def _create_widgets(self):
        # 输入目录选择
        ttk.Label(self, text="输入目录:").grid(row=0, column=0, padx=5, pady=5)
        self.input_dir = ttk.Entry(self, width=40)
        self.input_dir.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self, text="浏览...", command=self._select_input_dir).grid(row=0, column=2, padx=5)

        # 输出目录选择
        ttk.Label(self, text="透明输出目录:").grid(row=1, column=0, padx=5, pady=5)
        self.output_transparent = ttk.Entry(self, width=40)
        self.output_transparent.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self, text="浏览...", command=self._select_output_transparent_dir).grid(row=1, column=2, padx=5)

        ttk.Label(self, text="不透明输出目录:").grid(row=2, column=0, padx=5, pady=5)
        self.output_opaque = ttk.Entry(self, width=40)
        self.output_opaque.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self, text="浏览...", command=self._select_output_opaque_dir).grid(row=2, column=2, padx=5)

        # 执行按钮
        self.run_btn = ttk.Button(self, text="开始分类", command=self._run_processing)
        self.run_btn.grid(row=5, column=1, pady=10)

        # 进度状态
        self.status = ttk.Label(self, text="准备就绪")
        self.status.grid(row=6, column=0, columnspan=3)

        # 统计面板
        self.stats_frame = ttk.LabelFrame(self, text="分类结果")
        self.stats_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        ttk.Label(self.stats_frame, text="透明文件:").grid(row=0, column=0)
        self.transparent_count = ttk.Label(self.stats_frame, text="0")
        self.transparent_count.grid(row=0, column=1)

        ttk.Label(self.stats_frame, text="不透明文件:").grid(row=1, column=0)
        self.opaque_count = ttk.Label(self.stats_frame, text="0")
        self.opaque_count.grid(row=1, column=1)

    def _select_input_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir.delete(0, tk.END)
            self.input_dir.insert(0, directory)

    def _select_output_transparent_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_transparent.delete(0, tk.END)
            self.output_transparent.insert(0, directory)

    def _select_output_opaque_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_opaque.delete(0, tk.END)
            self.output_opaque.insert(0, directory)

    def _update_progress(self, transparent, opaque):
        self.transparent_count.config(text=str(transparent))
        self.opaque_count.config(text=str(opaque))

    def _run_processing(self):
        input_dir = self.input_dir.get()
        if not input_dir:
            self.status.config(text="请选择输入目录！", foreground="red")
            return

        self.status.config(text="处理中...", foreground="black")
        self.run_btn.config(state=tk.DISABLED)

        try:
            # 调用核心处理函数
            output_transparent = self.output_transparent.get() or "transparent"
            output_opaque = self.output_opaque.get() or "opaque"
            process_images(input_dir, output_transparent, output_opaque)
            
            # 更新统计结果
            transparent = len(os.listdir(output_transparent))
            opaque = len(os.listdir(output_opaque))
            self._update_progress(transparent, opaque)
            self.status.config(text="处理完成！", foreground="green")
        except Exception as e:
            self.status.config(text=f"错误: {str(e)}", foreground="red")
        finally:
            self.run_btn.config(state=tk.NORMAL)


def main():
    parser = argparse.ArgumentParser(description='分类PNG图片透明度')
    parser.add_argument('input_dir', help='输入目录路径')
    parser.add_argument('--transparent', default='transparent', help='透明图片输出目录')
    parser.add_argument('--opaque', default='opaque', help='不透明图片输出目录')
    
    args = parser.parse_args()
    
    print(f"正在处理目录: {args.input_dir}")
    process_images(args.input_dir, args.transparent, args.opaque)
    print("处理完成，结果保存在:")
    print(f"透明文件: {args.transparent}")
    print(f"不透明文件: {args.opaque}")


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("卡密验证")
        self.geometry("300x200")
        self._create_widgets()
        self.mac = str(uuid.getnode())
        self.version = "1.0"

    def _create_widgets(self):
        ttk.Label(self, text="卡密:").grid(row=0, column=0, padx=5, pady=5)
        self.key_entry = ttk.Entry(self, width=25)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)

        self.auth_btn = ttk.Button(self, text="验证", command=self._do_auth)
        self.auth_btn.grid(row=1, column=0, columnspan=2, pady=5)

        self.status_label = ttk.Label(self, text="等待验证")
        self.status_label.grid(row=2, column=0, columnspan=2)

        self.check_time_btn = ttk.Button(self, text="查询到期时间", 
                                      command=self._check_expire_time)
        self.check_time_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def _do_auth(self):
        key = self.key_entry.get()
        if not key:
            self.status_label.config(text="请输入卡密", foreground="red")
            return

        result = login(SingleCode=key, Ver=self.version, Mac=self.mac)
        if len(result) == 32:
            self.destroy()
            ImageClassifierGUI().mainloop()
        else:
            self.status_label.config(text=f"验证失败: {result}", foreground="red")

    def _check_expire_time(self):
        key = self.key_entry.get()
        if not key:
            return
        expire_time = get_expire_time(UserName=key)
        self.status_label.config(text=f"到期时间: {expire_time}", foreground="blue")

if __name__ == "__main__":
    import uuid
    from eydata import login, get_expire_time
    
    if len([arg for arg in sys.argv if not arg.startswith('@')]) > 1:
        main()
    else:
        LoginWindow().mainloop()
