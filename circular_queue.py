class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1

    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front

    def is_empty(self):
        return self.front == -1

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("Queue is full")
        if self.is_empty():
            self.front = 0
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self.queue[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        return item

    def size(self):
        if self.is_empty():
            return 0
        if self.rear >= self.front:
            return self.rear - self.front + 1
        return self.capacity - self.front + self.rear + 1

    def clear(self):
        self.front = self.rear = -1
        self.queue = [None] * self.capacity

    def __str__(self):
        if self.is_empty():
            return "Queue is empty"
        if self.rear >= self.front:
            return "Queue: " + " ".join(str(self.queue[i]) for i in range(self.front, self.rear + 1))
        return "Queue: " + " ".join(str(self.queue[i]) for i in range(self.front, self.capacity)) + " " + " ".join(str(self.queue[i]) for i in range(0, self.rear + 1))