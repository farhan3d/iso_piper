# module to draw objects on the canvas

import constants
import geometry
import isoplane
import functools
import db_manager
import uuid


# a container for all components currently in the drawing
# this is required for realtime refresh purposes since we cannot
# retrieve the data from the database on ever screen resize
components_container = {}


# draw a straight line in either of the 3 directions
# direction : this can be eithe x, y, or z
# x0 : the x component of the start point of the line
# y0 : the y component of the start point of the line
# line_length : optional length of the line relative to the bounding box
#               if not provided, length will be automatically adjusted
#               based on limits of the box to fit the entire set of graphics
# angle : the angle of the line relative to the current plane
def line(canvas, x0, y0, color, line_tag, direction='', line_length=0,
         line_thk=1, angle=0):
    second_point = geometry.translate_along_vector([x0, y0],
                                                   isoplane.dir_vec_map[direction],
                                                   line_length)
    line_item = canvas.create_line(x0, y0, second_point[0], second_point[1],
                                   fill=color, tags=line_tag, width=line_thk)
    return line_item


def toggle_plane(canvas):
    if isoplane.current_plane == 2:
        isoplane.planes_iterable = iter(isoplane.planes_dict)
        isoplane.current_plane = next(isoplane.planes_iterable)
        isoplane.current_plane = 0
    else:
        isoplane.current_plane = next(isoplane.planes_iterable)
    draw_isoplane(canvas)


# initialization is required since winfo_width and winfo_height do not
# return the correct parameters when the canvas is first initialized
def initialize_isoplane(canvas):
    base_pt = [constants.LEFT_PADDING, constants.DEFAULT_CANVAS_HEIGHT
               - constants.BOTTOM_PADDING]
    curr_plane_str = isoplane.planes_dict[isoplane.current_plane]
    canvas.create_line(base_pt[0], base_pt[1],
                       constants.LEFT_PADDING, constants.DEFAULT_CANVAS_HEIGHT
                       - constants.BOTTOM_PADDING
                       - constants.TRIAD_LEN, fill="red", tags="triadlinez",
                       width=('z' in curr_plane_str) * constants.TRIAD_THK)
    line(canvas, base_pt[0], base_pt[1], 'green3', "triadlinex", 'x',
         constants.TRIAD_LEN, ('x' in curr_plane_str) * constants.TRIAD_THK)
    line(canvas, base_pt[0], base_pt[1], 'gold2', "triadliney", 'y',
         constants.TRIAD_LEN, ('x' in curr_plane_str) * constants.TRIAD_THK)
    next(isoplane.planes_iterable)


def draw_isoplane(canvas):
    base_pt = [constants.LEFT_PADDING, canvas.winfo_height()
               - constants.BOTTOM_PADDING]
    curr_plane_str = isoplane.planes_dict[isoplane.current_plane]
    if canvas.winfo_height() == 1:
        initialize_isoplane(canvas)
        # self.redraw()
    else:
        z_line = canvas.find_withtag("triadlinez")
        if z_line:
            canvas.delete("triadlinez")
            canvas.create_line(base_pt[0], base_pt[1], constants.LEFT_PADDING,
                               canvas.winfo_height() - constants.BOTTOM_PADDING
                               - constants.TRIAD_LEN, fill="red", tags="triadlinez",
                               width=('z' in curr_plane_str) * constants.TRIAD_THK)
        x_line = canvas.find_withtag("triadlinex")
        if x_line:
            canvas.delete("triadlinex")
            line(canvas, base_pt[0], base_pt[1], 'green3', "triadlinex", 'x',
                 constants.TRIAD_LEN, ('x' in curr_plane_str) * constants.TRIAD_THK)
        y_line = canvas.find_withtag("triadliney")
        if y_line:
            canvas.delete("triadliney")
            line(canvas, base_pt[0], base_pt[1], 'gold2', "triadliney", 'y',
                 constants.TRIAD_LEN, ('y' in curr_plane_str) * constants.TRIAD_THK)


def draw_pipe(args, canvas):
    # get current window dimensions
    print(canvas)

    # determine the location of the existing port that the pipe
    # needs to be connected to. if no free ports available, place
    # the pipe in space

    # determine location of ports based on direction specified

    # recompute the rectangular center of all the ports currently
    # in the model space and scale down + readjust the entire model

    # create a unique pipe id and commit all information to the db

    pass


def draw_elbow(args):
    pass


draw_methods = {'pipe': draw_pipe,
                'elbow': draw_elbow}


# Function should create a component ID and ports location list,
# and return them to the calling function in input.py for storage
# Function is also responsible for drawing the component by creating
# a new instance of the component type
def draw_component(command_string, canvas):
    params = command_string[1:]
    draw_methods.get(command_string[0])(params, canvas)
