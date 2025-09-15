import numpy as np 
from math import sqrt, pi, ceil, floor 
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import colors 


class Polygon2D:
    def __init__(self, *vertices, color=colors.BLUE, fill=None, aplha=0.4 ):
        self.vertices = vertices
        self.color = color
        self.fill = fill
        self.alpha = aplha


class Points2D:
    def __init__(self, *vectors, color=colors.BLACK):
        self.vectors = list(vectors)
        self.color = color


class Arrow2D:
    def __init__(self, tip, tail=(0,0), color=colors.RED):
        self.tip = tip
        self.tail = tail
        self.color = color


class Segment2D:
    def __init__(self, start_point, end_point, color=colors.BLUE):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color


def round_up_to_multiple(val,size):
    return ceil((val + size) / size) * size


def round_down_to_multiple(val,size):
    return -floor((-val - size) / size) * size


def extract_vectors_2D(objects):
    for object in objects:
        if isinstance(object, Points2D):
            for vector in object.vectors:
                yield vector
        elif isinstance(object, Arrow2D):
            yield object.tip
            yield object.tail
        elif isinstance(object, Segment2D):
            yield object.start_point
            yield object.end_point
        elif isinstance(object, Polygon2D):
            for vertex in object.vertices:
                yield vertex
        else:
            raise ValueError(f"Unknown object type: {type(object)}")
        

def draw_2D(*objects, origin=True, axes=True, grid=(1,1), nice_aspect_ratio=True, width=6, save_as=None):
    all_vectors = list(extract_vectors_2D(objects)) 
    xs, ys = zip(*all_vectors)

    max_x, max_y, min_x, min_y = max(0, *xs), max(0, *ys), min(0, *xs), min(0, *ys)

    if grid: 
        x_padding = max(ceil(max_x - min_x), grid[0])
        y_padding = max(ceil(max_y - min_y), grid[1])
        plt.xlim(round_down_to_multiple(min_x, grid[0]), round_up_to_multiple(max_x, grid[0]))
        plt.ylim(round_down_to_multiple(min_y, grid[1]), round_up_to_multiple(max_y, grid[1]))

    else:
        x_padding = 0.05 * (max_x - min_x)
        y_padding = 0.05 * (max_y - min_y)
        plt.xlim(min_x - x_padding, max_x + x_padding)
        plt.ylim(min_y - y_padding, max_y + y_padding)
    
    if origin: 
        plt.scatter([0], [0], color=colors.BLACK, marker="x" )

    if grid:
        plt.gca().axhline(linewidth=2, color=colors.BLACK)
        plt.gca().axvline(linewidth=2, color=colors.BLACK)
    
    for object in objects:
        if type(object) == Polygon2D:
            if object.color:
                for i in range(0,len(object.vertices)):
                    x1, y1 = object.vertices[i]
                    x2, y2 = object.vertices[(i+1)%len(object.vertices)]
                    plt.plot([x1,x2],[y1,y2], color=object.color)
            if object.fill:
                patches = []
                poly = Polygon(object.vertices, True)
                patches.append(poly)
                p = PatchCollection(patches, color=object.fill)
                plt.gca().add_collection(p)
        elif type(object) == Points2D:
            xs = [v[0] for v in object.vectors]
            ys = [v[1] for v in object.vectors]
            plt.scatter(xs,ys,color=object.color)
        elif type(object) == Arrow2D:
            tip, tail = object.tip, object.tail
            tip_length = (plt.xlim()[1] - plt.xlim()[0]) / 20.
            length = sqrt((tip[1]-tail[1])**2 + (tip[0]-tail[0])**2)
            new_length = length - tip_length
            new_y = (tip[1] - tail[1]) * (new_length / length)
            new_x = (tip[0] - tail[0]) * (new_length / length)
            plt.gca().arrow(tail[0], tail[1], new_x, new_y,
            head_width=tip_length/1.5, head_length=tip_length,
            fc=object.color, ec=object.color)
        elif type(object) == Segment2D:
            x1, y1 = object.start_point
            x2, y2 = object.end_point
            plt.plot([x1,x2],[y1,y2], color=object.color)
        else:
            raise ValueError("Unrecognized object: {}".format(object))
    
    fig = plt.gcf()

    if nice_aspect_ratio:
        coords_height = (plt.ylim()[1] - plt.ylim()[0])
        coords_width = (plt.xlim()[1] - plt.xlim()[0])
        fig.set_size_inches(width , width * coords_height / coords_width)

    if save_as:
        plt.savefig(save_as)

    plt.show()