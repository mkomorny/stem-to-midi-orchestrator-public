#!/usr/bin/env python3
"""
Stem-to-MIDI Orchestrator & Multi-Track MIDI Exporter
Powered by Spotify Basic Pitch, Demucs / RoFormer, and pretty_midi.

Features:
- Orchestrates multi-stem audio-to-MIDI conversion using stem-specific neural presets.
- Merges individual transcribed stems into a single unified Multi-Track Type 1 MIDI file.
- Automatically assigns standard GM instrument programs and channel labels.
- Works either on an existing stem folder or directly on a raw mixed audio song.
"""

import os
import sys
import warnings
import logging
import json
import argparse
import importlib.util
import subprocess
from pathlib import Path

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

BASIC_PITCH_PYTHON = r"C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe"

# Auto re-exec in dedicated uv environment if needed
if not importlib.util.find_spec("basic_pitch"):
    if os.path.exists(BASIC_PITCH_PYTHON) and sys.executable.lower() != BASIC_PITCH_PYTHON.lower():
        result = subprocess.run([BASIC_PITCH_PYTHON] + sys.argv)
        sys.exit(result.returncode)

import numpy as np
import pretty_midi
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

# Import transcription helpers from stem-separation
STEM_SEP_SCRIPTS = Path(r"C:\Users\<you>\.agents\skills\stem-separation\scripts")
if str(STEM_SEP_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(STEM_SEP_SCRIPTS))

from stem_midi_transcriber import transcribe_stem, PRESETS

GM_PROGRAMS = {
    "vocals": 54,     # Synth Voice (or 52 Choir Aahs)
    "vocals_dry": 54,
    "bass": 33,       # Electric Bass (finger)
    "guitar": 25,     # Acoustic Guitar (steel)
    "piano": 0,       # Acoustic Grand Piano
    "other": 81,      # Lead 2 (sawtooth) / Pad
}


def build_unified_multitrack_midi(stem_midi_paths: dict, output_unified_path: str) -> str:
    """Combines individual stem .mid files into a single multi-track Type 1 MIDI file."""
    unified = pretty_midi.PrettyMIDI()

    for stem_name, mid_path in stem_midi_paths.items():
        if not os.path.exists(mid_path):
            continue
        try:
            pm = pretty_midi.PrettyMIDI(mid_path)
            for inst in pm.instruments:
                program = GM_PROGRAMS.get(stem_name, 0)
                inst.program = program
                inst.name = f"{stem_name.upper()}"
                unified.instruments.append(inst)
        except Exception as e:
            print(f"[!] Warning: Could not merge {mid_path}: {e}")

    unified.write(output_unified_path)
    print(f"[+] Unified multi-track MIDI saved: {output_unified_path}")
    return output_unified_path


def orchestrate_stem_to_midi(target_path: str, vocal_method: str = "roformer", bass_method: str = "mdx-kuielab") -> dict:
    target = Path(target_path).resolve()
    if not target.exists():
        raise FileNotFoundError(f"Target not found: {target}")

    stem_files = {}

    # Case A: target is already a directory containing stems
    if target.is_dir():
        print(f"[*] Target is a stem directory: {target}")
        for f in target.iterdir():
            if f.is_file() and f.suffix.lower() in (".wav", ".mp3", ".flac"):
                stem_name = f.stem.lower()
                if stem_name in ("vocals", "vocals_dry", "bass", "guitar", "piano", "other", "instrumental"):
                    stem_files[stem_name] = str(f)
        output_dir = target
        track_title = target.name.replace("_stems", "")
    else:
        # Case B: target is a single mixed audio file -> run stem separation first
        print(f"[*] Target is an audio track: {target.name}")
        print(f"[*] Executing SOTA stem separation (Vocals: {vocal_method}, Bass: {bass_method})...")
        sep_script = STEM_SEP_SCRIPTS / "separate_stems.py"
        cmd = [
            sys.executable, str(sep_script), str(target),
            "--vocal-method", vocal_method,
            "--bass-method", bass_method,
            "--bass-polish",
            "--to-midi"
        ]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            raise RuntimeError(f"Stem separation failed with code {result.returncode}")

        output_dir = target.parent / f"{target.stem}_stems"
        manifest_path = output_dir / "stems_manifest.json"
        if manifest_path.exists():
            with open(manifest_path, "r", encoding="utf-8") as mf:
                manifest = json.load(mf)
                return {
                    "output_dir": str(output_dir),
                    "stems": manifest.get("stems", {}),
                    "midi_files": manifest.get("midi_files", {})
                }
        track_title = target.stem

    # If we started from an existing stems dir, run transcriptions
    midi_paths = {}
    STEM_PRESET_MAP = {
        "vocals": "vocal",
        "vocals_dry": "vocal",
        "bass": "bass",
        "guitar": "guitar",
        "piano": "piano",
        "other": "chords",
        "instrumental": "chords"
    }

    for stem_name, audio_path in stem_files.items():
        preset = STEM_PRESET_MAP.get(stem_name, "default")
        out_mid = str(Path(audio_path).with_suffix(".mid"))
        try:
            transcribe_stem(audio_path, output_midi_path=out_mid, preset_name=preset)
            midi_paths[stem_name] = out_mid
        except Exception as e:
            print(f"[!] Error transcribing {stem_name}: {e}")

    # Build unified Type 1 MIDI
    unified_mid_path = str(output_dir / f"{track_title}_full_arrangement.mid")
    build_unified_multitrack_midi(midi_paths, unified_mid_path)
    midi_paths["full_arrangement"] = unified_mid_path

    return {
        "output_dir": str(output_dir),
        "midi_files": midi_paths
    }


def main():
    parser = argparse.ArgumentParser(description="Stem-to-MIDI Orchestrator & Multi-Track MIDI Exporter")
    parser.add_argument("target", help="Path to mixed audio file OR existing _stems directory")
    parser.add_argument("--vocal-method", default="roformer", help="Vocal isolation method (if separating)")
    parser.add_argument("--bass-method", default="mdx-kuielab", help="Bass isolation method (if separating)")

    args = parser.parse_args()

    res = orchestrate_stem_to_midi(args.target, vocal_method=args.vocal_method, bass_method=args.bass_method)
    print("\n[SUCCESS] Stem-to-MIDI Orchestration Complete:")
    print(f"  Stems Folder: {res['output_dir']}")
    for k, p in res.get("midi_files", {}).items():
        print(f"  - {k.upper():16} -> [{os.path.basename(p)}](file:///{p.replace(os.sep, '/')})")


if __name__ == "__main__":
    main()
