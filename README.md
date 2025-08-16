# audioSynth
Following the spirit of raytracerInOneWeekend I am learning about audio processing by writing a custom synthesizer!

## Setup
Virtual MIDI Keyboard: https://vmpk.sourceforge.io/
MIDI Loopback Listener: https://www.nerds.de/en/loopbe1.html
For virtual connections both must be listening, and the VMPK output connection must be attached to the loopback driver for pygame to pick it up.

## Feature List 
### Basic Usage
- [x] Basic waveforms
- [ ] Envelopes
- [ ] LFO; AM, FM
- [ ] Panner
- [ ] Modifier Chain
- [ ] Polyphany
- [ ] MIDI Input
- [ ] Keyboard Input
- [ ] Instrument sequencer
### User Interface
- [ ] GUI Sequencer
- [ ] GUI Instrument, track, effects creation
- [ ] GUI Sliders and options to change instrument settings
- [ ] Waveform visualisation
- [ ] Ability to save tracks into a midi file
- [ ] Ability to load midi files
### Noise Generation
- [ ] New noise oscillators (pink, white, fbm)
- [ ] Oscillator blend types
- [ ] Unison mode
- [ ] Karplus-Strong plucked string synthesis
### Post-Processing
- [ ] Filters (low-pass, high-pass, band-pass)
- [ ] Reverb
- [ ] Delay
- [ ] Distortion

