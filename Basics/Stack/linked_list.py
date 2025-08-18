class Node:

    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)


class Stack:

    def __init__(self, max_len):
        self.max_len = max_len
        self._m_stack_head = None

    def push(self, data, force=False):
        if self.get_current_length() == self.max_len and not force:
            print('stack overflow! please pop some elements first!')
        elif self.get_current_length() == self.max_len and force:
            new_node = Node(data)
            self.pop()
            curr = self._m_stack_head
            while curr.next is not None:
                curr = curr.next
            curr.next = new_node
            return
        else:
            new_node = Node(data)
            curr = self._m_stack_head
            if curr is None:
                self._m_stack_head = new_node
                return
            while curr.next is not None:
                curr = curr.next
            curr.next = new_node

    def pop(self):
        if self.get_current_length() == 0:
            print('stack is empty! push elements first!')
        else:
            curr = self._m_stack_head
            before = None
            while curr.next is not None:
                before = curr
                curr = curr.next
            ret_data = curr.data
            before.next = None
            return ret_data

    def get_current_length(self):
        cnt = 0
        if self._m_stack_head is None:
            return cnt
        curr = self._m_stack_head
        while curr is not None:
            cnt += 1
            curr = curr.next
        return cnt

    def print_stack(self):
        if self.get_current_length() == 0:
            print('stack is empty! push elements first!')
        else:
            curr = self._m_stack_head
            while curr is not None:
                print(curr.data)
                curr = curr.next
            return


def main():
    m_stack = Stack(4)
    m_stack.push(1)
    m_stack.push(2)
    m_stack.push(3)
    print(f"Number of data in stack is: {m_stack.get_current_length()}")
    m_stack.push(4, force=False)
    m_stack.push(5, force=True)
    print(f"Number of data in stack is: {m_stack.get_current_length()}")
    ret_data = m_stack.pop()
    print(f"Got data: {ret_data}")
    ret_data = m_stack.pop()
    print(f"Got data: {ret_data}")
    print(f"Number of data in stack after 2 pop is: {m_stack.get_current_length()}")
    m_stack.print_stack()


if __name__ == '__main__':
    main()
