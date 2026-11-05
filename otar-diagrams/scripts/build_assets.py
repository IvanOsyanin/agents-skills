"""Rebuild the educational OTAR assets from one text/geometry model (stdlib only)."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from html import escape
from pathlib import Path
import math
import os
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
COLORS = {
    "system": "#eaf2fc", "component": "#9fc5f3", "lane": "#ffffff",
    "function": "#efbb96", "action": "#bacbdd", "entity": "#a9c574",
    "payload": "#8faa50", "start": "#92ce50", "end": "#e5a5a5",
    "interface": "#fff2b2", "actor": "#ffffff", "label": "none",
}
LINE = "#41474b"


@dataclass
class Node:
    id: str
    kind: str
    text: str
    x: int
    y: int
    w: int
    h: int
    parent: str = "1"
    font: int = 20
    meta: dict[str, str] = field(default_factory=dict)


@dataclass
class Edge:
    id: str
    source: str
    target: str
    points: list[tuple[int, int]]
    dashed: bool = False
    mode: str = "sync"
    meta: dict[str, str] = field(default_factory=dict)


@dataclass
class Model:
    name: str
    width: int
    height: int
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    def node(self, id, kind, text, x, y, w, h, parent="1", font=20, **meta):
        self.nodes.append(Node(id, kind, text, x, y, w, h, parent, font, meta))

    def edge(self, id, source, target, points, dashed=False, mode="sync", **meta):
        self.edges.append(Edge(id, source, target, points, dashed, mode, meta))


def notation() -> Model:
    m = Model("Примитивы ОТАР — основной профиль", 1520, 1360)
    n = m.node
    n("title", "label", "ОТАР: фигуры и связи", 30, 18, 1460, 50, font=30)
    n("subtitle", "label", "По официальным материалам • учебные фигуры, не шаблон банка • 04.11.2026", 30, 76, 1460, 35, font=19)
    n("component", "component", "Документы. Хранилище", 30, 150, 650, 480, font=25)
    for i, text in enumerate(("Записать файл", "Прочитать файл", "Удалить файл")):
        n(f"function-{i}", "function", text, 60, 250 + i * 92, 265, 66, "component")
    n("copy", "entity", "D1\nКопия файла", 360, 245, 285, 125, "component", entity_id="D1", role="component-data")
    n("metadata", "entity", "D2\nМетаданные файла", 360, 410, 285, 125, "component", entity_id="D2", role="component-data")
    n("one-entity", "label", "Один блок — одна функция или сущность", 55, 565, 600, 40, font=20)
    n("lane-a", "lane", "Заявки. Портал", 750, 150, 330, 900, font=23)
    n("lane-b", "lane", "Заявки. Сервис", 1110, 150, 360, 900, font=23)
    n("start", "start", "", 890, 300, 50, 50, "lane-a")
    n("start-label", "label", "Подать заявку", 780, 255, 270, 30, "lane-a", font=18)
    n("send", "action", "Отправить заявку", 790, 375, 250, 95, "lane-a")
    n("payload", "payload", "D3\nЗаявка", 810, 595, 210, 100, "lane-a", entity_id="D3", role="exchange-data")
    n("receive", "action", "Принять заявку", 1160, 595, 260, 100, "lane-b")
    n("stored", "entity", "D3\nЗаявка", 1160, 765, 240, 100, "lane-b", entity_id="D3", role="component-data")
    n("end", "end", "", 1265, 940, 50, 50, "lane-b")
    n("end-label", "label", "Заявка принята", 1140, 1000, 300, 35, "lane-b", font=18)
    m.edge("begin", "start", "send", [(915, 350), (915, 375)])
    m.edge("call", "send", "receive", [(1040, 422), (1095, 422), (1095, 625), (1160, 625)])
    m.edge("output", "send", "payload", [(915, 470), (915, 595)], dashed=True)
    m.edge("input", "payload", "receive", [(1020, 665), (1160, 665)], dashed=True)
    m.edge("store", "receive", "stored", [(1280, 695), (1280, 765)], dashed=True)
    m.edge("finish", "receive", "end", [(1420, 645), (1445, 645), (1445, 965), (1315, 965)])
    n("client", "component", "Документы. Клиент", 30, 735, 260, 135, font=20)
    n("provider", "component", "Документы. Сервис", 430, 735, 250, 135, font=20)
    n("provider-function", "function", "Принять файл", 475, 795, 180, 45, "provider", font=17)
    m.edge("upload", "client", "provider-function", [(290, 815), (475, 815)], interface_number="1", provider="provider")
    n("upload-label", "label", "Копия файла\n[Принять файл]", 283, 740, 145, 65, font=17)
    n("provider-marker", "interface", "1", 418, 803, 24, 24, font=15, interface_number="1", provider="provider")
    n("provider-note", "label", "Кружок у поставщика, даже если он получает данные", 30, 895, 650, 60, font=20)
    n("sync-left", "label", "", 30, 1000, 1, 1)
    n("sync-right", "label", "", 200, 1000, 1, 1)
    n("async-left", "label", "", 30, 1060, 1, 1)
    n("async-right", "label", "", 200, 1060, 1, 1)
    m.edge("sync", "sync-left", "sync-right", [(30, 1000), (200, 1000)])
    m.edge("async", "async-left", "async-right", [(30, 1060), (200, 1060)], mode="async")
    n("sync-label", "label", "Синхронно: заполненный наконечник", 220, 980, 470, 40, font=20)
    n("async-label", "label", "Асинхронно: открытый наконечник", 220, 1040, 470, 40, font=20)
    n("note-1", "label", "Цилиндр — данные компонента. Объект со складкой — данные обмена. Общий ID допустим.", 30, 1130, 1460, 45, font=21)
    n("note-2", "label", "Пунктир — вход/выход данных; сплошная связь действий — вызов/переход. Условия подписывают явно.", 30, 1195, 1460, 45, font=21)
    n("note-3", "label", "Номер интерфейса общий для всего ОТАР; не номер шага. Цвета — приближение, не корпоративные RGB.", 30, 1260, 1460, 45, font=21)
    return m


def example_pair() -> Model:
    m = Model("ОТАР — согласованная пара", 2240, 1780)
    n = m.node
    n("title", "label", "ОТАР: одна модель — два представления", 30, 15, 2180, 55, font=31)
    n("subtitle", "label", "Учебный синхронный сценарий. Названия условные; схема не описывает систему банка.", 30, 80, 2180, 40, font=21)
    n("info-title", "label", "1. Информационная архитектура", 20, 145, 880, 45, font=25)
    n("func-title", "label", "2. Функциональная архитектура", 1000, 145, 1200, 45, font=25)
    n("system", "system", "АС «Заявки»", 20, 220, 880, 970, font=26)
    n("i-c1", "component", "C1\nЗаявки. Портал", 40, 325, 300, 820, "system", font=23, component_id="C1", canonical_name="Заявки. Портал")
    n("i-c2", "component", "C2\nЗаявки. Сервис", 560, 325, 310, 820, "system", font=23, component_id="C2", canonical_name="Заявки. Сервис")
    functions = {
        "C1.F1": ("C1", "Отправить заявку"),
        "C1.F2": ("C1", "Получить решение"),
        "C1.F3": ("C1", "Показать решение"),
        "C2.F1": ("C2", "Принять заявку"),
        "C2.F2": ("C2", "Рассчитать решение"),
        "C2.F3": ("C2", "Предоставить решение"),
    }
    for ref, (component, name) in functions.items():
        x = 55 if component == "C1" else 610
        y = 440 + (int(ref[-1]) - 1) * 145
        n(f"i-{ref}", "function", f"{ref}\n{name}", x, y, 270 if component == "C1" else 240, 85, f"i-{component.lower()}", font=20,
          function_id=ref, component_id=component, canonical_name=name)
    for id, name, y in (("D1", "Заявка", 880), ("D2", "Решение", 1020)):
        n(f"i-{id}", "entity", f"{id}\n{name}", 600, y, 230, 100, "i-c2", entity_id=id, role="component-data")
    n("transit", "label", "Транзит данных:\nцилиндр не требуется", 60, 1015, 260, 75, "i-c1", font=19)
    m.edge("i-submit", "i-C1.F1", "i-C2.F1", [(325, 485), (610, 485)], interface_number="1", provider="C2", service="C2.F1", data_id="D1", initiator="C1")
    m.edge("i-result", "i-C2.F3", "i-c1", [(610, 780), (340, 780)], interface_number="2", provider="C2", service="C2.F3", data_id="D2", initiator="C1")
    n("i-submit-label", "label", "Заявка\n[Принять заявку]", 347, 410, 205, 65, font=17)
    n("i-result-label", "label", "Решение\n[Предоставить решение]", 342, 695, 215, 75, font=16)
    for number, y in (("1", 485), ("2", 780)):
        n(f"i-interface-{number}", "interface", number, 547, y - 13, 26, 26, font=16, interface_number=number, provider="C2")
    n("i-actor", "actor", "", 70, 1230, 45, 65)
    n("i-actor-label", "label", "Заявитель", 30, 1300, 130, 30, font=18)
    n("i-participation-label", "label", "Отправить заявку", 195, 1195, 270, 40, font=18)
    m.edge("i-participation", "i-actor", "i-c1", [(92, 1230), (92, 1205), (190, 1205), (190, 1145)], dashed=True)
    n("i-note-1", "label", "1: заявка → Сервис; поставщик — Сервис.", 210, 1240, 680, 45, font=21)
    n("i-note-2", "label", "2: решение → Портал; поставщик — Сервис.", 210, 1300, 680, 45, font=21)
    n("i-note-3", "label", "В обоих случаях вызов инициирует Портал.\nСтрелка показывает основные данные, не инициатора.", 30, 1390, 860, 80, font=21)
    n("i-note-4", "label", "Протоколы и технический ответ приёма опущены.\nФункции и сущности показаны раздельно.", 30, 1510, 860, 80, font=21)
    for component, x in (("C1", 1000), ("C2", 1640)):
        name = "Заявки. Портал" if component == "C1" else "Заявки. Сервис"
        n(f"f-{component.lower()}", "lane", f"{component}\n{name}", x, 220, 540, 1430, font=24, component_id=component, canonical_name=name)
    n("f-start", "start", "", 1245, 375, 50, 50, "f-c1")
    n("f-start-label", "label", "Подать заявку", 1100, 330, 340, 30, "f-c1", font=19)
    n("f-actor", "actor", "", 1040, 355, 45, 65, "f-c1")
    n("f-actor-label", "label", "Заявитель", 1010, 425, 130, 35, "f-c1", font=18)
    positions = {"C1.F1": (1100, 470), "C1.F2": (1100, 1040), "C1.F3": (1100, 1410),
                 "C2.F1": (1680, 620), "C2.F2": (1680, 860), "C2.F3": (1680, 1220)}
    for ref, (component, name) in functions.items():
        x, y = positions[ref]
        n(f"f-{ref}", "action", f"{ref}\n{name}", x, y, 320, 100, f"f-{component.lower()}", font=21,
          function_id=ref, component_id=component, canonical_name=name)
    n("f-request", "payload", "D1\nЗаявка", 1130, 680, 230, 100, "f-c1", entity_id="D1", role="exchange-data")
    n("f-stored-request", "entity", "D1\nЗаявка", 2015, 735, 145, 100, "f-c2", font=19, entity_id="D1", role="component-data")
    n("f-stored-result", "entity", "D2\nРешение", 2015, 1050, 145, 100, "f-c2", font=19, entity_id="D2", role="component-data")
    n("f-result", "payload", "D2\nРешение", 1130, 1250, 230, 100, "f-c1", entity_id="D2", role="exchange-data")
    n("f-end", "end", "", 1245, 1550, 50, 50, "f-c1")
    n("f-end-label", "label", "Решение показано", 1100, 1610, 340, 30, "f-c1", font=19)
    m.edge("f-begin", "f-start", "f-C1.F1", [(1270, 425), (1270, 470)])
    m.edge("f-participation", "f-actor", "f-C1.F1", [(1085, 387), (1140, 387), (1140, 470)], dashed=True)
    m.edge("f-submit", "f-C1.F1", "f-C2.F1", [(1420, 520), (1585, 520), (1585, 670), (1680, 670)], interface_number="1", provider="C2", service="C2.F1")
    m.edge("f-request-out", "f-C1.F1", "f-request", [(1245, 570), (1245, 680)], dashed=True)
    m.edge("f-request-in", "f-request", "f-C2.F1", [(1360, 730), (1605, 730), (1605, 700), (1680, 700)], dashed=True)
    m.edge("f-accept-calc", "f-C2.F1", "f-C2.F2", [(1840, 720), (1840, 860)])
    m.edge("f-request-store", "f-C2.F1", "f-stored-request", [(2000, 670), (2087, 670), (2087, 735)], dashed=True)
    m.edge("f-request-read", "f-stored-request", "f-C2.F2", [(2087, 835), (2087, 910), (2000, 910)], dashed=True)
    m.edge("f-result-store", "f-C2.F2", "f-stored-result", [(2000, 935), (2087, 935), (2087, 1050)], dashed=True)
    m.edge("f-submit-return", "f-C2.F2", "f-C1.F2", [(1680, 910), (1570, 910), (1570, 1090), (1420, 1090)])
    n("f-ack-label", "label", "Приём завершён", 1320, 875, 210, 30, font=17)
    m.edge("f-get", "f-C1.F2", "f-C2.F3", [(1420, 1070), (1550, 1070), (1550, 1250), (1680, 1250)], interface_number="2", provider="C2", service="C2.F3")
    m.edge("f-result-read", "f-stored-result", "f-C2.F3", [(2087, 1150), (2087, 1290), (2000, 1290)], dashed=True)
    m.edge("f-return", "f-C2.F3", "f-C1.F3", [(1680, 1290), (1590, 1290), (1590, 1460), (1420, 1460)], interface_number="2", provider="C2", service="C2.F3")
    m.edge("f-result-out", "f-C2.F3", "f-result", [(1680, 1310), (1360, 1310)], dashed=True)
    m.edge("f-result-in", "f-result", "f-C1.F3", [(1245, 1350), (1245, 1410)], dashed=True)
    m.edge("f-finish", "f-C1.F3", "f-end", [(1270, 1510), (1270, 1550)])
    n("f-interface-1", "label", "1", 1500, 480, 50, 35, font=21, interface_number="1", provider="C2")
    n("f-interface-2", "label", "2", 1490, 1160, 50, 35, font=21, interface_number="2", provider="C2")
    n("f-return-label", "label", "2: возврат", 1445, 1360, 140, 35, font=17)
    n("footer", "label", "Точные имена и ID функций совпадают. 1 и 2 — интерфейсы всего ОТАР, не номера шагов сценария.", 30, 1700, 2180, 45, font=23)
    return m


def style(n: Node) -> str:
    common = f"html=0;whiteSpace=wrap;fontFamily=Arial;fontSize={n.font};strokeColor={LINE};fillColor={COLORS[n.kind]};"
    if n.kind in ("component", "system", "lane"):
        return common + ("swimlane;startSize=95;horizontal=1;collapsible=0;swimlaneFillColor=#ffffff;" if n.kind == "lane" else "rounded=1;arcSize=4;verticalAlign=top;spacingTop=15;") + "fontStyle=1;"
    extra = {"function": "rounded=1;arcSize=12;", "action": "rounded=1;arcSize=16;",
             "entity": "shape=cylinder;size=15;spacingTop=15;", "payload": "shape=note;size=22;",
             "start": "ellipse;", "end": "ellipse;strokeWidth=5;",
             "interface": "ellipse;", "actor": "shape=umlActor;", "label": "text;strokeColor=none;"}
    return common + extra[n.kind]


def cell_parent(root: ET.Element, id: str, text: str, meta: dict) -> tuple[ET.Element, dict]:
    if meta:
        obj = ET.SubElement(root, "object", {"id": id, "label": text, "evidence": "Учебный пример; не факт проекта", **meta})
        return obj, {}
    return root, {"id": id, "value": text}


def drawio(m: Model) -> bytes:
    root_file = ET.Element("mxfile", {"host": "app.diagrams.net", "type": "device"})
    diagram = ET.SubElement(root_file, "diagram", {"id": m.name, "name": m.name})
    graph = ET.SubElement(diagram, "mxGraphModel", {"grid": "1", "gridSize": "10", "page": "1", "pageScale": "1", "pageWidth": str(m.width), "pageHeight": str(m.height)})
    root = ET.SubElement(graph, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    nodes = {n.id: n for n in m.nodes}
    for n in m.nodes:
        parent, attrs = cell_parent(root, n.id, n.text, n.meta)
        cell = ET.SubElement(parent, "mxCell", {**attrs, "vertex": "1", "parent": n.parent, "style": style(n)})
        px, py = (nodes[n.parent].x, nodes[n.parent].y) if n.parent != "1" else (0, 0)
        ET.SubElement(cell, "mxGeometry", {"as": "geometry", "x": str(n.x - px), "y": str(n.y - py), "width": str(n.w), "height": str(n.h)})
    for e in m.edges:
        source, target = nodes[e.source], nodes[e.target]
        sx, sy = e.points[0]
        tx, ty = e.points[-1]
        edge_style = f"rounded=0;endArrow={'open' if e.mode == 'async' else 'block'};endFill={'0' if e.mode == 'async' else '1'};strokeWidth=1.8;strokeColor={LINE};"
        edge_style += f"exitX={(sx-source.x)/source.w};exitY={(sy-source.y)/source.h};exitPerimeter=0;entryX={(tx-target.x)/target.w};entryY={(ty-target.y)/target.h};entryPerimeter=0;"
        if e.dashed:
            edge_style += "dashed=1;dashPattern=6 4;"
        parent, attrs = cell_parent(root, e.id, "", e.meta)
        cell = ET.SubElement(parent, "mxCell", {**attrs, "edge": "1", "parent": "1", "source": e.source, "target": e.target, "style": edge_style})
        geometry = ET.SubElement(cell, "mxGeometry", {"as": "geometry", "relative": "1"})
        points = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in e.points[1:-1]:
            ET.SubElement(points, "mxPoint", {"x": str(x), "y": str(y)})
    ET.indent(root_file)
    return ET.tostring(root_file, encoding="utf-8", xml_declaration=True)


def svg(m: Model) -> bytes:
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{m.width}" height="{m.height}" viewBox="0 0 {m.width} {m.height}">', '<rect width="100%" height="100%" fill="white"/>']

    def node(n):
        x, y, w, h = n.x, n.y, n.w, n.h
        fill = COLORS[n.kind]
        attrs = f'fill="{fill}" stroke="{LINE}" stroke-width="1.5"'
        if n.kind in ("system", "component", "lane", "function", "action"):
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{0 if n.kind == "lane" else 10}" {attrs}/>')
            if n.kind == "lane":
                out.append(f'<path d="M{x},{y+95}h{w}" stroke="{LINE}"/>')
        elif n.kind == "entity":
            out.append(f'<path d="M{x},{y+15}a{w/2},15 0 0 1 {w},0v{h-30}a{w/2},15 0 0 1 -{w},0z" {attrs}/>')
            out.append(f'<ellipse cx="{x+w/2}" cy="{y+15}" rx="{w/2}" ry="15" {attrs}/>')
        elif n.kind == "payload":
            out.append(f'<path d="M{x},{y}h{w-22}l22,22v{h-22}h-{w}z" {attrs}/>')
            out.append(f'<path d="M{x+w-22},{y}v22h22" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
        elif n.kind in ("start", "end", "interface"):
            out.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="{LINE}" stroke-width="{5 if n.kind == "end" else 1.5}"/>')
        elif n.kind == "actor":
            out.append(f'<circle cx="{x+w/2}" cy="{y+9}" r="9" fill="white" stroke="{LINE}"/>')
            out.append(f'<path d="M{x+w/2},{y+18}v27m-{w/2},-18h{w}m-{w/2},18l-{w/2},20m{w/2},-20l{w/2},20" fill="none" stroke="{LINE}" stroke-width="2"/>')
        lines = n.text.splitlines()
        leading = n.font * 1.25
        top = y + 22 if n.kind in ("component", "system", "lane") else y + (h - len(lines) * leading) / 2
        if n.kind == "entity":
            top += 7.5  # Center the label below the cylinder's top cap.
        for i, text in enumerate(lines):
            out.append(f'<text x="{x+w/2}" y="{top + (i+0.8)*leading}" font-family="Arial, sans-serif" font-size="{n.font}" text-anchor="middle" fill="#252b30" font-weight="{700 if n.kind in ("system", "component", "lane") else 400}">{escape(text)}</text>')

    for n in m.nodes:
        if n.kind in ("system", "component", "lane"):
            node(n)
    for e in m.edges:
        points = " ".join(f"{x},{y}" for x, y in e.points)
        out.append(f'<polyline points="{points}" fill="none" stroke="{LINE}" stroke-width="1.8" stroke-linejoin="round"' + (' stroke-dasharray="6 4"' if e.dashed else '') + '/>')
        (px, py), (x, y) = e.points[-2:]
        angle = math.atan2(y-py, x-px)
        back = (x-11*math.cos(angle), y-11*math.sin(angle))
        a = (back[0]+4.5*math.sin(angle), back[1]-4.5*math.cos(angle))
        b = (back[0]-4.5*math.sin(angle), back[1]+4.5*math.cos(angle))
        out.append(f'<path d="M{a[0]},{a[1]}L{x},{y}L{b[0]},{b[1]}" fill="{"none" if e.mode == "async" else LINE}" stroke="{LINE}" stroke-width="1.8"/>')
    for n in m.nodes:
        if n.kind not in ("system", "component", "lane"):
            node(n)
    out.append('</svg>')
    return '\n'.join(out).encode('utf-8')


def validate(m: Model) -> None:
    ids = [n.id for n in m.nodes] + [e.id for e in m.edges]
    assert len(ids) == len(set(ids)), "Duplicate IDs"
    nodes = {n.id: n for n in m.nodes}
    for n in m.nodes:
        assert n.w > 0 and n.h > 0
        assert 0 <= n.x <= m.width-n.w and 0 <= n.y <= m.height-n.h, n.id
        if n.parent != "1":
            p = nodes[n.parent]
            assert p.x <= n.x <= p.x+p.w-n.w and p.y <= n.y <= p.y+p.h-n.h, n.id
    for e in m.edges:
        assert e.source in nodes and e.target in nodes
        for id, point in ((e.source, e.points[0]), (e.target, e.points[-1])):
            n, (x, y) = nodes[id], point
            assert n.x <= x <= n.x+n.w and n.y <= y <= n.y+n.h, (e.id, id)
            assert x in (n.x, n.x+n.w) or y in (n.y, n.y+n.h), (e.id, "not on boundary")
    if m.name == "ОТАР — согласованная пара":
        for ref in (f"C{c}.F{f}" for c in (1, 2) for f in (1, 2, 3)):
            info, action = nodes[f"i-{ref}"], nodes[f"f-{ref}"]
            assert info.text == action.text and info.meta == action.meta, ref
        for number, y in (("1", 485), ("2", 780)):
            marker = nodes[f"i-interface-{number}"]
            assert marker.x+marker.w/2 == nodes["i-c2"].x and marker.y+marker.h/2 == y
            assert marker.meta["provider"] == "C2"
        assert {e.meta["interface_number"] for e in m.edges if e.id.startswith("i-") and "interface_number" in e.meta} == {"1", "2"}
        assert {e.meta["interface_number"] for e in m.edges if e.id.startswith("f-") and "interface_number" in e.meta} == {"1", "2"}
        assert nodes["i-D1"].meta["entity_id"] == nodes["f-request"].meta["entity_id"]
        assert nodes["i-D2"].meta["entity_id"] == nodes["f-result"].meta["entity_id"]


def check_xml(data: bytes) -> None:
    root = ET.fromstring(data)
    graph_root = root.find("./diagram/mxGraphModel/root")
    ids = {item.attrib["id"] for item in graph_root}
    assert len(ids) == len(graph_root)
    for cell in graph_root.iter("mxCell"):
        for key in ("parent", "source", "target"):
            if key in cell.attrib:
                assert cell.attrib[key] in ids, cell.attrib[key]


def png(m: Model, svg_data: bytes, destination: Path, browser: Path) -> None:
    temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "opencode"
    with tempfile.TemporaryDirectory(prefix="otar-", dir=temp_root if temp_root.is_dir() else None) as directory:
        temp = Path(directory)
        html = temp / "preview.html"
        html.write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0}svg{display:block}</style>' + svg_data.decode("utf-8"), encoding="utf-8")
        subprocess.run([str(browser), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--user-data-dir={temp / 'profile'}", f"--window-size={m.width},{m.height}",
                        f"--screenshot={destination}", html.as_uri()], check=True, capture_output=True, timeout=90)
        data = destination.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        assert struct.unpack(">II", data[16:24]) == (m.width, m.height), "Unexpected viewport size"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate models and compare generated Draw.io/SVG with assets; do not write")
    parser.add_argument("--browser", type=Path, help="Optional Chromium/Edge executable for rendering SVG to PNG")
    args = parser.parse_args()
    if args.browser and (args.check or not args.browser.is_file()):
        parser.error("--browser needs an existing executable and cannot be combined with --check")
    for stem, model in (("notation", notation()), ("example-pair", example_pair())):
        validate(model)
        outputs = {"drawio": drawio(model), "svg": svg(model)}
        check_xml(outputs["drawio"])
        ET.fromstring(outputs["svg"])
        for extension, data in outputs.items():
            path = ROOT / "assets" / f"{stem}.{extension}"
            if args.check:
                assert path.read_bytes() == data, f"Stale asset: {path}"
            else:
                if extension == "svg" and (not path.exists() or path.read_bytes() != data):
                    path.with_suffix(".png").unlink(missing_ok=True)
                path.write_bytes(data)
        if args.browser:
            png(model, outputs["svg"], ROOT / "assets" / f"{stem}.png", args.browser.resolve())
        print(f"{stem}: {'checked' if args.check else 'built'}; {len(model.nodes)} nodes, {len(model.edges)} edges")


if __name__ == "__main__":
    main()
