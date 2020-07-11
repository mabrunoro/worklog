# Worklog Computer

Computes daily spent time from a simple task preemption pattern.

Expected pattern should be something like:

```
# 18-06-20
07:52 -- DESCRIPTION 0 -- TASK 0
08:53 -- TASK 1
09:23 -- TASK 0
11:15 -- DESCRIPTION 1 -- TASK 2
12:01 -- lunch
14:29 -- DESCRIPTION 2 -- TASK 1
15:13 -- DESCRIPTION 3 -- TASK 0
15:28 -- DESCRIPTION 4 -- TASK 3
16:10 -- TASK 0
16:23 -- snack
17:15 -- TASK 3
18:59 -- DESCRIPTION 5 -- TASK 4
19:59 --
```

Markdown listing is also allowed:

```
# 19-06-20
- 08:55 -- DESCRIPTION 0 -- TASK 0
- 11:10 -- TASK 1
- 13:08 -- lunch
- 14:22 -- DESCRIPTION 2 -- TASK 0
- 16:39 -- TASK 3
- 16:54 -- DESCRIPTION 4 -- TASK 1
- 18:35 --
```
# TODO

## #1
Include a system to compute normal and extra hours. This means specifying globally how many hours until normal and perhaps daily normal hours for each project. For instance:

```
$ 8:00 (Globally, normal hours)

# Someday
$ HDM -- 6:00
```

Then if more than 6h is registered on someday, the exceeding hours can be deduced and shown in another way.

## #2
Split tasks related to multiple issues

## #3
Improve output to highlight days and tasks

## #4
Group same projects' tasks
