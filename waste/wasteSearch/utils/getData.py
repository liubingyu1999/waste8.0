from wasteSearch.models import WasteInfo
from django.apps import apps
import sys
import re
import random
from django.db.models import Q


# 无用数据项
useless_label= ["数据来源","_state","dataId","序号"]
# 文本描述型(唯一值)
text_label = ["行业分类","废物类别","固废名称","产生工段","物理形态","废物描述"]

text_label_mutiple = ["形状","表观形貌","颜色","气味","表观形貌稍微详细","物质组成特性","特征指标","磁性",
            "表观形貌(稍微详细)", "物理形态(固态、半固态、液态)", "形状(块状、颗粒状、泥状、水状、粘稠状等)", 
            "表观形貌(球状、板状、粗糙、光滑、团聚、分散)", "容重"]

# 依据名称搜索相关的类
def searchByName(name):
    if name:
        queryset = WasteInfo.objects.filter(固废名称__icontains = name[0])
        for item in name:
            queryset_tmp = WasteInfo.objects.filter(固废名称__icontains = item)
            queryset = queryset & queryset_tmp

    else:
        queryset = WasteInfo.objects.all()
    return queryset

# 对初始数据进行统计，获得每一类的数据范围
def statistic(queryset):
    name2verboseName={}
    fields = apps.get_model('wasteSearch.WasteInfo')._meta.fields
    for item in fields:
        name2verboseName[item.name] = item.verbose_name
    
    res_dict = []
    for obj in queryset:
        name = obj.固废名称
        flag = True
        obj_dict = obj.__dict__
        for dict_item in res_dict:
            if dict_item["固废名称"] == name:
                flag = False
                index = res_dict.index(dict_item)
                for item in obj_dict:
                    if item in useless_label:
                        continue
                    else :
                        if obj_dict[item]:
                            if item not in res_dict[index]:
                                if item in text_label:
                                    res_dict[index][item] = obj_dict[item]
                                else:
                                    res_dict[index][item] = [obj_dict[item]]
                            else:
                                if item not in text_label:
                                    res_dict[index][item].append(obj_dict[item])
                break
        
        if flag:
            res_dict.append({"固废名称": name})
            index = res_dict.index({"固废名称": name})
            
            for item in obj_dict:
                if item in useless_label:
                    continue
                if obj_dict[item] not in (None, " "):
                    if item in text_label:
                        res_dict[index][item] = obj_dict[item]
                    else:
                        res_dict[index][item] = [obj_dict[item]]

    for dict in res_dict:
        for item in dict:
            if item not in text_label: 
                # 统一标签下数据去重
                dict[item] = list(set(dict[item]))
                # 文本型，将列表转换为字符串
                if item in text_label_mutiple:
                    tmp = ''
                    if len(dict[item]) == 1:
                        dict[item] = dict[item][0]
                    else:
                        for data in dict[item]:
                            tmp += data
                            tmp += ';'
                        dict[item] = tmp[:-1]
                # 数值型统计最值
                else:
                    range = ''
                    minnum = sys.float_info.max
                    maxnum = -1
                    for value in dict[item]:
                        value = value.replace(" ", "").replace("<", "").replace("ND", "")
                        if value == '-':
                            continue
                        if not value:
                            continue
                        # 数值中带有特殊字符需要特殊处理

                        if ('~' in value) | ('-' in value):
                            x1, x2 = re.split('~|-', value)
                            if float(x1) < float(minnum):
                                minnum = x1
                            if float(x2) > float(maxnum):
                                maxnum = x2
                            continue
                        
                        if float(value) < float(minnum):
                            minnum = value
                        if float(value) > float(maxnum):
                            maxnum = value
                    if minnum == maxnum:
                        range = minnum
                    else:
                        range = minnum + "~" + maxnum
                    dict[item] = range
    num = 1                
    for dict in res_dict:
        dict['dataId'] = 1000 + num
        WasteInfo.objects.create(**dict)
        num += 1

