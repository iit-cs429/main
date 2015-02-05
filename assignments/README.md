To submit an assignment:

1. Create a new directory in your private repo (e.g., a1 for assignment1).

2. Copy the homework files from the main repository to your private repository (e.g., main/assignments/assignment1/*) 

2. Do the homework, adding and modifying files in the assignment directory. **Commit often!**

3. Before the deadline, push all of your changes to GitHub. E.g.:
  ```
  cd assignment 0
  git add *
  git commit -m 'homework completed'
  git push
  ```

4. Double-check that you don't have any outstanding changes to commit:
  ```
  git status
  # On branch master
  nothing to commit, working directory clean
  ```

5. Double-check that everything works, by cloning your repository into a new directory and executing all tests.
  ```
  cd 
  mkdir tmp
  cd tmp
  git clone https://github.com/iit-cs429/[your_iit_id]
  cd [your_iit_id]/assignments/assignment0
  [...run any relevant scripts/tests]
  ```
