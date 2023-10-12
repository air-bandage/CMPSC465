class PriorityQueue(object):
    def __init__(self, lst=None):
        if lst is None:
            self._heap = []
        else:
            self._heap = lst
        self._size = len(self._heap)
        self._pos = {self._heap[i][1]: i for i in range(self._size)}
        self.build_heap()

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self._heap)

    @property
    def heap(self):
        return self._heap

    def pos(self, element=None):
        if element is None:
            return self._pos
        else:
            return self._pos[element]

    def swap(self, idx1, idx2):
        pos_key1 = self._heap[idx1][1]
        pos_key2 = self._heap[idx2][1]
        self._heap[idx1], self._heap[idx2] = self._heap[idx2], self._heap[idx1]
        self._pos[pos_key1], self._pos[pos_key2] = (
            self._pos[pos_key2],
            self._pos[pos_key1],
        )
        return 0

    def build_heap(self):
        for i in range((self._size - 1) // 2, -1, -1):
            self.heap_down(i)
        return 0

    def heap_up(self, k):
        if k == 0:
            return 0
        parent = (k - 1) >> 1
        if self._heap[k][0] < self._heap[parent][0]:
            self.swap(parent, k)
            self.heap_up(parent)
        return 0

    def heap_down(self, k):
        lchild_index = 2 * k + 1
        rchild_index = 2 * k + 2
        min_index = k
        if (
            rchild_index < self._size - 1
            and self._heap[rchild_index][0] < self._heap[min_index][0]
        ):
            min_index = rchild_index
        if (
            lchild_index < self._size - 1
            and self._heap[lchild_index][0] < self._heap[min_index][0]
        ):
            min_index = lchild_index
        if min_index != k:
            self.swap(k, min_index)
            self.heap_down(min_index)
        return 0

    def decrease_priority(self, k, new_priority):
        if new_priority >= self._heap[k][0]:
            raise ValueError(
                "The new priority should be smaller than the old priority."
            )
        self._heap[k] = (new_priority, self._heap[k][1])
        self.heap_up(k)

    def pop(self, k):
        if k != self._size - 1:
            self.swap(k, self._size - 1)
        r = self._heap.pop()
        del self._pos[r[1]]
        self._size -= 1
        self.heap_down(k)
        return r


def main():
    test = [(3, "A"), (10, "B"), (5, "C"), (11, "D"), (12, "E"), (6, "F"), (8, "G")]
    pq = PriorityQueue(test)
    print(pq.heap)
    print(pq.pos())
    pq.decrease_priority(2, 1)
    print(pq.heap)
    print(pq.pos())
    pq.pop(0)
    print(pq.heap)
    print(pq.pos())
    pq.pop(0)
    print(pq.heap)
    print(pq.pos())


if __name__ == "__main__":
    main()