# 构造雷达图所需数据  暂时不需要雷达图
def buildDetailsInfo_radar(name, group):
    verboseName2name = verbosename2name()
    obj = WasteInfo.objects.filter(固废名称=name).last()
    obj_dict = obj.__dict__ 
    group_info_max={}
    group_info_min={}

    for item in group:
        modelName = verboseName2name[item]
        if (obj_dict[modelName] != None) & (obj_dict[modelName] != '0'):
                if '~' in obj_dict[modelName]:
                    s, l = obj_dict[modelName].split('~', 1)
                    group_info_min[item] = s
                    group_info_max[item] = l
                else:
                    group_info_min[item] = obj_dict[modelName]
                    group_info_max[item] = obj_dict[modelName]


    group_max =sorted(group_info_max.items(), key=lambda x:x[1],reverse=True)
    group_indicator = []
    group_min = []
    for item in group_max:
        group_indicator.append({'name':item[0], 'max':float(item[1]) * 1.1})
        group_min.append((item[0], group_info_min[item[0]]))
    # print("group_indicator: ", group_indicator)
    # print("group_max: ", group_max)
    # print("group_min: ", group_min)
    return group_indicator, group_max, group_min

# 构造柱状图数据
def buildDetailsInfo_bar(name, group):
    verboseName2name = verbosename2name()
    obj = WasteInfo.objects.filter(固废名称=name).last()
    obj_dict = obj.__dict__

    group_info_max={}
    group_info_min={}
    #print("group",group)
    #print("verboseName2name", verboseName2name)
    for item in group:
        #print("item", item)
        #print("modelName", verboseName2name[item])
        modelName = verboseName2name[item]
        itemName = item.replace("T ", "").replace("L ", "")
        if (obj_dict[modelName] != None) & (obj_dict[modelName] != '0'):
            if '-' in obj_dict[modelName]:
                s, l = obj_dict[modelName].split('-', 1)
                group_info_min[itemName] = float(s)
                group_info_max[itemName] = float(l)
                # print("group_info_min[itemName]",group_info_min[itemName])
                # print("group_info_max[itemName]", group_info_max[itemName])
            elif (obj_dict[modelName][0] == '≤') or (obj_dict[modelName][0] =='<'):
                group_info_min[itemName] = 0
                group_info_max[itemName] = float(obj_dict[modelName][1])
            elif obj_dict[modelName][0] == '>':
                group_info_min[itemName] = float(obj_dict[modelName][0])
                group_info_max[itemName] = 14
            else:
                group_info_min[itemName] = float(obj_dict[modelName])
                group_info_max[itemName] = float(obj_dict[modelName])
    group_max = []
    group_indicator = []
    group_min = []
    group_txt= {}
    if '萘' in group:
        for item in group:
            group_indicator.append(item)
            if item in group_info_max:
                group_max.append((item, group_info_max[item]))
                group_min.append((item, group_info_min[item]))
                group_txt[item] = str(group_info_min[item])+"~"+str(group_info_max[item])
            else:
                group_max.append((item, 0))
                group_min.append((item, 0))
                group_txt[item] = 0
    else:
        group_max =sorted(group_info_max.items(), key=lambda x:x[1],reverse=True)
        for item in group_max:
            group_indicator.append(item[0])
            group_min.append((item[0], group_info_min[item[0]]))
            group_txt[item[0]] = str(group_info_min[item[0]])+"~"+str(group_info_max[item[0]])

    if len(group_indicator) == 0:
        group_txt["暂无数据"] = "暂无数据"
    if '萘' in group:
        flag = True
        for value in group_txt.values():
            if value != 0:
                flag = False
        if flag:
            group_txt.clear()
            group_txt["暂无数据"] = "暂无数据"
    return group_indicator, group_max, group_min, group_txt

# 构造气泡图相关数据
def buildDetailsInfo_bubble(name, group):
    verboseName2name = verbosename2name()
    obj = WasteInfo.objects.filter(固废名称=name).last()
    obj_dict = obj.__dict__

    res = []
    txt = {}
    num = 0
    for item in group:
        modelName = verboseName2name[item]

        if (obj_dict[modelName] != None) & (obj_dict[modelName] != '0') :
            randomSize = random.uniform(80,100)
            num += 1
            if '~' in obj_dict[modelName]:
                s, l = obj_dict[modelName].split('~', 1)
                txt[item] = obj_dict[modelName]
                res.insert(0,{"name": item, "value": (float(s) + float(l))/2, "symbolSize": randomSize, "draggable": 'true', "colors" : '#ADD8E6'})
            else:
                txt[item] = obj_dict[modelName]
                res.insert(0,{"name": item, "value": obj_dict[modelName], "symbolSize": randomSize, "draggable": 'true', "colors" : '#ADD8E6'})
        else:
            res.append({"name": item, "value": 0, "symbolSize": 10, "draggable": 'true', "colors" :'grey'})
    # print(res)
    if num == 0:
        txt["暂无数据"] = "暂无数据"
    return res, txt, num

