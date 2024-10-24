from datetime import datetime


class MyClass:
    @classmethod
    def myMethod(cls):
        print("Hello World")


MyClass.myMethod()

from Model.Entity.User import User

print(datetime.now())
