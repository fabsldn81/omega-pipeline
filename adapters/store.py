"""The store — the episode database the Showrunner reads pipeline state from.

  * LocalStore — JSON file under state/ (default; the source of truth when offline).
  * NotionStore — scaffold for Fabio's Notion via the Notion MCP/API (opt-in).

On Fabio's machine Notion is authoritative; LocalStore is the convenience mirror and
the zero-dependency default for development and tests.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from core.errors import AdapterNotConfigured
from core.jsonio import load_json, save_json
from core.models import Episode, MediaAsset
from core.status import Status
from core.paths import Paths


class Store(ABC):
    @abstractmethod
    def exists(self, slug: str) -> bool: ...

    @abstractmethod
    def get(self, slug: str) -> Episode: ...

    @abstractmethod
    def save(self, episode: Episode) -> None: ...

    @abstractmethod
    def list(self) -> list[Episode]: ...

    def create(self, episode: Episode) -> Episode:
        if self.exists(episode.slug):
            raise ValueError(f"Episode '{episode.slug}' already exists.")
        self.save(episode)
        return episode


class LocalStore(Store):
    """Episodes persisted as JSON at state/episodes.json."""

    def __init__(self, paths: Paths | None = None, db_path: Path | None = None) -> None:
        self.paths = paths or Paths()
        self.db_path = Path(db_path) if db_path else self.paths.state / "episodes.json"

    def _load(self) -> dict[str, Any]:
        if not self.db_path.exists():
            return {"episodes": {}}
        return load_json(self.db_path)

    def _save_all(self, data: dict[str, Any]) -> None:
        save_json(self.db_path, data)

    def exists(self, slug: str) -> bool:
        return slug in self._load().get("episodes", {})

    def get(self, slug: str) -> Episode:
        data = self._load().get("episodes", {})
        if slug not in data:
            raise KeyError(f"No episode '{slug}' in the store.")
        return Episode.from_dict(data[slug])

    def save(self, episode: Episode) -> None:
        data = self._load()
        data.setdefault("episodes", {})[episode.slug] = episode.to_dict()
        self._save_all(data)

    def list(self) -> list[Episode]:
        data = self._load().get("episodes", {})
        return [Episode.from_dict(v) for v in data.values()]


class NotionStore(Store):
    """Episode store backed by Fabio's Notion workspace (build plan Section 5).

    Uses the Notion REST API directly (stdlib urllib — no extra deps).
    Set NOTION_TOKEN and optionally NOTION_EPISODES_DB to override the default DB ID.

    Visible episode fields (Title, Slug, Status, …) are stored as first-class Notion
    properties. Runtime-only fields (pending_gate, artifacts, history, assets) are
    serialised as a JSON blob in the "Pipeline state" rich_text property so the
    Showrunner can roundtrip the full Episode without a separate local file.
    """

    _EPISODES_DB = "d21dede219684be2832f161d14b483dd"
    _API = "https://api.notion.com/v1"
    _VERSION = "2022-06-28"

    def __init__(self, token: str | None = None) -> None:  # pragma: no cover
        import os

        self.token = token or os.environ.get("NOTION_TOKEN")
        db_override = os.environ.get("NOTION_EPISODES_DB")
        if db_override:
            self._EPISODES_DB = db_override
        if not self.token:
            raise AdapterNotConfigured(
                "NOTION_TOKEN is not set. Set HT_STORE=local to use the local JSON mirror."
            )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:  # pragma: no cover
        import json
        import urllib.error
        import urllib.request

        url = f"{self._API}{path}"
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Notion-Version": self._VERSION,
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            body_text = exc.read().decode(errors="replace")
            raise RuntimeError(f"Notion API {method} {path} → {exc.code}: {body_text}") from exc

    def _query(self, filter_body: dict | None = None) -> list[dict]:  # pragma: no cover
        pages, cursor = [], None
        while True:
            body: dict = {"page_size": 100}
            if filter_body:
                body["filter"] = filter_body
            if cursor:
                body["start_cursor"] = cursor
            resp = self._request("POST", f"/databases/{self._EPISODES_DB}/query", body)
            pages.extend(resp.get("results", []))
            if not resp.get("has_more"):
                break
            cursor = resp.get("next_cursor")
        return pages

    @staticmethod
    def _rich_text_value(prop: dict) -> str:
        parts = prop.get("rich_text", [])
        return "".join(p.get("plain_text", "") for p in parts)

    @staticmethod
    def _title_value(prop: dict) -> str:
        parts = prop.get("title", [])
        return "".join(p.get("plain_text", "") for p in parts)

    def _page_to_episode(self, page: dict) -> Episode:  # pragma: no cover
        import json

        props = page["properties"]

        def rt(key: str) -> str:
            return self._rich_text_value(props[key]) if key in props else ""

        def num(key: str) -> float | None:
            p = props.get(key, {})
            return p.get("number")

        slug = rt("Slug")
        title = self._title_value(props.get("Title", {}))
        topic = rt("Topic / Civilisation")
        angle = rt("Angle / Thesis")
        target = int(num("Target length") or 12)
        status_name = (props.get("Status") or {}).get("select", {}) or {}
        status = Status(status_name.get("name", Status.IDEA.value)) if status_name else Status.IDEA
        date_prop = props.get("Publish date", {}).get("date") or {}
        publish_date = date_prop.get("start")
        metrics = {
            k: num(n)
            for k, n in [("views", "Views"), ("watch_time", "Watch time"), ("ctr", "CTR"), ("avg_retention", "Avg. retention")]
            if num(n) is not None
        }

        pipeline_json = rt("Pipeline state")
        pipeline: dict = {}
        if pipeline_json:
            try:
                pipeline = json.loads(pipeline_json)
            except json.JSONDecodeError:
                pass

        return Episode(
            slug=slug,
            title=title,
            topic=topic,
            angle=angle,
            target_length_min=target,
            status=status,
            publish_date=publish_date,
            pending_gate=pipeline.get("pending_gate"),
            artifacts=pipeline.get("artifacts", {}),
            assets=[MediaAsset.from_dict(a) for a in pipeline.get("assets", [])],
            metrics=metrics,
            history=pipeline.get("history", []),
        )

    def _episode_to_properties(self, episode: Episode) -> dict:  # pragma: no cover
        import json

        pipeline = json.dumps({
            "pending_gate": episode.pending_gate,
            "artifacts": episode.artifacts,
            "assets": [a.__dict__ for a in episode.assets],
            "history": episode.history,
        })
        props: dict = {
            "Title": {"title": [{"text": {"content": episode.title or episode.slug}}]},
            "Slug": {"rich_text": [{"text": {"content": episode.slug}}]},
            "Status": {"select": {"name": episode.status.value}},
            "Topic / Civilisation": {"rich_text": [{"text": {"content": episode.topic}}]},
            "Angle / Thesis": {"rich_text": [{"text": {"content": episode.angle}}]},
            "Target length": {"number": episode.target_length_min},
            "Pipeline state": {"rich_text": [{"text": {"content": pipeline}}]},
        }
        if episode.publish_date:
            props["Publish date"] = {"date": {"start": episode.publish_date}}
        for notion_key, metric_key in [("Views", "views"), ("Watch time", "watch_time"), ("CTR", "ctr"), ("Avg. retention", "avg_retention")]:
            if metric_key in episode.metrics:
                props[notion_key] = {"number": episode.metrics[metric_key]}
        return props

    def _find_page_id(self, slug: str) -> str | None:  # pragma: no cover
        pages = self._query({"property": "Slug", "rich_text": {"equals": slug}})
        return pages[0]["id"] if pages else None

    # ------------------------------------------------------------------
    # Store interface
    # ------------------------------------------------------------------

    def exists(self, slug: str) -> bool:  # pragma: no cover
        return self._find_page_id(slug) is not None

    def get(self, slug: str) -> Episode:  # pragma: no cover
        pages = self._query({"property": "Slug", "rich_text": {"equals": slug}})
        if not pages:
            raise KeyError(f"No episode '{slug}' in Notion.")
        return self._page_to_episode(pages[0])

    def save(self, episode: Episode) -> None:  # pragma: no cover
        props = self._episode_to_properties(episode)
        page_id = self._find_page_id(episode.slug)
        if page_id:
            self._request("PATCH", f"/pages/{page_id}", {"properties": props})
        else:
            self._request("POST", "/pages", {
                "parent": {"database_id": self._EPISODES_DB},
                "properties": props,
            })

    def list(self) -> list[Episode]:  # pragma: no cover
        return [self._page_to_episode(p) for p in self._query()]
