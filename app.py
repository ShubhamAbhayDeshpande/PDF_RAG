"""
Simple Tkinter GUI for RAG interaction

- Left pane: chat history and input box where the user types a question
- Right pane: retrieved context list (document name, page number, image paths) and a context text preview

The GUI uses the same retrieval + LLM flow as test_main.py but sends the user's input instead of the hard-coded QUERY_TEXT.

Requirements:
- chromadb DB at 'chroma_db' and collection named 'pdf_collection' (same as test_main.py)
- GEMINI_API_KEY in environment or .env (used by LLMAPI)

Usage:
    python app.py

"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import os
import subprocess
import sys

import chromadb

# Import local modules from the repo
import retriever
from llm_api import LLMAPI

# Helpers

def open_file_with_default_app(path):
    if not os.path.exists(path):
        messagebox.showerror("File not found", f"File not found: {path}")
        return
    try:
        if sys.platform.startswith("darwin"):
            subprocess.run(["open", path])
        elif os.name == "nt":
            os.startfile(path)
        else:
            subprocess.run(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("Error opening file", str(e))


class RAGApp:
    def __init__(self, root):
        self.root = root
        root.title("RAG GUI")
        root.geometry("1000x600")

        self._build_ui()

        # initialize chroma client and collection
        try:
            self.client = chromadb.PersistentClient(path=r"chroma_db")
            self.collection = self.client.get_collection(name="pdf_collection")
        except Exception as e:
            self.collection = None
            print("Warning: couldn't open chroma collection:", e)

        # retriever and LLM instances
        self.retriever = retriever.retriever()
        try:
            self.llm = LLMAPI()
        except Exception as e:
            self.llm = None
            print("Warning: LLMAPI not initialized:", e)

    def _build_ui(self):
        # Main panes
        main_pane = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=1)

        left_frame = ttk.Frame(main_pane, width=600)
        right_frame = ttk.Frame(main_pane, width=400)

        main_pane.add(left_frame, weight=3)
        main_pane.add(right_frame, weight=2)

        # Left: Chat history and input
        chat_label = ttk.Label(left_frame, text="Chat")
        chat_label.pack(anchor=tk.W, padx=6, pady=(6, 0))

        self.chat_history = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, state=tk.DISABLED, height=25)
        self.chat_history.pack(fill=tk.BOTH, expand=1, padx=6, pady=6)

        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill=tk.X, padx=6, pady=(0,6))

        self.user_input = ttk.Entry(input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=(0,6))
        self.user_input.bind('<Return>', lambda e: self._on_send())

        self.send_button = ttk.Button(input_frame, text="Send", command=self._on_send)
        self.send_button.pack(side=tk.RIGHT)

        # Right: Retrieved context list and preview
        context_label = ttk.Label(right_frame, text="Retrieved Context")
        context_label.pack(anchor=tk.W, padx=6, pady=(6, 0))

        cols = ("document", "page", "images")
        self.context_tree = ttk.Treeview(right_frame, columns=cols, show='headings', height=12)
        self.context_tree.heading("document", text="Document")
        self.context_tree.heading("page", text="Page")
        self.context_tree.heading("images", text="Image paths (comma-separated)")
        self.context_tree.column("document", width=150)
        self.context_tree.column("page", width=60)
        self.context_tree.column("images", width=180)
        self.context_tree.pack(fill=tk.BOTH, expand=1, padx=6, pady=6)

        # Buttons for selected item
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, padx=6)

        self.open_image_button = ttk.Button(btn_frame, text="Open Selected Image", command=self._open_selected_image)
        self.open_image_button.pack(side=tk.LEFT)

        # Context preview
        preview_label = ttk.Label(right_frame, text="Context Preview")
        preview_label.pack(anchor=tk.W, padx=6, pady=(6, 0))

        self.context_preview = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=10)
        self.context_preview.pack(fill=tk.BOTH, expand=1, padx=6, pady=6)
        self.context_preview.configure(state=tk.DISABLED)

    def _append_chat(self, speaker, text):
        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"{speaker}: {text}\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.configure(state=tk.DISABLED)

    def _on_send(self):
        question = self.user_input.get().strip()
        if not question:
            return
        # disable input while processing
        self.send_button.config(state=tk.DISABLED)
        self.user_input.delete(0, tk.END)
        self._append_chat("User", question)

        thread = threading.Thread(target=self._process_question, args=(question,))
        thread.daemon = True
        thread.start()

    def _process_question(self, question):
        try:
            answer, documents = self._retrieve_and_call_llm(question)
        except Exception as e:
            self._append_chat("System", f"Error during retrieval/LLM call: {e}")
            self.send_button.config(state=tk.NORMAL)
            return

        # update UI with retrieved context and answer
        self.root.after(0, lambda: self._update_context_display(documents))
        self._append_chat("Assistant", answer if answer else "(No answer returned)")
        self.send_button.config(state=tk.NORMAL)

    def _retrieve_and_call_llm(self, question):
        if self.collection is None:
            raise RuntimeError("chroma collection not found. Build the collection first (run test_main.py or ensure chroma_db exists).")

        # 1. compute embedding for query
        query_emb = self.retriever.query_embedding(question)

        # 2. query collection
        result = self.collection.query(
            query_embeddings=query_emb,
            n_results=5
        )

        output_document_lst = result.get("documents") or []
        # Build a context string similar to test_main.py
        CONTEXT = ""
        if len(output_document_lst) > 0 and len(output_document_lst[0])>0:
            for info in output_document_lst[0]:
                CONTEXT += info + "\n"

        # Gather metadata lists
        document_name_lst = []
        image_paths = []
        page_numbers_lst = []
        output_metadata_lst = result.get("metadatas")
        documents_display = []

        if output_metadata_lst and len(output_metadata_lst)>0:
            for individual_metadata in output_metadata_lst[0]:
                # metadata values may be stored as strings; keep safe
                doc_name = individual_metadata.get("document_name")
                pg = individual_metadata.get("page_number")
                image_paths_lst = []
                raw_img = individual_metadata.get("image_paths")
                try:
                    image_paths_lst = json.loads(raw_img) if raw_img else []
                except Exception:
                    # if it's already a list or invalid json
                    if isinstance(raw_img, list):
                        image_paths_lst = raw_img
                    else:
                        image_paths_lst = []

                document_name_lst.append(doc_name)
                page_numbers_lst.append(pg)
                if image_paths_lst:
                    image_paths.extend(image_paths_lst)

                documents_display.append({
                    "document_name": doc_name,
                    "page_number": pg,
                    "image_paths": image_paths_lst,
                })

        # 3. Call LLM API with context
        if self.llm is None:
            raise RuntimeError("LLMAPI not initialized. Check GEMINI_API_KEY in environment or .env file.")

        answer = self.llm.generate_answer(question=question, context=CONTEXT)

        return answer, documents_display

    def _update_context_display(self, documents):
        # Clear current items
        for i in self.context_tree.get_children():
            self.context_tree.delete(i)
        # Populate
        for doc in documents:
            images_str = ", ".join(doc.get("image_paths") or [])
            self.context_tree.insert("", tk.END, values=(doc.get("document_name"), doc.get("page_number"), images_str))

        # Update preview area with concatenated context
        preview_text = ""
        for doc in documents:
            preview_text += f"Document: {doc.get('document_name')}\n"
            preview_text += f"Page: {doc.get('page_number')}\n"
            imgs = doc.get('image_paths') or []
            if imgs:
                preview_text += "Images:\n"
                for p in imgs:
                    preview_text += f"  - {p}\n"
            preview_text += "\n"

        self.context_preview.configure(state=tk.NORMAL)
        self.context_preview.delete(1.0, tk.END)
        self.context_preview.insert(tk.END, preview_text)
        self.context_preview.configure(state=tk.DISABLED)

    def _open_selected_image(self):
        sel = self.context_tree.selection()
        if not sel:
            messagebox.showinfo("No selection", "Please select a context row that contains image paths.")
            return
        item = self.context_tree.item(sel[0])
        values = item.get("values") or []
        if len(values) < 3 or not values[2]:
            messagebox.showinfo("No images", "No image paths available for the selected item.")
            return
        # take first image path from the comma separated list
        images_str = values[2]
        images = [p.strip() for p in images_str.split(",") if p.strip()]
        if not images:
            messagebox.showinfo("No images", "No image paths available for the selected item.")
            return
        # open the first image
        open_file_with_default_app(images[0])


if __name__ == "__main__":
    root = tk.Tk()
    app = RAGApp(root)
    root.mainloop()
