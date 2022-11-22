import os

files = [f for f in os.listdir() if os.path.isfile(f) and not f.endswith('.py')]

def findBoneMarkupList(i):
    try:
        print([idx for idx, s in enumerate(i) if '_class = "PhysicsShapeList"' in s][0])
        print("Found existing physics in file. Ignoring this file.")
        return -1
    except:
        return [idx for idx, s in enumerate(i) if 'bone_cull_type = "None"' in s][0]
    

def findKeyData(i):
    return i[[idx for idx, s in enumerate(i) if "filename =" in s][0]], i[[idx for idx, s in enumerate(i) if "name =" in s][0]]
           
def findEndString(i):
    return [idx for idx, s in enumerate(i) if '\t\tmodel_archetype = ""' in s][0]

for file in files:
    tempFile = open(file).read().split("\n")
    outFile = ""
    tab = (' ' * 4)
    boneMarkup = findBoneMarkupList(tempFile)
    if boneMarkup != -1:
        keyData = findKeyData(tempFile)
        kd1_noTab = keyData[1].replace('\t', '')
        kd2_noTab = keyData[0].replace('\t', '')
        physicsAddition = """
                    {
                            _class = "PhysicsShapeList"
                            children = 
                            [
                                    {
"""
        physicsAddition += f"""
                                            _class = "PhysicsMeshFile"
                                            {kd1_noTab}
                                            parent_bone = ""
                                            surface_prop = "default"
                                            collision_prop = "default"
                                            recenter_on_parent_bone = false
                                            offset_origin = [ 0.0, 0.0, 0.0 ]
                                            offset_angles = [ 0.0, 0.0, 0.0 ]
                                            {kd2_noTab}"""
        physicsAddition += """
                                            import_scale = 1.0
                                            maxMeshVertices = 0
                                            qemError = 0.0
                                            import_filter = 
                                            {
                                                    exclude_by_default = false
                                                    exception_list = [  ]
                                            }
                                    },
                            ]
                    },
"""
        endSplice = "\n".join(tempFile[(findEndString(tempFile)-1):])
        startSplice = "\n".join(tempFile[:(findBoneMarkupList(tempFile)+2)])+","
        outFile = "\n".join([startSplice, physicsAddition, endSplice])
        with open(f"{file.split('.')[0]}.vmdl", "w+") as f:
            f.write(outFile)
