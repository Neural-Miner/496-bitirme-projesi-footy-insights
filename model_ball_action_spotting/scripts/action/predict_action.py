# from google.colab import drive
# drive.mount('/content/drive')

# %pip install -r /content/drive/MyDrive/colab_notebooks/son_ball-action-spotting/requirements.txt -f https://download.pytorch.org/whl/cu118/torch_stable.html

# Commented out IPython magic to ensure Python compatibility.
# 1) requirements.txt'teki tüm paketleri zorla yeniden yükle
# %pip install --upgrade --force-reinstall \
#    -r /content/drive/MyDrive/colab_notebooks/son_ball-action-spotting/requirements.txt \
#    -f https://download.pytorch.org/whl/cu118/torch_stable.html

# 2) Bellekteki eski C-uzantılarını temizlemek için runtime’ı yeniden başlat
import os
os.kill(os.getpid(), 9)

import sys
project_path = "/content/drive/MyDrive/colab_notebooks/son_ball-action-spotting"
sys.path.append(project_path)

# ! pip install -r /content/drive/MyDrive/colab_notebooks/son_ball-action-spotting/requirements.txt

# ! pip install --no-cache-dir -r /content/drive/MyDrive/colab_notebooks/son_ball-action-spotting/requirements.txt --extra-index-url https://download.pytorch.org/whl/cu118

import os, torch;
# torch.backends.cuda.enable_cudnn();
# torch.backends.cuda.cudnn_graphs = False

# import torch
print(torch.cuda.is_available())

# ! pip install pytorch-argus
# ! pip install kornia

# ! pip install SoccerNet
# import gc

# !pip install timm
# !pip install opencv-python

import os
import gc

import argparse
from pathlib import Path

from tqdm import tqdm
import numpy as np

from src.action.annotations import raw_predictions_to_actions, prepare_game_spotting_results
from src.utils import get_best_model_path, get_video_info
from src.predictors import MultiDimStackerPredictor
#from src.frame_fetchers import NvDecFrameFetcher
from src.frame_fetchers.opencv import OpencvFrameFetcher as NvDecFrameFetcher
from src.action import constants

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "video_codec;h264"

RESOLUTION = "720p"
INDEX_SAVE_ZONE = 1
TTA = False

# print(predictor.__dict__)  # mevcut ozellikler

import os
import gc
import json
from pathlib import Path
from typing import List, Tuple

import numpy as np
import torch
from tqdm import tqdm

from src.predictors import MultiDimStackerPredictor
from src.frame_fetchers.opencv import OpencvFrameFetcher as NvDecFrameFetcher
from src.action.annotations import (
    raw_predictions_to_actions,
    prepare_game_spotting_results,
)
from src.utils import get_video_info
from src.action import constants

CONFIG = {
    # Drive kök dizin (tek noktadan değiştirilebilir)
    "ROOT": Path("/content/drive/MyDrive"),
    # Model
    "MODEL_PATH": "colab_notebooks/son_ball-action-spotting/data/action/experiments/action_sampling_weights_002/model-019-0.797827.pth",
    # İşlenecek video
    "VIDEO_PATH": "/content/drive/MyDrive/cropped_2023-2024_11_fraport-tav-antalyaspor_besiktas.mp4",
    # Tahminlerin (.npz + json) kaydedileceği klasör
    "OUTPUT_DIR": "colab_notebooks/goal_detection/2023-2024_11_fraport-tav-antalyaspor_besiktas",
    # Soccernet game adı (json formatlama için)
    "GAME_NAME": "2023-2024_11_fraport-tav-antalyaspor_besiktas",
}

RESOLUTION = "720p"
INDEX_SAVE_ZONE = 1
TTA = False
BATCH_SIZE = 16  # duruma gore degistilebilir
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "video_codec;h264"

