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

### Level 1: Introduction

-    **Distributed**: everyone has a copy of the repo, not *centralised*.
-    Initial config:

        git config --global user.name "Asim Ihsan"
        git config --global user.email user@host.com
        git config --global color.ui true
        
-    Git workflow
    -    Create a file.
    -    Add file to staging area
    -    Commit changes.
    -    Modify file again.
    -    Add file to staging area.
    -    Commit changes.
    -    etc.

### Level 2: Staging and Remotes

-    To find unstaged differences since last commit, `git diff`.
-    Once you `git add` (stage) then `git diff` it won't show anything!
    -    `git diff --staged` to diff the staged files.
-    `git reset HEAD <file>` to unstage files.
-    `HEAD` is the last commit on the current branch / timeline that we're on.
-    `git checkout -- <filename>` to restore file to state at last commit.
-    `git commit -a -m "message"` to add changes from all tracked files; untracked files are ignored.

#### How to undo

-    Only do these command **before** you push.
-    `git reset --soft HEAD^` to undo last commit, put changes into staging. You will move to the previous commit.
-    `git commit --amend -m "modify"` to add our stage to the previous commit, and overwrite the previous commit message with a new one.
-    `git reset --hard HEAD^`: undo last commit and all changes will be lost. You will move to the previous commit.
-    `git reset --hard HEAD^^` undo the last two commits and all changes will be lost. You will move two commits back.

#### How to share

-    `git` doesn't do access control. If you need this use a hosted or self-managed solution.
-    Hosted:
    -    GitHub
    -    BitBucket
-    Self-Managed
    -    Gitosis
    -    Gitorious
    -    GitLab

-    `git remote add origin <url>`: add a remote called "origin" with a URL.
-    `git remote -v`: show remote repositories
-    `git push -u origin master`: push local branch called "master" to remote called "origin".
    -    You'll need to use [password caching](https://help.github.com/articles/set-up-git) if you don't want to type in password every time.
    -    `-u` stores this remote and branch as default.

-    `git pull`: pull changes down from the remote
-    Common to have multiple remotes
    -    origin
    -    test
    -    production
-    `git remote rm <name>` to remove remote

### Level 3: Cloning and Branching

#### Collaborating

-    Find e.g. GitHub URL, then `git clone <URL>`.
-    Or change name of clone directory, `git clone <URL> <name>`.

#### Branches

-    `git branch <branch_name>`: create a branch name, but don't switch to it.
-    `git checkout <branch_name>`: switch timelines to another branch.
-    Once you're done with a feature branch you want to merge it into the main master branch.
-    `git checkout master`.
-    `git merge <branch_name>`: merge another branch called "branch_name" into the current branch (master).
-    On merging it says it is "fast-forwarding". What does that mean?
    -    We've made changes to the feature branch without any interim changes on the master branch.
    -    It is very easy to merge: just "fast-forward".
-    Once you're done with a branch then delete it.
-    `git branch -d <branch_name>`: delete a branch.
-    `git checkout -b <branch_name>`: create then switch to a branch.
-    Complex merges can't use fast-forward, and git creates a new commit with a message.

### Level 4: Collaboration Basics

-    `git add --all` to add all tracked files to the stage.
-    Suppose you're working on a file locally, and someone pushes changes to it that you haven't pulled.
-    If you `git push` now, you'll get "rejected".
-    You could `git pull` then `git push`, and it'll work.
-    But what does `git pull` do?
    -    Fetch (or sync) our local repo with the remote one. This is the same as `git fetch`.
    -    But this doesn't update any local code! It actually fetches to `origin/master`.
    -    The second step is it merges `origin/master` with `master`. This is the same as `git merge origin/master`.
-    Hence `git pull` is actually:
    1.    `git fetch`.
    2.    `git merge origin/master`.
-    Some people think "merge commits" via `git pull` pollutes the log.
    -    `rebase` is one way to get around this.
    
#### Merge conflict

-    Suppose `git pull` hits a merge conflict?
-    `git status` will emphasise this.
-    Editing the file will reveal the commit, and then you'll manually need to fix it.
    -    First section are your changes, second section are their changes.
    -    Handily, these sections are labelled "HEAD" or "<commit hash>".
-    After resolving a conflict just `git commit -a` without a commit message because git will auto-fill a useful message mentioning the conflict for you.

### Level 5: Remote Branches and Tags

-    When you need other people to work on your branch.
-    Any branch that will last more than a day.
-    `git checkout -b <branch_name>`.
-    `git push <remote_name> <branch_name>`: push branch to remote.
    -    Don't need a `-u`; subsequent `push` will know that this is the current tracking branch.
-    A subsequent `git pull` will tell people about the new remote branch.
-    However, a `git branch` (list all local branches) won't reveal it.
-    `git branch -r` to list all remote branches.
-    `git remote show origin`: show all remotes, and whether their branches are tracked or not, and status of local branches wrt remote branches.
-    `git push <remote_name> :<branch_name>`: delete remote branch.
-    `git branch -d <branch_name>`: delete local branch.
    -    If any unmerged changes in branch git will default to preventing this.
-    `git branch -D <branch_name>`: delete local branch, ignoring unmerged changes.
-    What happens if you push and the remote branch doesn't exist any more?
    -    No easy error messages.
    -    You want to `git remote show <remote name>`
    -    git will say "stale" to indicate a local branch that no longer has corresponding remote branch.
-    `git remote prune <remote_name>`: clean up deleted remote branches.

#### Heroku

-    Heroku only deploys off of the master branch.
-    Hence if you push to some other branch, e.g. `git push heroku-staging staging`, it won't deploy.
-    `git push heroku-staging staging:master` will push to remote called 'heroku-staging' with `local:remote` branches.
    -    Push from staging to master.

