# Stem-to-MIDI Orchestrator & Multi-Track MIDI Exporter

> **Tri-Platform Agent Skill** for Claude Desktop / Code, Grok CLI, and Google Antigravity / Gemini.  
> End-to-end multi-instrument audio-to-MIDI orchestrator that isolates mixed audio into individual stems, runs instrument-specific Basic Pitch neural models, and compiles both individual MIDI tracks and a unified multi-track Type 1 MIDI arrangement file.

---

## Overview

Transcribing an entire mixed audio track into MIDI with a single polyphonic model inevitably leads to cross-talk, guitar-vocal collision, and muddy low-end. 

**`stem-to-midi-orchestrator`** solves this by establishing an end-to-end production pipeline:
1. **Source Separation**: Splits mixed audio into isolated stems (`vocals`, `bass`, `guitar`, `piano`, `other`) using Mel-Band RoFormer and MDX-Net Kuielab.
2. **Specialized Neural Transcription**: Transcribes each isolated stem using Spotify Basic Pitch parameters customized for that instrument's acoustic profile.
3. **Unified Multi-Track Assembly**: Merges all individual tracks into a single standard **Type 1 Multi-Track MIDI** arrangement file (`{song}_full_arrangement.mid`), tagged with General MIDI instrument programs and channel labels.

---

## Neural Transcription Profiles

| Stem | General MIDI Program | Preset Characteristics |
| :--- | :--- | :--- |
| **`vocals.mid`** | 54 (Synth Voice) | Strict monophonic melody tracking, breath rejection, and vibrato smoothing. |
| **`bass.mid`** | 33 (Electric Bass) | Low-pass frequency clamping (<320 Hz) with sub-bass legato gap merging. |
| **`guitar.mid`** | 25 (Steel Acoustic) | Polyphonic strumming onset alignment and multiple pitch bend tracking. |
| **`piano.mid`** | 0 (Acoustic Grand) | Full dynamic velocity range tracking and wide keyboard voicings. |
| **`other.mid`** | 81 (Lead / Synth Pad) | Polyphonic background harmony, strings, and synth layer capture. |

---

## CLI Usage

The script accepts either a raw mixed audio file or a pre-existing stems directory:

```bash
# 1. End-to-end separation + MIDI transcription:
python scripts/orchestrate.py "C:\Music\MySong.mp3"

# 2. Custom separation models:
python scripts/orchestrate.py "C:\Music\MySong.mp3" --vocal-method roformer --bass-method mdx-kuielab

# 3. Transcribe an existing stems folder:
python scripts/orchestrate.py "C:\Music\MySong_stems"
```

### Output Layout
```
{song_directory}/{song_name}_stems/
├── drums.wav
├── bass.wav
├── guitar.wav
├── piano.wav
├── vocals.wav
├── other.wav
├── bass.mid
├── guitar.mid
├── piano.mid
├── vocals.mid
├── other.mid
├── {song_name}_full_arrangement.mid    # Drag-and-drop into Ableton / DAW
└── stems_manifest.json
```

---

## Tri-Platform Architecture

Zero duplicate code across tools. Canonical source resides in `.agents`:
- **Canonical**: `C:\Users\<you>\.agents\skills\stem-to-midi-orchestrator`
- **Claude**: `C:\Users\<you>\.claude\skills\stem-to-midi-orchestrator` (NTFS Junction)
- **Grok**: `C:\Users\<you>\.grok\skills\stem-to-midi-orchestrator` (NTFS Junction)
- **Antigravity**: `C:\Users\<you>\.gemini\config\skills\stem-to-midi-orchestrator` (NTFS Junction)

---

## Documentation Suite

- [`HOW_TO_USE.txt`](file:///C:/Users/<you>/.agents/skills/stem-to-midi-orchestrator/HOW_TO_USE.txt): Standardized user guide and prompt templates.
- [`IMPLEMENTATION_PLAN.md`](file:///C:/Users/<you>/.agents/skills/stem-to-midi-orchestrator/IMPLEMENTATION_PLAN.md): Feature checklist and roadmap.
- [`App Changes Tracker.html`](file:///C:/Users/<you>/.agents/skills/stem-to-midi-orchestrator/App%20Changes%20Tracker.html): Interactive visual version log.
- [`SKILL.md`](file:///C:/Users/<you>/.agents/skills/stem-to-midi-orchestrator/SKILL.md): Agent system instructions and triggers.