# 构造饼图相关数据
def buildDetailsInfo_pie(name, group):
    verboseName2name = verbosename2name()
    obj = WasteInfo.objects.filter(固废名称=name).last()
    obj_dict = obj.__dict__

    group_info={}
    for item in group:
        modelName = verboseName2name[item]
        if (obj_dict[modelName] != None) & (obj_dict[modelName] != '0'):
            if '-' in obj_dict[modelName]:
                s, l = obj_dict[item].split('-', 1)
                group_info[item] = (float(s)+float(l))/2
            else:
                group_info[item] = obj_dict[modelName]

    res = []
    flag = 0
    for item in group:
        if not (item in group_info):
            flag += 1
    if flag:
        left = 0.0
        percentage = 0.0
        for key in group_info:
            percentage += float(group_info[key])
        left = (100 - percentage) / flag
        if left <= 0:
            left = 0
        left = round(left, 2)
        for item in group:
            if not (item in group_info):
                group_info[item] = left
    txt={}
    for item in group:
        res.append({'value': group_info[item], 'name':item})
        txt[item] = group_info[item]
    return res, txt

# 构造箱线图
def buildDetailsInfo_boxplot(name, group):
    verboseName2name = verbosename2name()
    # queryset = WasteInfo.objects.filter(固废名称=name).all()
    group_info3=[]
    group_info5=[]
    group_info10=[]
    group_info3.append(["name", "value"])
    group_info5.append(["name", "value"])
    group_info10.append(["name", "value"])

    #print("boxplot_group", group)
    allrange, indicator, txt = getAllRange(name, group)
    max3 = indicator[0:3]
    max5 = indicator[3:5]
    max10 = indicator[5:10]
    # obj_dict = queryset[0].__dict__
    for item in max3:
        for data in allrange[item]:
            group_info3.append([item, data])
            group_info5.append([item, data])
            group_info10.append([item, data])
    for item in max5:
        for data in allrange[item]:
            group_info5.append([item, data])
            group_info10.append([item, data])
    for item in max10:
        for data in allrange[item]:
            group_info10.append([item, data])
    dict_slice = {}
    num = 0
    if len(indicator) == 0:
        dict_slice["暂无数据"] = "暂无数据"
    else:
        for k in max3:
            num += 1
            dict_slice[k] = txt[k]
        for k in max5:
            num += 1
            dict_slice[k] = txt[k]
        for k in max10:
            num += 1
            dict_slice[k] = txt[k]
    # print(dict_slice)
    # print(group_info3)
    return group_info3,group_info5,group_info10, dict_slice, num

def buildDetailsInfo_bar3D(name, group):
    queryset = getsameGroup(name)
    verboseName2name = verbosename2name()
    labels = []
    wastenames = []
    lowerbound = []
    upperbound = []
    for obj in queryset:
        obj_dict = obj.__dict__
        wastename = obj.固废名称
        wastenames.append(wastename)
        for item in group:
            modelName = verboseName2name[item]
            if obj_dict[modelName] != None:
                if item not in labels:
                    labels.append(item)
    
    if len(labels) == 0:
        labels.append("暂无数据")
        return labels, wastenames, lowerbound, upperbound, 0
    if '萘' in group:
        labels = group
    i = 0
    j = 0
    id = wastenames.index(name)
    # print(name)
    # print(wastenames)
    # print(id)
    for label in labels:
        for obj in queryset:
            obj_dict = obj.__dict__
            modelName = verboseName2name[label]
            if obj_dict[modelName] != None:
                s,l = getminmax(obj_dict[modelName])
                lowerbound.append([i,j,round(s,2)])
                upperbound.append([i,j,round(float(l)-float(s),2)])
            else:
                lowerbound.append([i,j,0])
                upperbound.append([i,j,0])
            j += 1
        i += 1
        j = 0
    return labels, wastenames, lowerbound, upperbound, id
            

