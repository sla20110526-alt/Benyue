from __future__ import annotations

import csv
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "outputs" / "_script_revision_v131"))

import v131_content as v131  # noqa: E402


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def build_payload() -> dict[str, object]:
    payload: dict[str, object] = {
        "scene_count": len(v131.SCENES),
        "shot_count": sum(len(scene["shots"]) for scene in v131.SCENES),
        "duration_seconds": sum(scene["duration"] for scene in v131.SCENES),
        "scenes": [],
    }

    shot_number = 1
    speakers: list[str] = []
    for scene_index, scene in enumerate(v131.SCENES, start=1):
        scene_row = {
            "scene_no": scene_index,
            "title": scene["title"],
            "duration": scene["duration"],
            "location": scene["location"],
            "beat": scene["beat"],
            "shots": [],
        }
        for shot in scene["shots"]:
            duration, camera, image, sound, note = shot
            speakers.extend(re.findall(r"([\u4e00-\u9fffA-Za-z0-9·]+)：", sound))
            scene_row["shots"].append(
                {
                    "shot_no": shot_number,
                    "duration": duration,
                    "camera": camera,
                    "image": image,
                    "sound": sound,
                    "note": note,
                }
            )
            shot_number += 1
        payload["scenes"].append(scene_row)

    payload["speakers"] = list(dict.fromkeys(speakers))

    assets = load_csv(ROOT / "data" / "阶段1_资产统计表_V1.2.csv")
    active_by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
    historical_by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assets:
        target = (
            historical_by_type
            if ("停止" in row["确认状态"] or "历史" in row["确认状态"])
            else active_by_type
        )
        target[row["资产类型"]].append(
            {
                "id": row["生产资产ID"],
                "name": row["资产名称"],
                "priority": row["资产级别"],
                "status": row["确认状态"],
            }
        )

    payload["active_assets"] = dict(active_by_type)
    payload["historical_assets"] = dict(historical_by_type)

    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", nargs=2, type=int, metavar=("START", "END"))
    parser.add_argument("--assets", action="store_true")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    payload = build_payload()

    if args.shots:
        start, end = args.shots
        selected = []
        for scene in payload["scenes"]:
            shots = [
                shot
                for shot in scene["shots"]
                if start <= shot["shot_no"] <= end
            ]
            if shots:
                selected.append(
                    {
                        "scene_no": scene["scene_no"],
                        "title": scene["title"],
                        "location": scene["location"],
                        "shots": shots,
                    }
                )
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        return

    if args.assets:
        print(
            json.dumps(
                {
                    "active_assets": payload["active_assets"],
                    "historical_assets": payload["historical_assets"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.summary:
        print(
            json.dumps(
                {
                    "scene_count": payload["scene_count"],
                    "shot_count": payload["shot_count"],
                    "duration_seconds": payload["duration_seconds"],
                    "speakers": payload["speakers"],
                    "scenes": [
                        {
                            "scene_no": scene["scene_no"],
                            "title": scene["title"],
                            "duration": scene["duration"],
                            "shot_range": [
                                scene["shots"][0]["shot_no"],
                                scene["shots"][-1]["shot_no"],
                            ],
                            "location": scene["location"],
                        }
                        for scene in payload["scenes"]
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
