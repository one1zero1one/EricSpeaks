# Project: AI-Enhanced Storytelling with OpenAI

## Overview
This project brings to life the imaginative stories of a 3-year-old by using the OpenAI API to create videos with AI-generated images and subtitles. Recordings of a child's voice are transcribed, subtitled, and then transformed into captivating videos with visually appealing background images.

Initial results  [here](https://www.youtube.com/watch?v=oH6EAnmP20A&list=PLK-fukR2qF4yxx7bKOAnfiWA_KT7RAYn_&ab_channel=DanielRadu)

## Setup
```bash
export OPENAI_API_KEY=...
mkdir sources
# Place the mp3 files in the sources folder
```

## Workflow

### Audio Segmentation
Split long audio files into smaller segments (up to 20MB each) for efficient processing.
```bash
segment.py sources/eric1.mp3
# Results: sources/eric1_0.mp3, sources/eric1_1.mp3, ...
```

### Transcription

Convert audio segments to text and subtitles.
```bash
transcribe.py sources/eric1
concatenate.py sources/eric1_
transcribe_srt.py sources/eric1
concatenate_srt.py sources/eric1_
# Results: eric1.txt, eric1.srt
```

### Text Improvement with GPT-4 (optional)
Refine the transcribed text using GPT-4 for more coherent storytelling.
```bash
prompt.py sources/eric1
# Results: eric1_0_corrected.txt, eric1_1_corrected.txt, ...
```

### Simple Video Creation
Generate a basic video with audio and subtitles.
```bash
video.py sources/eric1
```

### Enhanced Video with DALL-E Images

Create a video with DALL-E generated images for every minute of audio.

```bash
# creates a new srt with 1 minute accumulation of text.
python3 video_dallee_accumulated.py 

# creates a new srt with prompts instead of accumulationm of text
python3 video_dallee_gpt4.py

# creates the images from the prompts into a folder
python3 video_dallee_dalle.py

# creates the video using the mp3, the subtitles, and the images (from the folder, using the timestamps in the srt)
python3 video_dalle.py
```

## TODO (in progress)
- [x] **Audio Segmentation**: Split long audio files into smaller segments (up to 20MB each) for efficient processing.
- [x] **Transcription**: Convert audio segments to text and subtitles.
- [x] **Text Improvement with GPT-4**: Refine the transcribed text using GPT-4 for more coherent storytelling.
- [ ] **DALL-E Image Generation**: Use DALL-E to generate images for every minute of audio.
  - [x] first run, multiple scripts 
  - [ ] concatenate all scripts into one
- [ ] **Dynamic lenght**: Algorithm for a dynamic lenght of video segments, based on the content of the audio
  - [ ] when there is a lot of conent, the video segments are shorter.
  - [ ] try to figure out if there's a story, if there are characters, if there's a plot, etc.
  - [ ] use the above to determine the lenght of the video segments
  - [ ] use the above to determine the content of the video segments
- [ ] **Automate the Workflow**: Develop a script to automate the entire process from audio segmentation to video creation.
  - [ ] Use SQLlite to store data and deal with SRT timestamps

## TODO (future)
- [ ] **Interactive Web Interface**: Create a web application allowing users to upload audio and customize the video generation process.
- **Interactive Web Interface**: Create a web application allowing users to upload audio and customize the video generation process.
- **Narrative Enhancement**: Implement more advanced NLP techniques to enrich the storytelling aspect.
- **Custom Image Styles**: Integrate options for different illustration styles in DALL-E image generation.

## References
- [OpenAI Speech-to-Text Quickstart](https://platform.openai.com/docs/guides/speech-to-text/quickstart)
