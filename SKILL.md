---
name: stem-to-midi-orchestrator
description: End-to-end multi-instrument audio-to-MIDI orchestrator. Splits mixed audio into stems (vocals, bass, drums, guitar, piano, other) using state-of-the-art AI separation, runs instrument-specific Basic Pitch neural models on each stem, and compiles both individual MIDI tracks and a unified multi-track Type 1 MIDI arrangement file.
---

# Stem-to-MIDI Orchestrator & Multi-Track Exporter

Takes any finished mixed song or audio loop, isolates each instrument via state-of-the-art stem separation (Mel-Band RoFormer & MDX-Net Kuielab), and transcribes each tonal stem into tailored MIDI tracks using Spotify's Basic Pitch.

## Workflow & Output Structure

1. **Stem Isolation**: Separates the audio file into 6 stems (`vocals.wav`, `bass.wav`, `guitar.wav`, `piano.wav`, `other.wav`, `drums.wav`).
2. **Neural Preset Transcription**:
   - **`vocals.mid`**: Monophonic vocal lead tracking, breath rejection, and vibrato smoothing.
   - **`bass.mid`**: Clamped to low frequencies (< 320 Hz) with sub-bass legato gap merging.
   - **`guitar.mid`**: Polyphonic strumming alignment and multiple pitch bends.
   - **`piano.mid`**: Wide dynamic velocity tracking and keyboard chord voicings.
   - **`other.mid`**: Polyphonic synthesizer and background harmony capture.
3. **Unified Arrangement File**: Combines all transcribed stems into a single **`{song}_full_arrangement.mid`** (Standard Type 1 Multi-Track MIDI) with General MIDI program assignments and track labels, ready to drop into any DAW.

---

## Usage

```bash
# Full end-to-end separation and multi-track MIDI extraction:
python "C:\Users\<you>\.agents\skills\stem-to-midi-orchestrator\scripts\orchestrate.py" "C:\Music\MySong.mp3"

# Transcribe an existing stems folder:
python "C:\Users\<you>\.agents\skills\stem-to-midi-orchestrator\scripts\orchestrate.py" "C:\Music\MySong_stems"
```
