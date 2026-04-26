import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mobi
import shutil
import os
import glob
import threading

class MobiExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mobi漫画提取图片~doubledxm~")
        self.root.geometry("500x420")
        self.root.minsize(450, 350)
        
        self.file_paths = []
        
        # UI Elements
        self.setup_ui()
        
    def setup_ui(self):
        # Apply padding to the main window
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- File Selection Frame ---
        file_frame = ttk.LabelFrame(main_frame, text="电子书文件 (.mobi)")
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Upper part: Listbox
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 0))
        
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(list_frame, yscrollcommand=scroll.set, selectmode=tk.EXTENDED, height=8)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.listbox.yview)
        
        # Lower part: Buttons
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="清空列表", command=self.clear_files).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="移除选中", command=self.remove_selected_files).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="添加文件", command=self.add_files).pack(side=tk.RIGHT)
        
        # --- Output Directory Frame ---
        out_frame = ttk.LabelFrame(main_frame, text="输出目录")
        out_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.output_to_source_var = tk.BooleanVar(value=False)
        cb = ttk.Checkbutton(out_frame, text="输出在源文件夹 (在电子书所在目录下创建图片文件夹)", variable=self.output_to_source_var, command=self.toggle_output_dir)
        cb.pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        self.dir_inner_frame = ttk.Frame(out_frame)
        self.dir_inner_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.output_dir_var = tk.StringVar()
        self.output_dir_var.set(os.path.abspath("./output"))
        
        self.dir_entry = ttk.Entry(self.dir_inner_frame, textvariable=self.output_dir_var)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.browse_btn = ttk.Button(self.dir_inner_frame, text="浏览...", command=self.browse_output_dir)
        self.browse_btn.pack(side=tk.RIGHT)
        
        # --- Action Frame ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(action_frame, text="开始提取", command=self.start_extraction)
        self.start_btn.pack(side=tk.RIGHT)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(action_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪")
        ttk.Label(main_frame, textvariable=self.status_var, anchor=tk.W, foreground="gray").pack(fill=tk.X, pady=(5, 0))

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="选择 Mobi 文件",
            filetypes=[("Mobi 文件", "*.mobi"), ("所有文件", "*.*")]
        )
        for f in files:
            if f not in self.file_paths:
                self.file_paths.append(f)
                self.listbox.insert(tk.END, f)

    def remove_selected_files(self):
        selected_indices = self.listbox.curselection()
        for i in reversed(selected_indices):
            self.listbox.delete(i)
            del self.file_paths[i]

    def clear_files(self):
        self.listbox.delete(0, tk.END)
        self.file_paths.clear()

    def browse_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir_var.set(dir_path)

    def toggle_output_dir(self):
        if self.output_to_source_var.get():
            self.dir_entry.config(state=tk.DISABLED)
            self.browse_btn.config(state=tk.DISABLED)
        else:
            self.dir_entry.config(state=tk.NORMAL)
            self.browse_btn.config(state=tk.NORMAL)

    def update_status(self, text):
        self.status_var.set(text)
        self.root.update_idletasks()

    def start_extraction(self):
        if not self.file_paths:
            messagebox.showwarning("警告", "请先添加要提取的 Mobi 文件！")
            return
            
        output_base_dir = self.output_dir_var.get()
        if not self.output_to_source_var.get() and not output_base_dir:
            messagebox.showwarning("警告", "请设置输出目录！")
            return
            
        self.start_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        
        # 启动后台线程执行提取，避免阻塞主 UI
        threading.Thread(target=self.extraction_process, args=(output_base_dir,), daemon=True).start()

    def extraction_process(self, output_base_dir):
        total_files = len(self.file_paths)
        success_count = 0
        
        for i, file_path in enumerate(self.file_paths):
            self.update_status(f"正在处理 ({i+1}/{total_files}): {os.path.basename(file_path)}")
            
            # 获取电子书名称作为子文件夹名
            book_name = os.path.splitext(os.path.basename(file_path))[0]
            
            if self.output_to_source_var.get():
                source_dir = os.path.dirname(os.path.abspath(file_path))
                book_output_dir = os.path.join(source_dir, book_name)
            else:
                book_output_dir = os.path.join(output_base_dir, book_name)
            
            if self.extract_single_mobi(file_path, book_output_dir):
                success_count += 1
                
            # 更新进度条
            progress = ((i + 1) / total_files) * 100
            self.root.after(0, self.progress_var.set, progress)
            
        self.root.after(0, self.extraction_finished, success_count, total_files)

    def extract_single_mobi(self, mobi_path, output_dir):
        tempdir = None
        try:
            tempdir, filepath = mobi.extract(mobi_path)
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            # 搜索图片
            image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.gif')
            images_found = []
            
            for ext in image_extensions:
                search_path = os.path.join(tempdir, '**', ext)
                images_found.extend(glob.glob(search_path, recursive=True))
                
            if not images_found:
                print(f"[{mobi_path}] 未找到图片")
                return False
                
            # 排序并拷贝图片
            images_found.sort()
            for i, img_path in enumerate(images_found):
                ext = os.path.splitext(img_path)[1]
                new_filename = f"image_{i:04d}{ext}"
                dest_path = os.path.join(output_dir, new_filename)
                shutil.copy2(img_path, dest_path)
                
            return True
            
        except Exception as e:
            print(f"[{mobi_path}] 提取出错: {e}")
            return False
        finally:
            if tempdir and os.path.exists(tempdir):
                try:
                    shutil.rmtree(tempdir)
                except Exception as e:
                    print(f"清理临时目录失败 {tempdir}: {e}")

    def extraction_finished(self, success_count, total_files):
        self.update_status(f"提取完成！成功: {success_count}/{total_files}")
        self.start_btn.config(state=tk.NORMAL)
        messagebox.showinfo("完成", f"批量提取已完成。\n成功提取 {success_count} 个文件。\n输出目录: {self.output_dir_var.get()}")

if __name__ == '__main__':
    root = tk.Tk()
    app = MobiExtractorApp(root)
    root.mainloop()
