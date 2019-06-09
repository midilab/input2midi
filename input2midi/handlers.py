# notepad global data
#...

# drumpad global data
last_index = 0

def notepad(param, data, state, core):
    """
    Handle a serial tone keypad for notes
    """
    if state == 'down' and data['value'] == 0:
        data['value'] = 1
        # a command request?
        if 'cmd' in data:
            # prev and next root note
            if 'prev_root_note' in data['cmd']:
                param['root-note'] -= 1
            if 'next_root_note' in data['cmd']:
                param['root-note'] += 1
            # prev and next harmonic rules
            if 'prev_scale' in data['cmd']:
                core.harmony.set_harmony_by_index(-1)
            if 'next_scale' in data['cmd']:
                core.harmony.set_harmony_by_index(1)
        # a midi note request?
        else:
            data['note_on'] = core.harmony.harmonize(data['note'] + param['root-note'])
            #print("note on harmony: {scale} ch:{channel} note:{note} vel:{velocity}".format(scale=core.harmony.scale, channel=param['channel'], note=data['note_on'], velocity=param['velocity']))
            core.midi.send_message([0x90 | param['channel'], data['note_on'], param['velocity']]) # Note on
    elif state == 'up':
        data['value'] = 0
        if 'cmd' not in data:
            #print("note off ch:{channel} note:{note} vel:{velocity}".format(channel=param['channel'], note=data['note_on'], velocity=param['velocity']))
            core.midi.send_message([0x80 | param['channel'], data['note_on'], param['velocity']]) # Note off

def drumpad(param, data, state, core):
    """
    Handle various individual drum pads per key
    """
    global last_index
    if state == 'down' and data['value'] == 0:
        data['value'] = 1
        # a command request?
        if 'cmd' in data:
            if 'prev_note' in data['cmd']:
                param['note'][last_index] -= 1
            if 'next_note' in data['cmd']:
                param['note'][last_index] += 1
        # a midi note request?
        else:
            #print("note on drums ch:{channel} note:{note} vel:{velocity}".format(channel=param['channel'], note=param['note'][data['index']], velocity=param['velocity']))
            core.midi.send_message([0x90 | param['channel'], param['note'][data['index']], param['velocity']]) # Note on
            last_index = data['index']
    elif state == 'up':
        data['value'] = 0
        if 'cmd' not in data:
            if param['note-off']:
                #print("note off drums ch:{channel} note:{note} vel:{velocity}".format(channel=param['channel'], note=data['note'][data['index']], velocity=param['velocity']))
                core.midi.send_message([0x80 | param['channel'], param['note'][data['index']], param['velocity']]) # Note off

def mouse(param, state):
    print(param)
