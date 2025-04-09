from collections import deque

class ColaMisiones:
    def __init__(self):
        self.misiones = deque()

    def enqueue(self, mission):
        self.misiones.append(mission)

    def dequeue(self):
        if not self.is_empty():
            return self.misiones.popleft()
        return None

    def first(self):
        if not self.is_empty():
            return self.misiones[0]
        return None

    def is_empty(self):
        return len(self.misiones) == 0

    def size(self):
        return len(self.misiones)
