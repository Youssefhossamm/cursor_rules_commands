"""Tests for cursor_docs_content: parsing, validators, builders, and the starter kit."""

import io
import zipfile

import cursor_docs_content as c


# ---------------------------------------------------------------------------
# parse_frontmatter
# ---------------------------------------------------------------------------

class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        fm, body = c.parse_frontmatter("---\ndescription: hi\nalwaysApply: true\n---\n\n# Body")
        assert fm == {"description": "hi", "alwaysApply": True}
        assert body == "# Body"

    def test_no_frontmatter(self):
        fm, body = c.parse_frontmatter("# Just markdown")
        assert fm is None
        assert body == "# Just markdown"

    def test_unclosed_frontmatter(self):
        fm, _ = c.parse_frontmatter("---\ndescription: hi")
        assert fm is None

    def test_invalid_yaml(self):
        fm, _ = c.parse_frontmatter("---\n{ not: valid: yaml\n---\nbody")
        assert fm is None


# ---------------------------------------------------------------------------
# validate_rule
# ---------------------------------------------------------------------------

GOOD_RULE = '---\ndescription: Python conventions\nglobs:\n  - "**/*.py"\nalwaysApply: false\n---\n\n# Standards\n\n- Use type hints\n'


def _messages(results, level=None):
    return [r["message"] for r in results if level is None or r["level"] == level]


class TestValidateRule:
    def test_empty_content_is_error(self):
        assert _messages(c.validate_rule("  "), "error") == ["Empty content"]

    def test_missing_frontmatter_is_error(self):
        assert "Missing frontmatter" in _messages(c.validate_rule("# no frontmatter"), "error")

    def test_good_rule_has_no_errors(self):
        assert _messages(c.validate_rule(GOOD_RULE), "error") == []

    def test_mdc_extension_reminder_present(self):
        assert any("mdc" in m.lower() for m in _messages(c.validate_rule(GOOD_RULE)))

    def test_over_500_lines_is_error(self):
        rule = "---\ndescription: x\n---\n\n# T\n\n" + "\n".join(["- line"] * 520)
        assert any("too long" in m for m in _messages(c.validate_rule(rule), "error"))

    def test_large_code_blocks_warned(self):
        rule = "---\ndescription: x\n---\n\n# T\n\n```python\n" + "\n".join(["code"] * 50) + "\n```\n"
        assert any("code blocks" in m.lower() for m in _messages(c.validate_rule(rule), "warning"))

    def test_always_apply_plus_globs_warned(self):
        rule = '---\ndescription: x\nglobs:\n  - "**/*.py"\nalwaysApply: true\n---\n\n# T\n\n- x'
        assert any("alwaysApply + globs" in m for m in _messages(c.validate_rule(rule), "warning"))

    def test_unknown_fields_warned(self):
        rule = "---\ndescription: x\nbogus: y\n---\n\n# T\n\n- x"
        assert any("Unknown frontmatter" in m for m in _messages(c.validate_rule(rule), "warning"))


# ---------------------------------------------------------------------------
# validate_skill
# ---------------------------------------------------------------------------

GOOD_SKILL = "---\nname: deploy-checklist\ndescription: How to deploy safely. Use when asked to deploy.\n---\n\n# Steps\n\n1. test\n2. ship\n"


class TestValidateSkill:
    def test_good_skill_has_no_errors(self):
        assert _messages(c.validate_skill(GOOD_SKILL, folder_name="deploy-checklist"), "error") == []

    def test_invalid_name_format(self):
        bad = "---\nname: My Skill!\ndescription: does things when needed\n---\nbody"
        assert any("Invalid name" in m for m in _messages(c.validate_skill(bad), "error"))

    def test_folder_mismatch(self):
        assert any(
            "mismatch" in m
            for m in _messages(c.validate_skill(GOOD_SKILL, folder_name="other-name"), "error")
        )

    def test_missing_name_and_description(self):
        errs = _messages(c.validate_skill("---\npaths: ['**/*.py']\n---\nbody"), "error")
        assert any("Missing name" in m for m in errs)
        assert any("Missing description" in m for m in errs)

    def test_short_description_warned(self):
        skill = "---\nname: ok-skill\ndescription: short\n---\nbody"
        assert any("very short" in m for m in _messages(c.validate_skill(skill), "warning"))

    def test_legacy_globs_noted(self):
        skill = "---\nname: ok-skill\ndescription: does things, use for testing stuff\nglobs: ['**/*.py']\n---\nbody"
        assert any("globs" in m for m in _messages(c.validate_skill(skill), "info"))

    def test_non_boolean_dmi_warned(self):
        skill = "---\nname: ok-skill\ndescription: does things, use for testing stuff\ndisable-model-invocation: yes please\n---\nbody"
        assert any("boolean" in m for m in _messages(c.validate_skill(skill), "warning"))


# ---------------------------------------------------------------------------
# builders
# ---------------------------------------------------------------------------

class TestBuilders:
    def test_build_rule_roundtrip(self):
        content = c.build_rule_content(
            description="My rule", globs=["**/*.py"], always_apply=False, title="Title", body="- x"
        )
        fm, body = c.parse_frontmatter(content)
        assert fm["description"] == "My rule"
        assert fm["globs"] == ["**/*.py"]
        assert fm["alwaysApply"] is False
        assert body.startswith("# Title")

    def test_build_skill_roundtrip(self):
        content = c.build_skill_content(
            name="my-skill",
            description="Does things. Use when doing things.",
            paths=["src/**"],
            disable_model_invocation=True,
            body="# Steps",
        )
        fm, body = c.parse_frontmatter(content)
        assert fm["name"] == "my-skill"
        assert fm["paths"] == ["src/**"]
        assert fm["disable-model-invocation"] is True
        assert c.validate_skill(content, folder_name="my-skill")
        assert not [r for r in c.validate_skill(content, folder_name="my-skill") if r["level"] == "error"]

    def test_build_skill_omits_optional_fields(self):
        content = c.build_skill_content("s1", "desc here for use", [], False, "body")
        assert "paths:" not in content
        assert "disable-model-invocation" not in content


