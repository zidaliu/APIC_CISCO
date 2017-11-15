# -*- coding: UTF-8 -*-
from Tkinter import *
import ttk
import requests

requests.packages.urllib3.disable_warnings()
import cobra.mit.access
import cobra.mit.access as mo
import cobra.mit.session as session
import cobra.mit.request
import cobra.mit.session
from tabulate import tabulate
import time
import requests.packages.urllib3


# 画出spine
def spine(frm):
    bm = PhotoImage(file='images/spine.gif')
    label_1 = Label(frm, image=bm, text="Spine", compound='top', bitmap='error', font=('微软雅黑', 15), fg='black',
                    bg="orange")
    label_1.bm = bm
    label_1.pack(side=LEFT, padx=30, pady=20, anchor=NW)


# 画出leaf
def leaf(frm):
    bm = PhotoImage(file='images/leaf.gif')
    label_1 = Label(frm, image=bm, text="Leaf", compound='top', bitmap='error', font=('微软雅黑', 15), fg='black',
                    bg="orange")
    label_1.bm = bm
    label_1.pack(side=LEFT, padx=30, pady=40, anchor=NW)


# 画出表单
def formlist(frm):
    frm_3 = Frame(frm)
    bookList = []
    tree = ttk.Treeview(frm_3, height=20,
                        columns=['Time', 'name', 'Drop', 'DropPrecent', 'Totdrop', 'Tottras', 'Totrecv'],
                        show='headings')
    tree.heading('Time', text='更新时间')
    tree.heading('name', text='路径')
    tree.heading('Drop', text='当前丢包数')
    tree.heading('DropPrecent', text='当前丢包率')
    tree.heading('Totdrop', text='总丢包数')
    tree.heading('Tottras', text='总发包数')
    tree.heading('Totrecv', text='总收包数')
    for item in range(1000):
        tree.insert('', item)
    tree.pack()
    frm_3.pack()

#画出特定链接
def draw_line(canvas, trail):
    for item in trail:
        spine_item = canvas.find_withtag(item[6:9]+'a')
        leaf1_item = canvas.find_withtag(item[10:13]+'a')
        leaf2_item = canvas.find_withtag(item[14:17]+'a')
        canvas.create_line(canvas.coords(spine_item)[0], canvas.coords(spine_item)[1], canvas.coords(leaf1_item)[0],
                           canvas.coords(leaf1_item)[1], fill='red')
        canvas.create_line(canvas.coords(spine_item)[0], canvas.coords(spine_item)[1], canvas.coords(leaf2_item)[0],
                           canvas.coords(leaf2_item)[1], fill='red')


def canvas(frm, spine, leaf, spine_list, leaf_list, trail_list):

    canvas = Canvas(frm, width=1200, height=350, bg='yellow')
    for i in range(1, len(spine_list)+1):
        canvas.create_image(300 + i * 150, 50, image=spine, tags=spine_list[i-2]+'a')
        canvas.create_text(300 + i * 150, 50 + 30, text=spine_list[i-2], font=('微软雅黑', 20))
        # print canvas.find_withtag('201a')

    for j in range(1, len(leaf_list)+1):
        canvas.create_image(j * 250, 200, image=leaf, tags=leaf_list[j-2]+'a')
        canvas.create_text(j * 250, 200 + 60, text=leaf_list[j-2], font=('微软雅黑', 20))

    draw_line(canvas, trail_list)
    canvas.pack()

def main():
    mo = cobra.mit.access
    apicurl = 'http://10.124.4.101'
    mo_dir = mo.MoDirectory(session.LoginSession(apicurl, 'admin', 'Cisco123'))
    mo_dir.login()
    clAcPath = cobra.mit.access.ClassQuery('fabricTrail')
    dbgAcPathA_objlist = mo_dir.query(clAcPath)
    dbgAclist_spine = []
    dbgAclist_leaf = []
    dbgAclist_trail = []

    for m in dbgAcPathA_objlist:
        dbgAclist_leaf.append(str(m.n1))
        dbgAclist_spine.append(str(m.transit))
        dbgAclist_trail.append(str(m.rn))
    print dbgAclist_trail


    dbgAclist_spine = list(set(dbgAclist_spine))
    dbgAclist_leaf = list(set(dbgAclist_leaf))



    top = Tk()
    top.title('闪断检测程序')
    top.geometry("1200x600")
    top.resizable(width=True, height=False)
    spine = PhotoImage(file='images/spine.gif')
    leaf = PhotoImage(file='images/leaf.gif')
    canvas(top, spine, leaf,dbgAclist_spine,dbgAclist_leaf,dbgAclist_trail)
    formlist(top)
    top.mainloop()

    return


if __name__ == '__main__':
    main()  