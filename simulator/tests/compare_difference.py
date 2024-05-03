from ..models.model import Model

def test_basic():
	file = 'data/gs_temp'
	file2 = 'data/gs_large_scale'
	file3 = 'data/gs_large_scale2'
	# Should output nothing
	# import pdb; pdb.set_trace()
	assert Model.compare_difference([file, file]) == 0
	assert Model.compare_difference([file2, file3]) != 0
	
if __name__ == '__main__':
	test_basic()