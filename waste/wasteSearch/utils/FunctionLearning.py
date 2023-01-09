# encoding="utf-8"
import joblib
import os
from waste.settings import BASE_DIR

def data_record(model_name):
    """
    函数名称：data_record
    函数功能：记录加载模型的参数。
    参数1：model_name表示调用模型的名称。
    返回值：X_label表示选取指标的名称，y_label表示结果对应的名称。
    """
    if model_name == "废物类别_一级指纹.pkl":
        X_label = ["表观形貌", "物理形态", "含水率"]
        y_label = {0: "固相热处理渣", 1: "液固相浸出渣", 2: "液相反应残液", 3: "蒸馏精馏", 4: "收尘灰", 5: "蒸发结晶", 6: "废水处理污泥"}
    elif model_name == "固相热处理渣_二级指纹.pkl":
        X_label = ["Fe", "Cu", "Zn", "Al2O3", "MgO", "Fe2O3", "SiO2", "CaO", "PbO", "BaO"]
        y_label = {0: "铜火法冶炼熔炼渣", 1: "铜火法冶炼吹炼渣", 2: "铅火法冶炼烟化炉水淬渣", 3: "锌湿法冶炼挥发窑渣", 4: "铅火法冶炼精炼炉除铜渣", 5: "铅火法冶炼精炼渣",
                   6: "锌湿法冶炼熔铸工段产生的锌浮渣", 7: "铝电解铸造工段产生的铝灰渣", 8: "铝电解铸造熔炼炉扒渣处理后的二次铝灰", 9: "再生铝铸造熔炼炉扒渣处理产生的盐渣",
                   10: "碳酸钡生产过程中回转窑焙烧后产生的水淬渣（黑钡渣）", 11: "碳酸钡生产过程中回转窑焙烧后产生的水淬渣（白钡渣）", 12: "有钙焙烧生产金属铬和铬盐过程产生的少钙铬渣",
                   13: "无钙焙烧生产金属铬和铬盐过程产生的无钙铬渣", 14: "电炉法生产黄磷过程中高温熔融产生的磷渣", 15: "电炉法生产黄磷过程中熔融产生的磷铁",
                   16: "氯化法钛白粉氯化工段产生的废熔盐渣", 17: "煤气化炉气化灰渣"}
    elif model_name == "液固相浸出渣_二级指纹.pkl":
        X_label = ["Cr", "Ni", "Cu", "Zn", "Al2O3", "MgO", "Fe2O3", "SiO2", "MnO", "CaO", "TiO2"]
        y_label = {0: "铅电解精炼阳极泥", 1: "锌湿法冶炼焙烧浸出渣", 2: "电炉法生产黄磷的粗磷精制过程中产生的泥磷", 3: "硫酸法生产钛白粉过程中钛精矿酸溶后产生的酸解残渣",
                   4: "碳碱法生产硼砂过程中硼镁矿碳解过滤产生的硼泥", 5: "碳化法氧化镁生产过程中溶液离心分离后产生的镁渣", 6: "硫酸-碳酸铵法生产氧化镁过程中溶液过滤产生的镁渣",
                   7: "硫酸锰生产过程中软锰矿焙烧酸溶后产生的锰渣", 8: "硫酸生产过程中产生的硫铁矿烧渣", 9: "硫磺制酸工艺产生的焚硫渣", 10: "镀锡产生的废槽渣", 11: "镀锌产生的废槽渣",
                   12: "镀镉产生的废槽渣", 13: "镀镍产生的废槽渣", 14: "镀铜产生的废槽渣", 15: "镀铬产生的废槽渣"}
    elif model_name == "蒸馏精馏_二级指纹.pkl":
        X_label = ["灰分", "挥发分", "C", "H", "O"]
        y_label = {0: "石油炼制过程产生的酸焦油及其他焦油", 1: "高温煤焦油", 2: "中低温煤焦油", 3: "焦油渣", 4: "高温煤沥青", 5: "中低温煤沥青", 6: "煤液化残渣"}
    elif model_name == "收尘灰_二级指纹.pkl":
        X_label = ["Zn", "Pb", "Al2O3", "P Cl", "Fe2O3", "SiO2", "CaO"]
        y_label = {0: "铜火法冶炼熔炼收尘烟灰", 1: "铜火法冶炼吹炼收尘烟灰", 2: "铅火法冶炼还原炉收尘烟灰", 3: "铅火法冶炼烟化炉收尘烟灰", 4: "锌湿法冶炼原矿焙烧收尘烟灰",
                   5: "氧化铝生产铝土矿煅烧收尘烟灰", 6: "铝电解熔铸炉收尘烟灰", 7: "再生铝熔铸炉烟灰", 8: "再生铝冶炼精炼工序烟灰", 9: "氯化法生产钛白粉过程中产生的氯化收尘渣",
                   10: "煤气化炉飞灰", 11: "干熄焦除尘灰"}
    elif model_name == "收尘灰_三级指纹.pkl":
        X_label = ["T Cu", "T Pb", "T Zn", "T Ni", "T Cr", "T As", "T Ba"]
        y_label = {0: "铜火法冶炼熔炼收尘烟灰", 1: "铜火法冶炼吹炼收尘烟灰", 2: "铅火法冶炼还原炉收尘烟灰", 3: "铅火法冶炼烟化炉收尘烟灰", 4: "锌湿法冶炼原矿焙烧收尘烟灰",
                   5: "氧化铝生产铝土矿煅烧收尘烟灰", 6: "铝电解熔铸炉收尘烟灰", 7: "再生铝熔铸炉烟灰", 8: "再生铝冶炼精炼工序烟灰", 9: "氯化法生产钛白粉过程中产生的氯化收尘渣",
                   10: "煤气化炉飞灰", 11: "干熄焦除尘灰"}

    return [X_label, y_label]


