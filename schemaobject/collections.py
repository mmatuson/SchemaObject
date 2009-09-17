class OrderedDict(dict):
    """
    A Dictionary whose items are returned in the order they were first added
    """

    def __init__(self):
        self._list = []
        self._current = 0
        super(OrderedDict, self).__init__()

    def __setitem__(self, item, value):
        self._list.append(item)
        super(OrderedDict, self).__setitem__(item, value)

    def iterkeys(self):
        for key in self._list:
            yield key

    def keys(self):
        return self._list

    def iteritems(self):
        for key in self._list:
            yield (key, super(OrderedDict, self).__getitem__(key))

    def items(self):
        return [(k, super(OrderedDict, self).__getitem__(k)) for k in self._list]

    def __iter__(self):
        return self

    def next(self):
        i = self._current
        self._current += 1
        if self._current > len(self._list):
            self._current = 0
            raise StopIteration

        return self._list[i]
