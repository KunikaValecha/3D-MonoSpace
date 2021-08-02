## Requirements
- OpenGL 3.3 and above
- GLEW
- GLFW
- GLM
- STB Image
- Assimp

To install 

sudo apt install mesa-utils mesa-common-dev
sudo apt-get install libglew-dev
sudo apt-get install libglfw3-dev
sudo apt-get install libglm-dev
git clone https://github.com/nothings/stb.git
sudo cp stb/stb_image.h /usr/include/
git clone https://github.com/assimp/assimp.git
cd assimp
cmake CMakeLists.txt
make -j4
sudo make install
export LD_LIBRARY_PATH=/usr/local/lib


## Execution
To compile and execute run
make all
./p inputfile.txt

#### Note
run
export LD_LIBRARY_PATH=/usr/local/lib
if you see <error while loading shared libraries: libassimp.so.4: cannot open shared object file: No such file or directory>


