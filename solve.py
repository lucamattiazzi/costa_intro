import json

import nltk

nltk.download('punkt')
RESULTS_FOLDER = "./results"
MORNING_DISTANCE_THRESHOLD = 3
COMINCIAMO_DISTANCE_THRESHOLD = 3

results = json.loads(open(f"{RESULTS_FOLDER}/results.json", "r").read())
unsolved = [r for r in results if r["intro_end"] == -1]

def find_song_segment(episode, segments):
  for segment in segments:
    words = [w.lower() for w in nltk.word_tokenize(segment["text"])]
    cominciamo_like = [idx for idx, word in enumerate(words) if nltk.edit_distance("cominciamo", word) <= COMINCIAMO_DISTANCE_THRESHOLD]
    if len(cominciamo_like) == 0:
      continue
    cominciamo_idx = cominciamo_like[0]
    useful_words = words[:cominciamo_idx][::-1]
    morning_like = [word for word in useful_words if nltk.edit_distance("morning", word) <= MORNING_DISTANCE_THRESHOLD]
    if len(morning_like) == 0:
      continue
    return segment


def find_episode_in_list(list, episode):
  for idx, ep in enumerate(list):
      if ep['raw_date'] == episode:
        return idx
  return -1

for episode in unsolved:
  try:
    transcription = json.loads(open(f"{RESULTS_FOLDER}/{episode['raw_date']}.mp3.json", "r").read())
    song_segment = find_song_segment(episode, transcription["segments"])
    if song_segment is None:
      print(episode)
      raise Exception
    last_segment = transcription["segments"][-1]
    results_idx = find_episode_in_list(results, episode["raw_date"])
    results[results_idx]["intro_end"] = song_segment["end"]
    results[results_idx]["length"] = last_segment["end"]
    open(f"{RESULTS_FOLDER}/results_fixed.json", "w").write(json.dumps(results, indent=2))
  except Exception as e:
    print(e)