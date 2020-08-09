class CallStack:
    def __init__(self):
        self.__records = []

    def push(self, item):
        self.__records.append(item)

    def pop(self):
        return self.__records.pop()

    def peek(self):
        return self.__records[-1]

    def is_empty(self):
        return len(self.__records) == 0

    def __repr__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self.__records))
        s = f'CALL STACK\n{s}\n'
        return s


from enum import Enum

class ARType(Enum):
    PROGRAM = 'PROGRAM'
    PROCEDURE = 'PROCEDURE'


class ActivationRecord:
    def __init__(self, name, type, nesting_level):
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.__members = {}

    def __setitem__(self, key, value):
        self.__members[key] = value

    def __getitem__(self, key):
        return self.__members[key]

    def get(self, key):
        return self.__members.get(key)

    def __repr__(self):
        lines = [f'{self.nesting_level}: {self.type} {self.name}']
        for name, val in self.__members.items():
            lines.append(f'{name:<20}: {val}')

        s = '\n'.join(lines)
        return s
