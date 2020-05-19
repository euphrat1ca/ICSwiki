import itertools

for combination in itertools.product(xrange(10), repeat=4):
	    print ''.join(map(str, combination))
