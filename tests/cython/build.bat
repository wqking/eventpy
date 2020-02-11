python cython_setup.py build_ext --inplace
del main.pyd
ren main*.pyd main.pyd
