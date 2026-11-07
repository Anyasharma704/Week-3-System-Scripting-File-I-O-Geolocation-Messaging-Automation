import tkinter as tk
from tkinter import messagebox
from urllib.request import Request, urlopen
from pathlib import Path
import json, webbrowser
from datetime import datetime

HISTORY=Path(__file__).with_name("location_history.json")
current={}
def lookup():
    try:
        req=Request("https://ipapi.co/json/",headers={"User-Agent":"PythonLocationTracker/1.0"})
        with urlopen(req,timeout=12) as r: data=json.loads(r.read().decode())
        if data.get("error"): raise RuntimeError(data.get("reason","Lookup failed"))
        current.update(data)
        record={"city":data.get("city"),"country":data.get("country_name"),
                "latitude":data.get("latitude"),"longitude":data.get("longitude"),
                "time":datetime.now().astimezone().isoformat(timespec="seconds")}
        history=json.loads(HISTORY.read_text()) if HISTORY.exists() else []
        history.append(record); HISTORY.write_text(json.dumps(history,indent=2))
        output.config(text=f"{record['city']}, {record['country']}\nLatitude: {record['latitude']}\nLongitude: {record['longitude']}\nSaved lookup: {record['time']}")
        mapbtn.config(state="normal")
    except Exception as e: messagebox.showerror("Lookup failed",str(e))
def show_map():
    webbrowser.open(f"https://www.openstreetmap.org/?mlat={current['latitude']}&mlon={current['longitude']}#map=13/{current['latitude']}/{current['longitude']}")
root=tk.Tk(); root.title("Location Tracker"); root.geometry("480x330"); root.configure(bg="#f4f0ff")
tk.Label(root,text="Location Tracker",font=("Arial",21,"bold"),bg="#f4f0ff",fg="#513a78").pack(pady=22)
tk.Label(root,text="Look up approximate location from your public IP",bg="#f4f0ff").pack()
tk.Button(root,text="Get my location",command=lookup,bg="#6d4bc3",fg="white",padx=14,pady=8).pack(pady=15)
output=tk.Label(root,text="No lookup yet.",bg="#f4f0ff",justify="center"); output.pack(pady=12)
mapbtn=tk.Button(root,text="Open map",command=show_map,state="disabled"); mapbtn.pack()
tk.Label(root,text="IP location is approximate, not GPS. Lookup happens only when clicked.",bg="#f4f0ff",fg="#666",wraplength=420).pack(side="bottom",pady=15)
root.mainloop()
