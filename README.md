# batch-png-lsbhiding

Batch png lsbhiding. Can be used to generate data set

## lsbhide.py

Install stegano
`pip3 install stegano`

Change the `target_dir`. It refers to the directory containing cover images.
`hide_len` is the range of random ascii string's length.
`secret.save("")`is the path of result. The directory should be made before running if it is not existed.

Run
`python3 lsbhide.py`

It implements batch png lsbhiding via stegano, the hide_msg are ascii strings which are randomly generated.

## bitStream

```bash
pip3 install --upgrade pip #pip3 >= 19.3
pip3 install opencv-python
```

The embedding rate is around(lower than) 80%. It can be changed by `s`.
Change `cv.imwrite('',imgStego)` to path of your results. The directory should be made before running if it is not existed.
Change `target_dir` to the directory containing cover images.

Run
`python3 lsbhide_bin.py`

It implements batch png lsbhiding by generating a random bit stream of certain length.
The length of the bit stream depends on the embedding rate you want.
It also normalizes the bit stream and gets the positions to embed randomly.

