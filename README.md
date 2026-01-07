# About

This repo contains utility scripts to process notes that I bring into Obsidian. Some of these utilities include using `Whisper` to transcribe audio recordings into text files, which I them summarize with an LLM.

## How To Transcribe Audio Recordings:

I put most of the Whisper CLI commands into [transcribe.sh](./transcribe.sh).

<!-- IDEA: I could turn this into a make command like `make transcribe`-->

```shell
./transcribe.sh <path_to_audio_file>
```

On my Linux Desktop:

```shell
'/mnt/ssd/vm_share/OneDrive/Obsidian-Utils/transcribe.sh' <path_to_audio_file>
```

I frequently use the drag-and-drop feature of the `Files` Ubuntu OS application to drop the file into the terminal so I don't have to type out long paths.