# ---------------------------------------------------------------------------
# starter kit
# ---------------------------------------------------------------------------

def _zip_names(data: bytes):
    return zipfile.ZipFile(io.BytesIO(data)).namelist()


class TestStarterKit:
    def test_default_kit_contents(self):
        names = _zip_names(c.generate_starter_kit_zip())
        rules = [n for n in names if "/.cursor/rules/" in n]
        skills = [n for n in names if "/.cursor/skills/" in n]
        agents = [n for n in names if "/.cursor/agents/" in n]
        commands = [n for n in names if "/.cursor/commands/" in n]

        assert len(rules) == 5 and all(n.endswith(".mdc") for n in rules)
        assert len(skills) == 10 and all(n.endswith("/SKILL.md") for n in skills)
        assert len(agents) == 3
        assert commands == []  # legacy commands are opt-in only
        assert any(n.endswith("hooks.json.example") for n in names)
        assert any(n.endswith("AGENTS.md") for n in names)
        assert any(n.endswith("README.md") for n in names)

    def test_all_kit_skills_validate(self):
        zf = zipfile.ZipFile(io.BytesIO(c.generate_starter_kit_zip()))
        for n in zf.namelist():
            if n.endswith("/SKILL.md"):
                folder = n.split("/")[-2]
                content = zf.read(n).decode("utf-8")
                errors = [r for r in c.validate_skill(content, folder_name=folder) if r["level"] == "error"]
                assert errors == [], f"{folder}: {errors}"

    def test_subagents_have_valid_frontmatter(self):
        for fname, content in c.STARTER_KIT_SUBAGENTS.items():
            fm, body = c.parse_frontmatter(content)
            assert fm is not None, fname
            assert fm["name"] == fname.replace(".md", "")
            assert fm["description"]
            assert body.strip()

    def test_checker_subagents_are_readonly(self):
        for fname in ("verifier.md", "code-reviewer.md"):
            fm, _ = c.parse_frontmatter(c.STARTER_KIT_SUBAGENTS[fname])
            assert fm.get("readonly") is True, fname

    def test_custom_kit_respects_selection(self):
        names = _zip_names(c.generate_custom_starter_kit_zip(
            ["cursor-rules.mdc"], ["debug.md"], True,
            selected_skills=["commit"], selected_subagents=["verifier.md"],
            include_hooks_example=True,
        ))
        assert any("/rules/cursor-rules.mdc" in n for n in names)
        assert any("/commands/debug.md" in n for n in names)
        assert any("/skills/commit/SKILL.md" in n for n in names)
        assert any("/agents/verifier.md" in n for n in names)
        assert any(n.endswith("hooks.json.example") for n in names)

    def test_custom_kit_backward_compatible_signature(self):
        names = _zip_names(c.generate_custom_starter_kit_zip(["cursor-rules.mdc"], [], True))
        assert any("cursor-rules.mdc" in n for n in names)

    def test_options_cover_all_groups(self):
        opts = c.get_starter_kit_options()
        assert {len(opts["rules"]), len(opts["skills"]), len(opts["commands"]), len(opts["subagents"])} == {5, 10, 10, 3}
        assert all(k.endswith(".mdc") for k in opts["rules"])


# ---------------------------------------------------------------------------
# docs data the app renders
# ---------------------------------------------------------------------------

class TestDocsData:
    def test_hooks_documentation(self):
        h = c.get_hooks_documentation()
        assert sum(len(v) for v in h["hook_groups"].values()) == 21
        assert '"version": 1' in h["example"]
        assert "options_summary" in h

    def test_skills_docs_keys(self):
        sd = c.get_skills_docs()
        for key in ("overview", "locations", "bundled_dirs", "builtin_skills", "migration", "example"):
            assert key in sd

    def test_subagents_docs_keys(self):
        sa = c.get_subagents_docs()
        for key in ("overview", "locations", "frontmatter", "builtins", "invocation", "cloud", "best_practices", "example"):
            assert key in sa
        assert len(sa["builtins"]) == 3

    def test_prompt_template_categories(self):
        assert len(c.get_prompt_templates("rules")) == 8
        assert len(c.get_prompt_templates("commands")) == 3
        assert len(c.get_prompt_templates("skills")) == 2
        assert len(c.get_prompt_templates("subagents")) == 2
        assert c.get_prompt_templates("nonexistent") == []

    def test_rule_prompts_output_mdc(self):
        for p in c.get_prompt_templates("rules"):
            assert p["output_file"].endswith(".mdc"), p["output_file"]

    def test_whats_new_timeline(self):
        entries = c.get_whats_new()
        assert len(entries) >= 8
        for e in entries:
            assert e["version"] and e["date"] and e["highlights"]

    def test_example_files_load_mdc_rules(self):
        ex = c.load_example_files()
        assert len(ex["rules"]) == 3
        assert all(name.endswith(".mdc") for name in ex["rules"])
        assert len(ex["commands"]) == 7
