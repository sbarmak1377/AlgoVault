class Queue:

    def __init__(self, max_len):
        self.max_len = max_len
        self._m_queue = []

    def push(self, data, force=False):
        if len(self._m_queue) == self.max_len and not force:
            print('queue overflow! please pop some elements first!')
        elif len(self._m_queue) == self.max_len and force:
            self.pop()
            self._m_queue.insert(0, data)
        else:
            self._m_queue.insert(0, data)

    def pop(self):
        if len(self._m_queue) == 0:
            print('queue is empty! push elements first!')
        else:
            return self._m_queue.pop(0)

    def get_current_length(self):
        return len(self._m_queue)

    def print_queue(self):
        if len(self._m_queue) == 0:
            print('queue is empty! push elements first!')
        else:
            print(self._m_queue)

def main():
    m_queue = Queue(3)
    m_queue.push(1)
    m_queue.push(2)
    m_queue.push(3)
    m_queue.push(4, force=False)
    m_queue.push(5, force=True)
    print(f"Number of data in queue is: {m_queue.get_current_length()}")
    ret_data = m_queue.pop()
    print(f"Got data: {ret_data}")
    ret_data = m_queue.pop()
    print(f"Got data: {ret_data}")
    print(f"Number of data in queue after 2 pop is: {m_queue.get_current_length()}")
    m_queue.print_queue()


if __name__ == '__main__':
    main()