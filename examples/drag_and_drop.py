import tkinter as tk


class DragAndDrop(tk.Frame):
    def __init__(self, master):
        """
        Initialize the program
        :param master: tk.Tk
        """
        super().__init__(master)
        self.master = master
        self.configure_master()
        self.initialize_canvas()

    def configure_master(self):
        """
        Configure master window's properties
        :return: None
        """
        self.master.title("Drag And Drop")
        self.master.iconbitmap("dnd.ico")
        self.master.geometry("600x600")
        self.master.resizable(False, False)

    def initialize_canvas(self):
        """
        Set up the canvas and place test objects on it
        :return: None
        """
        self.canvas = tk.Canvas(width=600, height=600, bg="cyan")
        self.canvas.pack()

        self.move_data = {"object": None, "x": 0, "y": 0}

        self.create_objects("movable")
        self.bind_tags("movable")

    def create_objects(self, tag):
        """
        Create example objects with given tag
        :param tag: str
        :return: None
        """
        objs = [(200, 200, "white"), (400, 400, "red"), (200, 400, "green"), (400, 200, "black")]
        for x, y, color in objs:
            self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, outline=color, fill=color, tags=tag)

    def bind_tags(self, tag):
        """
        Binding the given tag to events that correspond to drag and drop action
        :param tag: str
        :return: None
        """
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.move_start)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.move_stop)
        self.canvas.tag_bind(tag, "<B1-Motion>", self.move)

    def move_start(self, event):
        """
        Method that gets called whenever the drag and drop action starts
        :param event: tk.Event
        :return: None
        """
        print(type(event))
        self.move_data["object"] = self.canvas.find_closest(event.x, event.y)[0]
        self.move_data["x"] = event.x
        self.move_data["y"] = event.y
        self.canvas.tag_raise(self.move_data["object"])

    def move_stop(self, event):
        """
        Method that gets called whenever the drag and drop action finishes
        :param event: tk.Event
        :return: None
        """
        self.move_data["object"] = None
        self.move_data["x"] = 0
        self.move_data["y"] = 0

    def move(self, event):
        """
        Method that gets called while the drag and drop action continues
        :param event: tk.Event
        :return: None
        """
        dx = event.x - self.move_data["x"]
        dy = event.y - self.move_data["y"]

        self.canvas.move(self.move_data["object"], dx, dy)

        self.move_data["x"] = event.x
        self.move_data["y"] = event.y


def main():
    root = tk.Tk()
    app = DragAndDrop(root)
    app.mainloop()


if __name__ == "__main__":
    main()
