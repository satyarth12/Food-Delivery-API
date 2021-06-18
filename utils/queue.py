
class Queue(object):
	def __init__(self):
		self.item = []

	def __str__(self):
		return f'{self.item}'

	def __repr__(self):
		return f'{self.item}'

	def enque(self, add):
		self.item.insert(0, add)
		return True

	def size(self):
		return len(self.item)

	def is_empty(self):
		if self.size() == 0:
			return True
		return False

	def deque(self):
		if self.size() == 0:
			return None
		return self.item.pop()
