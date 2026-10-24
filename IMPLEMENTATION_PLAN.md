# Implementation Plan: Stem-to-MIDI Orchestrator

End-to-end multi-instrument audio-to-MIDI orchestrator that isolates mixed audio into individual stems, runs instrument-specific Basic Pitch neural models, and compiles both individual MIDI tracks and a unified multi-track Type 1 MIDI arrangement file.

---

## Deliverables Checklist

### v1.0.0 — Initial Release
- [x] **Core Orchestration Script**: `scripts/orchestrate.py` automating end-to-end pipeline (audio -> stems -> MIDI -> unified arrangement). ✅ done in v1.0.0
- [x] **Dual Input Support**: Handles both raw mixed audio files (`.wav`, `.mp3`, `.flac`) and pre-existing `_stems` directories. ✅ done in v1.0.0
- [x] **Stem-Specific Neural Presets**: Monophonic vocal lead, low-pass clamped bass (<320 Hz), polyphonic guitar/piano chord voicer, and synth pads. ✅ done in v1.0.0
- [x] **Type 1 Multi-Track Compiler**: `pretty_midi` integration merging individual stems into a single arrangement file with General MIDI program maps. ✅ done in v1.0.0
- [x] **Tri-Platform Accessibility**: Canonical `.agents` installation linked to Claude, Grok, and Antigravity via NTFS junctions. ✅ done in v1.0.0
- [x] **Standard Documentation Suite**: `SKILL.md`, `HOW_TO_USE.txt`, `README.md`, `App Changes Tracker.html`, and `dev-notes-v1.0.0.md`. ✅ done in v1.0.0

---

## Roadmap & Future Enhancements

### v1.1.0 — Drum-to-MIDI Transcriber
- [ ] Add AI drum transcription stem isolating Kick (Note 36), Snare (Note 38), and Hi-Hats (Note 42) into General MIDI Channel 10.
- [ ] Quantization options (1/16, 1/8 triplets, swing presets).
- [ ] Velocity curve normalization.

### v1.2.0 — Direct Ableton Project (.als) Generation
- [ ] Export directly as an Ableton Live Set (`.als`) with pre-loaded virtual instruments on each track.
- [ ] Export individual clips into Ableton User Library (`A:\User Library\Clips\Arrangements`).