ROOT = CONFIG["ROOT"]
MODEL_PATH = ROOT / CONFIG["MODEL_PATH"]
VIDEO_PATH = ROOT / CONFIG["VIDEO_PATH"]
OUTPUT_DIR = ROOT / CONFIG["OUTPUT_DIR"]
RAW_PRED_NPZ = OUTPUT_DIR / "preds.npz"
JSON_PATH = OUTPUT_DIR / "preds.json"
GAME_NAME = CONFIG["GAME_NAME"]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_raw_predictions(
    predictor: MultiDimStackerPredictor, video_path: Path, frame_count: int
) -> Tuple[List[int], np.ndarray]:

    print(f"Processing video: {video_path}, Total frames: {frame_count}")

    frame_fetcher = NvDecFrameFetcher(video_path, gpu_id=predictor.device.index)
    frame_fetcher.num_frames = frame_count

    idx_gen = predictor.indexes_generator
    min_idx = idx_gen.clip_index(0, frame_count, INDEX_SAVE_ZONE)
    max_idx = idx_gen.clip_index(frame_count, frame_count, INDEX_SAVE_ZONE)

    frame_idx2pred = {}
    predictor.reset_buffers()

    with tqdm(total=frame_count, desc="Processing Frames") as pbar:
        while True:
            frames, frame_indexes = [], []

            # read batches
            for _ in range(BATCH_SIZE):
                frame = frame_fetcher.fetch_frame()
                frame_idx = frame_fetcher.current_index
                if frame is None or frame_idx >= max_idx:
                    break
                frames.append(frame)
                frame_indexes.append(frame_idx)

            if not frames:
                break

            # prediction
            with torch.no_grad():
                batch_predictions = [
                    predictor.predict(f, idx) for f, idx in zip(frames, frame_indexes)
                ]

            # save results
            for pred, pred_idx in batch_predictions:
                if pred is not None and pred_idx >= min_idx:

                    if isinstance(pred, torch.Tensor):
                        pred = pred.cpu().numpy()
                    frame_idx2pred[pred_idx] = pred


            del batch_predictions, frames
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            gc.collect()
            pbar.update(len(frame_indexes))

            if frame_indexes and frame_indexes[-1] >= max_idx:
                break

    predictor.reset_buffers()

    if not frame_idx2pred:
        raise RuntimeError("Prediction error, batch size kucultmeyi dene")

    sorted_idx = sorted(frame_idx2pred)
    raw_preds = np.stack([frame_idx2pred[i] for i in sorted_idx])
    print(f"Processed {len(sorted_idx)} frames successfully.")
    return sorted_idx, raw_preds


def predict_video_to_json(predictor: MultiDimStackerPredictor):
    # npz + json ciktisi uretilir

    vid_info = get_video_info(VIDEO_PATH)
    assert abs(vid_info["fps"] - constants.video_fps) < 0.1, "FPS eşleşmiyor"

    # daha onceden npz uretildiyse
    # if RAW_PRED_NPZ.exists():
    #     npz = np.load(RAW_PRED_NPZ)
    #     frame_indexes, raw_predictions = npz["frame_indexes"], npz["raw_predictions"]
    #     print("NPZ yüklendi — modele gerek kalmadi")
    # else:
    #     frame_indexes, raw_predictions = get_raw_predictions(
    #         predictor, VIDEO_PATH, vid_info["frame_count"]
    #     )
    #     np.savez(RAW_PRED_NPZ, frame_indexes=frame_indexes, raw_predictions=raw_predictions)
    #     print(f"Ham tahminler kaydedildi ➜ {RAW_PRED_NPZ}")

    frame_indexes, raw_predictions = get_raw_predictions(
      predictor, VIDEO_PATH, vid_info["frame_count"]
    )
    np.savez(RAW_PRED_NPZ, frame_indexes=frame_indexes, raw_predictions=raw_predictions)
    print(f"Ham tahminler kaydedildi ➜ {RAW_PRED_NPZ}")

    # action verisini olustur
    class2actions = raw_predictions_to_actions(frame_indexes, raw_predictions)

    actions_json = {
        str(cls): [list(a) for a in acts]     # (frame, prob) → [frame, prob]
        for cls, acts in class2actions.items()
    }


    with open(JSON_PATH, "w", encoding="utf-8") as jf:
        json.dump(actions_json, jf, ensure_ascii=False, indent=2)
    print(f"JSON kaydedildi ➜ {JSON_PATH}")

    prepare_game_spotting_results({1: class2actions}, GAME_NAME, OUTPUT_DIR)


