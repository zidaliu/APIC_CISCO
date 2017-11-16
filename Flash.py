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
import datetime


class apic:

    def __init__(self):
        self.mo = cobra.mit.access
        apicurl = 'http://10.124.4.101'
        self.mo_dir = mo.MoDirectory(session.LoginSession(apicurl, 'admin', 'Cisco123'))
        self.mo_dir.login()

        self.clAcPath = cobra.mit.access.ClassQuery('fabricTrail')
        self.dbgAcPathA_objlist = self.mo_dir.query(self.clAcPath)
        self.dbgAclist_spine = []
        self. dbgAclist_leaf = []
        self. dbgAclist_trail = []

        for m in self.dbgAcPathA_objlist:
            self.dbgAclist_leaf.append(str(m.n1))
            self.dbgAclist_spine.append(str(m.transit))
            self.dbgAclist_trail.append(str(m.rn))

        self.dbgAclist_spine = list(set(self.dbgAclist_spine))
        self.dbgAclist_leaf = list(set(self.dbgAclist_leaf))

        self.top = Tk()
        self.top.title('闪断检测程序')
        self.top.geometry("1200x600")
        self.top.resizable(width=True, height=False)
        self.spine = PhotoImage(file='images/spine.gif')
        self.leaf = PhotoImage(file='images/leaf.gif')
        self.canvas(self.top, self.spine, self.leaf, self.dbgAclist_spine, self.dbgAclist_leaf, self.dbgAclist_trail)
        self.formlist(self.top, self.mo_dir)
        self.top.mainloop()

    # 调用方法获取表格内容插入
    def get_tree(self):
        # 删除原节点
        # for _ in map(self.tree.delete, self.tree.get_children("")):
        #     pass

        # 更新插入新节点
        now = datetime.datetime.now()
        self.tree.insert("", "end", values=(now.strftime('%Y-%m-%d %H:%M:%S'),1,1,1,1,1,1))
        self.tree.after(2000, self.get_tree)

    # 画出表单
    def formlist(self, frm, mo):

        clAcPath = cobra.mit.access.ClassQuery('dbgAcTrail')
        dbgAcPathA_objlist = mo.query(clAcPath)

        frm_3 = Frame(frm)
        self.tree = ttk.Treeview(frm_3, height=20,
                            columns=['Time', 'name', 'Drop', 'DropPrecent', 'Totdrop', 'Tottras', 'Totrecv'],
                            show='headings')
        self.tree.heading('Time', text='更新时间')
        self.tree.heading('name', text='路径')
        self.tree.heading('Drop', text='当前丢包数')
        self.tree.heading('DropPrecent', text='当前丢包率')
        self.tree.heading('Totdrop', text='总丢包数')
        self.tree.heading('Tottras', text='总发包数')
        self.tree.heading('Totrecv', text='总收包数')

        self.get_tree()

        # for item in range(1, 11):
        #     now = datetime.datetime.now()
        #     tree.insert('', item,
        #                 values=(now.strftime('%Y-%m-%d %H:%M:%S'), dbgAcPathA_objlist[0].rn, dbgAcPathA_objlist[0].
        #                         dropPkt, dbgAcPathA_objlist[0].dropPktPercentage, dbgAcPathA_objlist[0].totDropPkt,
        #                         dbgAcPathA_objlist[0].totRxPkt, dbgAcPathA_objlist[0].totTxPkt))

        self.tree.pack()
        frm_3.pack()

    # 画出特定链接
    def draw_line(self, canvas, trail):
        for item in trail:
            spine_item = canvas.find_withtag(item[6:9] + 'a')
            leaf1_item = canvas.find_withtag(item[10:13] + 'a')
            leaf2_item = canvas.find_withtag(item[14:17] + 'a')
            canvas.create_line(canvas.coords(spine_item)[0], canvas.coords(spine_item)[1], canvas.coords(leaf1_item)[0],
                               canvas.coords(leaf1_item)[1], fill='red')
            canvas.create_line(canvas.coords(spine_item)[0], canvas.coords(spine_item)[1], canvas.coords(leaf2_item)[0],
                               canvas.coords(leaf2_item)[1], fill='red')

    #构建画布，画出拓扑图
    def canvas(self,frm, spine, leaf, spine_list, leaf_list, trail_list):
        canvas = Canvas(frm, width=1200, height=350, bg='yellow')

        for i in range(1, len(spine_list) + 1):
            canvas.create_image(300 + i * 150, 50, image=spine, tags=spine_list[i - 2] + 'a')
            canvas.create_text(300 + i * 150, 50 + 30, text=spine_list[i - 2], font=('微软雅黑', 20))

        for j in range(1, len(leaf_list) + 1):
            canvas.create_image(j * 250, 200, image=leaf, tags=leaf_list[j - 2] + 'a')
            canvas.create_text(j * 250, 200 + 60, text=leaf_list[j - 2], font=('微软雅黑', 20))

        self.draw_line(canvas, trail_list)
        canvas.pack()



if __name__ == '__main__':
    apic()