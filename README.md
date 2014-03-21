2048player
==========

Selenium plays 2048 in Firefox.

How To
==========

Run from command line:

```bash
python play2048.py [GAME METHOD]
```

Current game methods:

* random (chooses directions at random)

* ordered (iterates up, right, down, left in order continuously)

* preferred (tries to move down if able, then right, then left, then up)
