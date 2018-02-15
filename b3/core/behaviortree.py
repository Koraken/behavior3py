import b3
import uuid

__all__ = ['BehaviorTree']

class BehaviorTree(object):
    def __init__(self):
        self.id = str(uuid.uuid1())
        self.title = 'Behavior3'
        self.description = ''
        self.properties = {}
        self.root = None
        self.debug = None

    def load(self, data, names=None):
        names = names or {}
        self.title = data['title'] or self.title
        self.description = data['description'] or self.description
        self.properties = data['properties'] or self.properties

        nodes = {}
        for key in data['nodes']:
            spec = data['nodes'][key]

            if spec['name'] in names:
                cls = names[spec['name']]

            elif hasattr(b3, spec['name']):
                cls = getattr(b3, spec['name'])

            else:
                raise AttributeError('BehaviorTree.load: Invalid node name "%s"'%spec['name'])

            node = cls()
            node.id = spec['id'] or node.id
            node.title = spec['title'] or node.title
            node.description = spec['description'] or node.description
            node.properties = spec['properties'] or node.properties
            nodes[key] = node

        for key in data['nodes']:
            spec  = data['nodes'][key]
            node = nodes[key]
            
            if node.category == b3.COMPOSITE and 'children' in spec:
                for cid in spec['children']:
                    node.children.append(nodes[cid])

            elif node.category == b3.DECORATOR and 'child' in spec:
                node.child = nodes[spec['child']]

        if (data['root']):
            self.root = nodes[data['root']];


    def dump(self):
        data = {}
        custom_names = []

        data['title'] = self.title
        data['description'] = self.description
        data['root'] = self.root.id if self.root else None
        data['properties'] = self.properties
        data['nodes'] = {}
        data['custom_nodes'] = []

        if not self.root:
            return data

        stack = [self.root]
        while len(stack) > 0:
            node = stack.pop()
            spec = {}
            spec['id'] = node.id
            spec['name'] = node.name
            spec['title'] = node.title
            spec['description'] = node.description
            spec['properties'] = node.properties

            name = node.__class__.__name__
            if not hasattr(b3, name) and name not in custom_names:
                subdata = {}
                subdata['name'] = name
                subdata['title'] = node.title
                subdata['category'] = node.category

                custom_names.append(name)
                data['custom_nodes'].append(subdata)

            if node.category == b3.COMPOSITE and hasattr(node, 'children'):
                children = []
                for c in reversed(node.children):
                    children.append(c.id)
                    stack.append(c)
                spec['children'] = children
            elif node.category == b3.DECORATOR and hasattr(node, 'child'):
                stack.append(node.child)
                spec['child'] = node.child.id

            data['nodes'][node.id] = spec

        return data


    def tick(self, target, blackboard):

        # Create the TICK object
        tick = b3.Tick()
        tick.target = target
        tick.blackboard = blackboard
        tick.tree = self
        tick.debug = self.debug

        # Tick node
        self.root._execute(tick)