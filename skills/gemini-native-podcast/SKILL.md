# Gemini Native Podcast Skill

## Overview
`scripts/gemini_podcast_gen.py` is the executable at the heart of this skill. It reads a multi-speaker script, renders each line via `gemini-2.5-flash-native-audio`, stitches the speaker WAVs together, mixes them with a looping lofi bed, and exports MP3/Opus deliverables. The skill documents how to operate the CLI end-to-end in a podcast-style workflow.

## Inputs
1. Gemini API key passed via `--api-key` or the `GENAI_API_KEY` environment variable for authenticated TTS calls.
2. A script, provided with `--script-text`, `--script-file`, or the built-in `--demo`, where each non-empty line follows `Speaker: dialogue` and may include emotional fillers such as `[laugh]`, `[sigh]`, or `[breath]`.
3. Optional `--speaker-voice Name=GeminiVoice` mappings to override or extend the default Aoede and Charon voices.

## Outputs
1. One or two final files inside `--output-dir` with the prefix `--output-prefix`:
   - MP3 using `libmp3lame` when `--output-format` is `mp3` or `both`.
   - Opus using `libopus` when `--output-format` is `opus` or `both`.
2. A cached copy of `bensound-littleidea.mp3` (downloading it only if missing) for consistent background ambiance.

## Workflow
1. Run the CLI with `scripts/gemini_podcast_gen.py --api-key $KEY --script-file myscript.txt`.
2. The script parses each `Speaker: line`, respecting emotional fillers, and uses `--speaker-voice` mappings to pick the Gemini voice per character.
3. Each segment is requested from Gemini with WAV output, then decoded and temporarily stored.
4. The segments are concatenated via `ffmpeg` and mixed with the background loop at ~25% volume so speech remains dominant.
5. Final encodings are produced with `libmp3lame` and/or `libopus`, saved under the chosen directory.

## Background Music Handling
- Background track: `https://www.bensound.com/bensound-music/bensound-littleidea.mp3`.
- Cached in `scripts/.cache/bensound-littleidea.mp3`; reuses existing download when available.
- Looping and volume reduction handled by `ffmpeg` before final encoding.

## Demonstration
1. `scripts/gemini_podcast_gen.py --demo --api-key $KEY --output-dir out --output-prefix demo --output-format both`
   - Exercises Aoede and Charon conversations, including `[sigh]`/`[laugh]` fillers, downloads background if needed, and exports MP3 + Opus.
2. `scripts/gemini_podcast_gen.py --script-file story.txt --speaker-voice Nimbus=Isa --speaker-voice Charon=Charon --output-format mp3 --output-dir episodes`
   - Shows custom speaker mapping with a third participant, verifying multi-speaker mixing and final MP3 creation.

## Expectations
- `ffmpeg` must be installed on the host; the script errors early if missing.
- The JSON payload targets `gemini-2.5-flash-native-audio` explicitly and requests WAV audio per segment.
- The script prints progress per segment and lists the exported file paths on completion.
