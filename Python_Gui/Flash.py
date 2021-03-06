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
from tkMessageBox import *


class apic:

    def __init__(self):
        self.top = Tk()
        self.top.title('闪断检测程序')
        self.top.geometry("1200x1000")
        self.top.resizable(width=True, height=False)

        self.client_input(self.top)
        self.top.mainloop()

#输入信息后才开始执行函数：
    def excution(self,frm,leaf_1,leaf_2):
        self.spine = PhotoImage(file='images/spine.gif')
        self.leaf = PhotoImage(file='images/leaf.gif')
        [self.dbgAclist_spine, self.dbgAclist_leaf, self.dbgAclist_trail] = self.connect(frm,leaf_1, leaf_2)
        self.canvas(frm, self.spine, self.leaf, self.dbgAclist_spine, self.dbgAclist_leaf, self.dbgAclist_trail)
        self.formlist(frm,leaf_1,leaf_2)


#用户输入信息的函数
    def client_input(self,frm):
        frm_1 = Frame(frm)
        l_user_1 = Label(frm_1, text='叶子节点1：')
        l_user_1.pack(side = LEFT)
        e_user_1 = Entry(frm_1)
        e_user_1.pack(side = LEFT)
        l_user_2 = Label(frm_1, text='叶子节点2：')
        l_user_2.pack(side=LEFT)
        e_user_2 = Entry(frm_1)
        e_user_2.pack(side = LEFT)
        b_login = Button(frm_1, text='查询',command=lambda :self.excution(frm,e_user_1.get(),e_user_2.get()))
        b_login.pack(side=LEFT)

        frm_1.pack()


    # 连接远程端获取服务
    def connect(self,frm,leaf_1,leaf_2):
        flag = 0
        self.mo = cobra.mit.access
        apicurl = 'http://10.124.4.101'
        self.mo_dir = mo.MoDirectory(session.LoginSession(apicurl, 'admin', 'Cisco123'))
        self.mo_dir.login()

        self.clAcPath = cobra.mit.access.ClassQuery('fabricTrail')
        self.dbgAcPathA_objlist = self.mo_dir.query(self.clAcPath)
        self.dbgAclist_spine = []
        self.dbgAclist_leaf = []
        self.dbgAclist_trail = []

        for m in self.dbgAcPathA_objlist:
            # 根据用户选定特定的leaf的值
            if leaf_1 in str(m.rn) and leaf_2 in str(m.rn):
                self.dbgAclist_leaf.append(str(m.n1))
                self.dbgAclist_spine.append(str(m.transit))
                self.dbgAclist_trail.append(str(m.rn))
            else:
                flag += 1
        """当flag和长度相等时,说明没有找到对应路径"""
        if flag != len(self.dbgAcPathA_objlist):
            self.dbgAclist_spine = list(set(self.dbgAclist_spine))
            """数组中重复的去除,如201-102只能画一次"""
            self.dbgAclist_leaf = list(set(self.dbgAclist_leaf))
            return self.dbgAclist_spine, self.dbgAclist_leaf, self.dbgAclist_trail
        else:
            showerror("Answer", "Sorry, there is no trail bwtween the two leafs!")



    # 调用方法获取表格内容插入
    def get_tree(self,leaf_1,leaf_2):
        # 删除原节点
        # for _ in map(self.tree.delete, self.tree.get_children("")):
        #     pass

        # 更新插入新节点
        clAcPath = cobra.mit.access.ClassQuery('dbgAcTrail')
        dbgAcPathA_objlist = self.mo_dir.query(clAcPath)

        now = datetime.datetime.now()

        """objlist[0]代表第几条path"""
        if leaf_1 in str(dbgAcPathA_objlist[0].dn) and leaf_2 in str(dbgAcPathA_objlist[0].dn):
            self.tree.insert("", "end",
                             values=(now.strftime('%Y-%m-%d %H:%M:%S'), dbgAcPathA_objlist[0].dn, dbgAcPathA_objlist[0].
                                     dropPkt, dbgAcPathA_objlist[0].dropPktPercentage, dbgAcPathA_objlist[0].totDropPkt,
                                     dbgAcPathA_objlist[0].totRxPkt, dbgAcPathA_objlist[0].totTxPkt))


        self.tree.after(2000,lambda :self.get_tree(leaf_1,leaf_2))


    # 画出表单
    def formlist(self,frm,leaf_1,leaf_2):

        frm_3 = Frame(frm)
        self.vbar = ttk.Scrollbar(frm_3, orient=VERTICAL)
        self.tree = ttk.Treeview(frm_3, height=20,
                            columns=['Time', 'name', 'Drop', 'DropPrecent', 'Totdrop', 'Tottras', 'Totrecv'],
                            show='headings',yscrollcommand = self.vbar.set)
        self.vbar.config(command=self.tree.yview)
        self.vbar.pack(side = LEFT, fill = Y )
        self.tree.heading('Time', text='更新时间')
        self.tree.heading('name', text='路径')
        self.tree.heading('Drop', text='当前丢包数')
        self.tree.heading('DropPrecent', text='当前丢包率')
        self.tree.heading('Totdrop', text='总丢包数')
        self.tree.heading('Tottras', text='总发包数')
        self.tree.heading('Totrecv', text='总收包数')

        self.get_tree(leaf_1,leaf_2)
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
            canvas.create_image(600/len(spine_list)+(i-1)*1200/len(spine_list), 50, image=spine, tags=spine_list[i - 2] + 'a')
            canvas.create_text(600/len(spine_list)+(i-1)*1200/len(spine_list), 50 + 30, text=spine_list[i - 2], font=('微软雅黑', 20))

        for j in range(1, len(leaf_list) + 1):
            canvas.create_image(600/len(leaf_list)+(j-1)*1200/len(leaf_list), 200, image=leaf, tags=leaf_list[j - 2] + 'a')
            canvas.create_text(600/len(leaf_list)+(j-1)*1200/len(leaf_list), 200 + 60, text=leaf_list[j - 2], font=('微软雅黑', 20))

        self.draw_line(canvas, trail_list)
        canvas.pack()



if __name__ == '__main__':
    apic()