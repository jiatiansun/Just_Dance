class Test() :
	def __init__(self, what):
		self.text = what

	@staticmethod
	def static_method_to_call():
		print("success")
	@staticmethod
	def another_static_method() :
		Test.static_method_to_call()

    # @classmethod
    # def another_class_method(cls) :
    #     cls.static_method_to_call()
	def what(self):
		Test.static_method_to_call();

one = Test('what');
print(one.text)
one.what();