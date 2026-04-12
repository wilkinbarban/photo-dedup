# Contributing

Thanks for considering a contribution to PhotoDedup.

## Important notice

This is an educational project that demonstrates Python desktop application development with PyQt6, media analysis workflows, and Windows distribution automation.

By submitting a contribution, you agree to license your work under the GNU General Public License v3.0 (GPLv3), the same license used by this project.

## Scope

Contributions should improve one or more of the following:

- Code quality and maintainability
- Reliability and error handling
- Documentation and onboarding
- Packaging and release automation
- User experience in the Windows desktop app

Please do not contribute features that encourage misuse, violate platform terms, or weaken security.

## Before you start

- Read README.md, CHANGELOG.md, and the educational disclaimer.
- Open an issue before starting large changes.
- Keep pull requests focused and reviewable.
- Prioritize compatibility with Windows 10/11.

## Setup

### Windows (recommended)

Use the existing dependency installer:

```cmd
install_dependencies.bat
```

Then run:

```cmd
python src\main\photo_dedup.py
```

### Manual setup

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python src\main\photo_dedup.py
```

## Local validation before PR

At minimum, run:

```cmd
python -m py_compile src\main\photo_dedup.py scripts\maintenance\update_analyzer.py scripts\maintenance\update_texts.py src\interfaces\language_dialog.py src\interfaces\main_window.py src\interfaces\screens.py src\interfaces\theme.py src\interfaces\widgets.py src\modules\config\i18n.py src\modules\config\state.py src\modules\services\ai_model.py src\modules\services\analyzer.py src\modules\services\models.py src\modules\services\takeout.py src\modules\utils\logger.py src\modules\utils\paths.py
```

If your change touches packaging/release flow, validate:

```powershell
./scripts/build_windows.ps1 -Version local-test -Clean
```

Before creating a new release tag, regenerate release notes from template:

```cmd
python scripts\generate_release_md.py --version X.Y.Z
```

## Release process (one tag push)

After updating `src/main/photo_dedup.py` version and `CHANGELOG.md` for `X.Y.Z`, publish with one command:

```cmd
git push origin vX.Y.Z
```

This triggers `.github/workflows/publish-release-from-tag.yml`, which:
- validates tag/version consistency,
- generates `RELEASE.md` from `CHANGELOG.md`,
- creates the GitHub Release.

Then `.github/workflows/build-release-exe.yml` runs on release publish and uploads EXE assets automatically.

## Coding guidelines

- Prefer small, clear commits.
- Keep architecture modular between `src/modules` and `src/interfaces`.
- Avoid unrelated refactors in the same PR.
- Preserve desktop usability and responsiveness.
- Update README.md and/or CHANGELOG.md when behavior changes.
- Do not add new dependencies without updating requirements.txt and explaining why.
- Write new comments and docstrings in English.

## Pull request checklist

- [ ] Change is scoped and clearly explained.
- [ ] App still starts normally on Windows.
- [ ] Python syntax check passes (`py_compile`).
- [ ] Docs updated if behavior changed (README.md and/or CHANGELOG.md).
- [ ] No unnecessary dependency additions.
- [ ] PR title is descriptive.

## Commit style

Recommended prefixes:

- feat: new user-visible functionality
- fix: bug fixes and regressions
- docs: documentation only
- ci: workflow and automation updates
- build: packaging/build process changes
- chore: maintenance tasks

Examples:

- feat: add stable release channel for secure installer
- fix: handle in-memory execution in secure installer signature check
- ci: add Windows EXE smoke-test workflow
- docs: add Download Windows EXE section for non-technical users
