txt = "I like bananas"

ex = [ " a n o t h e r _ r a n d o m . j p g " , " I M G _ 5 6 3 5 . p n g " , " I M G _ 5 9 1 0 . p n g " ]

for i in range(0, len(ex)):
    ex[i] = ex[i].replace(" ", "")
print(type(ex))

