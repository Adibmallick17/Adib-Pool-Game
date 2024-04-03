# # Compiler and compiler flag variables
# CC := clang
# CFLAGS := -Wall -pedantic -std=c99 -fPIC
# PYTHON_INCLUDE := /usr/include/python3.11/
# LIBS := -lm
# PYTHON_LIB := /usr/lib/python3.11
# SWIG := swig

# # Default target
# all: _phylib.so

# # Target for phylib.o
# phylib.o: phylib.c
# 	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

# # Target for libphylib.so
# libphylib.so: phylib.o
# 	$(CC) -shared -o libphylib.so phylib.o $(LIBS)

# # Targets for SWIG generated files (phylib_wrap.c and phylib.py)
# phylib_wrap.c phylib.py: phylib.i
# 	$(SWIG) -python phylib.i

# # Target for phylib_wrap.o
# phylib_wrap.o: phylib_wrap.c
# 	$(CC) $(CFLAGS) -I$(PYTHON_INCLUDE) -c phylib_wrap.c -o phylib_wrap.o

# # Target for _phylib.so
# _phylib.so: phylib_wrap.o libphylib.so
# 	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L$(PYTHON_LIB) -lpython3.11 -lphylib -o _phylib.so

# # Clean target
# clean:
# 	rm -f *.o *.so phylib_wrap.c phylib.py 

CC = clang
CFLAGS = -std=c99 -Wall -pedantic
SWIG = swig
PYTHON_INCLUDE = /usr/include/python3.11
PYTHON_LIB = /usr/lib/python3.11/config-3.11-x86_64-linux-gnu
EXTRA_LIB = /usr/lib/x86_64-linux-gnu
LIB_NAME = phylib
PYTHON_VERSION = python3.11

all: _$(LIB_NAME).so

$(LIB_NAME).o: $(LIB_NAME).c
	$(CC) $(CFLAGS) -fPIC -c $^ -o $@

lib$(LIB_NAME).so: $(LIB_NAME).o
	$(CC) -shared $^ -o $@ -lm

$(LIB_NAME)_wrap.c $(LIB_NAME).py: $(LIB_NAME).i
	$(SWIG) -python $^

$(LIB_NAME)_wrap.o: $(LIB_NAME)_wrap.c
	$(CC) $(CFLAGS) -fPIC -c $^ -o $@ -I$(PYTHON_INCLUDE)

_$(LIB_NAME).so: $(LIB_NAME)_wrap.o lib$(LIB_NAME).so
	$(CC) -shared $^ -o $@ -L. -L$(PYTHON_LIB) -L$(EXTRA_LIB) -l$(PYTHON_VERSION) -l$(LIB_NAME)

clean:
	rm -f *.o *.so $(LIB_NAME).py $(LIB_NAME)_wrap.c
