from ..models.model import Model
from ..models.grayscott import GrayScott

import timeit

def test_opt_take_step():
	file_1 = 'data/temp_1'
	file_2 = 'data/temp_2'
	
	frames=100
	steps_per_frame=50
	
	gs1 = GrayScott()
	gs2 = GrayScott()
	
	Model.to_file(gs1, file_1, frames=frames, steps_per_frame=steps_per_frame)
	Model.to_file(gs2, file_2, frames=frames, steps_per_frame=steps_per_frame, optimised=2)
	
	diff_count = Model.compare_difference([file_1, file_2])
	print(f"Difference count is: {diff_count}")
	assert diff_count == 0
	
	pass

def time_opt_take_step():
	file_1 = 'data/temp_1'
	# file_2 = 'data/temp_2'
	
	frames=100
	steps_per_frame=50
	
	gs1 = GrayScott()
	# gs2 = GrayScott()
	
	Model.to_file(	gs1, 
					file_1, 
					frames=frames, 
					steps_per_frame=steps_per_frame,
					# optimised=True,
					)
	# time_2 = timeit.timeit(	Model.to_file(	gs2, 
	# 								  		file_2, 
	# 								  		frames=frames, 
	# 										steps_per_frame=steps_per_frame,
	# 										optimised=True),
	# 						number=1)
	
	# diff = time_1 - time_2
	# print(f"Unoptimised took: {time_1}", f"Optimised took: {time_2}", f"Difference: {diff}", sep='\n')
	# assert diff > 0
	
	pass

if __name__ == '__main__':
	# test_opt_take_step()
	time_opt_take_step()