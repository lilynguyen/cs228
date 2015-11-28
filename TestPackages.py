# ======================================
# python v 2.7 **
# ======================================

# ======================================
# PIL v 1.1.7
# ======================================

# ======================================
# mpl v 1.4.3
# ======================================

try:
	import matplotlib
except ImportError:
	print "matplotlib is not installed"

# ======================================
# numpy v 1.6.1
# ======================================

try:
    import numpy
except ImportError:
    print "numpy is not installed"

# ======================================
# scipy v 0.11.0
# ======================================

try:
    import scipy
except ImportError:
    print "scipy is not installed"
    
print "done"