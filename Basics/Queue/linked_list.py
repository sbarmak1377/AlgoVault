class Node:

    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)


class Queue:

    def __init__(self, max_len):
        self.max_len = max_len
        self._m_queue_head = None

    def push(self, data, force=False):
        if self.get_current_length() == self.max_len and not force:
            print('queue overflow! please pop some elements first!')
        elif self.get_current_length() == self.max_len and force:
            new_node = Node(data)
            self.pop()
            new_node.next = self._m_queue_head
            self._m_queue_head = new_node
            return
        else:
            new_node = Node(data)
            curr = self._m_queue_head
            if curr is None:
                self._m_queue_head = new_node
                return
            new_node.next = self._m_queue_head
            self._m_queue_head = new_node

    def pop(self):
        if self.get_current_length() == 0:
            print('queue is empty! push elements first!')
        else:
            ret_data = self._m_queue_head.data
            self._m_queue_head = self._m_queue_head.next
            return ret_data

    def get_current_length(self):
        cnt = 0
        if self._m_queue_head is None:
            return cnt
        curr = self._m_queue_head
        while curr is not None:
            cnt += 1
            curr = curr.next
        return cnt

    def print_queue(self):
        if self.get_current_length() == 0:
            print('queue is empty! push elements first!')
        else:
            curr = self._m_queue_head
            while curr is not None:
                print(curr.data)
                curr = curr.next
            return


def main():
    m_queue = Queue(4)
    m_queue.push(1)
    m_queue.push(2)
    m_queue.push(3)
    print(f"Number of data in queue is: {m_queue.get_current_length()}")
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
