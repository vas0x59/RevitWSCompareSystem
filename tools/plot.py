
import json
from utils import *
import numpy as np
import matplotlib.pyplot as plt

class SimpleBD:
    def __init__(self):
        self.dict = {}
        self.groups = {}

expert_json = json.load(open("../examples/000_SampleModel_2019_BIMAcademy.json", "r"))
test_json = json.load(open("../examples/000_SampleModel_2019_BIMAcademy_test.json", "r"))
# print(test_json)



bd_expert = SimpleBD()
bd_test = SimpleBD()

for el in ["doors", "windows", "grids", "levels", "families"]:
    el_d, el_l = reshapeToId(expert_json[el])
    bd_expert.groups[el] = el_l
    bd_expert.dict.update(el_d)

for el in ["doors", "windows", "grids", "levels", "families"]:
    el_d, el_l = reshapeToId(test_json[el])
    bd_test.groups[el] = el_l
    bd_test.dict.update(el_d)
# print(bd_expert.groups)

# print(groupByLevels(bd_expert.dict, bd_expert.groups["doors"], bd_expert.groups["levels"]))
# print(bd_expert.dict["13071"])

def getObjectPoints(bd_expert, bd_test, levels, obj_type):
    expert_doors_g_by_level = groupByLevelsName(bd_expert.dict, bd_expert.groups[obj_type], bd_expert.groups["levels"])
    test_doors_g_by_level = groupByLevelsName(bd_test.dict, bd_test.groups[obj_type], bd_test.groups["levels"])
    # print(expert_doors_g_by_level)
    # print(test_doors_g_by_level)
    d_out = {}
    for l_name in levels:
        expert_doors_ids = expert_doors_g_by_level[l_name]
        test_doors_ids = test_doors_g_by_level[l_name]

        # print(l_name, len(expert_doors_ids), len(test_doors_ids))
        expert_doors_points = [(door_id, np.array([bd_expert.dict[door_id]["location"]["x"], bd_expert.dict[door_id]["location"]["y"], bd_expert.dict[door_id]["location"]["z"]])) for door_id in expert_doors_ids]
        test_doors_points = [(door_id, np.array([bd_test.dict[door_id]["location"]["x"], bd_test.dict[door_id]["location"]["y"], bd_test.dict[door_id]["location"]["z"]])) for door_id in test_doors_ids]
        d_out[l_name] = (expert_doors_points, test_doors_points)
        # # print(expert_doors_points, test_doors_points)
        # for i in range(len(expert_doors_points)):
        #     plt.plot(expert_doors_points[i][0], expert_doors_points[i][1], marker = 'o', color=(1, 0, 0))
        # for i in range(len(test_doors_points)):
        #     plt.plot(test_doors_points[i][0], test_doors_points[i][1], marker = 'o', color=(0, 0, 1))
        # plt.show()
    return d_out

# print(c_doors_points)
# for pnt in c_doors_points["L1"][0]:
#     plt.plot(pnt[1][0], pnt[1][1], marker = 'o', color=(1, 0, 0))
# for pnt in c_doors_points["L1"][1]:
#     plt.plot(pnt[1][0], pnt[1][1], marker = 'o', color=(0, 0, 1))
# plt.show()


def dist(pnt1, pnt2):
    return ((pnt1[0] - pnt2[0])**2 + (pnt1[1] - pnt2[1])**2 + (pnt1[2] - pnt2[2])**2)**0.5
def comparePoints(bd_expert, bd_test, expert_objs, test_objs):
        report_str = "points compare:\n"
        for obj in expert_objs:
            # report_str += "  :" + str(bd_expert[obj[0]]["name"]) + 
            report_str += "  {}({}) ".format(str(bd_expert.dict[str(obj[0])]["name"]), obj[0])
            report_str += " -> "
            nearst = sorted(test_objs, key=lambda x:dist(obj[1], x[1]))
            if len(nearst) == 0 or dist(obj[1], nearst[0][1]) > 1.5:
                report_str += " NOT FOUND"
            else:
                obj2 = nearst[0]
                # print(bd_test.dict[str(obj2[0])]["name"])
                report_str += " {}({}) dist:{}".format(bd_test.dict[str(obj2[0])]["name"], str(obj2[0]), dist(obj[1], obj2[1]))
            report_str += "\n"
        return report_str

levels_to_test = ["B1", "L1", "L2"]
c_doors_points = getObjectPoints(bd_expert, bd_test, levels_to_test, "doors")
for level in  levels_to_test:   
    # print()
    report_str = "Level: {}   expert_count:{}     test_count:{}\n".format(level, len(c_doors_points[level][0]), len(c_doors_points[level][1]))
    report_str += comparePoints(bd_expert, bd_test, c_doors_points[level][0], c_doors_points[level][1])
    print(report_str)

