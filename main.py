import sys

from src.synth_engine import SynthEngine
import pygame.midi
from PyQt6.QtWidgets import QApplication, QLabel, QWidget


def main():
    # Debug PyQT App
    # app = QApplication([])
    # print(app)

    # window = QWidget()
    # window.setWindowTitle("PyQt App")
    # window.setGeometry(100, 100, 280, 80)
    # helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
    # helloMsg.move(60, 15)

    # window.show()
    # sys.exit(app.exec())

    # MIDI App
    pygame.midi.init()
    
    default_id = pygame.midi.get_default_input_id()
    midi_input = pygame.midi.Input(device_id=default_id)
    try: 
        while True:
            if midi_input.poll():
                print(midi_input.read(num_events=16))
    except KeyboardInterrupt as err:
        print("Stopping...")
    
    pygame.midi.quit()


    # Synthesizer Instrument Generation
    # engine: SynthEngine = SynthEngine()
    # engine.run()


if __name__ == "__main__":
    main()
