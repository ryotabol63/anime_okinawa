from matplotlib import animation
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
ax2 = fig.add_subplot(121)
ax3 = fig.add_subplot(122)
#ax2.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
#ax3.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
#ax2.tick_params(bottom=False, left=False, right=False, top=False)
#ax3.tick_params(bottom=False, left=False, right=False, top=False)
ax2.axis("off")
ax3.axis("off")
ax.set_xlim(0,8)
ax.set_ylim(0,6)
ax2.set_xlim(0,10)
ax2.set_ylim(0,6)
ax3.set_xlim(0,10)
ax3.set_ylim(0,6)


def jointext(textlist):
    printtext = []
    isodd = True
    for text in textlist:
        if isodd:
            firsttext = text
            isodd = False
        else:
            addtext = firsttext + '  ' + text
            printtext.append(addtext)
            isodd = True
    if not isodd:
        printtext.append(firsttext + '      ')
    printtext_str = "\n".join(printtext)
    return printtext_str




# bboxの作成
boxdic = {
    "facecolor" : "lightgreen",
    "edgecolor" : "black",
    "boxstyle" : "Round",
    "linewidth" : 2
}
textlist = ['3JKU','IJKK','9KJI','9JHK','8JKJ', '9KJI']

textlist_str = jointext(textlist)
print(textlist_str)
    
textleft  = "hoge\nhoge"
textright = "hoge\nhoge"


ax.text(2, 5.5, "Left", size=40, bbox=boxdic, horizontalalignment="center", verticalalignment="center")
ax.text(6, 5.5, "Right", size=40, bbox=boxdic, horizontalalignment="center", verticalalignment="center")
ax.text(2, 5, textlist_str, size=30, horizontalalignment="center", verticalalignment="top", fontfamily = 'monospace')
ax.text(6, 5, "9HJI", size=30, horizontalalignment="center", verticalalignment="top")

ax.plot([0.2, 3.8], [5.5, 5.5],color="black")
ax.plot([0.2, 3.8], [0.2, 0.2],color="black")
ax.plot([0.2, 0.2], [0.2, 5.5],color="black")
ax.plot([3.8, 3.8], [0.2, 5.5],color="black")
ax.plot([4.2, 7.8], [5.5, 5.5],color="black")
ax.plot([4.2, 7.8], [0.2, 0.2],color="black")
ax.plot([4.2, 4.2], [0.2, 5.5],color="black")
ax.plot([7.8, 7.8], [0.2, 5.5],color="black")
plt.show()
