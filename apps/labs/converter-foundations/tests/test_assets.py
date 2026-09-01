"""Asset checks: every referenced circuit image exists and is flattened."""

from pathlib import Path

import pytest

from callbacks.plots_callback import _CIRCUIT_IMG_SRC as CM1_SRC
from callbacks.cm2_plots_callback import _CIRCUIT_IMG_SRC as CM2_SRC

ASSETS = Path(__file__).resolve().parent.parent / 'assets'

referenced = sorted(set(CM1_SRC.values()) | set(CM2_SRC.values()))


@pytest.mark.parametrize('url', referenced)
def test_referenced_circuit_image_exists(url):
    assert url.startswith('/assets/')
    assert (ASSETS / url.removeprefix('/assets/')).is_file()


@pytest.mark.parametrize('png', sorted(ASSETS.glob('*.png')), ids=lambda p: p.name)
def test_png_has_no_embedded_editable_diagram(png):
    # draw.io stores the editable diagram in a tEXt/zTXt chunk keyed "mxfile".
    # The export step must have stripped it (audit change 2).
    from PIL import Image

    with Image.open(png) as im:
        assert 'mxfile' not in im.info
        assert not any(k.lower().startswith('mxfile') for k in im.info)
