class Target:
    def request(self):
        return None


class Adaptee:
    def specific_request(self):
        return None


class Adapter(Target, Adaptee):
    def request(self):
        return self.specific_request()


def client_code(target):
    print(target.request(), end="")


if __name__ == "__main__":
    target = Target()
    client_code(target)
    print("\n")
    adaptee = Adaptee()
    print(adaptee.specific_request())
    adapter = Adapter()
    client_code(adapter)
