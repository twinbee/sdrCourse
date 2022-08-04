# this module will be imported in the into your flowgraph

f1 = 400e6
f2 = 470e6

f = f1

step = 1e6

def sweeper(prob_lvl):
	global f1,f2,f,step;
	if (prob_lvl):
		f += step;
	if (f >= f2):
		f = f1;
	
	return f;
	

