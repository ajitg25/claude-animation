import tkinter as tk
from claude_animation.animations.whip import bezier_points, spark_lines

W, H = 820, 420


class WhipWindow:
    def __init__(self, frames: list[dict]) -> None:
        self.frames = frames
        self.idx = 0

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.94)
        self.root.configure(bg='#080808')

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - W) // 2
        y = (sh - H) // 2
        self.root.geometry(f'{W}x{H}+{x}+{y}')

        self.canvas = tk.Canvas(self.root, width=W, height=H,
                                bg='#080808', highlightthickness=0)
        self.canvas.pack()

        # close on click or Escape
        self.root.bind('<Button-1>', lambda _: self.root.destroy())
        self.root.bind('<Escape>', lambda _: self.root.destroy())

        self.root.after(80, self._tick)
        self.root.mainloop()

    def _tick(self) -> None:
        if self.idx >= len(self.frames):
            self.root.destroy()
            return
        frame = self.frames[self.idx]
        self._draw(frame)
        self.idx += 1
        self.root.after(frame['ms'], self._tick)

    def _draw(self, frame: dict) -> None:
        c = self.canvas
        c.delete('all')

        # subtle border
        c.create_rectangle(1, 1, W - 1, H - 1, outline='#222222', width=1)

        pts = bezier_points(frame['p0'], frame['p1'], frame['p2'], frame['p3'])

        if frame['crack']:
            # glow layers
            c.create_line(*pts, fill='#FF8800', width=frame['width'] + 10,
                          smooth=True, capstyle='round')
            c.create_line(*pts, fill='#FFDD00', width=frame['width'] + 4,
                          smooth=True, capstyle='round')

        c.create_line(*pts, fill=frame['color'], width=frame['width'],
                      smooth=True, capstyle='round', joinstyle='round')

        # handle grip
        hx, hy = frame['p0']
        c.create_rectangle(hx - 7, hy - 22, hx + 7, hy + 6,
                           fill='#3E1F00', outline='#7B4A1A', width=2)
        c.create_rectangle(hx - 5, hy - 20, hx + 5, hy + 4,
                           fill='#5C3010', outline='')

        if frame['crack']:
            tx, ty = frame['p3']
            c.create_oval(tx - 36, ty - 36, tx + 36, ty + 36,
                          fill='#FF6600', outline='')
            c.create_oval(tx - 22, ty - 22, tx + 22, ty + 22,
                          fill='#FFD700', outline='')
            c.create_oval(tx - 10, ty - 10, tx + 10, ty + 10,
                          fill='#FFFFFF', outline='')
            for x0, y0, x1, y1 in spark_lines(tx, ty):
                c.create_line(x0, y0, x1, y1, fill='#FFB300', width=2)

        if frame.get('label'):
            text, color, size = frame['label']
            c.create_text(W // 2, H - 45, text=text,
                          fill=color, font=('Helvetica', size, 'bold'))


def play(frames: list[dict]) -> None:
    WhipWindow(frames)
