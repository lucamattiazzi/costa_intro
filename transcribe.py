import json
import os

import whisper

EPISODES_FOLDER = "./episodes"
RESULTS_FOLDER = "./results"
data = json.loads(open(f"{EPISODES_FOLDER}/episodes.json", "r").read())
results = json.loads(open(f"{RESULTS_FOLDER}/results.json", "r").read())

model = whisper.load_model("tiny")
episodes = [ep for ep in os.listdir(EPISODES_FOLDER) if ep[-3:] == "mp3"]

def find_song_segment(segments):
  valid_segments_idx = [idx for idx, segment in enumerate(segments) if "cominciamo" in segment["text"]]
  if len(valid_segments_idx) == 0:
    valid_segments_idx = [idx for idx, segment in enumerate(segments) if "morning" in segment["text"]]
  for idx in valid_segments_idx:
    distance = segments[idx + 1]["start"] - segments[idx]["end"]
    if distance > 5:
      return segments[idx]

def find_episode_in_list(list, episode):
  for idx, ep in enumerate(list):
      if f"{ep['raw_date']}.mp3" == episode:
        return idx
  return -1

def episode_has_been_checked_already(episode):
  idx = find_episode_in_list(results, episode)
  return idx != -1

for episode in episodes:
  try:
    should_skip = episode_has_been_checked_already(episode)
    if (should_skip):
      continue
    file = f"{EPISODES_FOLDER}/{episode}"
    result = model.transcribe(file, language="it")
    open(f"{RESULTS_FOLDER}/{episode}.json", "w").write(json.dumps(result, indent=2))
    song_segment = find_song_segment(result["segments"])
    last_segment = result["segments"][-1]
    data_idx = find_episode_in_list(data, episode)
    updated_data = {
      **data[data_idx],
      "intro_end": song_segment["end"],
      "length": last_segment["end"]
    }
    results.append(updated_data)
    open(f"{RESULTS_FOLDER}/results.json", "w").write(json.dumps(results, indent=2))
  except Exception as e:
    data_idx = find_episode_in_list(data, episode)
    updated_data = {
      **data[data_idx],
      "intro_end": -1,
      "length": -1
    }
    results.append(updated_data)
    open(f"{RESULTS_FOLDER}/results.json", "w").write(json.dumps(results, indent=2))
    print(e)