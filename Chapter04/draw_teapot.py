from teapot import load_triangles
from draw_model import draw_model
from vectors import scale, add
####################################################################
#### this code takes a snapshot to reproduce the exact figure 
#### shown in the book as an image saved in the "figs" directory
#### to run it, run this script with command line arg --snapshot
import sys
import camera
if '--snapshot' in sys.argv:
    camera.default_camera = camera.Camera('fig_4.4_draw_teapot',[0])
####################################################################

original_triangles = load_triangles()

scaled_triangles = [
    [scale(0.4, vertex) for vertex in triangle] for triangle in original_triangles
]

translated_triangles = [
    [add((-1, 0, 0), vertex) for vertex in triangle] for triangle in scaled_triangles
]



draw_model(translated_triangles)