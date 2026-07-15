"""
Metaclasses - Advanced Python Exercises
========================================
Metaclasses are classes that create classes. They control
how classes are constructed and behave.
"""

from typing import Any, Dict


# =============================================================================
# 1. type() Function
# =============================================================================

def demo_type():
    """Demonstrate type() for class creation."""
    # type can create classes dynamically
    MyClass = type("MyClass", (object,), {"greet": lambda self: "Hello!"})
    obj = MyClass()
    print(f"  Dynamic class: {obj.greet()}")
    print(f"  Class name: {MyClass.__name__}")
    print(f"  Base classes: {MyClass.__bases__}")

    # Check type of existing class
    print(f"  type(42) = {type(42)}")
    print(f"  type('hello') = {type('hello')}")


# =============================================================================
# 2. Custom Metaclass
# =============================================================================

class ValidationMeta(type):
    """Metaclass that validates class attributes."""

    def __new__(mcs, name, bases, namespace):
        # Skip for base classes
        if bases:
            # Check for required attributes
            if 'required_attr' not in namespace:
                raise TypeError(f"Class {name} must define 'required_attr'")

            # Validate attribute types
            for key, value in namespace.items():
                if key.startswith('_'):
                    continue
                if callable(value) and not key.startswith('_'):
                    # Add validation to methods
                    original = value

                    def wrapper(*args, _original=original, _name=key, **kwargs):
                        print(f"  Calling {name}.{_name}")
                        return _original(*args, **kwargs)

                    namespace[key] = wrapper

        return super().__new__(mcs, name, bases, namespace)


class BaseAPI(metaclass=ValidationMeta):
    """Base class requiring required_attr."""
    required_attr = True


class UserAPI(BaseAPI):
    """User API - must define required_attr."""
    required_attr = True

    def get_user(self, id: int) -> dict:
        return {"id": id, "name": "Alice"}


# =============================================================================
# 3. Singleton Metaclass
# =============================================================================

class SingletonMeta(type):
    """Metaclass implementing singleton pattern."""

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """Singleton database connection."""

    def __init__(self):
        self.connection_id = id(self)

    def query(self, sql: str) -> str:
        return f"Executing: {sql}"


# =============================================================================
# 4. Class Registry Metaclass
# =============================================================================

class RegistryMeta(type):
    """Metaclass that registers subclasses."""

    _registry: Dict[str, type] = {}

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if bases:  # Don't register base class
            RegistryMeta._registry[name] = cls

    @classmethod
    def get_registry(mcs):
        return dict(mcs._registry)

    @classmethod
    def create_instance(mcs, class_name: str, *args, **kwargs):
        if class_name not in RegistryMeta._registry:
            raise ValueError(f"Unknown class: {class_name}")
        return RegistryMeta._registry[class_name](*args, **kwargs)


class Serializer(metaclass=RegistryMeta):
    """Base serializer class."""
    def serialize(self, data) -> str:
        raise NotImplementedError


class JSONSerializer(Serializer):
    def serialize(self, data) -> str:
        import json
        return json.dumps(data)


class XMLSerializer(Serializer):
    def serialize(self, data) -> str:
        return f"<data>{data}</data>"


class CSVSerializer(Serializer):
    def serialize(self, data) -> str:
        if isinstance(data, dict):
            return ",".join(str(v) for v in data.values())
        return str(data)


# =============================================================================
# 5. Auto-Representation Metaclass
# =============================================================================

class ReprMeta(type):
    """Metaclass that adds __repr__ to classes."""

    def __new__(mcs, name, bases, namespace):
        fields = [
            k for k, v in namespace.items()
            if not k.startswith('_') and not callable(v)
        ]

        def __repr__(self):
            attrs = ", ".join(f"{f}={getattr(self, f)!r}" for f in fields)
            return f"{name}({attrs})"

        namespace['__repr__'] = __repr__
        return super().__new__(mcs, name, bases, namespace)


class Point(metaclass=ReprMeta):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Person(metaclass=ReprMeta):
    def __init__(self, name, age):
        self.name = name
        self.age = age


# =============================================================================
# 6. __new__ vs __init__
# =============================================================================

class DemoNew(metaclass=type):
    """Demonstrate __new__ vs __init__."""

    def __new__(cls, *args, **kwargs):
        print(f"  __new__ called with args={args}")
        instance = super().__new__(cls)
        print(f"  __new__ created instance {id(instance)}")
        return instance

    def __init__(self, value):
        print(f"  __init__ called with value={value}")
        self.value = value


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("METACLASSES DEMO")
    print("=" * 60)

    # 1. type() function
    print("\n--- type() Function ---")
    demo_type()

    # 2. Custom metaclass
    print("\n--- Custom Metaclass ---")
    user_api = UserAPI()
    result = user_api.get_user(1)
    print(f"  Result: {result}")

    # 3. Singleton
    print("\n--- Singleton Metaclass ---")
    db1 = Database()
    db2 = Database()
    print(f"  Same instance: {db1 is db2}")
    print(f"  db1.query: {db1.query('SELECT * FROM users')}")

    # 4. Registry
    print("\n--- Registry Metaclass ---")
    print(f"  Registry: {list(RegistryMeta.get_registry().keys())}")

    json_ser = RegistryMeta.create_instance("JSONSerializer")
    xml_ser = RegistryMeta.create_instance("XMLSerializer")
    csv_ser = RegistryMeta.create_instance("CSVSerializer")

    data = {"name": "Alice", "age": 30}
    print(f"  JSON: {json_ser.serialize(data)}")
    print(f"  XML: {xml_ser.serialize(data)}")
    print(f"  CSV: {csv_ser.serialize(data)}")

    # 5. Auto-repr
    print("\n--- Auto-Repr Metaclass ---")
    p = Point(3, 4)
    person = Person("Bob", 25)
    print(f"  {p}")
    print(f"  {person}")

    # 6. __new__ vs __init__
    print("\n--- __new__ vs __init__ ---")
    obj = DemoNew(42)

    print("\n" + "=" * 60)
    print("All metaclass demos complete!")
    print("=" * 60)
