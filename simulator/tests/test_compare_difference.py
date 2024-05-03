from ..models.model import Model

def test_basic():
	file = 'data/gs_temp'
	# Should output nothing
	import pdb; pdb.set_trace()
	Model.compare_difference([file, file])
	
if __name__ == '__main__':
	test_basic()