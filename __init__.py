"""Freqtrade package shim for git-submodule usage.

When this repository is embedded as a git submodule (e.g. inside
PortfolioBench), Python's default PathFinder may discover this repo-root
directory as an implicit namespace package *before* the setuptools editable-
install finder runs.  That shadows the real ``freqtrade`` Python package which
lives one level deeper at ``freqtrade/freqtrade/``.

This shim turns the repo root into a proper package by:
1. Redirecting ``__path__`` to the inner ``freqtrade/`` directory so that
   sub-package imports (``from freqtrade.strategy import …``) resolve
   correctly.
2. Re-exporting ``__version__`` from the inner package.
"""

import importlib.util as _iu
import os as _os

_inner = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "freqtrade")
_inner_init = _os.path.join(_inner, "__init__.py")

if _os.path.isfile(_inner_init):
    # 1) Redirect sub-package lookups to the inner tree.
    __path__ = [_inner]

    # 2) Load the inner __init__.py to obtain __version__.
    _spec = _iu.spec_from_file_location(
        "__freqtrade_inner__",
        _inner_init,
        submodule_search_locations=[_inner],
    )
    _mod = _iu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    __version__ = _mod.__version__
