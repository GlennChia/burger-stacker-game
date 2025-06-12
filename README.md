# Burger Stacker Game built with Amazon Q Developer

![cover image](./docs/00-cover/cover-image.png)

# 1. Introduction

Exploratory repo that uses Amazon Q Developer CLI to generate a PyGame for a Burger Stacker Game based on a series of prompts used. This repo elaborates on Q Developer CLI, the prompts used, and how to play the game. This repo is also linked to the blog post [Grilling Games: Build Burger Stacker with Amazon Q Developer CLI](https://community.aws/content/2yK6VCidazUoocEO92BhTWYr7mM)

Try the game here: https://glennchia.github.io/burger-stacker-game/

# 2. Pre-reqs

Install Amazon Q Developer CLI. Installation steps detailed here: [Amazon Q Developer User Guide: Installing Amazon Q for command line](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-installing.html)

# 3. Prompting

Refer to [prompt-sequence.md](./prompt-sequence.md) for each step of prompt refinement.

# 4. Game files

Amazon Q Developer generated the following files

- [burger_stacker.py](./q-generated-files/burger_stacker.py)
- [README.md](./q-generated-files/README.md)
- [requirements.txt](./q-generated-files/requirements.txt)

# 5. Running the game

Follow the installation instructions in [q-generated-files/README.md](./q-generated-files/README.md) to install the relevant packages and run the game

# 6. Game UI

![final UI](./docs/04-third-prompt/04-final-ui.png)

# 7. Misc

## 7.1 GitHub pages debugging

If the PyGame build is showing a blank screen, access the GitHub page at `#debug` like `https://glennchia.github.io/burger-stacker-game/#debug` and follow the on-screen instructions to click some keys and view the debug logs.