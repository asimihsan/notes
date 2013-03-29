# Git courses

## Try Git

Via Code School

### Init, status

-    `git init` to initialize a repo.
-    `git status` to see what the current state it.
    -    *staged*: ready to be committed.
    -    *unstaged*: changed files that have not been prepared to be committed.
    -    *untracked*: not tracked by Git.
    -    *deleted*: deleted, waiting to be removed by Git.
    
### Add, reset, log    
    
-    `git add <filepath>`: add to Git
    -    `git add .` to add all files in current directory and under it.
    -    `git add '*.txt'`: add all TXT files. (quotes are important: Git wants to add all files in subdirs too).
-    `git reset <filepath>`: remove from staging area.
-    **Staging area**: where we group files before we commit them to Git.
-    **Commit**: a snapshot of your repo.
-    `git log`: details of each commit.
    -    `git log --summary`: even more details of each commit.

### Add remote, push, pull to remote

-    Typical to call the main remote `origin`.
-    `git remote add origin git@github.com:asimihsan/try_git.git`: add a remote called `origin` with that URI.
-    `git push -u <remote_name> <branch_name>`: Push the local branch to that remote.
    -    `-u` means remember the parameters
    -    `git push -u origin master`: push the local `master` branch to the `origin` remote, whilst remembering the parameters.
-    See [Customizing Git - Git Hooks](http://git-scm.com/book/en/Customizing-Git-Git-Hooks) for how to do cool things every time you push, e.g. upload to webserver.
-    `git pull <remote_name> <branch_name>`: pull the remote into the local branch.
-    Sometimes when you want to pull you have changes you don't want to commit.
    -    `git stash` will stash your changes.
    -    `git stash apply` to re-apply the changes after the pull.
    
### Differences

-    `HEAD` is a pointer to the most recent commit.
-    `git diff <pointer>`: pointer is either SHA digest or some alias, e.g. `HEAD`.
-    Try to commit different files in unique commits.
-    `git diff --staged`: changes in your staged files (e.g. `add`-ed).

### Undo

-    `git checkout -- <target>`: change files to how they were at the last commit for the target.
    -    Using `--` because we're promising the command-line that there aren't any more parameters. Allows us to have a branch called `<target>`.
    
### Branching

-    `git branch <branch_name>`: create a local branch.
-    `git checkout <branch_name>`: switch to a branch.
-    `git checkout -b <branch_name>`: both create and switch to a new branch.
-    `git branch`: see all local branches.

### Removing

-    `git rm '-*.txt'`: remove all TXT files.
-    `git rm -r folder`: recursively remove all folders and files from `folder`.
-    If you accidentally delete a file before `git rm` it, you can do `git commit -a` to auto-remove deleted files with a commit.

### Merging, deleting branches

-    `git checkout <branch_name>`
-    Do stuff
-    `git checkout master`
-    `git merge <branch_name>`: merge another branch into the current branch.
-    `git branch -d <branch_name>`: delete branch
    -    By default can't delete a branch that hasn't been merged (there's a risk you're being a muppet!)
    -    `git branch -d --force <branch_name>` to force delete an unmerged branch.
    -    `git branch -D <branch_name>` for shortcut to force delete unmerged branch.
    
## Git Real

Via Code School