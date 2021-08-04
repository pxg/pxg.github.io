---
layout: til
title: "Today I learnt about tee"
date: 2021-08-04
---

Tee is a command line utility that will print output and save to a file. So rather than running the following:
```
date > date.txt
```
Where I can't see the outoput of the `date` command. I can now run the following and see the output and save to the file `date.txt`:
```
date | tee date.txt
Wed  4 Aug 2021 08:14:17 BST
```

Thanks to [Neil Reilly](https://www.linkedin.com/in/neilreilly/) for teaching me this when we were pairing.