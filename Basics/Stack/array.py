class Stack:

    def __init__(self, max_len):
        self.max_len = max_len
        self._m_stack = []

    def push(self, data, force=False):
        if len(self._m_stack) == self.max_len and not force:
            print('stack overflow! please pop some elements first!')
        elif len(self._m_stack) == self.max_len and force:
            self.pop()
            self._m_stack.append(data)
        else:
            self._m_stack.append(data)

    def pop(self):
        if len(self._m_stack) == 0:
            print('stack is empty! push elements first!')
        else:
            return self._m_stack.pop()

    def get_current_length(self):
        return len(self._m_stack)

    def print_stack(self):
        if len(self._m_stack) == 0:
            print('stack is empty! push elements first!')
        else:
            print(self._m_stack)

def main():
    m_stack = Stack(3)
    m_stack.push(1)
    m_stack.push(2)
    m_stack.push(3)
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