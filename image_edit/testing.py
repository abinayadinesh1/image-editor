txt = "I like bananas"

ex = [ " a n o t h e r _ r a n d o m . j p g " , " I M G _ 5 6 3 5 . p n g " , " I M G _ 5 9 1 0 . p n g " ]

for i in range(0, len(ex)):
    ex[i] = ex[i].replace(" ", "")
print(type(ex))





def update_image_list(self):
    storedList = localStorage.getItem("images")
    try:
        res = storedList.strip('][').split(', ')
        newItem = res[-1]
        newItem = newItem.replace('"', '')
        self.img = newItem

        for item in self.imgs:
            print(item)
            if item == newItem:
                return
        self.imgs.append(newItem)
    except:
        print("nothing in local storage")