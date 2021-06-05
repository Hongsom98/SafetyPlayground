import tkinter as tk

root = tk.Tk()
photo = tk.PhotoImage(file="Photo/horseRight.gif")
gif_index = 0

def next_frame():
    global gif_index
    try:
        #XXX: Move to the next frame
        photo.configure(format="gif -index {}".format(gif_index))
        gif_index += 1
    except tk.TclError:
        gif_index = 0
        return next_frame()
    else:
        root.after(500, next_frame) # XXX: Fixed animation speed
label = tk.Label(root, image=photo)
label.pack()
root.after_idle(next_frame)
root.mainloop()