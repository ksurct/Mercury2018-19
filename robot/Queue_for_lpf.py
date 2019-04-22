# From: https://www.geeksforgeeks.org/queue-set-1introduction-and-array-implementation/
class Queue: 
  
    # __init__ function 
    def __init__(self, capacity): 
        self.front = self.size = 0
        self.rear = capacity -1
        self.Q = [(int)(0)]*capacity 
        self.capacity = capacity 
      
    # Queue is full when size becomes 
    # equal to the capacity  
    def isFull(self): 
        return self.size == self.capacity 
      
    # Queue is empty when size is 0 
    def isEmpty(self): 
        return self.size == 0
  
    # Function to add an item to the queue.  
    # It changes rear and size 
    def EnQueue(self, item): 
        if self.isFull(): 
            print("Full") 
            return
        self.rear = (self.rear + 1) % (self.capacity) 
        self.Q[self.rear] = item 
        self.size = self.size + 1
        print("%s enqueued to queue"  %str(item)) 
  
    # Function to remove an item from queue.  
    # It changes front and size 
    def DeQueue(self): 
        if self.isEmpty(): 
            print("Empty") 
            return
          
        print("%s dequeued from queue" %str(self.Q[self.front])) 
        self.front = (self.front + 1) % (self.capacity) 
        self.size = self.size -1
          
    # Function to get front of queue 
    def que_front(self): 
        if self.isEmpty(): 
            print("Queue is empty") 
  
        print("Front item is", self.Q[self.front]) 
          
    # Function to get rear of queue 
    def que_rear(self): 
        if self.isEmpty(): 
            print("Queue is empty") 
        print("Rear item is",  self.Q[self.rear]) 

    # Function to take the average value of all members of queue
    def get_avg_val(self):
        total = 0
        for i in range(0, self.capacity):
            total += (int)(self.Q[i])
        return (total/self.capacity)

# Driver Code 
if __name__ == '__main__': 
  
    queue = Queue(3)
    queue.EnQueue(10)
    queue.EnQueue(20)
    queue.EnQueue(30)
    print(queue.get_avg_val())
    #queue.EnQueue(10) 
    #queue.EnQueue(20) 
    #queue.EnQueue(30)
    if queue.isFull():
        queue.DeQueue() 
    queue.EnQueue(40)
    print(queue.get_avg_val()) 
    #queue.DeQueue() 
    #queue.que_front() 
    #queue.que_rear() 