llc -filetype=obj out.ll  -o out.o 

clang -shared -fPIC io.c -o io.so
clang -emit-llvm -o io.bc -c io.c 
llc -filetype=obj io.bc -o io.o 

clang out.o io.o -o out.exe