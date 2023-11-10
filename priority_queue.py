from min_heap import MinHeap


class AdaptablePriorityQueue(MinHeap):
    class Locator(MinHeap._Node):
        __slots__ = "index"

        def __init__(self, key, value, index):
            super().__init__(key, value)
            self.index = index

        def __str__(self):
            return f"({self.key}, {self.value}, {self.index})"

        def __repr__(self):
            return f"({self.key}, {self.value}, {self.index})"

    def __init__(self):
        super().__init__()
        self._elements: list[AdaptablePriorityQueue.Locator] = []

    def _swap(self, index, other_index):
        super()._swap(index, other_index)
        # Reset locators post swap
        self._elements[index].index = index
        self._elements[other_index].index = other_index

    def _bubble(self, index):
        parent_index = self._parent_index(index)
        if index > 0 and self._elements[index].key < self._elements[parent_index].key:
            self._sift_up(index)
        else:
            self._sift_down(index)

    def add(self, key, value):
        token = self.Locator(key, value, len(self))
        self._elements.append(token)
        self._sift_up(len(self))
        self._count += 1
        return token

    def update(self, locator: Locator, new_key, new_value):
        index = locator.index

        if not (0 <= index < len(self) and self._elements[index] is locator):
            raise ValueError("Invalid locator")

        locator.key = new_key
        locator.value = new_value
        self._bubble(index)

    def remove(self, locator: Locator):
        index = locator.index

        if not (0 <= index < len(self) and self._elements[index] is locator):
            raise ValueError("Invalid locator")

        if index == len(self) - 1:
            self._elements.pop()
            self._count -= 1
        else:
            self._swap(index, len(self) - 1)  # Swap item to last position
            self._elements.pop()  # Remove from list
            self._count -= 1
            self._bubble(index)  # Fix item displaced from swap

        return locator.key, locator.value

    def remove_min(self):
        old_min = self._remove_min_helper()
        return old_min.key, old_min.value, old_min.index

    def locators(self):
        return self._elements.__iter__()

    def string_sequential(self):
        output = "["
        j = 0

        for element in self:
            if j < len(self) - 1:
                output += f"{str(element)}, "
            else:
                output += str(element)
            j += 1

        output += "]"

        return output
