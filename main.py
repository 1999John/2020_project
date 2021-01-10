from LR.SLR import build_SLR,build_DFA
from LR.util import *
from LR.project import Project
import numpy as np
from DataStruct.MyList import MyList
if __name__ == '__main__':
    action_di,goto_di = get_di()
    stack = [0]
    inp = input("input language:")
    inp = parse_inp(inp)
    ori_project = get_ori_project()
    build_project = Project(ori_project.products,True)
    build_DFA([build_project])
    analysis_table = build_SLR(True)
    print(action_di,goto_di)
    for item in analysis_table.items():
        print(item)
    # an_1 = build_SLR(ori_project)
    # an_2 = build_SLR()
    # print(an_1)
    # print(an_2)
    # exit(0)
    while True:
        cur_state = stack[-1]
        ter = inp[0]
        ind = get_action_position(ter)
        cont = analysis_table[cur_state]["action"][ind]
        if cont is np.nan:
            print("error")
            exit(1)
        elif cont == "acc":
            print("answer: ",stack[-2].val)
            print(stack[-2].val.name)
            print("0 error,0 warning")
            exit(0)
        elif cont >= 0:
            print("移进")
            inp = inp[1:]
            stack.append(ter)
            stack.append(cont)
            ter = inp[0]
            cur_state = stack[-1]
        elif cont < 0:
            cont = 0 - cont-1
            p = ori_project.products[cont]
            print("按照" + str(p) + "规约")
            poplist = MyList()
            for _ in range((len(p.right)-1) * 2):
                poplist.append(stack.pop())
            non_ter = compute(p,poplist)
            cur_state = stack[-1]
            stack.append(non_ter)
            goto_ind = get_goto_position(p.left)
            goto_state = analysis_table[cur_state]["goto"][goto_ind]
            if goto_state is np.nan:
                print("error")
                exit(1)
            else:
                stack.append(goto_state)
                cur_state = goto_state
