#!/usr/bin/env python3

'''
Domain coloring for the visualization of complex functions of a single variable
on the Riemann sphere.

Author: M. Patrick Kelly
Last Updated: November 10, 2020 
'''

import colorsys
import argparse
from numpy import *
from PIL import Image
from mayavi import mlab
from tvtk.api import tvtk


class ComplexGraph:

    def __init__(self, function = 'z', resolution=1024, log_contours=False, image_name = 'my_image'):
        self.function = function
        self.steps = resolution
        self.log_contours = log_contours
        self.image_name = image_name
        self.array = self.make_array()
        self.flat_image = self.make_image()

    def make_array(self):
        print('Calculating array...')
        phi, theta = self.get_spherical_grid()
        rect = self.get_rectilinear_z(theta, phi)
        fz = self.func(rect)
        h = self.get_h(fz)
        s = ones(fz.shape)
        if self.log_contours:
            l = self.get_l(self.get_logbars(fz))
        else:
            l = self.get_l(fz)
        hls = dstack((h, l, s))
        rgb_array = self.get_rgb(hls)  #Convert hls color values to rgb
        rgb_array[isnan(rgb_array)] = 255 #Replace NaNs with 255
        print('Array complete!')
        return rgb_array
        #self.rgb_array = np.rot90(self.rgb_array)

    def get_spherical_grid(self):
        theta = linspace(0, 2*pi, self.steps)
        phi = linspace(pi, 0, int(self.steps / 2))
        phi, theta = meshgrid(phi, theta)
        return phi, theta

    def pol2cart(self, r, phi):
    #Convert polar coordinates to Cartesian coordinates
        x = r * cos(phi)
        y = r * sin(phi)
        return x, y

    def get_rectilinear_z(self, theta, phi):
        R = sin(phi)/(1 - cos(phi))
        THETA = theta
        x, y = self.pol2cart(R, THETA)
        z = x + 1j*y
        return z

    def func(self, np_array):
        allowed_dict['z'] = np_array
        code = compile(self.function, '<string>', 'eval')
        return eval(code, {'__builtins__': None}, allowed_dict)

    def get_h(self, z):
        h = (angle(z) + pi)/(2 * pi) #Get hue from argument of fz
        return h

    def get_l(self, z):
        l = (2 / pi) * (arctan(absolute(.6*z))) #Get lightness from modulus
        return l

    def get_rgb(self, hls_array):
        rgb_array = empty_like(hls_array)
        rows = hls_array.shape[0]
        cols = hls_array.shape[1]
        for i in range(0, rows):
            for j in range(0, cols):
                hls = hls_array[i,j]
                rgbs = 255 * array(colorsys.hls_to_rgb(hls[0], hls[1], hls[2]))
                rgb_array[i,j] = rgbs
        return rgb_array

    def get_logbars(self, nparray):
        grey_array = 1 * mod(log(absolute(nparray)),1)
        return grey_array

    def make_image(self):
        print('Rendering equirectangular projection...')
        newimg = Image.new('RGB', (self.array.shape[0], self.array.shape[1]))
        pixels = newimg.load()
        for i in range(newimg.size[0]):
            for j in range(newimg.size[1]):
                hls_vals = tuple(self.array[i, j])
                pixels[i, j] = tuple([int(k) for k in hls_vals])
        newimg.save(self.image_name + '.jpg')
        print('Rendering complete!')
        return newimg

    def display(self):
        self.flat_image.show()


def riemann_sphere(imagefile):
    #Create figure window
    fig = mlab.figure(size=(1200, 1200))

    #Load and map texture
    img = tvtk.JPEGReader()
    img.file_name = imagefile + '.jpg'
    texture = tvtk.Texture(input_connection=img.output_port, interpolate=1)

    # Use TexturedSphereSource
    R = 1
    Nrad = 180

    #Create the sphere source with a given radius and angular resolution
    sphere = tvtk.TexturedSphereSource(radius=R, theta_resolution=Nrad, \
                                       phi_resolution=Nrad)

    #Assemble rest of the pipeline, assign texture
    sphere_mapper = tvtk.PolyDataMapper(input_connection=sphere.output_port)
    sphere_actor = tvtk.Actor(mapper=sphere_mapper, texture=texture)
    fig.scene.add_actor(sphere_actor)

    #Display
    mlab.show()


def main():

    #Command line options (-c,-d,-i,-p,-o,-s,-g) with argparse module:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--contours', action='store_true', help='render logarithmic contor lines')
    parser.add_argument('-d', '--display', action='store_true', help='display flat theta-phi image')
    parser.add_argument('-r', '--resolution', action='store', type=int, help='resolution of array')
    parser.add_argument('-f', '--function', type=str, help='function to graph')
    parser.add_argument('-i', '--image_file', type=str, help='name of image file')

    #Create parser
    args = parser.parse_args()

    #Set variables with command-line inputs
    contours = args.contours
    display = args.display
    res = args.resolution
    func = args.function
    im_name = args.image_file

    if not res:
        res = 1024
    if not func:
        func = 'z'
    if not args.image_file:
        im_name = 'my_image'


    my_graph = ComplexGraph(function=func, resolution=res, log_contours=contours, image_name=im_name)

    if display:
        my_graph.display()
    riemann_sphere(my_graph.image_name)


if __name__ == '__main__':

    #List of safe methods (to prevent code injection via the eval() function
    allowed_list = ['arccos', 'arcsin', 'arctan', 'arctan2', 'sin', 'tan', 'log',
                    'log10', 'log2', 'exp', 'exp2', 'pi', 'sinh', 'cosh', 'tanh',
                    'arcsinh', 'arccosh', 'arctanh', 'add', 'multiply', 'prod',
                    'divide', 'subtract', 'power', 'true_divide', 'floor_divide',
                    'mod', 'remainder', 'divmod', 'isreal', 'conj', 'real', 'imag',
                    'angle', 'absolute', 'sqrt', 'cbrt', 'round', 'cumsum', 'cumprod',
                    'gradient']

    #Dictionary of allowed methods
    allowed_dict = dict([(k, globals().get(k, None)) for k in allowed_list])

    main()
