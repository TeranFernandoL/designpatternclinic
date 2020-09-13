
class Component:
    def operation(self):
        pass


class ConcreteComponent(Component):
    def operation(self):
        return "ConcreteComponent"


class Decorator(Component):
    _component: Component = None

    def __init__(self, component):
        self._component = component

    @property
    def component(self):
        return self._component

    def operation(self):
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    def operation(self):
        return f"ConcreteDecoratorA({self.component.operation()})"


class ConcreteDecoratorB(Decorator):
    def operation(self):
        return f"ConcreteDecoratorB({self.component.operation()})"


def client_code(component):
    print(f"RESULT: {component.operation()}", end="")


if __name__ == "__main__":
    # This way the client code can support both simple components...
    simple = ConcreteComponent()
    print("Client: I've got a simple component:")
    client_code(simple)
    print("\n")
    decorator1 = ConcreteDecoratorA(simple)
    decorator2 = ConcreteDecoratorB(decorator1)
    print("Client: Now I've got a decorated component:")
    client_code(decorator1)
    client_code(decorator2)