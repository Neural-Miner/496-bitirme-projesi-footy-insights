import whisper
import warnings

# Terminaldeki uyarilari gizlemek icin
warnings.filterwarnings("ignore")

model = whisper.load_model("medium")  # base / medium / large

result = model.transcribe("audio.wav", language="tr")
outputFile = "videoTranscript_medium.txt"

with open(outputFile, "w", encoding="utf-8") as f:
    f.write(result["text"])
