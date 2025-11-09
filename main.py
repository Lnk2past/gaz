import datetime
import sys
import time
from typing import Any

sys.path.append("build/Release/src")

import holoviews as hv
import numpy as np
import pandas as pd
import panel as pn
from holoviews.streams import Stream

import gaz
import simple_model

hv.extension("bokeh")
pn.extension()


# WalkModel = gaz.Gaz
WalkModel = simple_model.Model

gaz_model = WalkModel(1000)
update_callback = None
last_start_time = None

# widgets
entity_count_slider = pn.widgets.IntSlider(
    name="N", start=1, end=100000, step=100, value=1000
)
launch_button = pn.widgets.Button(name="Launch")


def launch(event: Any) -> None:
    """Starts/stops updating the Gaz model

    Args:
        event: what triggered this function
    """
    global update_callback, gaz_model, model_data
    if gaz_model is None:
        gaz_model = WalkModel(entity_count_slider.value)
        model_data = gaz_model.get()
    if update_callback is not None and update_callback.running:
        update_callback.stop()
        update_callback = None
        gaz_model = None
    else:
        update_callback = pn.state.add_periodic_callback(update, 33)


launch_button.on_click(launch)


@pn.depends(entity_count_slider, watch=True)
def set_number_of_entities(n: int) -> None:
    """Dynamically sets the number of entities to simulate. This stops
    any callbacks and resets the state of the simulation.

    Args:
        n: number of entities to simulate
    """
    global update_callback, gaz_model, model_data
    if update_callback is not None and update_callback.running:
        update_callback.stop()
        update_callback = None
    gaz_model = WalkModel(n)
    model_data = gaz_model.get()


last_start_time = None


def update() -> None:
    """Updates the underlying model and triggers a refresh of the visualization"""
    global last_start_time
    start = time.perf_counter()

    gaz_model.update(datetime.timedelta(seconds=0.1))
    trigger.event(refresh=not trigger.refresh)

    duration = (time.perf_counter() - start) * 1000
    if duration > 33:
        print(f"⚠️ Update took {duration:.1f} ms (>33 ms)")

    last_start_time = start


rng = np.random.default_rng(1337)


def viz_gaz(**kwargs) -> hv.Points:
    """Visualizes the model data from Gaz"""
    model_data = gaz_model.get()
    return hv.Points(model_data)


# Custom trigger definition + instance for refreshing the visualization
trigger = Stream.define("Trigger", refresh=False)()

# Dynamic visualization
dynamic_map = hv.DynamicMap(viz_gaz, streams=[trigger]).opts(hv.opts.Points(size=1))

# Layout
pn.Column(
    entity_count_slider,
    launch_button,
    dynamic_map.opts(
        height=600, width=600, aspect="equal", xlim=(-510, 510), ylim=(-510, 510)
    ),
).servable()
