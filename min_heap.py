from copy import deepcopy
from typing import Iterable, Any


class MinHeap:
    """An array-based heap where the root is the smallest element"""

    class _Node:
        # To streamline memory usage
        __slots__ = "key", "value"

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __str__(self):
            return f"({self.key}, {self.value})"

        def __repr__(self):
            return f"({self.key}, {self.value})"

    class EmptyHeapException:
        def __init__(self, msg="Cannot perform operation on an empty heap"):
            super().__init__()
            self.msg = msg

    def __init__(self, elements: Iterable[tuple[Any, Any]] = ()):
        self._elements: list[MinHeap._Node] = [self._Node(k, v) for k, v in elements]
        self._count = len(self._elements)

        if self._count > 1:
            self._bottom_up_construction()

    def __len__(self):
        return self._count

    def __str__(self):
        return str(self._elements)

    def is_empty(self):
        return len(self) == 0

    def insert(self, key, value):
        """Insert an item with key k and value v into the min heap"""
        new_node = MinHeap._Node(key, value)

        self._elements.append(new_node)
        index = self._count
        self._count += 1

        self._sift_up(index)

    def remove_min(self):
        """
        Remove an item with minimum key from the min heap
        :returns: A tuple (k,v) representing the key
         and the value of the removed item
        :raises: `EmptyHeapException`
        """
        if self.is_empty():
            raise self.EmptyHeapException

        new_min = self._elements[self._count - 1]
        old_min = self._elements[0]
        self._elements[0] = new_min
        self._elements.remove(new_min)

        self._count -= 1
        self._sift_down(0)

        return old_min.key, old_min.value

    def min(self):
        """
        Returns, but does not remove the item with minimum key
        :returns: A tuple (k,v) representing the item's key and value
        """
        min_element = self._elements[0]
        return min_element.key, min_element.value

    @staticmethod
    def _parent_index(child_index):
        return (child_index - 1) // 2

    @staticmethod
    def _left_index(parent_index):
        return 2 * parent_index + 1

    @staticmethod
    def _right_index(parent_index):
        return 2 * parent_index + 2

    def _has_left_child(self, parent_index):
        return self._left_index(parent_index) < len(self)

    def _has_right_child(self, parent_index):
        return self._right_index(parent_index) < len(self)

    def _sift_up(self, child_index):
        if child_index > 0:
            parent_index = (child_index - 1) // 2
            if self._elements[parent_index].key > self._elements[child_index].key:
                self._swap(child_index, parent_index)
                self._sift_up(parent_index)

    def _sift_down(self, parent_index):
        left_index = 2 * parent_index + 1
        right_index = 2 * parent_index + 2

        index_of_smallest = parent_index

        if left_index < len(self) and \
                self._elements[parent_index].key > self._elements[left_index].key:
            index_of_smallest = left_index
        elif right_index < len(self) and \
                self._elements[parent_index].key > self._elements[right_index].key:
            index_of_smallest = right_index

        if index_of_smallest != parent_index:
            self._swap(parent_index, index_of_smallest)
            self._sift_down(index_of_smallest)

    def _swap(self, index, other_index):
        self._elements[index], self._elements[other_index] \
            = self._elements[other_index], self._elements[index]

    def _bottom_up_construction(self):
        index_last = len(self) - 1
        start = self._parent_index(index_last)
        for j in range(start, -1, -1):
            self._sift_down(j)

    def __iter__(self):
        return _MinHeapIterator(deepcopy(self))


class _MinHeapIterator:
    """Used to get all  the elements of a min heap in increasing order without altering the min heap"""

    def __init__(self, min_heap: MinHeap):
        self._min_heap = min_heap
        self._count = len(self._min_heap)

    def __iter__(self):
        return self

    def __next__(self):
        if self._count > 0:
            minimum = self._min_heap.remove_min()
            self._count = len(self._min_heap)
            return minimum
        else:
            raise StopIteration
