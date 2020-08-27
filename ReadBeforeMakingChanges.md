# Important Read Before Making Changes

This repository is meant to have a live development link to a GitHub repository.  This page is a reminder to make sure to NOT be on the master branch when making ANY changes to the repository.

**Working with Branches**

Follow these steps to see if other branches exist on the development machine and that the development branch (in this case it is coresetup) is selected before any changes are made.

```
git branch -a # list branches
git checkout -b coresetup # creates and checks out branch
# make changes to branch, add, commit
git checkout master # switch back to master
git merge coresetup --no-ff #merge changes to master branch
git push #push changes to github - a message may be required
git branch -d coresetup # delete branch OR
git checkout coresetup # keep dev branch open and switch back to it
```

It is optional to delete the development branch, but advised if ongoing development is not taking place.