if __name__ == "__main__":
    device_id = 0
    predictor = MultiDimStackerPredictor(str(MODEL_PATH), device=f"cuda:{device_id}", tta=TTA)
    predict_video_to_json(predictor)

import os
import gc
import json
from pathlib import Path
from typing import List, Tuple

import numpy as np
import torch
from tqdm import tqdm

from src.predictors import MultiDimStackerPredictor
from src.frame_fetchers.opencv import OpencvFrameFetcher as NvDecFrameFetcher
from src.action.annotations import raw_predictions_to_actions
from src.utils import get_video_info
from src.action import constants

# CONFIGURATION
CONFIG = {
    "ROOT": Path("/content/drive/MyDrive"),
    "MODEL_PATH": "colab_notebooks/son_ball-action-spotting/data/action/experiments/action_sampling_weights_002/model-019-0.797827.pth",
    "VIDEO_PATH": "/content/drive/MyDrive/cropped_2023-2024_11_fraport-tav-antalyaspor_besiktas.mp4",
    "OUTPUT_DIR": "colab_notebooks/goal_detection/2023-2024_11_fraport-tav-antalyaspor_besiktas",
    "GAME_NAME": "2023-2024_11_fraport-tav-antalyaspor_besiktas",
}

# derived paths
ROOT = CONFIG["ROOT"]
MODEL_PATH = ROOT / CONFIG["MODEL_PATH"]
VIDEO_PATH = Path(CONFIG["VIDEO_PATH"])
OUTPUT_DIR = ROOT / CONFIG["OUTPUT_DIR"]
GAME_NAME = CONFIG["GAME_NAME"]

# inference settings
BATCH_SIZE = 16
INDEX_SAVE_ZONE = 1
TTA = False

# make output dir
(OUTPUT_DIR / GAME_NAME).mkdir(parents=True, exist_ok=True)

def get_raw_predictions(
    predictor: MultiDimStackerPredictor,
    video_path: Path,
    frame_count: int
) -> Tuple[List[int], np.ndarray]:
    print(f"Processing video: {video_path}, frames: {frame_count}")
    fetcher = NvDecFrameFetcher(video_path, gpu_id=predictor.device.index)
    fetcher.num_frames = frame_count
    idx_gen = predictor.indexes_generator
    min_idx = idx_gen.clip_index(0, frame_count, INDEX_SAVE_ZONE)
    max_idx = idx_gen.clip_index(frame_count, frame_count, INDEX_SAVE_ZONE)

    frame_to_pred = {}
    predictor.reset_buffers()
    with tqdm(total=frame_count, desc="Frames") as pbar:
        while True:
            batch_frames, batch_idxs = [], []
            for _ in range(BATCH_SIZE):
                frame = fetcher.fetch_frame()
                idx = fetcher.current_index
                if frame is None or idx >= max_idx:
                    break
                batch_frames.append(frame)
                batch_idxs.append(idx)
            if not batch_frames:
                break
            with torch.no_grad():
                preds = [predictor.predict(f, i) for f, i in zip(batch_frames, batch_idxs)]
            for pred, idx in preds:
                if idx >= min_idx and pred is not None:
                    frame_to_pred[idx] = pred.cpu().numpy()
            torch.cuda.empty_cache()
            gc.collect()
            pbar.update(len(batch_frames))
            if batch_idxs and batch_idxs[-1] >= max_idx:
                break
    predictor.reset_buffers()
    sorted_idxs = sorted(frame_to_pred)
    raw_preds = np.stack([frame_to_pred[i] for i in sorted_idxs], axis=0)
    print(f"Raw predictions done: {len(sorted_idxs)} frames.")
    return sorted_idxs, raw_preds

