Python не имеет концепции интерфейсов как в Java, которые определяют общие методы, которые классы должны реализовывать.
Вместо этого в Python используется понятие абстрактных базовых классов (abstract base classes или ABC).

ABC предоставляют набор методов-заглушек (абстрактных методов), которые описывают общий интерфейс, который должен
реализовываться дочерними классами. Пример использования ABC в Python:

- с использованием метода `__subclasshook__` без явного наследования

  ```python
  
  from abc import ABC, abstractmethod
  
  
  class MyABC(ABC):
  
      @classmethod
      def __subclasshook__(cls, C):
          if cls is MyABC:
              if any("foo" in B.__dict__ and "bar" in B.__dict__ for B in C.__mro__):
                  return True
              return False
          return NotImplemented
  
      @abstractmethod
      def foo(self):
          pass
  
      @abstractmethod
      def bar(self):
          pass
  
  
  class MyClass:
      def foo(self):
          pass
  
      def bar(self):
          pass
  
  
  a = MyClass()
  
  print(issubclass(MyClass, MyABC))  # Output: True
  print(isinstance(a, MyABC))  # Output: True
  ```

  В этом примере класс MyABC содержит два абстрактных метода foo и bar, а также метод `__subclasshook__`,
  который определяет, что объекты с методами foo и bar будут считаться дочерними классами MyABC без обязательного
  наследования.
  
  Класс MyClass реализует метод foo, bar, а так же не является явным наследником класса MyABC, но при этом проходит
  проверки `issubclass` и `isinstance`, принадлежности к абстрактному классу MyABC, благодаря методу `__subclasshook__`.


- без метода `__subclasshook__` с явным наследованием

  ```python
  
  from abc import ABC, abstractmethod
  
  
  class MyABC(ABC):
  
      @abstractmethod
      def foo(self):
          pass
  
      @abstractmethod
      def bar(self):
          pass
  
  
  class MyClass(MyABC):
      def foo(self):
          pass
  
      def bar(self):
          pass
  
  
  a = MyClass()
  
  print(issubclass(MyClass, MyABC))  # Output: True
  print(isinstance(a, MyABC))  # Output: True
  ```

  В этом примере класс MyABC так же содержит два абстрактных метода foo и bar, но метод `__subclasshook__` не
  реализован.
  
  Класс MyClass так же реализует метод foo, bar, но уже явно наследуется от класса MyABC и, для того чтоб пройти
  проверки `issubclass` и `isinstance` в базовом классе метод `__subclasshook__` не нужен.

<div align="right">

[Вернуться к вопросам](../Вопросы.md)

</div>
