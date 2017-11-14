
from tkinter import *
from tkinter import ttk

#画出spine
def spine(frm):
    bm = PhotoImage(file = 'images/spine.gif')
    label_1 = Label(frm,image=bm, text="Spine",compound='top',bitmap = 'error',font=('微软雅黑',15),fg='black')
    label_1.bm = bm
    label_1.pack(side=LEFT,padx=30,pady=20,anchor=NW)

#画出leaf
def leaf(frm):
    bm = PhotoImage(file = 'images/leaf.gif')
    label_1 = Label(frm,image = bm,text="Leaf",compound='top',bitmap = 'error',font=('微软雅黑',15),fg='black')
    label_1.bm = bm
    label_1.pack(side=LEFT,padx=30,pady=40,anchor=NW)


def main():
    top = Tk()
    top.title('闪断检测程序')
    top.geometry("1200x600")
    top.resizable(width=True, height=False)

    #摆放拓扑图spine
    frm_1 = Frame(top)
    for i in range(1,3):
        spine(frm_1)
    frm_1.pack(side=TOP)

    #摆放拓扑图leaf
    frm_2 = Frame(top)
    for i in range(1,5):
        leaf(frm_2)
    frm_2.pack(side=TOP,pady=40)

    #最下方放置表单
    frm_3 = Frame(top)
    bookList=[] 
    tree=ttk.Treeview(frm_3,height=20,columns=['Time','name','Drop','DropPrecent','Totdrop','Tottras','Totrecv'],show='headings')  
    tree.heading('Time',text='更新时间')  
    tree.heading('name',text='路径')  
    tree.heading('Drop',text='当前丢包数')  
    tree.heading('DropPrecent',text='当前丢包率')  
    tree.heading('Totdrop',text='总丢包数')
    tree.heading('Tottras',text='总发包数')
    tree.heading('Totrecv',text='总收包数')
    for item in range(1000):  
        tree.insert('',i)  
    tree.pack()  
    frm_3.pack()

    top.mainloop()

if __name__ == '__main__':  
    main()  