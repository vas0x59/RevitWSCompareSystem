"""export json"""
import json
doc = __revit__.ActiveUIDocument.Document
from Autodesk.Revit import DB
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import Transaction

all_fams = DB.FilteredElementCollector(doc)\
             .OfClass(DB.Family)\
             .ToElements()
families_to_json = []
for fam in all_fams:
    obj_dict = {}
    if fam.IsEditable:
        fam_doc = doc.EditFamily(fam)
        obj_dict["fam_path"] = fam_doc.PathName.ToString()
    obj_dict["fam_creator"] = \
        DB.WorksharingUtils.GetWorksharingTooltipInfo(doc,
                                                        fam.Id).Creator.ToString()
    obj_dict["category_name"] = fam.FamilyCategory.Name.ToString()
    obj_dict["name"] = fam.Name.ToString()
    obj_dict["id"] = fam.Id.ToString()
    families_to_json.append(obj_dict)


doors = Fec(doc).OfCategory(Bic.OST_Doors).WhereElementIsNotElementType().ToElements()
windows = Fec(doc).OfCategory(Bic.OST_Windows).WhereElementIsNotElementType().ToElements()
levels = Fec(doc).OfCategory(Bic.OST_Levels).WhereElementIsNotElementType().ToElements()
grids = Fec(doc).OfCategory(Bic.OST_Grids).WhereElementIsNotElementType().ToElements()

levels_to_json = []

for level in levels:
    level_dict = {"id":level.Id.ToString(), "name":level.Name.ToString(), "elevation":level.Elevation}
    levels_to_json.append(level_dict)

grids_to_json = []

for grid in grids:
    obj_dict = {}
    obj_dict["name"] = grid.Name
    obj_dict["id"] = grid.Id.ToString()
    obj_dict["origin"] = {"x":grid.Curve.Origin[0], "y":grid.Curve.Origin[1], "z":grid.Curve.Origin[2]}
    obj_dict["direction"] = {"x":grid.Curve.Direction[0], "y":grid.Curve.Direction[1], "z":grid.Curve.Direction[2]}
    grids_to_json.append(obj_dict)

doors_to_json = []

for door in doors:
    obj_dict = {}
    x = door.Location.Point[0]
    y = door.Location.Point[1]
    z = door.Location.Point[2]
    obj_dict["location"] = {"x":x, "y":y, "z":z}
    obj_dict["name"] = door.Name.ToString()
    obj_dict["id"] = door.Id.ToString()
    obj_dict["level_id"] = door.LevelId.ToString()
    obj_dict["type_id"] = door.GetTypeId().ToString()
    obj_dict["family_id"] = door.Symbol.Family.Id.ToString()
    obj_dict["family_name"] = door.Symbol.FamilyName.ToString()
    doors_to_json.append(obj_dict)

windows_to_json = []

for window in windows:
    obj_dict = {}
    x = window.Location.Point[0]
    y = window.Location.Point[1]
    z = window.Location.Point[2]
    obj_dict["location"] = {"x":x, "y":y, "z":z}
    obj_dict["name"] = window.Name.ToString()
    obj_dict["id"] = window.Id.ToString()
    obj_dict["level_id"] = window.LevelId.ToString()
    obj_dict["type_id"] = window.GetTypeId().ToString()
    obj_dict["family_id"] = door.Symbol.Family.Id.ToString()
    obj_dict["family_name"] = door.Symbol.FamilyName.ToString()
    windows_to_json.append(obj_dict)

splited_path = str(doc.PathName).split('\\')

doc_to_json = {"families":families_to_json, "grids":grids_to_json, "doc_filename":splited_path[-1], "levels":levels_to_json, "doors":doors_to_json, "windows":windows_to_json}
json_path = "/".join(splited_path[:-1]) + "/" + splited_path[-1].split(".")[0] + ".json"
# print(json_path)
# print(json.dumps(doc_to_json))

file_to = open(json_path, "w+")
# file_to.write(json.dumps(doc_to_json))
json.dump(doc_to_json, file_to)

