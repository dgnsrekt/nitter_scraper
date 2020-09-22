import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["tests", "cover", "lint"]


@nox.session
def tests(session):
    """Pytests"""
    session.install("poetry")
    session.run("poetry", "install")
    session.run("poetry", "run", "pytest", "-v", "--cov=nitter_scraper")
    session.notify("cover")


@nox.session
def cover(session):
    """Coverage analysis"""
    session.install("coverage")
    session.run("coverage", "report", "--show-missing", "--fail-under=70")
    session.run("coverage", "erase")


@nox.session(python="3.8")
def lint(session):
    """Code Linting"""
    session.install(
        "black",
        "flake8",
        "flake8-import-order",
        "flake8-bugbear",
        "poetry",
        # "check-manifest",
    )
    session.run("poetry", "check")
    # session.run("check-manifest")

    session.run("black", "--line-length", "99", "--check", "nitter_scraper")
    session.run("black", "--line-length", "99", "--check", "tests")
    session.run("black", "--line-length", "99", "--check", "examples")
    session.run("black", "--line-length", "99", "--check", "noxfile.py")

    session.run("flake8", "--import-order-style", "google", "nitter_scraper")
    session.run("flake8", "--import-order-style", "google", "tests")
    session.run("flake8", "--import-order-style", "google", "examples")


@nox.session()
def docs(session):
    session.install("pydoc-markdown", "mkdocs-material")
    session.run("pydoc-markdown", "pydoc-markdown.yml", "--server", "--open")
