<!-- Written by Alexander Holman 19/08/2019 -->
<!--
This file should contain a step by step guide on how to install, update and remove the software, along with any 
prerequisites for each step should they exist. It is written to be used with most internal projects, but as per the 
other documents feel free to adapt it to fit your needs, adding, modifying and removing as necessary.
-->

# Installation

## Prerequisites 
<!-- List of a conditions that need to be met prior to installation, including os requirements, dependancies, etc -->
<!-- EXAMPLE START -->
* Git for cloning the repository
* Bash shell (for running validation scripts)
* A GitHub account (if using as a template repository)
<!--  EXAMPLE END -->

## From scratch
<!-- Step-by-step guide on how to install -->
<!-- EXAMPLE START -->
Use this repository as a GitHub template to create your own {{package-name}}, or clone it directly to work with the definitions.

**Option 1: Use GitHub's Template Feature (Recommended)**
1. Visit the [{{repo-name}} repository](https://github.com/alexanderholman/{{repo-name}})
2. Click the green "Use this template" button
3. Select "Create a new repository"
4. Fill in your new repository details and click "Create repository"
5. Clone your new repository and start customizing

**Option 2: Clone for Direct Use**
Clone the repository to use directly:
```bash
git clone https://github.com/alexanderholman/{{repo-name}}.git
cd {{repo-name}}
```
<!--  EXAMPLE END -->

## Updating
<!-- Step-by-step guide on how to update -->
<!-- EXAMPLE START -->
**Note:** If you created a repository from this template, it becomes independent from {{repo-name}}. You can customize as needed.

However, if you want to pull updates from {{repo-name}}:

**Option 1: Pull Updates (For Direct Clones)**
If you cloned the repository directly:
```bash
git pull origin main
```

**Option 2: Manual Update (For Template-Based Repositories)**
1. Add {{repo-name}} as a remote:
```bash
git remote add upstream https://github.com/alexanderholman/{{repo-name}}.git
git fetch upstream
```
2. Carefully merge specific files or changes as needed (note: this may conflict with your customizations):
```bash
git checkout upstream/main -- path/to/file
```

**Option 3: Fresh Start**
If you want to adopt all new changes, create a new repository from the updated template and migrate your customizations.
<!--  EXAMPLE END -->

## Removal and how-to uninstall
<!-- Step-by-step guide on how to remove the software -->
<!-- EXAMPLE START -->
If you created a repository from this template and want to remove it:

**On GitHub:**
1. Go to your repository Settings
2. Scroll to the bottom "Danger Zone" section
3. Click "Delete this repository"

**Locally:**
Simply remove the directory from your system:
```bash
rm -rf your-repository-name
```
<!--  EXAMPLE END -->