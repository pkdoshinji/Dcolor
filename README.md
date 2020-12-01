# Dcolor
Domain-color graphs of single-valued complex functions on the Riemann sphere

### Overview
Dcolor is a command-line Python tool for visualizing the graphs of complex functions of a single 
variable on the Riemann sphere. For more on the mathematical background, see the discussion in
about.pdf

### Installation

```
git clone https://github.com/pkdoshinji/Dcolor
sudo pip3 install pillow
sudo pip3 install mayavi
sudo apt-get install python3-pyqt.qtsvg
```

The installation of mayavi can be a bit tricky, see the official documentation for additional info:
https://docs.enthought.com/mayavi/mayavi/installation.html


### Help

```
usage: dcolor.py [-h] [-c] [-d] [-r RESOLUTION] [-f FUNCTION] [-i IMAGE_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -c, --contours        render logarithmic contor lines
  -d, --display         display flat theta-phi image
  -r RESOLUTION, --resolution RESOLUTION
                        resolution of array
  -f FUNCTION, --function FUNCTION
                        function to graph
  -i IMAGE_FILE, --image_file IMAGE_FILE
                        name of image file
```

### Examples

```
python3 main.py -f 'log(sin((z**3 - 2*z + 1j)/(1j*z**2)))' -c
```
<img src="/Images/img1.png" alt="example" width="1000" height="500" />

```
./main.py -f 'sin(log(z**5 - 2*z**3 - 1j*z))' -c
```
<img src="/Images/img2.png" alt="example" width="1000" height="500" />

```
./main.py -f 'sin(log(z**5 - 2*z**3 - 1j*z))'
```
<img src="/Images/img3.png" alt="example" width="1000" height="500" />

```
./main.py -f '((((((((z**2+z)**2+z)**2+z)**2+z)**2+z)**2+z)**2+z)**2+z)**2+z'
```
(The Mandelbrot set)
<img src="/Images/img4.png" alt="example" width="1000" height="500" />

```
 ./main.py -f 'sin(((z**2 + 1)/(z))**3-1)'
```
<img src="/Images/img5.png" alt="example" width="1000" height="500" />