def getAllRange(name, group):
    
    queryset = WasteInfo.objects.filter(固废名称=name).all()
    verboseName2name = verbosename2name()
    allRange = {}
    for obj in queryset:
        obj_dict = obj.__dict__

        for item in group:
            modelName = verboseName2name[item]
            itemName = item.replace("T ", "").replace("L ", "")
            if (obj_dict[modelName] != None) and (obj_dict[modelName] != 'ND') and (obj_dict[modelName] != ' '):
                if itemName not in allRange:
                    allRange[itemName] = []
                if '-' in obj_dict[modelName]:
                    s, l = obj_dict[modelName].split('-', 1)
                    if (len(s) == 0) or (len(l) == 0):
                        continue
                    allRange[itemName].append(float(s))
                    allRange[itemName].append(float(l))
                elif (obj_dict[modelName][0] == '≤') or (obj_dict[modelName][0] =='<'):
                    allRange[itemName].append(float(obj_dict[modelName][1]))
                else:
                    allRange[itemName].append(float(obj_dict[modelName]))
    group_info_max={}
    group_info_min={}
    for key in allRange:
        group_info_max[key] = max(allRange[key])
        group_info_min[key] = min(allRange[key])
    
    group_max = []
    group_indicator = []
    group_min = []
    group_txt= {}

    group_max =sorted(group_info_max.items(), key=lambda x:x[1],reverse=True)
    for item in group_max:
        group_indicator.append(item[0])
        group_min.append((item[0], group_info_min[item[0]]))
        group_txt[item[0]] = str(group_info_min[item[0]])+" ~ "+str(group_info_max[item[0]])
    
    # print(group_info_max)
    # print(group_info_min)
    # print(allRange)
    # print(group_max)
    # print(group_txt)
    return allRange, group_indicator, group_txt

def getBasicInfo(name,txt_label,data_label):
    basic_info = {}
    verboseName2name = verbosename2name()
    name2verboseName = {}
    fields = apps.get_model('wasteSearch.WasteInfo')._meta.fields
    # 建立models中存储的表名还原
    for item in fields:
        name2verboseName[item.name] = item.verbose_name
    
    obj = WasteInfo.objects.filter(固废名称=name).first()
    obj_dict = obj.__dict__ 
    # print(obj_dict)
    basic_info["固废名称"] = name
    for item in obj_dict:
        if obj_dict[item]:
            if item in useless_label:
                continue
            if (name2verboseName[item] in text_label) or (item in text_label):
                basic_info[name2verboseName[item]] = obj_dict[item]
        else:
            if item in useless_label:
                continue
            if (name2verboseName[item] in text_label) or (item in text_label):
                basic_info[name2verboseName[item]] = "暂无数据"
    
    allData={}
    queryset = WasteInfo.objects.filter(固废名称=name).all()
    for obj in queryset:
        obj_dict = obj.__dict__ 
        for item in data_label:
            modelName = verboseName2name[item]
            if (obj_dict[modelName] != None) and (obj_dict[modelName] != 'ND') and (obj_dict[modelName] != ' '):
                if item not in allData:
                    allData[item] = []
                if '-' in obj_dict[modelName]:
                    s, l = range.split('-', 1)
                    allData[item].append(float(s))
                    allData[item].append(float(l))
                elif (obj_dict[modelName][0] == '≤') or (obj_dict[modelName][0] =='<'):
                    allData[item].append(float(obj_dict[modelName][1]))
                else:
                    allData[item].append(float(obj_dict[modelName]))
            else:
                if item not in allData:
                    allData[item] = []
    for key in allData:
        if len(allData[key]):
            upper = max(allData[key])
            lower = min(allData[key])
            if upper == lower :
                basic_info[key] = upper
            else :
                basic_info[key] = str(lower) + ' ~ ' + str(upper)
        else:
            basic_info[key] = "暂无数据"
    # print(basic_info)
    return basic_info


def getColor():
    color1 = random.randint(16, 255)
    color2 = random.randint(16, 255)
    color3 = random.randint(16, 255)
    color1 = hex(color1)
    color2 = hex(color2)
    color3 = hex(color3)
    ans = "#" + color1[2:] + color2[2:] + color3[2:]
    return ans

# 建立models中存储的表名还原
def verbosename2name():
    verboseName2name = {}
    fields = apps.get_model('wasteSearch.WasteInfo')._meta.fields
    for item in fields:
        verboseName2name[item.verbose_name.strip()] = item.name
    return verboseName2name

# 获取数据范围的上下界
# 数据包括以下几种形式
# s-l
# <l
# >l
# l
def getminmax(range):
    if range == 'ND':
        return 0, 0
    if '-' in range:
        s, l = range.split('-', 1)
    elif (range[0] == '≤') or range[0] == '<':
        s = 0
        l = float(range[1])
    elif range[0] == '>':
        s = float(range[1])
        l = 14
    else:
        s = float(range)
        l = float(range)
    return float(s), float(l)

def getsameGroup(name):
    obj = WasteInfo.objects.filter(固废名称=name).first()
    industryname = obj.行业分类
    categoryname = obj.废物类别
    queryset = WasteInfo.objects.filter(Q(行业分类=industryname) & Q(废物类别=categoryname))
    return queryset
