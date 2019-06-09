import signal
import time
import rtmidi
from . import handlers
from .lib.keyboard import keyboard
#from .lib.mouse import mouse
from .harmonizer import Harmony

class Core:
        """Input2Midi main core

        Usage::
                >>> from input2midi import input2midi
                >>> opendsp = input2midi.Core()
                >>> opendsp.init()
                >>> opendsp.run()
        """

        # self instance for singleton control
        _singleton = None    

        #action_mode = False
        running = False
        midi = None

        # our main runtime object for input2midi actions
        keymap = {}

        # main harmonizer object
        harmony = None

        def __init__(self):        
                # singleton him
                if Core._singleton:
                        raise Core._singleton
                Core._singleton = self
                signal.signal(signal.SIGINT, self.signal_handler)
                signal.signal(signal.SIGTERM, self.signal_handler)

        def __del__(self):
                self.stop()

        def init(self, map_config):
                self.harmony = Harmony()
                # parse our map_config into keymap object for runtime logic
                self.generate_keymap(map_config['keyboard'], self.keymap)
                # Init virtual midi port    
                self.init_midi()
                # installs the global keyboard hook
                keyboard.hook(self.hook_keyboard)
                # special action trigger
                keyboard.add_hotkey('ctrl+x', self.action_mode_call)
                # installs the global mouse hook
                #mouse.hook(hookMouse)

        def run(self):
                # set running state 
                self.running = True
                # Block me... and let the hook threads do their jobs
                while self.running:
                        time.sleep(100)

        def stop(self):
                # remove the keyboard hook
                keyboard.unhook_all()
                # remove the mouse hook
                #mouse.unhook_all()
                # clear midi_out object
                del self.midi_out

        # catch SIGINT and SIGTERM and stop application
        def signal_handler(self, sig, frame):
                self.running = False

        def hook_keyboard(self, event):
                """
                On each keyboard event, check the keymap dictionary
                for a registred action callback handler
                """
                obj = self.keymap.get(event.name, None)
                if obj is not None:
                        # call the action callback registred based on .json config along with params and memory data, event type and midi_out serial object
                        obj['callback'](obj['params'], obj['data'], event.event_type, self._singleton)
                        
        def hook_mouse(self, event):
                print(event)

        def action_mode_call(self):
                #action_mode = True
                print('action call')

        def init_midi(self):
                self.midi = rtmidi.MidiOut(rtapi=rtmidi.API_UNIX_JACK, name='inputtomidi')
                ##self.midi_obj = rtmidi.MidiOut(rtapi=rtmidi.API_LINUX_ALSA, name='inputtomidi')
                self.midi.open_virtual_port('out')


        def generate_keymap(self, keymap_data, data):
                """
                Returns a dictionary of keycodes that contains a 
                list of [ callbackHandler, callbackParams[], value ]
                """
                try:
                        # iterate over each keyboard setup object
                        for obj in keymap_data:
                                # generic parse
                                obj_params = obj['params']
                                obj_params['channel'] = obj_params['channel']-1

                                # notepad parse
                                if obj['type'] == 'notepad':
                                        callback = handlers.notepad
                                        if 'harmonize' in obj_params:
                                                self.harmony.set_harmony_by_name(obj_params['harmonize'])
                                        # parse map?
                                        if 'map' in obj:
                                                for i in range(len(obj['map'])):
                                                        obj_data = {}
                                                        obj_data['value'] = 0
                                                        obj_data['note'] = i
                                                        # assign new global data keymap
                                                        data[obj['map'][i]] = { 'callback': callback, 'params': obj_params, 'data': obj_data }
                                        # parse cmd request?
                                        if 'select-root' in obj:
                                                # only two keys allowed for this cmd
                                                if len(obj['select-root']) == 2:
                                                        for i in range(2):
                                                                obj_data = {'cmd': {}}
                                                                obj_data['value'] = 0
                                                                if i == 0:
                                                                        obj_data['cmd']['prev_root_note'] = True
                                                                if i == 1:
                                                                        obj_data['cmd']['next_root_note'] = True
                                                                # assign new global data keymap
                                                                data[obj['select-root'][i]] = { 'callback': callback, 'params': obj_params, 'data': obj_data }
                                        if 'select-scale' in obj:
                                                # only two keys allowed for this cmd
                                                if len(obj['select-scale']) == 2:
                                                        for i in range(2):
                                                                obj_data = {'cmd': {}}
                                                                obj_data['value'] = 0
                                                                if i == 0:
                                                                        obj_data['cmd']['prev_scale'] = True
                                                                if i == 1:
                                                                        obj_data['cmd']['next_scale'] = True
                                                                # assign new global data keymap
                                                                data[obj['select-scale'][i]] = { 'callback': callback, 'params': obj_params, 'data': obj_data }

                                # drumpad parse
                                if obj['type'] == 'drumpad':
                                        callback = handlers.drumpad
                                        # parse map?
                                        if 'map' in obj:
                                                for i in range(len(obj['map'])):
                                                        obj_data = {}
                                                        obj_data['value'] = 0   
                                                        obj_data['index'] = i
                                                        # assign new global data keymap
                                                        data[obj['map'][i]] = { 'callback': callback, 'params': obj_params, 'data': obj_data }
                                        # parse cmd request?
                                        if 'select-note' in obj:
                                                # only two keys allowed for this cmd
                                                if len(obj['select-note']) == 2:
                                                        for i in range(2):
                                                                obj_data = {'cmd': {}}
                                                                obj_data['value'] = 0
                                                                if i == 0:
                                                                        obj_data['cmd']['prev_note'] = True
                                                                if i == 1:
                                                                        obj_data['cmd']['next_note'] = True
                                                                # assign new global data keymap
                                                                data[obj['select-note'][i]] = { 'callback': callback, 'params': obj_params, 'data': obj_data }
                except KeyError:
                        print('error while trying to parse the keymap config file')

        def generate_mousemap(obj_data):
                """
                Returns a dictionary of mousecodes that contains a 
                list of [ callbackHandler, calbackParams[], value ]
                """
                pass

        # on generate: str.lower() str.upper()?!?!

        # notes...
        #print(event.name)
        #print(event.scan_code)
        #print(event.device)
        #print(event.event_type)
        #print(event.is_keypad)
        #print(event.modifiers)
        #if action_mode == True:
        #        if event.name == 'esc':
        #                action_mode = False
        #                return
        #        print('action mode on')         


