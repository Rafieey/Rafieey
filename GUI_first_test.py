"""
GOD..
FR
"""

import tkinter as tk
import heapq

graph = {
    'A': [('B', 3), ('F', 7)],
    'B': [('A', 3), ('C', 4), ('G', 6)],
    'C': [('B', 4), ('D', 5), ('H', 8)],
    'D': [('C', 5), ('E', 2), ('I', 3)],
    'E': [('D', 2), ('J', 7)],
    'F': [('A', 7), ('G', 3), ('K', 9)],
    'G': [('B', 6), ('F', 3), ('H', 1), ('L', 2)],
    'H': [('C', 8), ('G', 1), ('I', 2), ('M', 4)],
    'I': [('D', 3), ('H', 2), ('J', 3), ('N', 5)],
    'J': [('E', 7), ('I', 3), ('O', 6)],
    'K': [('F', 9), ('L', 4), ('P', 3)],
    'L': [('G', 2), ('K', 4), ('M', 2), ('Q', 7)],
    'M': [('H', 4), ('L', 2), ('N', 1), ('R', 5)],
    'N': [('I', 5), ('M', 1), ('O', 3), ('S', 2)],
    'O': [('J', 6), ('N', 3), ('T', 8)],
    'P': [('K', 3), ('Q', 6), ('U', 4)],
    'Q': [('L', 7), ('P', 6), ('R', 2), ('V', 5)],
    'R': [('M', 5), ('Q', 2), ('S', 3), ('W', 7)],
    'S': [('N', 2), ('R', 3), ('T', 4), ('X', 6)],
    'T': [('O', 8), ('S', 4), ('Y', 3)],
    'U': [('P', 4), ('V', 3)],
    'V': [('Q', 5), ('U', 3), ('W', 2)],
    'W': [('R', 7), ('V', 2), ('X', 1)],
    'X': [('S', 6), ('W', 1), ('Y', 2)],
    'Y': [('T', 3), ('X', 2)],
}

positions = {
    'A': (50, 50), 'B': (120, 50), 'C': (190, 50), 'D': (260, 50), 'E': (330, 50),
    'F': (50, 110), 'G': (120, 110), 'H': (190, 110), 'I': (260, 110), 'J': (330, 110),
    'K': (50, 170), 'L': (120, 170), 'M': (190, 170), 'N': (260, 170), 'O': (330, 170),
    'P': (50, 230), 'Q': (120, 230), 'R': (190, 230), 'S': (260, 230), 'T': (330, 230),
    'U': (50, 290), 'V': (120, 290), 'W': (190, 290), 'X': (260, 290), 'Y': (330, 290),
}

window = tk.Tk()
window.title("گراف و مسیر کوتاه با انیمیشن")

canvas = tk.Canvas(window, width=400, height=350)
canvas.pack()

frame = tk.Frame(window)
frame.pack()

tk.Label(frame, text="شروع:").grid(row=0, column=0)
start_entry = tk.Entry(frame)
start_entry.grid(row=0, column=1)

tk.Label(frame, text="پایان:").grid(row=1, column=0)
end_entry = tk.Entry(frame)
end_entry.grid(row=1, column=1)

result_label = tk.Label(window, text="")
result_label.pack()

btn = tk.Button(frame, text="شروع الگوریتم", command=lambda: start_animation())
btn.grid(row=2, column=0, columnspan=2)


# وضعیت های رنگ:
COLOR_DEFAULT = "lightblue"
COLOR_FRONTIER = "deepskyblue"   # در صف
COLOR_VISITED = "lightgreen"      # قطعی شده
COLOR_CURRENT = "orange"          # در حال پردازش
COLOR_PATH = "red"                # مسیر کوتاه نهایی


