harmony_table = {
    # chromatic scale
    'chromatic': {
        'scale': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        'size': 12
    },
    # greek modes
    'ionian': {
        'scale': [0, 2, 4, 5, 7, 9, 11],
        'size': 7
    },
    'dorian': {
        'scale': [0, 2, 3, 5, 7, 9, 10],
        'size': 7
    },  
    'phrygian': {
        'scale': [0, 1, 3, 5, 7, 8, 10],
        'size': 7
    },  
    'lydian': {
        'scale': [0, 2, 4, 6, 7, 9, 11],
        'size': 7
    },  
    'mixolydian': {
        'scale': [0, 2, 4, 5, 7, 9, 10],
        'size': 7
    },  
    'aeolian': {
        'scale': [0, 2, 3, 5, 7, 8, 10],
        'size': 7
    },
    'locrian': {
        'scale': [0, 1, 3, 5, 6, 8, 10],
        'size': 7
    },
    # harmonic minor modes
    'harmonicMinor': {
        'scale': [0, 2, 3, 5, 7, 8, 11],
        'size': 7
    },
    'melodicMinor': {
        'scale': [0, 2, 3, 5, 7, 9, 11],
        'size': 7
    },
    'lydianDominant': {
        'scale': [0, 2, 4, 6, 7, 9, 10],
        'size': 7
    },
    # symmetric scales
    'wholeTone': {
        'scale': [0, 2, 4, 6, 8, 10],
        'size': 6
    },  
    'wholeHalfStep': {
        'scale': [0, 2, 3, 5, 6, 8, 9, 11],
        'size': 8
    },      
    'halfWholeStep': {
        'scale': [0, 1, 3, 4, 6, 7, 9, 10],
        'size': 8
    },      
    # pentatonic scales
    'majorPentatonic': {
        'scale': [0, 2, 4, 7, 9],
        'size': 5
    },          
    'minorPentatonic': {
        'scale': [0, 3, 5, 7, 10],
        'size': 5
    },          
    'suspendedPentatonic': {
        'scale': [0, 2, 5, 7, 10],
        'size': 5
    },  
    'inSen': {
        'scale': [0, 1, 5, 7, 10],
        'size': 5
    },  
    # derived scales
    'blues': {
        'scale': [0, 3, 5, 6, 7, 10],
        'size': 6
    },      
    'majorBebop': {
        'scale': [0, 2, 4, 5, 7, 8, 9, 11],
        'size': 8
    },      
    'dominantBebop': {
        'scale': [0, 2, 4, 5, 7, 9, 10, 11],
        'size': 8
    },
    'minorBebop': {
        'scale': [0, 2, 3, 4, 5, 7, 9, 10],
        'size': 8
    },      
    'minorBebop': {
        'scale': [0, 2, 3, 4, 5, 7, 9, 10],
        'size': 8
    },
	# arpeggios
    'majorArp': {
        'scale': [0, 4, 7],
        'size': 3
    },      
    'minorArp': {
        'scale': [0, 3, 7],
        'size': 3
    },  
    'majorMaj7Arp': {
        'scale': [0, 4, 7, 11],
        'size': 4
    }, 
    'majorMin7Arp': {
        'scale': [0, 4, 7, 10],
        'size': 4
    }, 	
    'minorMin7Arp': {
        'scale': [0, 3, 7, 10],
        'size': 4
    }, 	
    'minorMaj7Arp': {
        'scale': [0, 3, 7, 11],
        'size': 4
    }, 	
    'majorMaj7Arp9': {
        'scale': [0, 2, 4, 7, 11],
        'size': 5
    }, 		
    'majorMaj7ArpMin9': {
        'scale': [0, 1, 4, 7, 11],
        'size': 5
    }, 	
    'majorMin7Arp9': {
        'scale': [0, 2, 4, 7, 10],
        'size': 5
    }, 		
    'majorMin7ArpMin9': {
        'scale': [0, 1, 4, 7, 10],
        'size': 5
    }, 		
    'minorMin7Arp9': {
        'scale': [0, 2, 3, 7, 10],
        'size': 5
    }, 		
    'minorMin7ArpMin9': {
        'scale': [0, 1, 3, 7, 10],
        'size': 5
    }, 										
    'minorMaj7Arp9': {
        'scale': [0, 2, 3, 7, 11],
        'size': 5
    }, 		
    'minorMaj7ArpMin9': {
        'scale': [0, 1, 3, 7, 11],
        'size': 5
    }, 		
    'minorMaj7ArpMin9': {
        'scale': [0, 1, 3, 7, 11],
        'size': 5
    }, 			
}

class Harmony:

    scale = 'chromatic'
    selected_scale_index = 0

    def harmonize(self, note):
        if self.scale is None:
            return note
        octave = int(note / harmony_table[self.scale]['size'])
        relative_note = note % harmony_table[self.scale]['size']
        return harmony_table[self.scale]['scale'][relative_note] + (octave*12)

    def set_harmony_by_index(self, index):
        tmp_index = self.selected_scale_index + index
        if (tmp_index < len(harmony_table) and tmp_index >= 0):
            self.selected_scale_index = tmp_index
            self.scale = list(harmony_table)[self.selected_scale_index]

    def set_harmony_by_name(self, name):
        if name in harmony_table:
            self.scale = name
            self.selected_scale_index = list(harmony_table).index(self.scale)    