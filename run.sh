
./build.py clean
sed -i 's/case1\.CFLAGS.*\[.*\]/case1\.CFLAGS = \["-O0"\]/' ./build.py
sed -i 's/case1\.LINK_EXE_FLAGS.*\[.*\]/case1\.LINK_EXE_FLAGS = \[]/' ./build.py
echo 'Build -O0'
./build.py run

./build.py clean
sed -i 's/case1\.CFLAGS.*\[.*\]/case1\.CFLAGS = \["-O1"\]/' ./build.py
sed -i 's/case1\.LINK_EXE_FLAGS.*\[.*\]/case1\.LINK_EXE_FLAGS = \[]/' ./build.py
echo 'Build -O1'
./build.py run

./build.py clean
sed -i 's/case1\.CFLAGS.*\[.*\]/case1\.CFLAGS = \["-O2"\]/' ./build.py
sed -i 's/case1\.LINK_EXE_FLAGS.*\[.*\]/case1\.LINK_EXE_FLAGS = \[]/' ./build.py
echo 'Build -O2'
./build.py run

./build.py clean
sed -i 's/case1\.CFLAGS.*\[.*\]/case1\.CFLAGS = \["-O3"\]/' ./build.py
sed -i 's/case1\.LINK_EXE_FLAGS.*\[.*\]/case1\.LINK_EXE_FLAGS = \[]/' ./build.py
echo 'Build -O3'
./build.py run

./build.py clean
sed -i 's/case1\.CFLAGS.*\[.*\]/case1\.CFLAGS = \["-O3","-flto"\]/' ./build.py
sed -i 's/case1\.LINK_EXE_FLAGS.*\[.*\]/case1\.LINK_EXE_FLAGS = \["-flto"\]/' ./build.py
echo 'Build -O3 -flto'
./build.py run