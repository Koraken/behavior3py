import b3

__all__ = ['Sequence']

class Sequence(b3.Composite):

    def __init__(self, children=None):
        super(Sequence, self).__init__(children)

    def tick(self, tick):
        for node in self.children:
            # The ID that the parent has for the child being ticked
            tick.child_id = self.children.index(node)
            tick.parent = self
            status = node._execute(tick)

            if status != b3.SUCCESS:
                return status

        return b3.SUCCESS
