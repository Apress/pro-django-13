class SubclassTracker(type):
    def __init__(cls, name, bases, attrs):
        try:
            if TrackedClass not in bases:
                return
        except NameError:
            return
        TrackedClass._registry.append(cls)


# This is an alternative way to describe a class with a metaclass,
# which is syntax-compatible with both Python 2 and Python 3.
TrackedClass = SubclassTracker('TrackedClass', (object,), {
    '_registry': [],
})


if __name__ == '__main__':
    class ClassOne(TrackedClass):
        pass
    assert TrackedClass._registry == [ClassOne]
    
    class ClassTwo(TrackedClass):
        pass
    assert TrackedClass._registry == [ClassOne, ClassTwo]
