# Costa Intro

Quick and dirty nighttime project to analyze the intro length of every episode of the great Morning podcast from Francesco Costa.
Steps: 
- Download every episode with beautifulsoup (btw, even without subscription as of today it's still possible to download the mp3 from the website) 
- Use whisper (MAGIC, PURE MAGIC) to quickly transcribe the episodes, even at the lower quality
- Use nltk to look for words similar to "morning cominciamo" in this order
- Use jupyter + pandas + matplotlib to plot
