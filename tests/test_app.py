"""Smoke and interaction tests for the Streamlit app via streamlit.testing."""

import pytest
from streamlit.testing.v1 import AppTest

APP_FILE = "cursor_docs_app.py"


@pytest.fixture()
def at():
    app = AppTest.from_file(APP_FILE, default_timeout=120)
    app.run()
    return app


def test_app_renders_without_exceptions(at):
    assert not at.exception, [e.message for e in at.exception]
    # 5 main tabs + 4 Build sub-tabs + 3 Skills & Commands sub-tabs
    assert len(at.tabs) == 12


def test_decision_helper_skill_and_subagent_paths(at):
    at.radio(key="dh_when").set_value("On demand — when I ask, or when the task matches")
    at.run()
    assert any(r.key == "dh_what" for r in at.radio)
    assert any("Skill" in s.value for s in at.success)

    at.radio(key="dh_what").set_value(
        "A separate specialist with its own context window (reviewer, verifier, domain expert)"
    )
    at.run()
    assert any("Subagent" in s.value for s in at.success)
    assert not at.exception


def test_decision_helper_hook_path(at):
    at.radio(key="dh_when").set_value(
        "Automatically around agent actions (before/after tool calls, edits, prompts)"
    )
    at.run()
    assert any("Hook" in s.value for s in at.success)


def test_skill_builder_normalizes_name(at):
    at.text_input(key="sb_name").set_value("My Deploy Skill")
    at.text_input(key="sb_desc").set_value("How to deploy safely. Use when asked to deploy.")
    at.run()
    assert any("my-deploy-skill" in s.value for s in at.success)
    assert not at.exception


def test_validator_skill_mode_flags_bad_skill(at):
    at.radio(key="rv_kind").set_value("Skill (SKILL.md)")
    at.run()
    at.text_area(key="rv_input").set_value("---\nname: Bad Name\n---\nbody")
    at.run()
    errors = [e.value for e in at.error]
    assert any("Invalid name" in e for e in errors)
    assert any("Missing description" in e for e in errors)


def test_validator_rule_mode_flags_missing_frontmatter(at):
    at.text_area(key="rv_input").set_value("just some text")
    at.run()
    assert any("Missing frontmatter" in e.value for e in at.error)