def run_inference(use_saved: bool, gpu_id: int):
    # get video info
    vid_info = get_video_info(VIDEO_PATH)
    assert abs(vid_info["fps"] - constants.video_fps) < 0.1, "FPS mismatch"

    # raw npz path
    raw_npz = OUTPUT_DIR / GAME_NAME / "1_raw_predictions.npz"
    if use_saved and raw_npz.exists():
        with np.load(raw_npz) as arr:
            frame_idxs = arr["frame_indexes"]
            raw_preds = arr["raw_predictions"]
        print(f"Loaded saved predictions: {raw_npz}")
    else:
        predictor = MultiDimStackerPredictor(str(MODEL_PATH), device=f"cuda:{gpu_id}", tta=TTA)
        frame_idxs, raw_preds = get_raw_predictions(predictor, VIDEO_PATH, vid_info["frame_count"])
        # save npz
        raw_npz.parent.mkdir(parents=True, exist_ok=True)
        with open(raw_npz, "wb") as f:
            np.savez(f, frame_indexes=frame_idxs, raw_predictions=raw_preds)
            f.flush()
            os.fsync(f.fileno())
        print(f"NPZ saved: {raw_npz}")

    # post-process to actions
    class2actions = raw_predictions_to_actions(frame_idxs, raw_preds)

    # build a flat list of events and filter by label-specific thresholds
    filtered = []
    kick_off_found = False
    for label, (frames, confs) in class2actions.items():
        for frame, conf in zip(frames, confs):
            event = {"label": label, "frame": int(frame), "confidence": float(conf)}
            if label == "yellow card":
                if conf >= 0.50:
                    filtered.append(event)
            elif label in ["throw in", "throw-in"]:
                if conf >= 0.80:
                    filtered.append(event)
            elif label == "substitution":
                if conf >= 0.95:
                    filtered.append(event)
            elif label == "shots on target":
                if conf >= 0.38:
                    filtered.append(event)
            elif label == "shots off target":
                if conf >= 0.40:
                    filtered.append(event)
            elif label == "offside":
                if conf >= 0.88:
                    filtered.append(event)
            elif label == "kick off":
                if not kick_off_found:
                    filtered.append(event)
                    kick_off_found = True
            elif label == "direct free kick":
                if conf >= 0.60:
                    filtered.append(event)
            elif label == "foul":
                if conf >= 0.75:
                    filtered.append(event)
            elif label == "corner":
                if conf >= 0.90:
                    filtered.append(event)
            elif label == "ball out of play":
                if conf >= 0.55:
                    filtered.append(event)
            elif label == "indirect free kick":
                filtered.append(event)
            else:
                # includes goals and any other labels
                filtered.append(event)

    filtered.sort(key=lambda e: e["frame"])

    # split into only_goal and without_goal
    only_goal = [e for e in filtered if e["label"].lower() == "goal"]
    without_goal = [e for e in filtered if e["label"].lower() != "goal"]

    # helper to attach gameTime and write to json
    def write_events(events, filename):
        out = []
        for e in events:
            sec = int(e["frame"] / constants.video_fps)
            mm, ss = divmod(sec, 60)
            e_out = {
                "gameTime": f"{mm:02d}:{ss:02d}",
                "label": e["label"],
                "confidence": f"{e['confidence']:.6f}"
            }
            out.append(e_out)
        path = OUTPUT_DIR / filename
        with open(path, "w", encoding="utf-8") as jf:
            json.dump(out, jf, ensure_ascii=False, indent=2)
        print(f"Saved {len(out)} events to {path}")

    # save two jsons
    write_events(only_goal, "events_only_goals.json")
    write_events(without_goal, "events_without_goals.json")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_saved_predictions", action="store_true")
    parser.add_argument("--gpu_id", type=int, default=0)
    args, _ = parser.parse_known_args()
    run_inference(args.use_saved_predictions, args.gpu_id)