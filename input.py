import components
import sys

current_component_id = ''


# Function is responsible for calling the creation function,
# retrieving the component instance, ID, and ports, and adding
# the new component in the project database
def add_component(comp_string, canvas):
    # print(len(comp_string))
    # print(comp_string[0])
    # print(command_list.get(comp_string[0])[1])
    if comp_string[0] in command_list and len(comp_string) == \
            command_list.get(comp_string[0])[1]:
        print("adding " + comp_string[0] + " component...")
        components.draw_component(comp_string, canvas)
    else:
        print("bad command or incorrect number of parameters!")


# the primary container for all possible commands
# list structure (space separated parameters) : function | number of parameters
# pipe : main placement function | parent port number | direction
# elbow : main placement function | parent port number | direction 1 | direction 2
command_list = {"pipe": [add_component, 3],
                "elbow": [add_component, 4],
                "exit": [sys.exit]}


# primary input callback from ui
def input_manager(event, args):
    # print("event type: " + str(event.type))
    command_split = args[0].get().split()
    command_input = command_split[0]
    output_label = args[1].label.label
    if command_input in command_list:
        output_label.config(text='creating ' + str(args[0].get()) + '...')
        command_list.get(command_input)[0](command_split, args[2])
    else:
        output_label.config(text='bad command!')
    args[0].delete(0, len(args[0].get()))
