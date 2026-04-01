import tkinter as tk
from gui import App

from config import USE_LLM, LLM_PROVIDER
from ollama_manager import ensure_ollama_running

if USE_LLM and LLM_PROVIDER == "ollama":
    ensure_ollama_running()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()