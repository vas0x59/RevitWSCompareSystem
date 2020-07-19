import json
import numpy as np


# def groupByLevels(objects, levels):
#     levels_dict_id_to_name = {}
#     for level in levels:
#         levels_dict_id_to_name[level["id"]] = level["name"]

def groupByLevels(bd_dict, objects_ids, levels_ids):
    group_dict = {}
    for obj_id in objects_ids:
        if bd_dict[obj_id]["level_id"] is not None:
            group_dict[bd_dict[obj_id]["level_id"]] = group_dict.get(bd_dict[obj_id]["level_id"], []) + [obj_id]
    return group_dict
def groupByLevelsName(bd_dict, objects_ids, levels_ids):
    group_dict = {}
    for obj_id in objects_ids:
        if bd_dict[obj_id]["level_id"] is not None:
            l_name = bd_dict[bd_dict[obj_id]["level_id"]]["name"]
            group_dict[l_name] = group_dict.get(l_name, []) + [obj_id]
    return group_dict

def reshapeToId(list_obj):
    id_dict = {}
    id_list = []
    for i in list_obj:
        # print(i)
        id_dict[i["id"]] = i
        id_list.append(i["id"])
    return id_dict, id_list



