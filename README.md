# hemavarshini-mangai.github.io

Personal blog and portfolio website built with [Pelican](https://getpelican.com/) and deployed to GitHub Pages via GitHub Actions.

🔗 **Live site:** https://hemavarshini-mangai.github.io

## Setup

```bash
pip install -r requirements.txt
```

## Local Development

```bash
make devserver
```

Serves the site locally with auto-reload for development and testing.

## Build for Production

```bash
make publish
```

Generates the production-ready site using `publishconf.py` into the `output/` directory.

## Deployment

Pushes to `main` automatically trigger a GitHub Actions workflow that builds and deploys the site to GitHub Pages.

## Project Structure

```text
content/          # Blog posts and pages (Markdown)
content/images/   # Static images
content/pages/    # Static pages such as About
theme/            # Custom Pelican theme
pelicanconf.py    # Development configuration
publishconf.py    # Production configuration
requirements.txt  # Python dependencies
Makefile          # Development and build commands
.github/workflows/ # GitHub Actions deployment workflow
```

## About

This is my personal blog where I share my learning journey, projects, experiences, and insights in technology, Generative AI, programming, and software development.

## Technologies

* Python
* Pelican
* Markdown
* HTML/CSS
* Git & GitHub
* GitHub Pages
* GitHub Actions
