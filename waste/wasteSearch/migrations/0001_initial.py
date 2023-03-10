# Generated by Django 3.2.15 on 2022-12-22 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('usertype', models.CharField(blank=True, max_length=64, null=True, verbose_name='用户类型')),
                ('userstate', models.CharField(blank=True, max_length=64, null=True, verbose_name='用户状态')),
            ],
        ),
        migrations.CreateModel(
            name='WasteImage',
            fields=[
                ('dataId', models.IntegerField(primary_key=True, serialize=False, verbose_name='序号')),
                ('wasteName', models.CharField(blank=True, max_length=64, null=True, verbose_name='固废名称 ')),
                ('img', models.CharField(blank=True, max_length=128, null=True, verbose_name='废物图片 ')),
            ],
        ),
        migrations.CreateModel(
            name='WasteInfo',
            fields=[
                ('dataId', models.IntegerField(primary_key=True, serialize=False, verbose_name='序号')),
                ('废物类别', models.CharField(blank=True, max_length=64, null=True, verbose_name='废物类别')),
                ('行业分类', models.CharField(blank=True, max_length=64, null=True, verbose_name='行业分类')),
                ('固废名称', models.CharField(blank=True, max_length=64, null=True, verbose_name='固废名称 ')),
                ('别名', models.CharField(blank=True, max_length=64, null=True, verbose_name='别名')),
                ('产生工段', models.CharField(blank=True, max_length=128, null=True, verbose_name='产生工段')),
                ('表观形貌稍微详细', models.CharField(blank=True, max_length=64, null=True, verbose_name='表观形貌（稍微详细）')),
                ('物理形态', models.CharField(blank=True, max_length=64, null=True, verbose_name='物理形态')),
                ('形状', models.CharField(blank=True, max_length=64, null=True, verbose_name='形状')),
                ('颜色', models.CharField(blank=True, max_length=64, null=True, verbose_name='颜色')),
                ('气味', models.CharField(blank=True, max_length=64, null=True, verbose_name='气味')),
                ('密度', models.CharField(blank=True, max_length=64, null=True, verbose_name='密度')),
                ('含水率', models.CharField(blank=True, max_length=64, null=True, verbose_name='含水率')),
                ('pH', models.CharField(blank=True, max_length=64, null=True, verbose_name='pH')),
                ('含油率', models.CharField(blank=True, max_length=64, null=True, verbose_name='含油率')),
                ('COD', models.CharField(blank=True, max_length=64, null=True, verbose_name='COD')),
                ('热值', models.CharField(blank=True, max_length=64, null=True, verbose_name='热值')),
                ('烧失率', models.CharField(blank=True, max_length=64, null=True, verbose_name='烧失率')),
                ('水分', models.CharField(blank=True, max_length=64, null=True, verbose_name='水分')),
                ('灰分', models.CharField(blank=True, max_length=64, null=True, verbose_name='灰分')),
                ('挥发分', models.CharField(blank=True, max_length=64, null=True, verbose_name='挥发分')),
                ('固定碳', models.CharField(blank=True, max_length=64, null=True, verbose_name='固定碳')),
                ('C', models.CharField(blank=True, max_length=32, null=True, verbose_name='C')),
                ('H', models.CharField(blank=True, max_length=32, null=True, verbose_name='H')),
                ('N', models.CharField(blank=True, max_length=32, null=True, verbose_name='N')),
                ('O', models.CharField(blank=True, max_length=32, null=True, verbose_name='O')),
                ('F', models.CharField(blank=True, max_length=32, null=True, verbose_name='F')),
                ('Na', models.CharField(blank=True, max_length=32, null=True, verbose_name='Na')),
                ('Mg', models.CharField(blank=True, max_length=32, null=True, verbose_name='Mg')),
                ('Al', models.CharField(blank=True, max_length=32, null=True, verbose_name='Al')),
                ('Si', models.CharField(blank=True, max_length=32, null=True, verbose_name='Si\t')),
                ('P', models.CharField(blank=True, max_length=32, null=True, verbose_name='P')),
                ('S', models.CharField(blank=True, max_length=32, null=True, verbose_name='S')),
                ('Cl', models.CharField(blank=True, max_length=32, null=True, verbose_name='Cl')),
                ('K', models.CharField(blank=True, max_length=32, null=True, verbose_name='K')),
                ('Ca', models.CharField(blank=True, max_length=32, null=True, verbose_name='Ca')),
                ('Ti', models.CharField(blank=True, max_length=32, null=True, verbose_name='Ti')),
                ('V', models.CharField(blank=True, max_length=32, null=True, verbose_name='V')),
                ('Cr', models.CharField(blank=True, max_length=32, null=True, verbose_name='Cr')),
                ('Mn', models.CharField(blank=True, max_length=32, null=True, verbose_name='Mn')),
                ('Fe', models.CharField(blank=True, max_length=32, null=True, verbose_name='Fe')),
                ('Co', models.CharField(blank=True, max_length=32, null=True, verbose_name='Co')),
                ('Ni', models.CharField(blank=True, max_length=32, null=True, verbose_name='Ni')),
                ('Cu', models.CharField(blank=True, max_length=32, null=True, verbose_name='Cu\t')),
                ('Zn', models.CharField(blank=True, max_length=32, null=True, verbose_name='Zn')),
                ('As', models.CharField(blank=True, max_length=32, null=True, verbose_name='As')),
                ('Pb', models.CharField(blank=True, max_length=32, null=True, verbose_name='Pb')),
                ('Ag', models.CharField(blank=True, max_length=32, null=True, verbose_name='Ag')),
                ('Bi', models.CharField(blank=True, max_length=32, null=True, verbose_name='Bi')),
                ('Cd', models.CharField(blank=True, max_length=32, null=True, verbose_name='Cd')),
                ('Sn', models.CharField(blank=True, max_length=32, null=True, verbose_name='Sn')),
                ('Sb', models.CharField(blank=True, max_length=32, null=True, verbose_name='Sb')),
                ('I', models.CharField(blank=True, max_length=32, null=True, verbose_name='I')),
                ('Hg', models.CharField(blank=True, max_length=32, null=True, verbose_name='Hg')),
                ('Ba', models.CharField(blank=True, max_length=32, null=True, verbose_name='Ba')),
                ('Al2O3', models.CharField(blank=True, max_length=32, null=True, verbose_name='Al2O3')),
                ('MgO', models.CharField(blank=True, max_length=32, null=True, verbose_name='MgO')),
                ('Cl_2', models.CharField(blank=True, max_length=32, null=True, verbose_name='P Cl')),
                ('K2O', models.CharField(blank=True, max_length=32, null=True, verbose_name='K2O')),
                ('Na2O', models.CharField(blank=True, max_length=32, null=True, verbose_name='Na2O')),
                ('Fe2O3', models.CharField(blank=True, max_length=32, null=True, verbose_name='Fe2O3')),
                ('SiO2', models.CharField(blank=True, max_length=32, null=True, verbose_name='SiO2')),
                ('MnO', models.CharField(blank=True, max_length=32, null=True, verbose_name='MnO')),
                ('CaO', models.CharField(blank=True, max_length=32, null=True, verbose_name='CaO')),
                ('S_2', models.CharField(blank=True, max_length=32, null=True, verbose_name='P S')),
                ('SO3', models.CharField(blank=True, max_length=32, null=True, verbose_name='SO3')),
                ('As2O3', models.CharField(blank=True, max_length=32, null=True, verbose_name='As2O3')),
                ('TiO2', models.CharField(blank=True, max_length=32, null=True, verbose_name='TiO2')),
                ('Cr2O3', models.CharField(blank=True, max_length=32, null=True, verbose_name='Cr2O3')),
                ('CuO', models.CharField(blank=True, max_length=32, null=True, verbose_name='CuO')),
                ('ZnO', models.CharField(blank=True, max_length=32, null=True, verbose_name='ZnO')),
                ('PbO', models.CharField(blank=True, max_length=32, null=True, verbose_name='PbO')),
                ('F_2', models.CharField(blank=True, max_length=32, null=True, verbose_name='P F')),
                ('V2O5', models.CharField(blank=True, max_length=32, null=True, verbose_name='V2O5')),
                ('BaO', models.CharField(blank=True, max_length=32, null=True, verbose_name='BaO')),
                ('P2O5', models.CharField(blank=True, max_length=32, null=True, verbose_name='P2O5')),
                ('SnO2', models.CharField(blank=True, max_length=32, null=True, verbose_name='SnO2')),
                ('NiO', models.CharField(blank=True, max_length=32, null=True, verbose_name='NiO')),
                ('NaCl', models.CharField(blank=True, max_length=32, null=True, verbose_name='NaCl（%）')),
                ('KCl', models.CharField(blank=True, max_length=32, null=True, verbose_name='KCl')),
                ('MgCl2', models.CharField(blank=True, max_length=32, null=True, verbose_name='MgCl2')),
                ('MgOH2', models.CharField(blank=True, max_length=32, null=True, verbose_name='Mg(OH)2')),
                ('AlOH3', models.CharField(blank=True, max_length=32, null=True, verbose_name='Al(OH)3')),
                ('AlCl3', models.CharField(blank=True, max_length=32, null=True, verbose_name='AlCl3')),
                ('MnCl2', models.CharField(blank=True, max_length=32, null=True, verbose_name='MnCl2')),
                ('NH4Cl', models.CharField(blank=True, max_length=32, null=True, verbose_name='NH4Cl（%）')),
                ('TiCl4', models.CharField(blank=True, max_length=32, null=True, verbose_name='TiCl4')),
                ('FeCl2', models.CharField(blank=True, max_length=32, null=True, verbose_name='FeCl2')),
                ('FeCl3', models.CharField(blank=True, max_length=32, null=True, verbose_name='FeCl3')),
                ('CaCl2', models.CharField(blank=True, max_length=32, null=True, verbose_name='CaCl2')),
                ('CaF2', models.CharField(blank=True, max_length=32, null=True, verbose_name='CaF2')),
                ('CaSO4', models.CharField(blank=True, max_length=32, null=True, verbose_name='CaSO4')),
                ('CaCO3', models.CharField(blank=True, max_length=32, null=True, verbose_name='CaCO3')),
                ('BaO_2', models.CharField(blank=True, max_length=32, null=True, verbose_name='P BaO')),
                ('BaSO4', models.CharField(blank=True, max_length=32, null=True, verbose_name='BaSO4')),
                ('BaCO3', models.CharField(blank=True, max_length=32, null=True, verbose_name='BaCO3')),
                ('BaSiO3', models.CharField(blank=True, max_length=32, null=True, verbose_name='BaSiO3')),
                ('BaS', models.CharField(blank=True, max_length=32, null=True, verbose_name='BaS')),
                ('NaNO3', models.CharField(blank=True, max_length=32, null=True, verbose_name='NaNO3')),
                ('辉铜矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='辉铜矿')),
                ('黄铜矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='黄铜矿')),
                ('铜铁硫化相', models.CharField(blank=True, max_length=32, null=True, verbose_name='铜铁硫化相')),
                ('铁橄榄石', models.CharField(blank=True, max_length=32, null=True, verbose_name='铁橄榄石')),
                ('磁铁矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='磁铁矿')),
                ('钙铁辉石', models.CharField(blank=True, max_length=32, null=True, verbose_name='钙铁辉石')),
                ('玻璃相', models.CharField(blank=True, max_length=32, null=True, verbose_name='玻璃相')),
                ('石膏', models.CharField(blank=True, max_length=32, null=True, verbose_name='石膏')),
                ('方解石', models.CharField(blank=True, max_length=32, null=True, verbose_name='方解石')),
                ('石英', models.CharField(blank=True, max_length=32, null=True, verbose_name='石英')),
                ('砷铜矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='砷铜矿')),
                ('皓矾', models.CharField(blank=True, max_length=32, null=True, verbose_name='皓矾')),
                ('六水锌矾', models.CharField(blank=True, max_length=32, null=True, verbose_name='六水锌矾')),
                ('氧化锑', models.CharField(blank=True, max_length=32, null=True, verbose_name='氧化锑')),
                ('三氧化二砷', models.CharField(blank=True, max_length=32, null=True, verbose_name='三氧化二砷')),
                ('五氧化二砷', models.CharField(blank=True, max_length=32, null=True, verbose_name='五氧化二砷')),
                ('铅绿矾', models.CharField(blank=True, max_length=32, null=True, verbose_name='铅绿矾')),
                ('方铅矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='方铅矿')),
                ('铅黄', models.CharField(blank=True, max_length=32, null=True, verbose_name='铅黄')),
                ('铅', models.CharField(blank=True, max_length=32, null=True, verbose_name='铅')),
                ('密陀僧', models.CharField(blank=True, max_length=32, null=True, verbose_name='密陀僧')),
                ('红锌矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='红锌矿')),
                ('闪锌矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='闪锌矿')),
                ('锌', models.CharField(blank=True, max_length=32, null=True, verbose_name='锌')),
                ('纤锌矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='纤锌矿')),
                ('冰晶石', models.CharField(blank=True, max_length=32, null=True, verbose_name='冰晶石')),
                ('刚玉', models.CharField(blank=True, max_length=32, null=True, verbose_name='刚玉')),
                ('β氧化铝', models.CharField(blank=True, max_length=32, null=True, verbose_name='β-氧化铝')),
                ('钾冰晶石', models.CharField(blank=True, max_length=32, null=True, verbose_name='钾冰晶石')),
                ('铝', models.CharField(blank=True, max_length=32, null=True, verbose_name='铝')),
                ('锥冰晶石', models.CharField(blank=True, max_length=32, null=True, verbose_name='锥冰晶石')),
                ('西蒙冰晶石', models.CharField(blank=True, max_length=32, null=True, verbose_name='西蒙冰晶石')),
                ('氟铝钙锂石', models.CharField(blank=True, max_length=32, null=True, verbose_name='氟铝钙锂石')),
                ('白砷石', models.CharField(blank=True, max_length=32, null=True, verbose_name='白砷石')),
                ('三水胆矾', models.CharField(blank=True, max_length=32, null=True, verbose_name='三水胆矾')),
                ('副雄黄', models.CharField(blank=True, max_length=32, null=True, verbose_name='副雄黄')),
                ('砷华', models.CharField(blank=True, max_length=32, null=True, verbose_name='砷华')),
                ('铅矾', models.CharField(blank=True, max_length=32, null=True, verbose_name='铅矾')),
                ('块黑铅矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='块黑铅矿')),
                ('四水锌矾', models.CharField(blank=True, max_length=32, null=True, verbose_name='四水锌矾')),
                ('硒汞矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='硒汞矿')),
                ('尖晶石', models.CharField(blank=True, max_length=32, null=True, verbose_name='尖晶石')),
                ('氮化铝', models.CharField(blank=True, max_length=32, null=True, verbose_name='氮化铝')),
                ('方镁石', models.CharField(blank=True, max_length=32, null=True, verbose_name='方镁石')),
                ('铜靛矾', models.CharField(blank=True, max_length=32, null=True, verbose_name='铜靛矾')),
                ('CuSO4H2O', models.CharField(blank=True, max_length=32, null=True, verbose_name='CuSO4•H2O')),
                ('CdSO30_5H2O', models.CharField(blank=True, max_length=32, null=True, verbose_name='CdSO3•0.5H2O')),
                ('石盐', models.CharField(blank=True, max_length=32, null=True, verbose_name='石盐')),
                ('氟氯铅矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='氟氯铅矿')),
                ('铁白云石', models.CharField(blank=True, max_length=32, null=True, verbose_name='铁白云石')),
                ('钙铝矾', models.CharField(blank=True, max_length=32, null=True, verbose_name='钙铝矾')),
                ('氯铅矿', models.CharField(blank=True, max_length=32, null=True, verbose_name='氯铅矿')),
                ('T_B', models.CharField(blank=True, max_length=32, null=True, verbose_name='T B(mg/kg)')),
                ('T_Na', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Na(mg/kg)')),
                ('T_Mg', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Mg(mg/kg)')),
                ('T_Al', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Al(mg/kg)')),
                ('T_K', models.CharField(blank=True, max_length=32, null=True, verbose_name='T K(mg/kg)')),
                ('T_Ca', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Ca(mg/kg)')),
                ('T_Fe', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Fe')),
                ('T_Cu', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Cu')),
                ('T_Pb', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Pb')),
                ('T_Zn', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Zn')),
                ('T_Sn', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Sn')),
                ('T_Ni', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Ni')),
                ('T_Co', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Co')),
                ('T_Sb', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Sb')),
                ('T_Hg', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Hg')),
                ('T_Cd', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Cd')),
                ('T_Bi', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Bi')),
                ('T_Cr', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Cr（mg/kg）')),
                ('T_As', models.CharField(blank=True, max_length=32, null=True, verbose_name='T As')),
                ('T_Be', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Be')),
                ('T_Ba', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Ba')),
                ('T_Pd', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Pd')),
                ('T_Pt', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Pt')),
                ('T_V', models.CharField(blank=True, max_length=32, null=True, verbose_name='T V')),
                ('T_Mn', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Mn')),
                ('T_Ti', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Ti')),
                ('T_Al3', models.CharField(blank=True, max_length=32, null=True, verbose_name='T Al3+ （mg/L）')),
                ('T_SO42', models.CharField(blank=True, max_length=32, null=True, verbose_name='T SO42- （g/L)')),
                ('CN', models.CharField(blank=True, max_length=32, null=True, verbose_name='CN（mg/L)')),
                ('T_F', models.CharField(blank=True, max_length=32, null=True, verbose_name='T F（mg/L)')),
                ('萘', models.CharField(blank=True, max_length=32, null=True, verbose_name='萘')),
                ('苊烯', models.CharField(blank=True, max_length=64, null=True, verbose_name='苊烯')),
                ('苊', models.CharField(blank=True, max_length=64, null=True, verbose_name='苊')),
                ('芴', models.CharField(blank=True, max_length=64, null=True, verbose_name='芴')),
                ('菲', models.CharField(blank=True, max_length=64, null=True, verbose_name='菲')),
                ('蒽', models.CharField(blank=True, max_length=64, null=True, verbose_name='蒽')),
                ('荧蒽', models.CharField(blank=True, max_length=64, null=True, verbose_name='荧蒽')),
                ('芘', models.CharField(blank=True, max_length=64, null=True, verbose_name='芘')),
                ('苯并a蒽', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯并（a）蒽')),
                ('屈', models.CharField(blank=True, max_length=64, null=True, verbose_name='屈')),
                ('苯并b荧蒽', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯并（b）荧蒽')),
                ('苯并k荧蒽', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯并 (k)荧蒽')),
                ('苯并a芘', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯并（a）芘')),
                ('茚苯123_cd芘', models.CharField(blank=True, max_length=64, null=True, verbose_name='茚苯（1,2,3-cd）芘')),
                ('二苯并a_n蒽', models.CharField(blank=True, max_length=64, null=True, verbose_name=' 二苯并（a, n）蒽')),
                ('苯并ghi北二萘嵌苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯并（ghi）北（二萘嵌苯）')),
                ('乙酸乙酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='乙酸乙酯')),
                ('乙酸丁酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='乙酸丁酯')),
                ('乙酸异戊酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='乙酸异戊酯')),
                ('氨基甲酸乙酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='氨基甲酸乙酯')),
                ('邻甲酸甲酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻甲酸甲酯')),
                ('邻甲基苯甲酸', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻甲基苯甲酸')),
                ('丁酸丁酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='丁酸丁酯')),
                ('N_氰基乙酰亚胺甲酯乙酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='N-氰基乙酰亚胺甲酯（乙酯）')),
                ('_43甲基3甲亚基氨基苯基丁酸乙酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='4-[3-甲基-3-(（甲亚基氨基)）苯基]丁酸乙酯')),
                ('氯甲酸甲酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='氯甲酸甲酯')),
                ('邻苯二甲酸二甲酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二甲酯')),
                ('邻甲基苯甲酸甲酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻甲基苯甲酸甲酯')),
                ('邻苯二甲酸二乙酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二乙酯')),
                ('邻苯二甲酸二异丁酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二异丁酯')),
                ('邻苯二甲酸二正丁酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二正丁酯')),
                ('邻苯二甲酸二2甲氧基乙酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二(2-甲氧基)乙酯')),
                ('邻苯二甲酸二4甲基戊基酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二(4-甲基-2-戊基)酯')),
                ('邻苯二甲酸二2乙氧基乙酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二(2-乙氧基)乙酯')),
                ('邻苯二甲酸二戊酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二戊酯')),
                ('邻苯二甲酸二己酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二己酯')),
                ('邻苯二甲酸丁基苄基酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸丁基苄基酯')),
                ('邻苯二甲酸二2丁氧基乙酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二(2-丁氧基)乙酯')),
                ('邻苯二甲酸二环己酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二环己酯')),
                ('邻苯二甲酸二2乙基己酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二（2-乙基）己酯')),
                ('邻苯二甲酸二苯酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二苯酯')),
                ('邻苯二甲酸二正辛酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二正辛酯')),
                ('邻苯二甲酸二壬酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二甲酸二壬酯')),
                ('苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯')),
                ('甲苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='甲苯')),
                ('乙苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='乙苯')),
                ('二甲苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='二甲苯')),
                ('对二甲苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='对二甲苯')),
                ('间二甲苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='间二甲苯')),
                ('邻二甲苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻二甲苯')),
                ('异丙苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='异丙苯')),
                ('苯乙烯', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯乙烯')),
                ('乙烯基甲苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='乙烯基甲苯')),
                ('环己烷', models.CharField(blank=True, max_length=64, null=True, verbose_name='环己烷')),
                ('二氯甲烷', models.CharField(blank=True, max_length=64, null=True, verbose_name='二氯甲烷')),
                ('二氯乙烷', models.CharField(blank=True, max_length=64, null=True, verbose_name='二氯乙烷')),
                ('苯酚', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯酚')),
                ('邻甲酚', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻甲酚')),
                ('_24二氯酚', models.CharField(blank=True, max_length=64, null=True, verbose_name='2,4-二氯酚（mg/L）')),
                ('_25二氯苯酚', models.CharField(blank=True, max_length=64, null=True, verbose_name='2,5-二氯苯酚（mg/L）')),
                ('甲醛', models.CharField(blank=True, max_length=64, null=True, verbose_name='甲醛%')),
                ('间苯氧基苯甲醛', models.CharField(blank=True, max_length=64, null=True, verbose_name='间苯氧基苯甲醛')),
                ('甲酸_2', models.CharField(blank=True, max_length=64, null=True, verbose_name='甲酸%')),
                ('苯氧乙酸', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯氧乙酸（mg/L）')),
                ('氯乙酸', models.CharField(blank=True, max_length=64, null=True, verbose_name='氯乙酸')),
                ('羟基乙酸', models.CharField(blank=True, max_length=64, null=True, verbose_name='羟基乙酸（mg/L)')),
                ('_2甲4氯酸', models.CharField(blank=True, max_length=64, null=True, verbose_name='2甲4氯酸')),
                ('甲酸', models.CharField(blank=True, max_length=64, null=True, verbose_name='甲酸')),
                ('甘氨酸', models.CharField(blank=True, max_length=64, null=True, verbose_name='甘氨酸')),
                ('亚磷酸钠', models.CharField(blank=True, max_length=64, null=True, verbose_name='亚磷酸钠')),
                ('甲基草甘膦酸钠盐', models.CharField(blank=True, max_length=64, null=True, verbose_name='甲基草甘膦酸钠盐')),
                ('羟甲基磷酸钠盐', models.CharField(blank=True, max_length=64, null=True, verbose_name='羟甲基磷酸钠盐')),
                ('_24二氯苯氧乙酸钠', models.CharField(blank=True, max_length=64, null=True, verbose_name='2,4-二氯苯氧乙酸钠（mg/L)')),
                ('氯甲基吡啶', models.CharField(blank=True, max_length=64, null=True, verbose_name='氯甲基吡啶')),
                ('吡啶', models.CharField(blank=True, max_length=64, null=True, verbose_name='吡啶')),
                ('_2氯5氯甲基吡啶', models.CharField(blank=True, max_length=64, null=True, verbose_name='2-氯-5-氯甲基吡啶')),
                ('三氯吡啶醇钠', models.CharField(blank=True, max_length=64, null=True, verbose_name='三氯吡啶醇钠')),
                ('乙基氯化物', models.CharField(blank=True, max_length=64, null=True, verbose_name='乙基氯化物')),
                ('氯乙酰氯', models.CharField(blank=True, max_length=64, null=True, verbose_name='氯乙酰氯')),
                ('邻苯二胺', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻苯二胺')),
                ('苯肼', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯肼')),
                ('脲', models.CharField(blank=True, max_length=64, null=True, verbose_name='脲')),
                ('_1苯基氨基脲', models.CharField(blank=True, max_length=64, null=True, verbose_name='1-苯基氨基脲')),
                ('二甲胺', models.CharField(blank=True, max_length=64, null=True, verbose_name='二甲胺')),
                ('_2氯烟酰胺', models.CharField(blank=True, max_length=64, null=True, verbose_name='2-氯烟酰胺')),
                ('精胺', models.CharField(blank=True, max_length=64, null=True, verbose_name='精胺')),
                ('胺醚', models.CharField(blank=True, max_length=64, null=True, verbose_name='胺醚')),
                ('乙撑硫脲', models.CharField(blank=True, max_length=64, null=True, verbose_name='乙撑硫脲')),
                ('邻甲基苯基硫脲', models.CharField(blank=True, max_length=64, null=True, verbose_name='邻甲基苯基硫脲')),
                ('_2氯N氯甲基_N26二乙基苯基乙酰胺MRM', models.CharField(blank=True, max_length=64, null=True, verbose_name='2-氯-N-(氯甲基)-N-(2,6-二乙基苯基)乙酰胺（MRM）')),
                ('N_26二乙基苯基甲亚胺甲叉', models.CharField(blank=True, max_length=64, null=True, verbose_name='N-2,6-二乙基苯基甲亚胺（甲叉）')),
                ('丁草胺', models.CharField(blank=True, max_length=64, null=True, verbose_name='丁草胺')),
                ('_4_3乙基2甲亚基氨基苯基丁酰氯', models.CharField(blank=True, max_length=64, null=True, verbose_name='4-[3-乙基-2-(甲亚基氨基)苯基]丁酰氯')),
                ('_25二氯苯胺', models.CharField(blank=True, max_length=64, null=True, verbose_name='2,5-二氯苯胺')),
                ('_24D', models.CharField(blank=True, max_length=64, null=True, verbose_name='2,4-D（mg/L）')),
                ('草甘膦', models.CharField(blank=True, max_length=64, null=True, verbose_name='草甘膦（mg/L)')),
                ('增甘膦', models.CharField(blank=True, max_length=64, null=True, verbose_name='增甘膦mg/L')),
                ('双甘膦', models.CharField(blank=True, max_length=64, null=True, verbose_name='双甘膦mg/L')),
                ('西玛津', models.CharField(blank=True, max_length=64, null=True, verbose_name='西玛津mg/L')),
                ('三唑磷', models.CharField(blank=True, max_length=64, null=True, verbose_name='三唑磷mg/L')),
                ('烟嘧磺酰氯', models.CharField(blank=True, max_length=64, null=True, verbose_name='烟嘧磺酰氯mg/L')),
                ('烟嘧磺胺', models.CharField(blank=True, max_length=64, null=True, verbose_name='烟嘧磺胺mg/L')),
                ('烟嘧磺隆', models.CharField(blank=True, max_length=64, null=True, verbose_name='烟嘧磺隆mg/kg')),
                ('毒死蜱', models.CharField(blank=True, max_length=64, null=True, verbose_name='毒死蜱')),
                ('多菌灵', models.CharField(blank=True, max_length=64, null=True, verbose_name='多菌灵mg/L')),
                ('氟乐灵', models.CharField(blank=True, max_length=64, null=True, verbose_name='氟乐灵')),
                ('丁草胺_2', models.CharField(blank=True, max_length=64, null=True, verbose_name='丁草胺mg/L')),
                ('咪鲜胺', models.CharField(blank=True, max_length=64, null=True, verbose_name='咪鲜胺')),
                ('莠去津', models.CharField(blank=True, max_length=64, null=True, verbose_name='莠去津mg/L')),
                ('百草枯', models.CharField(blank=True, max_length=64, null=True, verbose_name='百草枯mg/L')),
                ('苯磺隆', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯磺隆')),
                ('吡虫啉', models.CharField(blank=True, max_length=64, null=True, verbose_name='吡虫啉')),
                ('咪唑烷', models.CharField(blank=True, max_length=64, null=True, verbose_name='咪唑（烷）')),
                ('丙环唑', models.CharField(blank=True, max_length=64, null=True, verbose_name='丙环唑')),
                ('代森锰', models.CharField(blank=True, max_length=64, null=True, verbose_name='代森锰mg/L')),
                ('敌百虫', models.CharField(blank=True, max_length=64, null=True, verbose_name='敌百虫')),
                ('啶虫脒', models.CharField(blank=True, max_length=64, null=True, verbose_name='啶虫脒')),
                ('麦草畏', models.CharField(blank=True, max_length=64, null=True, verbose_name='麦草畏')),
                ('杀虫单', models.CharField(blank=True, max_length=64, null=True, verbose_name='杀虫单')),
                ('乙草胺', models.CharField(blank=True, max_length=64, null=True, verbose_name='乙草胺')),
                ('溴丙烷', models.CharField(blank=True, max_length=64, null=True, verbose_name='溴丙烷')),
                ('四氯化碳', models.CharField(blank=True, max_length=64, null=True, verbose_name='四氯化碳')),
                ('丙溴磷', models.CharField(blank=True, max_length=64, null=True, verbose_name='丙溴磷')),
                ('对氯三氟甲苯', models.CharField(blank=True, max_length=64, null=True, verbose_name='对氯三氟甲苯')),
                ('功夫酰氯', models.CharField(blank=True, max_length=64, null=True, verbose_name='功夫酰氯')),
                ('苄基三乙基氯化铵', models.CharField(blank=True, max_length=64, null=True, verbose_name='苄基三乙基氯化铵')),
                ('二氯菊酰氯', models.CharField(blank=True, max_length=64, null=True, verbose_name='二氯菊酰氯')),
                ('_4甲基2肼基苯并骈噻唑', models.CharField(blank=True, max_length=64, null=True, verbose_name='4-甲基-2-肼基苯并骈噻唑')),
                ('苯唑醇', models.CharField(blank=True, max_length=64, null=True, verbose_name='苯唑醇')),
                ('二甲硫醚', models.CharField(blank=True, max_length=64, null=True, verbose_name='二甲硫醚')),
                ('硫酸二甲酯', models.CharField(blank=True, max_length=64, null=True, verbose_name='硫酸二甲酯')),
                ('甲醇', models.CharField(blank=True, max_length=64, null=True, verbose_name='甲醇')),
                ('乙醇', models.CharField(blank=True, max_length=64, null=True, verbose_name='乙醇')),
                ('辛硫磷', models.CharField(blank=True, max_length=64, null=True, verbose_name='辛硫磷')),
                ('_OO二乙基硫代磷酰氯', models.CharField(blank=True, max_length=64, null=True, verbose_name='O,O-二乙基硫代磷酰氯')),
                ('_2氯烟酰胺_2', models.CharField(blank=True, max_length=64, null=True, verbose_name='P 2-氯烟酰胺')),
                ('二氯甲烷_2', models.CharField(blank=True, max_length=64, null=True, verbose_name='P 二氯甲烷')),
                ('醋酸', models.CharField(blank=True, max_length=64, null=True, verbose_name='醋酸')),
                ('醋酸酐', models.CharField(blank=True, max_length=64, null=True, verbose_name='醋酸酐')),
                ('丙烯醛', models.CharField(blank=True, max_length=64, null=True, verbose_name='丙烯醛')),
                ('丙烯腈', models.CharField(blank=True, max_length=64, null=True, verbose_name='丙烯腈')),
                ('环戊二烯', models.CharField(blank=True, max_length=64, null=True, verbose_name='环戊二烯')),
                ('L_Ca', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Ca(mg/L)')),
                ('L_Mg', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Mg（mg/L)')),
                ('L_Fe', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Fe (mg/L)')),
                ('L_Cu', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Cu')),
                ('L_Pb', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Pb')),
                ('L_Zn', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Zn')),
                ('L_Ba', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Ba (mg/L)')),
                ('L_Sn', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Sn ')),
                ('L_Co', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Co')),
                ('L_Sb', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Sb')),
                ('L_Hg', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Hg')),
                ('L_Cd', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Cd')),
                ('L_Bi', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Bi')),
                ('L_Ni', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Ni')),
                ('L_Cr', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Cr （mg/L)')),
                ('L_Ag', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Ag')),
                ('L_As', models.CharField(blank=True, max_length=64, null=True, verbose_name='L As')),
                ('L_Mn', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Mn')),
                ('L_Se', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Se')),
                ('L_Br', models.CharField(blank=True, max_length=64, null=True, verbose_name='L Br')),
                ('L_V', models.CharField(blank=True, max_length=64, null=True, verbose_name='L V')),
            ],
        ),
    ]
