import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MOVIES=[
("The Matrix","Action Science Fiction","A hacker discovers reality is a simulation."),
("Inception","Action Science Fiction Thriller","A team enters dreams to plant an idea."),
("Interstellar","Adventure Science Fiction Drama","Explorers travel through space to save humanity."),
("The Dark Knight","Action Crime Drama","A hero faces a dangerous criminal mastermind."),
("Finding Nemo","Animation Adventure Comedy","A father crosses the ocean to find his son."),
("Toy Story","Animation Comedy Family","Toys come alive when humans are away."),
("The Shawshank Redemption","Drama","Two prisoners build friendship and hope."),
("The Godfather","Crime Drama","A powerful family navigates loyalty and crime."),
("Pride and Prejudice","Romance Drama","Two people overcome misunderstandings and fall in love."),
("La La Land","Romance Musical Drama","An actor and musician pursue their dreams."),
("The Hangover","Comedy","Friends try to reconstruct a chaotic night."),
("Jumanji","Adventure Comedy Fantasy","Players are pulled into a magical game."),
("Jurassic Park","Adventure Science Fiction Thriller","A dinosaur theme park becomes dangerous."),
("Titanic","Romance Drama","Two young people fall in love aboard a ship."),
("Coco","Animation Family Fantasy","A boy explores the land of the dead through music."),
("Get Out","Horror Thriller Mystery","A visitor uncovers disturbing secrets.")
]
def recommend():
    genre=choice.get()
    if genre=="Choose genre": messagebox.showinfo("Choose","Select a genre first."); return
    df=pd.DataFrame(MOVIES,columns=["title","genres","plot"])
    features=df["genres"]+" "+df["plot"]
    vectors=TfidfVectorizer(stop_words="english").fit_transform(features)
    query=TfidfVectorizer(stop_words="english")
    # Fit on movie descriptions, then transform the selected genre using the same vectorizer.
    model=TfidfVectorizer(stop_words="english")
    matrix=model.fit_transform(features)
    scores=cosine_similarity(model.transform([genre]),matrix).flatten()
    results.delete(0,tk.END); count=0
    for i in scores.argsort()[::-1]:
        if scores[i]<=0: continue
        results.insert(tk.END,f"{df.iloc[i]['title']}  | similarity {scores[i]:.2f}")
        count+=1
        if count==5: break
    if count==0: results.insert(tk.END,"No close matches in this demo dataset.")
root=tk.Tk(); root.title("Movie Recommendation System"); root.geometry("510x400"); root.configure(bg="#f4f0ff")
tk.Label(root,text="Movie Recommendation System",font=("Arial",18,"bold"),bg="#f4f0ff",fg="#513a78").pack(pady=20)
tk.Label(root,text="Choose a genre",bg="#f4f0ff").pack()
choice=tk.StringVar(value="Choose genre")
tk.OptionMenu(root,choice,"Action","Adventure","Animation","Comedy","Crime","Drama","Fantasy","Horror","Romance","Science Fiction","Thriller","Family","Musical").pack(pady=8)
tk.Button(root,text="Recommend movies",command=recommend,bg="#6d4bc3",fg="white",padx=12,pady=7).pack(pady=8)
results=tk.Listbox(root,width=58,height=12); results.pack(padx=12,pady=10)
tk.Label(root,text="Content-based demo using TF-IDF and cosine similarity.",bg="#f4f0ff",fg="#666").pack(side="bottom",pady=10)
root.mainloop()
