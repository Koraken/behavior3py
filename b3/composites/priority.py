import b3

__all__ = ['Priority']

class Priority(b3.Composite):
    def __init__(self, children=None):
        super(Priority, self).__init__(children)

    def tick(self, tick):
        for node in self.children:
            tick.child_id = self.children.index(node)
            tick.parent = self
            status = node._execute(tick)

            if status != b3.FAILURE:
                return status

        return b3.FAILURE