class DijkstraAnimator:
    def __init__(self, graph, start, end):
        self.graph = graph
        self.start = start
        self.end = end
        self.distances = {node: float('inf') for node in graph}
        self.distances[start] = 0
        self.previous = {node: None for node in graph}
        self.visited = set()
        self.queue = [(0, start)]
        heapq.heapify(self.queue)
        self.current_node = None
        self.finished = False

        # رنگ‌های گره‌ها
        self.node_colors = {node: COLOR_DEFAULT for node in graph}
        self.node_colors[start] = COLOR_FRONTIER

        # خطوط قرمز مسیر نهایی که بعدا میکشیم
        self.final_path = []

    def step(self):
        if not self.queue:
            self.finished = True
            return

        dist, node = heapq.heappop(self.queue)
        if node in self.visited:
            return

        self.current_node = node
        self.node_colors[node] = COLOR_CURRENT

        # به گره‌های قبلا بازدید شده سبز میدیم
        for v in self.visited:
            self.node_colors[v] = COLOR_VISITED

        # پردازش همسایه‌ها
        for neighbor, weight in self.graph[node]:
            if neighbor not in self.visited:
                new_dist = dist + weight
                if new_dist < self.distances[neighbor]:
                    self.distances[neighbor] = new_dist
                    self.previous[neighbor] = node
                    heapq.heappush(self.queue, (new_dist, neighbor))
                    self.node_colors[neighbor] = COLOR_FRONTIER

        self.visited.add(node)
        if node == self.end:
            self.finished = True
            # مسیر نهایی رو بسازیم
            self.final_path = []
            cur = node
            while cur:
                self.final_path.append(cur)
                cur = self.previous[cur]
            self.final_path.reverse()

    def draw(self):
        canvas.delete("all")

        # رسم یال‌ها با وزن‌ها و رنگ‌ها
        for node in self.graph:
            x1, y1 = positions[node]
            for neighbor, weight in self.graph[node]:
                x2, y2 = positions[neighbor]
                # رنگ یال قرمز اگر در مسیر نهایی باشه
                if self.final_path and node in self.final_path and neighbor in self.final_path:
                    idx_node = self.final_path.index(node)
                    idx_neigh = self.final_path.index(neighbor)
                    if abs(idx_node - idx_neigh) == 1:
                        canvas.create_line(x1, y1, x2, y2, width=3, fill=COLOR_PATH)
                        mid_x = (x1 + x2) // 2
                        mid_y = (y1 + y2) // 2
                        canvas.create_text(mid_x, mid_y, text=str(weight), fill="red", font=("Arial", 10, "bold"))
                        continue

                # رسم عادی
                canvas.create_line(x1, y1, x2, y2, fill="gray")
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                canvas.create_text(mid_x, mid_y, text=str(weight), fill="black", font=("Arial", 8))

        # رسم گره‌ها با رنگ‌های متناسب
        for node in self.graph:
            x, y = positions[node]
            color = self.node_colors.get(node, COLOR_DEFAULT)
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color)
            canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

    def get_result_text(self):
        if self.finished and self.final_path:
            dist = self.distances[self.end]
            path_str = " -> ".join(self.final_path)
            return f"فاصله: {dist}\nمسیر: {path_str}"
        else:
            return "الگوریتم در حال اجراست..."


animator = None

def animation_step():
    global animator
    if animator and not animator.finished:
        animator.step()
        animator.draw()
        result_label.config(text=animator.get_result_text())
        window.after(700, animation_step)  # هر 700 میلی‌ثانیه یک قدم
    elif animator and animator.finished:
        animator.draw()
        result_label.config(text=animator.get_result_text())


def start_animation():
    global animator
    start = start_entry.get().strip().upper()
    end = end_entry.get().strip().upper()
    if (start not in graph) or (end not in graph):
        result_label.config(text="گره وارد شده معتبر نیست.")
        return
    global animator
    animator = DijkstraAnimator(graph, start, end)
    animator.draw()
    result_label.config(text="الگوریتم شروع شد...")
    window.after(500, animation_step)


draw_graph_default = lambda: [canvas.delete("all") or canvas.create_text(200, 160, text="گره‌ها را وارد کنید و روی شروع کلیک کنید.", font=("Arial", 14))]

draw_graph_default()

window.mainloop()