def document_process(attribute_name, text):
    """
    函数名称：document_process
    函数功能：将文本型数据转化为数值型数据。
    参数1：attribute_name表示字段的名称。
    参数2：text表示文本型数据。
    返回值：转化的数值型数据。
    """
    attribute_form = {"固态": 1, "液态": 2, "固态、半固态": 3}
    attribute_appearance = {"板状、粗糙、团聚": 1, "板状、光滑": 2, "板状、光滑、团聚": 3, "晶体": 4, "球状、粗糙、团聚": 5, "球状、光滑、分散": 6, "无": 0}
    if attribute_name == "物理形态":
        if text in attribute_form:
            return attribute_form[text]
        else:
            return 0
    elif attribute_name == "表观形貌":
        if text in attribute_appearance:
            return attribute_appearance[text]
        else:
            return 0
    else:
        return float(text)

def modelname2filename(modelname):
    if modelname == "废物产生节点溯源":
        return "废物类别_一级指纹.pkl"
    elif modelname == "固相热处理渣类废物溯源":
        return "固相热处理渣_二级指纹.pkl"
    elif modelname == "收尘灰类废物溯源模型1":
        return "收尘灰_二级指纹.pkl"
    elif modelname == "收尘灰类废物溯源模型2":
        return "收尘灰_三级指纹.pkl"
    elif modelname == "浸出渣类废物溯源":
        return "液固相浸出渣_二级指纹.pkl"
    elif modelname == "精蒸馏残渣类废物溯源":
        return "蒸馏精馏_二级指纹.pkl"

def discriminationModel(modelname, labels):
    Al = {"Al2O3":"40.92-79.27","Al": "19.94-59.85","AlN":"5.16-12.04","F":"0.76-3.74" }
    surface = {"SnO2":"0.53-41.99","CuO": "0.9-31.49","Cr2O3":"3.55-23.41", "NiO":"3.92-15.53", "ZnO":"0.15-3.72"}
    if modelname == "铝灰溯源判别模型":
        accuracy = 0
        for key in labels:
            s,l = Al[key].split('-', 1)
            if (float(labels[key]) >= float(s)) and  (float(labels[key]) <= float(l)):
                accuracy += 1/4
        accuracy = round(accuracy,2) * 100
        return "铝灰，概率为： " + str(accuracy) + "%"
    elif modelname == "表面处理污泥溯源判别模型":
        accuracy = 0
        for key in labels:
            s,l = surface[key].split('-', 1)
            if (float(labels[key]) >= float(s)) and  (float(labels[key]) <= float(l)):
                accuracy += 1/5
        accuracy = round(accuracy,2) * 100
        return "表面处理污泥，概率为： " + str(accuracy) + "%"
def searchByModel(modelname,labels):
    # 加载模型
    if (modelname == "铝灰溯源判别模型") or (modelname == "表面处理污泥溯源判别模型"):
        return discriminationModel(modelname, labels)
    else:
        file_path = os.path.join(BASE_DIR,'wasteSearch\\files\\models\\')
        modelfilename = modelname2filename(modelname)
        model_path = "%s%s" % (file_path, modelfilename)
        # print(model_path)
        model = joblib.load(model_path)
        data = []
        for label in labels:
            data.append(document_process(label,labels[label]))
        # print(data)
        result = model.predict_proba([data]).tolist()[0]
        index = result.index(max(result))
        [X, y] = data_record(modelfilename)
        # print(y[index])
        return y[index]