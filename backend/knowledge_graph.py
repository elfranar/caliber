"""
Topological Knowledge Graph Engine
PT Chandra Asri Pacific Tbk - CALIBER 2026

Models physical plant topology (:FEEDS, :PART_OF), operational telemetry (:HAS_PARAMETER),
governance provenance (:DESCRIBED_BY), and failure memory (:HAS_INCIDENT).
Provides multi-hop impact traversal with exponential distance decay.
"""

import json
from typing import Dict, Any, List, Optional
from backend.config import GRAPH_PATH, DEFAULT_DECAY_RATE
from backend.dataset_catalog import load_dataset_manifests

EDGE_WEIGHTS = {
    "FEEDS": 1.0,
    "PART_OF": 0.85,
    "HAS_PARAMETER": 0.90,
    "DESCRIBED_BY": 0.75,
    "HAS_INCIDENT": 0.80,
    "AUTHORED_BY": 0.60
}


class KnowledgeGraphEngine:
    def __init__(self, graph_path=GRAPH_PATH):
        self.graph_path = graph_path
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.adj_list: Dict[str, List[Dict[str, Any]]] = {}  # source -> [{target, type, category}]
        self.rev_adj_list: Dict[str, List[Dict[str, Any]]] = {}  # target -> [{source, type, category}]
        self.edges: List[Dict[str, Any]] = []
        self._load_graph()

    def _load_graph(self):
        if not self.graph_path.exists():
            return
        with open(self.graph_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for n in data.get("nodes", []):
            self.nodes[n["id"]] = n
            self.adj_list[n["id"]] = []
            self.rev_adj_list[n["id"]] = []

        self.edges = data.get("edges", [])
        for e in self.edges:
            src = e["source"]
            tgt = e["target"]
            if src in self.adj_list:
                self.adj_list[src].append(e)
            if tgt in self.rev_adj_list:
                self.rev_adj_list[tgt].append(e)

        self._add_dataset_catalog(load_dataset_manifests())

    def _add_dataset_catalog(self, manifests: List[Dict[str, Any]]):
        for manifest in manifests:
            tag = manifest.get("equipment_tag")
            if not tag:
                continue

            if tag not in self.nodes:
                self.nodes[tag] = {
                    "id": tag,
                    "label": tag,
                    "name": manifest.get("equipment_name") or tag,
                    "type": "asset",
                    "asset_type": "equipment",
                    "criticality": "Unspecified",
                    "aliases": manifest.get("aliases", []),
                    "dataset_id": manifest.get("dataset_id"),
                    "color": "#3B82F6",
                }
                self.adj_list[tag] = []
                self.rev_adj_list[tag] = []

            for source in manifest["sources"]:
                source_id = source["source_id"]
                if source_id not in self.nodes:
                    self.nodes[source_id] = {
                        "id": source_id,
                        "label": source_id,
                        "name": source["file_name"],
                        "type": "document",
                        "doc_type": source.get("category", "other"),
                        "approval_status": source["approval_status"],
                        "dataset_id": manifest.get("dataset_id"),
                        "source_file": source.get("source_file"),
                        "version": source.get("version", "Not specified"),
                        "color": "#64748B",
                    }
                    self.adj_list[source_id] = []
                    self.rev_adj_list[source_id] = []

                if not any(
                    edge.get("source") == tag
                    and edge.get("target") == source_id
                    and edge.get("type") == "DESCRIBED_BY"
                    for edge in self.adj_list.get(tag, [])
                ):
                    edge = {
                        "source": tag,
                        "target": source_id,
                        "type": "DESCRIBED_BY",
                        "category": "dataset_catalog",
                    }
                    self.edges.append(edge)
                    self.adj_list[tag].append(edge)
                    self.rev_adj_list[source_id].append(edge)

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self.nodes.get(node_id)

    def get_full_graph(self) -> Dict[str, Any]:
        """Returns nodes and edges formatted for frontend graph visualizers."""
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges
        }

    def get_asset_subgraph(self, asset_tag: str) -> Dict[str, Any]:
        """Return an asset-centered graph with direct references and downstream FEEDS paths."""
        if asset_tag not in self.nodes:
            return {"root_asset": asset_tag, "nodes": [], "edges": []}

        included_ids = {asset_tag}
        included_edges = []
        upstream_frontier = [(asset_tag, 0)]
        downstream_frontier = [(asset_tag, 0)]
        visited_upstream = {asset_tag}
        visited_downstream = {asset_tag}

        while upstream_frontier:
            current, hop = upstream_frontier.pop(0)
            if hop >= 3:
                continue
            for edge in self.rev_adj_list.get(current, []):
                if edge.get("type") != "FEEDS":
                    continue
                included_edges.append(edge)
                source = edge["source"]
                included_ids.add(source)
                if source not in visited_upstream:
                    visited_upstream.add(source)
                    upstream_frontier.append((source, hop + 1))

        while downstream_frontier:
            current, hop = downstream_frontier.pop(0)
            if hop >= 3:
                continue
            for edge in self.adj_list.get(current, []):
                if edge.get("type") != "FEEDS":
                    continue
                included_edges.append(edge)
                target = edge["target"]
                included_ids.add(target)
                if target not in visited_downstream:
                    visited_downstream.add(target)
                    downstream_frontier.append((target, hop + 1))

        for edge in self.adj_list.get(asset_tag, []):
            if edge.get("type") != "FEEDS":
                included_edges.append(edge)
                included_ids.add(edge["target"])
        for edge in self.rev_adj_list.get(asset_tag, []):
            if edge.get("type") != "FEEDS":
                included_edges.append(edge)
                included_ids.add(edge["source"])

        unique_edges = {(e["source"], e["target"], e["type"]): e for e in included_edges}
        return {
            "root_asset": asset_tag,
            "nodes": [self.nodes[node_id] for node_id in included_ids if node_id in self.nodes],
            "edges": list(unique_edges.values()),
        }

    def downstream_impact_traversal(self, start_tag: str, max_hops: int = 3) -> List[Dict[str, Any]]:
        """
        Traverses :FEEDS edges to determine the cascading domino effect of an asset failure.
        Applies exponential hop-decay: Score = EdgeWeight * (0.7 ^ (hop - 1))
        """
        if start_tag not in self.nodes:
            return []

        results = []
        visited = {start_tag: 0}
        queue = [(start_tag, 1)]  # (current_node, current_hop)

        while queue:
            curr, hop = queue.pop(0)
            if hop > max_hops:
                continue

            for edge in self.adj_list.get(curr, []):
                if edge.get("type") == "FEEDS":
                    tgt = edge["target"]
                    if tgt not in visited or visited[tgt] > hop:
                        visited[tgt] = hop
                        decayed_score = EDGE_WEIGHTS.get("FEEDS", 1.0) * (DEFAULT_DECAY_RATE ** (hop - 1))
                        tgt_node = self.nodes.get(tgt, {})
                        results.append({
                            "impacted_asset": tgt,
                            "name": tgt_node.get("name", tgt),
                            "asset_type": tgt_node.get("asset_type", "equipment"),
                            "criticality": tgt_node.get("criticality", "Standard"),
                            "hop_distance": hop,
                            "normalized_relevance": round(decayed_score, 3),
                            "causal_path": f"{start_tag} -> [FEEDS] -> {tgt} (hop {hop})"
                        })
                        queue.append((tgt, hop + 1))

        # Sort by relevance descending
        results.sort(key=lambda x: -x["normalized_relevance"])
        return results

    def get_comprehensive_asset_context(self, asset_tag: str) -> Dict[str, Any]:
        """
        Executes a 360-degree graph expansion around the given asset.
        Gathers live parameters, linked documentation, incidents, and downstream impacts.
        """
        if asset_tag not in self.nodes:
            # Fallback check if it is a parameter
            for node_id, node in self.nodes.items():
                if node.get("type") == "parameter" and node_id == asset_tag:
                    # Find parent asset
                    for parent_edge in self.rev_adj_list.get(node_id, []):
                        if parent_edge.get("type") == "HAS_PARAMETER":
                            asset_tag = parent_edge["source"]
                            break

        node_info = self.nodes.get(asset_tag, {"id": asset_tag, "name": asset_tag})
        parameters = []
        documents = []
        incidents = []
        part_of = []

        # Outgoing edges
        for edge in self.adj_list.get(asset_tag, []):
            edge_type = edge.get("type")
            tgt_id = edge.get("target")
            tgt_node = self.nodes.get(tgt_id, {})

            if edge_type == "HAS_PARAMETER":
                parameters.append({
                    "tag": tgt_id,
                    "name": tgt_node.get("name", tgt_id),
                    "unit": tgt_node.get("unit"),
                    "trip": tgt_node.get("trip")
                })
            elif edge_type == "DESCRIBED_BY":
                documents.append({
                    "doc_id": tgt_id,
                    "title": tgt_node.get("name", tgt_id),
                    "version": tgt_node.get("version"),
                    "approval_status": tgt_node.get("approval_status")
                })
            elif edge_type == "HAS_INCIDENT":
                incidents.append({
                    "incident_id": tgt_id,
                    "title": tgt_node.get("name", tgt_id),
                    "root_cause": tgt_node.get("root_cause")
                })

        # Structural hierarchy (components part of this asset)
        for edge in self.rev_adj_list.get(asset_tag, []):
            if edge.get("type") == "PART_OF":
                src_id = edge.get("source")
                part_of.append(self.nodes.get(src_id, {"id": src_id}))

        downstream = self.downstream_impact_traversal(asset_tag)

        return {
            "asset": node_info,
            "live_parameters": parameters,
            "reference_documents": documents,
            "historical_incidents": incidents,
            "sub_components": part_of,
            "downstream_impacts": downstream
        }
