btn.bind("<Button-3>", lambda e, rr=r, cc=c: self._on_right_click(rr, cc))
btn.bind("<Control-Button-1>", lambda e, rr=r, cc=c: self._on_right_click(rr, cc))