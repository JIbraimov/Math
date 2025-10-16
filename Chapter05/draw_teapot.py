from teapot import load_triangles
from draw_model import draw_model
import sys
import camera

if '--snapshot' in sys.argv:
    camera.default_camera = camera.Camera('fig_5.36_draw_teapot',[0])

draw_model(load_triangles())