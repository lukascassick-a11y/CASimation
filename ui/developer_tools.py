from __future__ import annotations

import platform
import sys
from pathlib import Path

import streamlit as st

from estimator.health_check import all_checks_pass, git_metadata, run_health_checks


def render_developer_tools(root: str | Path, repo=None) -> None:
    """Render optional diagnostics without affecting normal estimating behavior."""
    root_path = Path(root).resolve()
    with st.sidebar.expander("Developer Tools", expanded=False):
        metadata = git_metadata(root_path)
        st.caption(f"Application path: {root_path}")
        st.caption(f"Python: {platform.python_version()}")
        st.caption(f"Git branch: {metadata['branch']}")
        st.caption(f"Commit: {metadata['commit']}")
        st.caption(f"Working tree: {metadata['working_tree']}")

        col1, col2 = st.columns(2)
        run_checks = col1.button("Run health check", key="dev_run_health_check", use_container_width=True)
        clear_cache = col2.button("Clear caches", key="dev_clear_caches", use_container_width=True)

        if clear_cache:
            st.cache_data.clear()
            st.cache_resource.clear()
            if repo is not None and hasattr(repo, "clear_cache"):
                repo.clear_cache()
            st.success("Application caches cleared.")

        if run_checks:
            results = run_health_checks(root_path)
            for result in results:
                icon = "✅" if result.ok else "❌"
                st.write(f"{icon} **{result.name}** — {result.message} ({result.elapsed_ms:.0f} ms)")
            if all_checks_pass(results):
                st.success("All startup checks passed.")
            else:
                st.error("One or more startup checks failed.")

        st.markdown("**Useful paths**")
        st.code(str(root_path / "data"), language=None)
        st.code(str(root_path / "projects"), language=None)
