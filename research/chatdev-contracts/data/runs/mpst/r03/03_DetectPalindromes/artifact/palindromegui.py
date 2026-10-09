self.output.config(state=tk.NORMAL)
self.output.delete("1.0", tk.END)
self.output.insert(tk.END, self.last_report)
self.output.config(state=tk.NORMAL)  # redundant
self.save_button.config(state=tk.NORMAL)