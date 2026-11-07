import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path
import shutil

CATS = {".jpg":"Images",".jpeg":"Images",".png":"Images",".gif":"Images",
".pdf":"Documents",".docx":"Documents",".txt":"Documents",".xlsx":"Documents",
".mp4":"Videos",".mov":"Videos",".zip":"Archives",".rar":"Archives"}

class App:
    def __init__(self, root):
        self.root=root; self.folder=Path.home()
        root.title("File Manager"); root.geometry("760x500"); root.configure(bg="#f4f0ff")
        tk.Label(root,text="File Manager",font=("Arial",21,"bold"),bg="#f4f0ff",fg="#513a78").pack(pady=12)
        bar=tk.Frame(root); bar.pack()
        for label, fn in [("Choose folder",self.choose),("Organize",self.organize),("New folder",self.new),
                          ("Rename",self.rename),("Copy",self.copy),("Move",self.move),("Delete",self.delete)]:
            tk.Button(bar,text=label,command=fn).pack(side="left",padx=3)
        self.path=tk.Label(root,bg="#f4f0ff"); self.path.pack(pady=8)
        self.search=tk.Entry(root,width=40); self.search.pack()
        tk.Button(root,text="Search / Refresh",command=self.refresh).pack(pady=4)
        self.items=tk.Listbox(root,width=90,height=19); self.items.pack(padx=12,pady=8,fill="both",expand=True)
        self.refresh()
    def choose(self):
        p=filedialog.askdirectory()
        if p: self.folder=Path(p); self.refresh()
    def refresh(self):
        self.path.config(text=str(self.folder)); self.items.delete(0,tk.END)
        q=self.search.get().casefold()
        try:
            for p in sorted(self.folder.iterdir()):
                if q in p.name.casefold(): self.items.insert(tk.END,("[DIR] " if p.is_dir() else "[FILE] ")+p.name)
        except OSError as e: messagebox.showerror("Error",str(e))
    def selected(self):
        s=self.items.curselection()
        if not s: messagebox.showinfo("Select item","Select an item first."); return None
        name=self.items.get(s[0])[6:] if self.items.get(s[0]).startswith("[FILE]") else self.items.get(s[0])[6:]
        return self.folder/name
    def new(self):
        n=simpledialog.askstring("New folder","Name:")
        if n:
            try: (self.folder/n).mkdir(); self.refresh()
            except OSError as e: messagebox.showerror("Error",str(e))
    def rename(self):
        p=self.selected()
        if p:
            n=simpledialog.askstring("Rename","New name:",initialvalue=p.name)
            if n:
                try: p.rename(p.with_name(n)); self.refresh()
                except OSError as e: messagebox.showerror("Error",str(e))
    def copy(self):
        p=self.selected(); d=filedialog.askdirectory()
        if p and d:
            try:
                dest=Path(d)/p.name
                if dest.exists(): raise FileExistsError("Destination already exists.")
                shutil.copytree(p,dest) if p.is_dir() else shutil.copy2(p,dest); self.refresh()
            except OSError as e: messagebox.showerror("Copy failed",str(e))
    def move(self):
        p=self.selected(); d=filedialog.askdirectory()
        if p and d:
            try:
                dest=Path(d)/p.name
                if dest.exists(): raise FileExistsError("Destination already exists.")
                shutil.move(str(p),str(dest)); self.refresh()
            except OSError as e: messagebox.showerror("Move failed",str(e))
    def delete(self):
        p=self.selected()
        if p and messagebox.askyesno("Confirm","Permanently delete "+p.name+"?"):
            try: shutil.rmtree(p) if p.is_dir() else p.unlink(); self.refresh()
            except OSError as e: messagebox.showerror("Delete failed",str(e))
    def organize(self):
        if not messagebox.askyesno("Confirm","Organize files in this folder? Choose a test folder first."): return
        count=0
        try:
            for p in list(self.folder.iterdir()):
                if p.is_file():
                    folder=CATS.get(p.suffix.lower(),"Others"); destdir=self.folder/folder; destdir.mkdir(exist_ok=True)
                    dest=destdir/p.name
                    if not dest.exists(): shutil.move(str(p),str(dest)); count+=1
            self.refresh(); messagebox.showinfo("Done",f"Moved {count} files.")
        except OSError as e: messagebox.showerror("Error",str(e))

if __name__=="__main__":
    root=tk.Tk(); App(root); root.mainloop()
