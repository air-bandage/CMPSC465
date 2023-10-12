import math


class PriorityQueue(object):
    def __init__(self, lst=None):
        if lst is None:
            self._heap = []
        else:
            self._heap = lst
        self._size = len(self._heap)
        self._pos = {self._heap[i][1]: i for i in range(self._size)}
        self._build_heap()

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self._heap)

    def _swap(self, idx1, idx2):
        """
        Swap two elements in the priority queue while keep tracking their
        position.
        :param idx1: the index of the first element to be swapped
        :param idx2: the index of the second element to be swapped
        :return:  the element at idx1 and idx2, and their position (in place)
        """
        self._pos[self._heap[idx1][1]], self._pos[self._heap[idx2][1]] = (
            self._pos[self._heap[idx2][1]], self._pos[self._heap[idx1][1]]
        )
        self._heap[idx1], self._heap[idx2] = self._heap[idx2], self._heap[idx1]
        return 0

    def _heap_up(self, k):
        """
        Heapify up the k-th element of a heap.
        :param k: the index of the element to be heapify up
        :return: the updated heap (in place)
        """
        child_index = k
        parent_index: int = math.floor((k - 1) / 2)
        if self._heap[child_index][0] < self._heap[parent_index][0]:
            self._swap(parent_index, child_index)
            self._heap_up(parent_index)

    def _heap_down(self, k):
        """
        Heapify down the k-th element of a heap.
        :param k: the index of the element to be heapify down
        :return: the updated heap (in place)
        """
        parent_index = k
        lchild_index = 2 * k + 1
        rchild_index = 2 * k + 2
        if rchild_index < self._size:
            p1 = min(self._heap[parent_index][0], self._heap[lchild_index][0],
                     self._heap[rchild_index][0])
            if p1 == self._heap[lchild_index][0]:
                self._swap(parent_index, lchild_index)
                self._heap_down(lchild_index)
            elif p1 == self._heap[rchild_index][0]:
                self._swap(parent_index, rchild_index)
                self._heap_down(rchild_index)
        else:
            if lchild_index < self._size:
                p2 = min(self._heap[parent_index][0], self._heap[lchild_index][0])
                if p2 == self._heap[lchild_index][0]:
                    self._swap(parent_index, lchild_index)
                    self._heap_down(lchild_index)

    def _build_heap(self):
        """
        Create a min heap from a list.
        :return: the min heap created from the list (in place)
        """
        i = math.floor((self._size - 1) / 2)
        while i >= 0:
            self._heap_down(i)
            i = i - 1
        return self._heap

    def insertion(self, element):
        """
        Add an element to the priority queue.
        :param element: the element to be inserted into the priority queue
        :return: the updated priority queue (in place)
        """
        # put the element at the end of the list and then heapify it up
        self._heap.append(element)
        self._size += 1
        self._pos[element[1]] = self._size - 1
        self._heap_up(self._pos[element[1]])

    def pop_top(self):
        """
        Remove the element with the highest (smallest) priority from the
        priority queue.
        :return: the element with the highest priority, and the updated
        priority queue (in place)
        """
        # swap the top element with the end element of the heap, pop the end
        # of the heap, then heap_down(0)
        self._swap(0, self._size - 1)
        removed = self._heap.pop()
        self._size -= 1
        self._heap_down(0)

    def decrease_priority(self, k, d):
        """
        Decrease the priority of an element in the priority queue.
        :param k: the index of the element to be decreased priority
        :param d: the new priority that needs to be updated to the element
        :return: the updated priority queue (in place)
        """
        self._heap[k] = (d, self._heap[k][1])
        self._build_heap()

    def pos(self, element):
        """
        Given an element, return its position in the priority queue.
        :param element: the element to search for position
        :return: the index of the given element in the priority queue
        """
        for item in self._pos:
            if item == element:
                return self._pos[item]


def main():
    lst = [(3, "A"), (10, "B"), (5, "C"), (11, "D"), (12, "E"), (6, "F"), (8, "G")]
    pq = PriorityQueue(lst)
    pq.decrease_priority(3, 7)
    print(pq)


if __name__ == "__main__":
    main()
