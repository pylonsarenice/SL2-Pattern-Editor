import json
import os
import PySimpleGUI as sg

cwd = os.getcwd()
input_file = os.path.join(cwd, 'template.tsl')
output_file = os.path.join(cwd, 'test.tsl')

nsteps = 24

fx_list = [
    'OFF',
    'PITCH',
    'FLANGER',
    'PHASER',
    'SWEEP',
    'FILTER',
    'RING',
    ]

step_list = [
    8,
    12,
    16,
    24,
    ]


def read_json(path):
    with open(path, 'r') as f:
        contents = json.load(f)
    return contents


def write_json(path, contents):
    with open(path, 'w') as f:
        json.dump(contents, f)
    return


def convert_decimal_to_hex_string(decimal):
    """Convert decimal to hex string"""
    return hex(int(decimal))[2:].zfill(2).upper()


def make_window(theme='Dark Blue 3'):

    sg.theme(theme)

    layout = []

    layout += [[
        sg.Text('Template:'),
        sg.Input(key='input_file', default_text=input_file, expand_x=True),
        sg.FileBrowse(button_text='Select', file_types=(("TSL Files", "*.tsl"),)),
        sg.Text('Output:'),
        sg.Input(key='output_file', default_text=output_file, expand_x=True),
        sg.FileBrowse(button_text='Select', file_types=(("TSL Files", "*.tsl"),)),
        sg.Button('Write', expand_x=True),
        ]]

    layout += [[
        sg.Text('Effect:'),
        sg.Combo(fx_list, default_value=fx_list[1], s=(15, 22), enable_events=True, readonly=True, key='fx', expand_x=True),
        sg.Text('# steps:'),
        sg.Combo(step_list, default_value=step_list[2], s=(15, 22), enable_events=True, readonly=True, key='step', expand_x=True),
        ]]
    layout += [[sg.Text('Length', expand_x=True, justification='center')]]
    layout += [[sg.Slider((0, 100), orientation='v', default_value=32, size=(8, 15), enable_events=True, key='length_{}'.format(i)) for i in range(0, nsteps)]]
    layout += [[sg.Text('Levels', expand_x=True, justification='center')]]
    layout += [[sg.Slider((0, 100), orientation='v', default_value=64, size=(8, 15), enable_events=True, key='level_{}'.format(i)) for i in range(0, nsteps)]]
    layout += [[sg.Text('Band', expand_x=True, justification='center')]]
    layout += [[sg.Slider((0, 6), orientation='v', default_value=0, size=(5, 15), enable_events=True, key='band_{}'.format(i), pad=((19, 5), (0, 0))) for i in range(0, nsteps)]]
    layout += [[sg.Text('Effect', expand_x=True, justification='center')]]
    layout += [[sg.Slider((0, 100), orientation='v', default_value=64, size=(8, 15), enable_events=True, key='effect_{}'.format(i)) for i in range(0, nsteps)]]
    layout += [[sg.Text('Pitch', expand_x=True, justification='center')]]
    layout += [[sg.Slider((-12, 12), orientation='v', default_value=0, size=(6, 15), enable_events=True, key='pitch_{}'.format(i), pad=((8, 5), (0, 0))) for i in range(0, nsteps)]]

    window = sg.Window(
        'SL-2 Pattern Editor',
        layout,
        )

    return window


window = make_window()

while True:  # Event Loop
    event, values = window.read()

    if event == 'Write':

        contents = read_json(values['input_file'])

        pattern = convert_decimal_to_hex_string(50)
        slicer_onoff = convert_decimal_to_hex_string(1)
        fx_type = convert_decimal_to_hex_string(fx_list.index(values['fx']))
        step_number = convert_decimal_to_hex_string(step_list.index(values['step']))

        basic = [pattern, slicer_onoff, fx_type, step_number]
        lengths = [convert_decimal_to_hex_string(values['length_{}'.format(i)]) for i in range(0, nsteps)]
        levels = [convert_decimal_to_hex_string(values['level_{}'.format(i)]) for i in range(0, nsteps)]
        bands = [convert_decimal_to_hex_string(values['band_{}'.format(i)]) for i in range(0, nsteps)]
        effects = [convert_decimal_to_hex_string(values['effect_{}'.format(i)]) for i in range(0, nsteps)]
        pitches = [convert_decimal_to_hex_string(values['pitch_{}'.format(i)]+12) for i in range(0, nsteps)]

        slicer = basic + lengths + levels + bands + effects + pitches

        contents['data'][0][0]['paramSet']['PATCH%SLICER(1)'] = slicer
        contents['data'][0][0]['paramSet']['PATCH%SLICER(2)'] = slicer

        write_json(values['output_file'], contents)

    if event == sg.WIN_CLOSED:
        break

window.close()
