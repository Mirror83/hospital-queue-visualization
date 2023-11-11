import unittest

from min_heap import MinHeap
from priority_queue import AdaptablePriorityQueue


class TestMinHeapMethods(unittest.TestCase):
    def test_insert(self):
        min_heap = MinHeap()
        min_heap.insert(4, "C")
        min_heap.insert(5, "A")
        min_heap.insert(6, "Z")
        min_heap.insert(15, "K")
        min_heap.insert(9, "F")
        min_heap.insert(7, "Q")
        min_heap.insert(20, "B")
        min_heap.insert(16, "X")
        min_heap.insert(25, "J")
        min_heap.insert(14, "E")
        min_heap.insert(12, "H")
        min_heap.insert(11, "S")
        min_heap.insert(13, "W")
        min_heap.insert(2, "T")
        self.assertEqual(14, len(min_heap))

    def test_min(self):
        min_heap = MinHeap()
        min_heap.insert(25, "J")
        min_heap.insert(12, "H")
        min_heap.insert(14, "E")
        min_heap.insert(16, "X")
        min_heap.insert(2, "T")
        min_heap.insert(11, "S")
        min_heap.insert(13, "W")

        self.assertEqual((2, "T"), min_heap.min())
        self.assertEqual(7, len(min_heap))
        previous_len = len(min_heap)

        minimum = min_heap.remove_min()
        self.assertEqual((2, "T"), minimum)
        self.assertEqual(previous_len - 1, len(min_heap))

    def test_constructor_with_elements(self):
        # Elements not maintaining heap order here. Need to find out why
        min_heap = MinHeap([(11, "A"), (10, "B"), (67, "C"), (14, "D"), (55, "E"), (2, "F"), (27, "G")])
        self.assertEqual(3, len(min_heap))
        self.assertEqual((1, "B"), min_heap.min())

    def test_iterator(self):
        elements = [(11, "A"), (10, "B"), (67, "C"), (14, "D"), (55, "E"), (2, "F"), (27, "G")]
        sorted_elements = sorted(elements)
        min_heap = MinHeap()

        for element in elements:
            min_heap.insert(element[0], element[1])

        pairs = []

        for (k, v) in min_heap:
            pairs.append((k, v))

        self.assertEqual(sorted_elements, pairs)
        self.assertEqual(len(elements), len(min_heap))


class TestAdaptablePriorityQueue(unittest.TestCase):
    def test_remove(self):
        pq = AdaptablePriorityQueue()
        key_locator_dict = dict()
        key_locator_dict[35] = pq.add(35, "F")
        key_locator_dict[10] = pq.add(10, "A")
        prev_len = len(pq)

        print(pq.remove(key_locator_dict[35]))
        print(pq)
        self.assertEqual(prev_len - 1, len(pq))


if __name__ == '__main__':
    unittest.main()
