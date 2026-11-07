import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pywhatkit

def schedule():
    phone=phone_entry.get().strip(); msg=message.get("1.0",tk.END).strip()
    try: hour=int(hour_entry.get()); minute=int(minute_entry.get())
    except ValueError: messagebox.showerror("Time","Enter numeric hour and minute."); return
    if not phone.startswith("+") or not phone[1:].isdigit():
        messagebox.showerror("Phone","Use international format, e.g. +911234567890."); return
    if not msg: messagebox.showerror("Message","Enter a message."); return
    if not (0<=hour<=23 and 0<=minute<=59):
        messagebox.showerror("Time","Hour 0–23; minute 0–59."); return
    now=datetime.now()
    if (hour,minute)<=(now.hour,now.minute):
        messagebox.showerror("Time","Choose a future time later today."); return
    if not messagebox.askyesno("Confirm",f"Send one message to {phone} at {hour:02d}:{minute:02d}?\n\n{msg}\n\nOnly message someone who agreed to receive it."): return
    try:
        pywhatkit.sendwhatmsg(phone,msg,hour,minute,wait_time=20,tab_close=True)
        messagebox.showinfo("Started","WhatsApp Web will open. Sign in if needed and keep your computer online.")
    except Exception as e: messagebox.showerror("Could not schedule",str(e))
root=tk.Tk(); root.title("WhatsApp Message Scheduler"); root.geometry("480x430"); root.configure(bg="#f4f0ff")
tk.Label(root,text="WhatsApp Message Scheduler",font=("Arial",18,"bold"),bg="#f4f0ff",fg="#513a78").pack(pady=18)
def field(label,default=""):
    tk.Label(root,text=label,bg="#f4f0ff").pack()
    e=tk.Entry(root,width=40); e.pack(pady=5); e.insert(0,default); return e
phone_entry=field("Phone number (international format)","+91")
tk.Label(root,text="Message",bg="#f4f0ff").pack()
message=tk.Text(root,width=42,height=5); message.pack(pady=6)
frame=tk.Frame(root,bg="#f4f0ff"); frame.pack(pady=6)
tk.Label(frame,text="Hour (0–23)",bg="#f4f0ff").grid(row=0,column=0)
tk.Label(frame,text="Minute (0–59)",bg="#f4f0ff").grid(row=0,column=1)
hour_entry=tk.Entry(frame,width=8); minute_entry=tk.Entry(frame,width=8)
hour_entry.grid(row=1,column=0,padx=8); minute_entry.grid(row=1,column=1,padx=8)
tk.Button(root,text="Review and schedule",command=schedule,bg="#6d4bc3",fg="white",padx=12,pady=7).pack(pady=10)
tk.Label(root,text="Requires pywhatkit, WhatsApp Web, and internet.",bg="#f4f0ff",fg="#666").pack()
root.mainloop()
