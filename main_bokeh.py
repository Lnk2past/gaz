# DISCLAIMER! I gave ChatGPT `main.py` and told it to convert it to use Bokeh directly
# while leaning into NumPy and this is what it produced

import datetime
import sys
import time
from typing import Any

sys.path.append("build/Release/src")

import numpy as np
import panel as pn
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

import gaz
import simple_model

pn.extension("bokeh")

# WalkModel = gaz.Gaz
WalkModel = simple_model.Model

gaz_model = WalkModel(1000)
update_callback = None
last_start_time = None

entity_count_slider = pn.widgets.IntSlider(
    name="N", start=1, end=100000, step=100, value=1000
)
launch_button = pn.widgets.Button(name="Launch")

fig = figure(
    height=600,
    width=600,
    x_range=(-510, 510),
    y_range=(-510, 510),
    match_aspect=True,
    title="Gaz Simulation",
    toolbar_location=None,
    tools="pan,wheel_zoom,box_zoom,reset",
    active_drag="pan",
    active_scroll="wheel_zoom",
)
fig.output_backend = "webgl"

model_data = gaz_model.get()
source = ColumnDataSource(
    data=dict(
        x=model_data[0].copy(),
        y=model_data[1].copy(),
    )
)

fig.scatter("x", "y", source=source, size=2)


def set_number_of_entities(n: int) -> None:
    """Reset simulation with new entity count."""
    global gaz_model, update_callback

    if update_callback is not None and update_callback.running:
        update_callback.stop()
        update_callback = None

    gaz_model = WalkModel(n)
    data = gaz_model.get()

    source.data["x"] = data[0].copy()
    source.data["y"] = data[1].copy()
    source.trigger("data", source.data, source.data)


entity_count_slider.param.watch(lambda e: set_number_of_entities(e.new), "value")


def update() -> None:
    """Advance model and update visualization in-place."""
    global last_start_time
    start = time.perf_counter()

    gaz_model.update(datetime.timedelta(seconds=0.1))
    new = gaz_model.get()

    x = source.data["x"]
    y = source.data["y"]
    np.copyto(x, new[0])
    np.copyto(y, new[1])

    source.trigger("data", source.data, source.data)

    duration = (time.perf_counter() - start) * 1000
    if duration > 33:
        print(f"⚠️ Update took {duration:.1f} ms (>33 ms)")

    last_start_time = start


def launch(event: Any) -> None:
    """Start/stop simulation updates."""
    global update_callback, gaz_model

    if update_callback is not None and update_callback.running:
        update_callback.stop()
        update_callback = None
        gaz_model = None
        launch_button.name = "Launch"
    else:
        if gaz_model is None:
            gaz_model = WalkModel(entity_count_slider.value)
        update_callback = pn.state.add_periodic_callback(update, period=33)
        launch_button.name = "Stop"


launch_button.on_click(launch)

dashboard = pn.Column(
    entity_count_slider,
    launch_button,
    fig,
)

dashboard.servable()
