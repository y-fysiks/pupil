"""
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2020 Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
"""
import logging

from pure_detector import PuReDetector
from pyglui import ui

from methods import normalize
from roi import RoiModel

from .detector_base_plugin import PupilDetectorPlugin
from .visualizer_2d import draw_pupil_outline

logger = logging.getLogger(__name__)


class PureDetectorPlugin(PupilDetectorPlugin):
    uniqueness = "by_class"
    icon_font = "pupil_icons"
    icon_chr = chr(0xEC18)

    def __init__(self, g_pool=None):
        super().__init__(g_pool=g_pool)
        self.detector = PuReDetector()
        self.debug_view = False

    def detect(self, frame):

        gray = frame.gray
        roi: RoiModel = self.g_pool.roi

        # slice out the roi
        if not roi.is_full():
            gray = gray[roi.slices].copy()

        if self.debug_view:
            result, debug_img = self.detector.detect_debug(gray)

            # TODO: BGR is not always the color image, might also be yuv. See UVC for
            # another related TODO.
            if roi.is_full():
                # replace bgr image (property is not writable, so we write directly into
                # the buffer)
                frame.bgr[:] = debug_img
            else:
                # stitch debug roi slice into bgr image
                frame.bgr[roi.slices] = debug_img
        else:
            result = self.detector.detect(gray)

        # if we are using roi, scale the results back up again
        if not roi.is_full():
            offset = roi.bounds[:2]
            result["location"] = tuple(
                coord + off for coord, off in zip(result["location"], offset)
            )
            result["ellipse"]["center"] = tuple(
                coord + off for coord, off in zip(result["ellipse"]["center"], offset)
            )

        eye_id = self.g_pool.eye_id
        location = result["location"]
        result["norm_pos"] = normalize(
            location, (frame.width, frame.height), flip_y=True
        )
        result["timestamp"] = frame.timestamp
        result["topic"] = f"pupil.{eye_id}"
        result["id"] = eye_id
        result["method"] = "2D PuRe"
        return result

    @property
    def pretty_class_name(self):
        return "PuRe Pupil Detector"

    def gl_display(self):
        if self._recent_detection_result:
            draw_pupil_outline(self._recent_detection_result, base_color=(1, 1, 0))

    @property
    def use_default_pupil_diameter(self):
        return self.detector.params.auto_pupil_diameter

    @use_default_pupil_diameter.setter
    def use_default_pupil_diameter(self, value):
        self.detector.params.auto_pupil_diameter = value
        for ui_elem in self.pupil_diameter_sliders:
            ui_elem.read_only = value

    def init_ui(self):
        super().init_ui()
        self.menu.label = self.pretty_class_name
        self.menu_icon.label_font = "pupil_icons"

        self.menu.append(
            ui.Switch(
                "use_default_pupil_diameter", self, label="Use Default Pupil Diameter"
            )
        )

        self.pupil_diameter_sliders = [
            ui.Slider(
                "min_pupil_diameter",
                attribute_context=self.detector.params,
                label="Min Pupil Diameter",
                min=1,
                max=250,
                step=1,
            ),
            ui.Slider(
                "max_pupil_diameter",
                attribute_context=self.detector.params,
                label="Max Pupil Diameter",
                min=50,
                max=400,
                step=1,
            ),
        ]

        # TODO: This does not work in init_ui. Probably a pylgui bug.
        for ui_elem in self.pupil_diameter_sliders:
            ui_elem.read_only = self.detector.params.auto_pupil_diameter

        self.menu.extend(self.pupil_diameter_sliders)

        self.menu.append(ui.Switch("debug_view", self, label="Debug View"))

    def on_resolution_change(self, old_size, new_size):
        pass
