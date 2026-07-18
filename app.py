import tkinter as tk

root = tk.Tk()
root.title("Gemini Chat")
root.geometry("800x600")

chat_area = tk.Text(
    root, 
    wrap="word",
    state="disabled"
)

chat_area.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

message_entry=tk.Entry(root)
message_entry.pack(
    fill="x",
    padx=10,
    pady=5
)

send_button=tk.Button(
    root,
    text="send"
)

send_button.pack(
    pady=5
)


root.mainloop()