#### Tags

-    A **tag** is a reference to a commit. Used for release versioning.
-    `git tag` to list all tags
-    `git checkout <tag_name>`: checkout code at commit.
-    `git tag -a <tag_name> -m "<description>"`: create a new tag with a tag description.
-    `git push --tags` to push local tags to remote.

-    Remember: only `git pull` if you want to do the second merge step. If all you want to do is update your knowledge of the remote you want to manually do the first step of `git fetch`.

### Level 6: Rebase Belong to Us

-    Merge commits are bad, pollute the log.
-    Instead of `git pull` then `git push`, we're going to do:
    -    `git fetch` (the first step of `git pull`, no merging).
    -    `git rebase`.
-    What does `git rebase` do?
    1.    Move all changes to `master` which are not in `origin/master` to a temporary area.
    2.    Run all `origin/master` commits onto `master`, one at a time.
    3.    Run all commits in the temporary area onto `master`, one at a time.

#### Work flow (before)

-    Work on branch.
-    `git checkout master`
-    `git merge <branch_name>`.

#### Work flow (rebase)

-    Work on branch.
-    `git rebase master`: run the master commits one at a time on the branch.
-    `git checkout master`
-    `git merge <branch_name>`: this will do a fast-forward.

#### Conflicts

-    `git fetch` to update our knowledge of the remote.
-    `git rebase`
-    But now we hit a conflict! You have options, because remember `rebase` runs commits one at a time.
    1.    Fix the conflict indicated, do a `git add <filename>`, then run `git rebase --continue` to continue the rebase.
    2.    Skip this patch, `git rebase --skip`.
    3.    Abort the rebasing, `git rebase --abort`.
-    During a rebase you will not be in a branch, so expect this during a `git status`.
   
#### Rebase vs merge

-    If the branch has been around for a long time, probably want a merge to track when you merged it with a log of what got changed.
-    If it's a short-lived feature rebase avoids the pollution of the logs.

### Level 7: History and Configuration

-    `git log` to view previous commits.
    -    SHA hash, author, date, message.
-    `git config --global color.ui true` to colourise the output.
-    `git log --pretty=online` for line-based log with `<hash> <commit message>` per line.
-    `git log --pretty=format:"%h %ad- %s [%an]"` for a customizable format for log.
-    `git log --oneline -p` will show patch-output for commits; what lines added/removed/modified.
-    `git log --oneline --stat` will show counts of lines added/removed/modified for each commit.
-    `git log --oneline --graph` for graph visualisation of the timelines.

#### Date Ranges

-    `git log --until=1.minute.ago` for until.
-    `git log --since=1.day.ago` for since in days.
-    `git log --since=1.hour.ago` for since in hours.
-    `git log --since=1.month.ago --until=2.weeks.ago` for since and until (relative).
-    `git log --sinace=2000-01-01 --until=2012-12-21` for since and until (absolute).

#### Diff

-    `git diff` for patch diff since last commit.
-    `git diff HEAD` is the same as `git diff`.
-    `git diff HEAD^^` goes two commits ago
-    `git diff HEAD~5` goes five commits ago.
-    `git diff HEAD^..HEAD` compares second most recent commit vs. most recent commit.

#### Earlier commits

-    `git diff <SHA1>..<SHA2>` to compare between range of SHAs.
    -    Can also use abbreviated SHAs, last 7 hex digits.
-    `git diff master bird`: diff branches
-    `git diff --since=1.week.ago --until=1.minute.ago`: time-based diff.

#### Blame

-    `git blame <filename> --date short`: figure out what commits, with date and author, changed what lines.

#### Excluding from local copy

-    Want to exclude from local repo, not from remote or from other people's locals.
-    Put patterns into `.git/info/exclude`.

#### Excluding from all copies

-    Use `.gitignore` to exclude patterns from all local repos and remote repo.

#### Removing files

-    `git rm <filename>` to remove.
-    Then `git commit`.

#### Untracking files

-    Sometims don't want to delete, just want to tell git `stop tracking this file`.
-    `git rm --cached <filename>` to stop tracking a file.
-    Afterwards `git status` will say it's been deleted but it won't be deleted from your file system, only from Git.

#### Config

-    `git config --global user.name "My name"`
-    `git config --global user.email "user@host.com"`
-    `git config --global core.editor emacs` to change editor
-    `git config --global merge.tool opendiff` to use a different diff tool.
-    Without the `--global` flag you can configure per-repo variables.
-    `git config --list` to see current config.

#### Aliases

-    `git config --global alias.mylog "log --pretty=format:'%h %s [%an]' --graph"` to create a log alias
-    `git config --global alias.lol "log --graph --decorate --pretty=oneline --abbrev-commit --all"` for a popular log output format.
-    To use then call `git mylog` or `git lol`.
-    Alias your frequent commands.

### Other commands I've found

-    `git revert HEAD`: revert changes introduced by a particular revert, add new commit to track this. Used when you want to revert pushed changes.

### References

-    [git-scm homepage](http://git-scm.com/)
    -    full book for free as well.
-    [github help page](https://help.github.com/)
-    [git immersion](http://gitimmersion.com)
    -    overview of git.
-    [git ready](http://gitready.com)
    -    Good reference.
-    [git from the bottom up](http://ftp.newartisans.com/pub/git.from.bottom.up.pdf)
    -    PDF of the technical internals of git.
-    [git internals PDF](https://peepcode.com/products/git-internals-pdf)
    -    More git internals
-    [git-flow blog post](http://nvie.com/posts/a-successful-git-branching-model/)
    -    Philosophy to git branching and merging and pushing.