import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OLD_ASSETS = DATA / "阶段1_资产统计表_V1.0.csv"
SCRIPT_JSON = ROOT / "outputs" / "_script_revision_v12" / "v12_structure.json"

FIELDS = [
    "生产资产ID", "资产类型", "资产名称", "资产级别", "剧本出处", "关联场次或段落",
    "基础描述", "补全设计信息", "状态变体", "材质结构或声音特点", "光影或环境要求",
    "使用或生成需求", "可复用范围", "信息来源", "确认状态", "阶段2处理建议",
]


def record(asset_id, asset_type, name, level, base, design, variants, material, light,
           need, reuse, source="V1.2剧本明确＋项目锁定＋公开工程资料边界",
           status="已确认生产方向", phase2="阶段2A重入后按生产包执行"):
    return {
        "生产资产ID": asset_id,
        "资产类型": asset_type,
        "资产名称": name,
        "资产级别": level,
        "剧本出处": "V1.2逐镜映射见data/阶段1_114镜资产调用映射_V1.2.csv",
        "关联场次或段落": "",
        "基础描述": base,
        "补全设计信息": design,
        "状态变体": variants,
        "材质结构或声音特点": material,
        "光影或环境要求": light,
        "使用或生成需求": need,
        "可复用范围": reuse,
        "信息来源": source,
        "确认状态": status,
        "阶段2处理建议": phase2,
    }


RETIRED = {
    "BY-CHR-P1-001-周明远": "V1.2不出场",
    "BY-CHR-P1-003-孙屹川": "V1.2不出场",
    "BY-CST-P1-003-周明远主播服装": "随角色停用",
    "BY-CST-P1-005-孙屹川专家服装": "随角色停用",
    "BY-VOI-P1-001-周明远声音": "随角色停用",
    "BY-VOI-P1-003-孙屹川声音": "随角色停用",
    "BY-SCN-P1-001-未来新闻演播室": "V1.2不使用演播室",
    "BY-SCN-P1-002-文昌发射场夜景": "V1.2从月轨相遇起片，不含发射",
    "BY-SCN-P1-004-北京飞控中心大厅": "由P0新资产BY-SCN-P0-006替代",
    "BY-LGT-P1-001-演播室中性直播光": "随演播室停用",
    "BY-LGT-P1-002-文昌夜间发射光": "随发射场停用",
    "BY-LGT-P0-003-月面固定太阳光": "由明确承担天文偏差的BY-LGT-P0-004替代",
    "BY-VEH-P1-001-长征十号揽月发射构型": "V1.2不含发射",
    "BY-VEH-P1-002-长征十号梦舟发射构型": "V1.2不含发射",
    "BY-VFX-P1-001-地球发射火焰与烟羽": "V1.2不含发射",
    "BY-SND-P2-001-新闻提示音": "V1.2无新闻包装提示音且全片无配乐",
    "BY-SYM-P1-002-新闻条与日期标牌系统": "V1.2已取消新闻段落；日期与任务阶段信息由BY-SYM-P1-003承担",
    "BY-REL-P0-004-刘定槎与两张空座椅": "叙事关系失效；由BY-REL-P0-009替代",
}


UPDATES = {
    "BY-SCN-P0-001-梦舟舱内三座布局": {
        "资产名称": "梦舟返回舱三座承力区",
        "基础描述": "返回舱内三张平行低位承力椅背、紧凑控制区和贴身弧形舱壁的局部空间。",
        "补全设计信息": "只锁定当前母图可见的座椅／材料／控制关系；不在一张图中解释舱门、完整地板或通道。",
        "状态变体": "三人返航承载；两座暂空；三人归位",
        "阶段2处理建议": "保留V3.0局部母图方向；不得回灌梦舟舱内01—05失败图",
    },
    "BY-SCN-P0-002-梦舟对接通道与舱门区": {
        "资产名称": "梦舟—揽月轴向对接转移通道",
        "基础描述": "两器前向舱门连接后的紧凑轴向通道，用于物品、人员和样品两次转移。",
        "状态变体": "关闭；压差归零；双门开启；物品先行；人员转移；样品回传",
        "阶段2处理建议": "作为独立场景母图验证，不与梦舟三座母图合并",
    },
    "BY-SCN-P0-003-揽月登月舱舱内": {
        "状态变体": "月轨交会；动力下降；着陆后；EVA准备／复压；月面起飞；再交会",
        "阶段2处理建议": "按V1.2状态链复核原设计，再做必要视图",
    },
    "BY-SCN-P0-004-月面着陆与作业区": {
        "光影或环境要求": "继承BY-LGT-P0-004艺术化任务日光；黑天空、真空、深阴影、有限地表反射。",
        "阶段2处理建议": "旧母图只作构型候选；以艺术化光照口径重新校准MASTER",
    },
    "BY-SCN-P1-005-月面后段科考区": {
        "资产名称": "月面科学任务路线与采样点",
        "状态变体": "月球车卸载；第一采样点；接触带采样；载荷布设；返程闭环",
        "阶段2处理建议": "与月面MASTER共用光向和地质材料，不另造独立天体环境",
    },
    "BY-LGT-P1-003-飞控大厅任务光": {
        "关联场次或段落": "第2、5、6、8、10、12、14—16场",
        "阶段2处理建议": "关联新P0北京飞控大厅资产",
    },
    "BY-LGT-P1-004-环月轨道太阳光": {
        "光影或环境要求": "统一外部主光与月球反照；只保证跨镜连续，不声称日期天文复原。",
    },
    "BY-VEH-P0-002-揽月完整构型": {
        "资产名称": "揽月着陆器＋推进舱月轨组合体",
        "状态变体": "交会接近；对接；分离；降轨点火；推进舱任务完成",
        "阶段2处理建议": "V1.2外部构型链首要验证资产",
    },
    "BY-VEH-P0-003-揽月登月舱": {
        "状态变体": "下降姿态；触月承载；月面驻留；整器起飞；环月交会",
    },
    "BY-PRP-P0-005-密封样品转移容器": {
        "资产名称": "主样品密封转移容器",
        "状态变体": "空载固定；装样封闭；外平台转移；揽月舱内锁止；跨舱转移；梦舟样品柜锁止",
    },
    "BY-PRP-P1-003-月面科学观测设备": {
        "资产名称": "小型月面科学载荷",
        "状态变体": "收纳；搬运；布放；安装后；遥测上线",
    },
    "BY-REL-P0-005-揽月构型状态链": {
        "基础描述": "着陆器＋推进舱交会对接—分离降轨—推进舱分离—着陆器下降／触月／整体起飞—再对接—受控处置。",
        "阶段2处理建议": "按V1.2扩展后的完整状态链执行",
    },
    "BY-REL-P0-008-样品转移链": {
        "基础描述": "月面编号采样—装袋封口—主容器封闭—揽月固定—样品先行跨舱—梦舟样品柜锁止—回收接收。",
    },
}


NEW = [
    record("BY-SCN-P0-005-梦舟环月工作位", "SCN", "梦舟返回舱环月工作位", "P0",
           "三座承力座椅区的环月工作状态视图；刘定槎从任务席完成交会、遥测和轨道协同。",
           "工作位不是第四个位置；任务席、共享前上方显示控制区和相邻两张空座属于同一承力座椅区。",
           "初次交会；环月留守；上升目标捕获；再交会；地月返回准备",
           "承力座椅、暖白喷涂面板、石墨灰控制件、织物软包、蓝色扶手",
           "舱顶暖白任务灯＋屏幕微弱冷光；窗外黑暗",
           "任务席MASTER、正向工作视图、肩后工作视图", "第1、3、9、11—14场"),
    record("BY-SCN-P0-006-北京飞控大厅与任务主屏", "SCN", "北京飞控大厅与任务主屏", "P0",
           "真实国家任务控制大厅尺度，核心席、任务主屏和分层工作席可辨。",
           "不做商业科幻舰桥；屏幕只生成无字结构底图，可读信息后期添加。",
           "交会；下降；触月；月面活动；起飞；再交会；返回；再入；任务完成",
           "低反光控制台、克制蓝灰屏光、暖白顶灯",
           "稳定任务光，人物与环境共享光源",
           "MASTER、任务席、主屏、控制台局部", "第2、5、6、8、10、12、14—16场"),
    record("BY-SCN-P0-007-返回舱再入视觉环境", "SCN", "返回舱再入视觉环境", "P0",
           "近地空间、高层大气、地球弧面和返回舱跳跃式再入的统一视觉环境。",
           "第一次擦入、短暂跃出、第二次再入、黑障和开伞属于同一连续轨迹。",
           "服务舱分离；第一次再入；跃出；第二次再入；辉光减弱；开伞",
           "地球蓝白层次、黑色近地空间、受控等离子辉光",
           "太阳光、地球反照与等离子自发光来源清楚",
           "再入MASTER及关键状态视图", "第15场"),
    record("BY-SCN-P0-008-预定着陆区与搜救现场", "SCN", "预定着陆区与搜救现场", "P0",
           "返回舱陆上着陆、空地搜救、舱体处置和医学接收的一体化现场。",
           "着陆地点保持泛化，不制造具体未公布地名。",
           "落点椭圆；气囊触地；空地抵达；安全检查；开舱；医学检查；样品接收",
           "真实荒漠／草原地表、工程车辆、医疗与安全装备",
           "克制日间自然光；现场风尘只按地球环境表现",
           "MASTER、航拍、手持长焦、舱门医疗视图", "第15—16场"),
    record("BY-SCN-P1-007-佳木斯66米深空测控站", "SCN", "佳木斯66米深空测控站", "P1",
           "大型深空天线与值班测控工作区。", "天线结构以公开资料为锚，界面无可读伪参数。",
           "月轨交会；动力下降；月面活动；月面起飞；地月返回",
           "真实天线钢结构、设备机柜和控制台", "外景自然光／夜间按镜头统一；室内任务光",
           "天线MASTER、长焦跟踪、值班工作区", "第1、5、8、11、14场"),
    record("BY-SCN-P1-008-喀什35米深空测控站", "SCN", "喀什35米深空测控站", "P1",
           "深空测控天线与备份链路工作区。", "与佳木斯在尺度和环境上可区分。",
           "降轨接力；动力下降备份；月面起飞双目标跟踪；地月返回",
           "公开天线结构、干旱地区工程环境", "外景自然光；室内任务光",
           "天线MASTER、跟踪状态视图", "第4、5、11、14场"),
    record("BY-SCN-P1-009-VLBI测轨席", "SCN", "VLBI测轨席／天衡界面", "P1",
           "多站测轨数据汇聚与轨道解算校核席位。", "不等同于单一青岛站；屏幕只做抽象底图。",
           "降轨解算；下降外测；起飞窗口；再交会校核；返回走廊",
           "克制控制台、深色任务屏、有限实体输入设备", "稳定室内任务光",
           "席位MASTER和控制台局部", "第4、5、10、12、14场"),
    record("BY-SCN-P1-010-北京飞控地质席", "SCN", "北京飞控地质席", "P1",
           "地质专家把落区图与月面摄像叠合的工作席。", "属于北京飞控体系，不另造科幻实验室。",
           "路线建议；样品点核对；载荷遥测", "控制台、无字地图底图、通信耳机", "继承飞控大厅任务光",
           "席位MASTER、分屏局部", "第9场"),
    record("BY-SCN-P1-011-搜救指挥中心", "SCN", "返回器搜救指挥中心", "P1",
           "落点预测、空地接力和回收状态闭合的指挥空间。", "与北京飞控可剪辑区分，界面后期添加。",
           "落点收敛；队伍接近；舱体与乘组状态闭合", "真实调度席、通信设备、地图屏底图", "克制任务光",
           "MASTER、主屏／席位局部", "第15—16场"),
    record("BY-LGT-P0-004-月面艺术化任务日光", "LGT", "月面艺术化任务日光", "P0",
           "为可见性与跨镜连续性建立的单一硬质平行主光。",
           "MASTER左前上方入光、阴影右后；方位225°、高度22°仅为美术生产坐标。",
           "下降；触月；EVA；国旗；科学任务；返舱；起飞",
           "高反差硬光、有限月壤反射、白色装备高光受控",
           "黑天空、无大气散射、无来源轮廓光、无HDR抬暗部",
           "先在月面MASTER锁定，再供所有月面视图继承", "第5—11场",
           status="用户已确认", phase2="重做月面MASTER光影校准测试"),
    record("BY-LGT-P0-005-返回舱再入等离子辉光", "LGT", "返回舱再入等离子辉光", "P0",
           "高速再入时防热大底周围的受控等离子自发光。", "两次再入强度变化清楚，不做爆炸火球。",
           "第一次再入；跃出减弱；第二次再入；黑障；恢复",
           "橙白核心、稀薄红橙尾迹、舱体暗部受自发光照亮", "与地球弧面和太阳光逻辑统一",
           "与再入VFX联动制作", "第15场"),
    record("BY-LGT-P1-006-深空测控站任务光", "LGT", "深空测控站任务光", "P1",
           "佳木斯、喀什和VLBI工作区统一的克制任务照明。", "不同站点保留环境差异。",
           "常态；关键窗口", "中性暖白顶灯、低亮屏光", "禁止科幻蓝光大厅", "随场景母图锁定", "第1、4、5、10—14场"),
    record("BY-LGT-P1-007-搜救着陆区日间自然光", "LGT", "搜救着陆区日间自然光", "P1",
           "回收现场可辨识的克制自然日光。", "不锁定具体回收地经纬度和天气实况。",
           "低空；着陆；搜救抵达；开舱；终景", "自然天空光、地表反射、返回舱高温表面", "无电影式金色逆光",
           "与搜救现场MASTER同步确认", "第15—16场"),
    record("BY-VEH-P0-005-梦舟月轨组合体", "VEH", "梦舟返回舱＋服务舱月轨组合体", "P0",
           "返回舱、无人服务舱、太阳翼和前向对接口可辨认的完整组合体。", "服务舱不可出现载人舷窗或观察室。",
           "环月待机；两次对接；地月转移姿态", "隔热材料、太阳翼、推进与热控外部设备", "继承环月轨道光",
           "完整组合体结构验证和关键状态视图", "第1—4、12—14场"),
    record("BY-VEH-P0-006-梦舟返回舱独立再入构型", "VEH", "梦舟返回舱独立再入构型", "P0",
           "服务舱分离后的独立返回舱，防热大底朝向清楚。", "外形以公开返回舱方向为锚，未公开细部克制补全。",
           "分离；姿态调整；等离子再入；开伞前", "烧蚀防热材料、耐高温外表、天线区域", "再入辉光与高层大气",
           "结构验证＋再入状态继承", "第15场"),
    record("BY-VEH-P0-007-返回舱群伞气囊着陆构型", "VEH", "返回舱群伞／气囊着陆构型", "P0",
           "返回舱稳定伞、主伞、充气气囊和陆上着陆状态。", "明确属于公开技术基础上的艺术方案。",
           "稳定伞；主伞；气囊充气；触地滚摆；着陆稳定", "高强织物伞具、烧蚀舱体、工程气囊", "地球大气与日间现场光",
           "与开伞、气囊VFX和搜救场景联合验证", "第15—16场"),
    record("BY-VEH-P1-004-揽月月面起飞状态", "VEH", "揽月整器月面起飞状态", "P1",
           "四条着陆腿随着陆器整体离月的构型。", "禁止阿波罗式留月下降级。",
           "点火；垂直上升；俯仰转弯；入轨", "继承已确认揽月材料", "艺术化月面日光与贴地羽流",
           "由揽月基础资产派生状态", "第11场"),
    record("BY-VEH-P1-005-揽月月轨再对接状态", "VEH", "揽月月轨再交会对接状态", "P1",
           "月面起飞后的揽月与梦舟轴向接近、捕获和硬连接。", "与首次对接使用同一接口家族。",
           "近程导引；百米点；最终接近；捕获；硬连接", "继承揽月和梦舟外部材料", "环月轨道光",
           "两器尺度与对接轴线验证", "第12—13场"),
    record("BY-VEH-P1-006-揽月受控处置状态", "VEH", "揽月受控分离处置状态", "P1",
           "人员与样品转移完成后，揽月与梦舟分离并进入另一条处置轨迹。", "不锁定具体撞击点。",
           "分离；安全距离；轨迹分叉；远离", "继承揽月基础构型", "环月轨道光",
           "与处置轨迹VFX联合制作", "第13场"),
    record("BY-VEH-P1-007-梦舟服务舱近地分离状态", "VEH", "梦舟服务舱近地分离状态", "P1",
           "近地再入前服务舱与返回舱分离，只有返回舱进入大气。", "服务舱保持无人非密封外部结构。",
           "主供能关闭；分离；返回舱调姿", "继承梦舟组合体材料", "近地空间与地球反照",
           "外部构型状态验证", "第15场"),
    record("BY-VEH-P1-008-搜救直升机与地面车辆", "VEH", "搜救直升机与地面车辆配置", "P1",
           "空中和地面两路接近返回舱的搜救载具。", "不绑定未公布型号和涂装细节。",
           "远距接近；抵达；医疗／样品转运", "真实搜救工程装备", "着陆区自然光",
           "载具配置与尺度验证", "第16场"),
    record("BY-PRP-P1-007-任务数据盒与随身救生包", "PRP", "任务数据盒与随身救生包", "P1",
           "人员转移前先行跨舱的小型固定任务物品。", "可由戴手套人员沿固定索传递。",
           "梦舟固定；通道传递；揽月固定", "耐磨织物包、硬壳数据盒、系留点", "舱内任务光",
           "道具结构与手套尺度验证", "第3场"),
    record("BY-PRP-P1-008-主样品容器编号与固定座", "PRP", "主样品容器编号、封签与固定座", "P1",
           "承载采样袋并贯穿月面—揽月—梦舟—回收链。", "编号、封签和可读信息后期添加。",
           "空载；接近上限；封闭；外平台锁止；舱内锁止；跨舱；回收接收", "金属／复合材料硬壳、双重锁止", "月面与舱内光影分别继承",
           "与BY-PRP-P0-005形成容器系统", "第9—10、13—16场"),
    record("BY-PRP-P1-009-污染控制用品", "PRP", "月尘污染控制用品", "P1",
           "返舱后擦拭登月服接口和样品容器的工具。", "不表现扬尘和随意脱服。",
           "收纳；擦拭；封存", "低掉屑擦拭材料、密封袋、固定夹", "揽月舱内任务光",
           "道具组轻量结构验证", "第10场"),
    record("BY-PRP-P1-010-返回舱样品柜与锁止", "PRP", "梦舟返回舱样品柜与锁止", "P1",
           "返航时独立固定主样品容器的紧凑柜体。", "与三座承载区不冲突。",
           "空；容器锁止；回收交接", "暖白设备柜、金属锁扣、软性防撞衬垫", "梦舟舱内任务光",
           "与梦舟返航构型联合验证", "第13—16场"),
    record("BY-PRP-P1-011-返回舱信标与现场安全工具", "PRP", "返回舱信标与现场安全处置工具", "P1",
           "着陆后定位、温度／电气安全检查和舱门处置用品。", "不写可读型号和未公布程序。",
           "信标工作；安全检查；开舱准备", "耐候工程设备、测温和绝缘工具", "着陆区自然光",
           "搜救场景道具组", "第15—16场"),
    record("BY-VFX-P0-005-返回舱等离子辉光与黑障视觉", "VFX", "返回舱等离子辉光与黑障视觉", "P0",
           "两次再入的等离子辉光、热流变化和通信衰减可见结果。", "黑障是信号状态，不表现飞船故障。",
           "第一次再入；跃出减弱；第二次再入；黑障；通信恢复", "受控橙白辉光、稀薄尾迹", "高层大气，无爆炸式火焰",
           "高风险技术测试", "第15场"),
    record("BY-VFX-P0-006-稳定伞与主伞展开", "VFX", "返回舱稳定伞／主伞展开", "P0",
           "辉光减弱后伞具按程序依次展开，下降姿态稳定。", "高度与伞型保持泛化。",
           "稳定伞；主伞；稳定下降", "真实织物充气和绳索受力", "地球大气环境",
           "与返回舱群伞构型联合测试", "第15场"),
    record("BY-VFX-P0-007-气囊触地滚摆", "VFX", "返回舱气囊触地与滚摆", "P0",
           "气囊充气、触地、短距离滚摆并稳定。", "属于艺术化陆上回收方案。",
           "充气；触地；滚摆；稳定", "地表尘土和气囊变形符合地球环境", "着陆区自然光",
           "与搜救MASTER联合测试", "第15场"),
    record("BY-VFX-P1-004-姿控喷流", "VFX", "月轨姿态控制喷流", "P1",
           "两器交会、分离和姿态调整时的短促微弱喷流。", "外部静音，不形成爆炸火焰。",
           "接近；停泊；分离；调姿", "稀薄短促羽流", "太空真空",
           "梦舟／揽月通用模板", "第2、4、12—15场"),
    record("BY-VFX-P1-005-半弹道跳跃式再入轨迹", "VFX", "半弹道跳跃式再入轨迹", "P1",
           "第一次擦入、跃出稠密大气、再次下弯和第二次再入的后期轨迹表达。", "不得写成进入地球同步轨道。",
           "第一次入射；跃出；第二次入射", "克制轨迹线和地球弧面", "可读数字后期制作",
           "后期轨迹模板", "第15场"),
    record("BY-VFX-P1-006-揽月受控处置轨迹", "VFX", "揽月受控处置轨迹", "P1",
           "梦舟与揽月分离后的轨迹分叉和安全距离。", "不锁定具体撞击点。",
           "分离；轨迹分叉；目标移除", "克制轨迹图形", "环月轨道环境",
           "与揽月处置状态联合制作", "第13场"),
    record("BY-VFX-P1-007-月球车轮迹与低重力扬尘", "VFX", "月球车轮迹与低重力扬尘", "P1",
           "车轮压出连续轨迹，少量颗粒按弹道落回。", "无空气翻滚尘云。",
           "卸载；行驶；转弯；返程", "月壤颗粒和轮迹压实", "艺术化月面任务日光",
           "月面物理测试", "第9场"),
    record("BY-SYM-P0-002-艺术化光照偏差推演声明", "SYM", "艺术化光照偏差推演声明", "P0",
           "片头短声明和片尾完整声明，明确日期／坐标与真实自然照明存在偏差。", "由后期准确排版，AI原图不生成文字。",
           "片头短版；片尾完整版", "后期字幕图形", "不适用",
           "按锁定文本制作", "镜001、114",
           status="用户已确认", phase2="建立后期包装规范；不进入生图正文"),
    record("BY-SYM-P1-004-任务轨迹与相位图模板", "SYM", "任务轨迹、相位与走廊图后期模板", "P1",
           "交会、下降、月面路线、地月转移和再入的克制信息图底图。", "可读参数、坐标和标注后期添加。",
           "交会；下降；路线；转移；再入", "深色任务界面、细线轨迹", "屏幕光受场景限制",
           "跨场复用后期模板", "全片任务屏"),
    record("BY-SYM-P1-005-样品编号与封签模板", "SYM", "样品编号、封签与接收状态模板", "P1",
           "采样袋、主容器和回收接收的统一编号体系。", "AI原图不生成可读编号。",
           "采样；封装；转移；接收", "后期贴图与字幕", "不适用",
           "与样品道具同步设计", "第9—10、13、16场"),
    record("BY-CRO-P1-002-深空测控值班团队", "CRO", "深空测控值班团队", "P1",
           "佳木斯、喀什和VLBI席位的专业值班人员配置。", "岗位、年龄和脸部有差异，不复制同脸。",
           "常态值班；关键窗口", "中国航天测控工作服方向", "站内任务光",
           "与测控场景配套", "第1、4、5、10—14场"),
    record("BY-CRO-P1-003-搜救与医疗团队", "CRO", "搜救、安全处置与医疗团队", "P1",
           "先安全检查、再开舱和医学接收的多岗位团队。", "不让航天员落地立即站立庆祝。",
           "空地接近；安全处置；开舱；医学检查；样品接收", "真实防护服、医疗和工程装备", "着陆区自然光",
           "与搜救场景和载具配套", "第16场"),
    record("BY-VOI-P1-005-林海深空测控声音", "VOI", "林海深空测控稳定音色", "P1",
           "佳木斯主链路席位的克制无线电声音。", "中性中低音、短句、清楚报数。", "中性样本", "稳定、专业、无表演腔", "不适用", "独立音色验证", "第1、5、8、11、14场"),
    record("BY-VOI-P1-006-叶河深空测控声音", "VOI", "叶河深空测控稳定音色", "P1",
           "喀什备份链路席位声音。", "与林海明显可辨。", "中性样本", "中音、简洁、冷静", "不适用", "独立音色验证", "第4、5、11、14场"),
    record("BY-VOI-P1-007-天衡测轨声音", "VOI", "天衡VLBI测轨稳定音色", "P1",
           "测轨网统一呼号声音。", "不等同于单一站点；语气偏数据校核。", "中性样本", "中低音、精确、无情绪化", "不适用", "独立音色验证", "第4、5、10、12、14场"),
    record("BY-VOI-P1-008-搜救指挥声音", "VOI", "搜救指挥稳定音色", "P1",
           "落点、空地接力和安全处置调度声音。", "与北京飞控主调度区分。", "中性样本", "中低音、现场调度感", "不适用", "独立音色验证", "第15—16场"),
    record("BY-VOI-P1-009-小天任务智能体声音", "VOI", "小天任务智能体稳定音色", "P1",
           "受限任务智能体的中性提示音色。", "不拟人化卖萌，不表现自主权威。", "中性样本", "清晰、中性、低情绪、短句", "不适用", "独立音色验证", "第1—15场"),
    record("BY-VOI-P1-010-北京地质席声音", "VOI", "北京地质席稳定音色", "P1",
           "月面路线与采样建议的科学席声音。", "与飞控主调度区分。", "中性样本", "专业、审慎、中等语速", "不适用", "独立音色验证", "第9场"),
    record("BY-VOI-P1-011-现场指挥声音", "VOI", "回收现场指挥稳定音色", "P1",
           "返回舱安全检查和开舱程序的现场声音。", "短句、明确、带现场通信质感。", "中性样本", "中音、清晰、无庆典语气", "不适用", "独立音色验证", "第16场"),
    record("BY-SND-P1-004-再入结构与通信衰减", "SND", "再入舱内结构与通信衰减", "P1",
           "再入振动、结构传导、无线电衰减与黑障噪声的同步生成约束。", "不独立制作基础音频。",
           "第一次再入；黑障；恢复", "低频结构声、通信噪声", "声音来自舱内与通信链路",
           "随镜头视频同步生成", "第15场"),
    record("BY-SND-P1-005-降落伞与着陆冲击", "SND", "降落伞气动与着陆冲击", "P1",
           "地球大气中的伞具气动、舱内冲击和地面接触声。", "不混入配乐。",
           "开伞；气囊触地；滚摆", "真实气动与结构声", "仅地球大气／舱内可传播",
           "随镜头视频同步生成", "第15场"),
    record("BY-SND-P1-006-搜救现场声", "SND", "搜救现场风声、车辆设备与远距通信", "P1",
           "回收现场的地球环境声和任务通信。", "不做英雄式音乐。",
           "接近；安全检查；开舱；终景", "自然风、车辆、设备、远距无线电", "地球大气环境",
           "随镜头视频同步生成", "第16场"),
    record("BY-SND-P1-007-月球车设备链路结构声", "SND", "月球车设备链路结构声", "P1",
           "经车载／通信设备传回的电机和结构振动。", "不是月面外部空气拾音。",
           "卸载；行驶；返程", "受限频带电机结构声", "通信链路来源",
           "随镜头视频同步生成", "第9场"),
    record("BY-SND-P1-008-飞控与测控大厅底噪", "SND", "飞控与测控大厅设备底噪", "P1",
           "北京飞控、深空测控和搜救指挥空间中的克制设备与席位环境声。", "不形成节奏性音乐。",
           "常态任务；关键节点", "低强度空调、设备风扇、键控与远距席位声", "地球室内环境",
           "随镜头视频同步生成", "地面系统场次"),
    record("BY-REL-P0-009-梦舟三座返航承载与环月工作位", "REL", "梦舟三座返航承载与环月工作位关系", "P0",
           "三把座椅组成同一承力与操作系统；刘定槎从中央任务席使用前上方共享控制区。", "相邻两张空座保留可识别边界，不增加第四个乘员位置。",
           "三人承载；一人留守两座空置；三人归位", "空间与岗位连续性", "梦舟舱内任务光",
           "梦舟所有舱内资产硬约束", "第1、3、9、11—15场"),
    record("BY-REL-P0-010-梦舟轴向转移顺序", "REL", "梦舟轴向通道人员／样品转移顺序", "P0",
           "第一次先任务物品后人员；第二次先主样品容器后人员。", "两侧舱门依次开闭并完成压差与密封检查。",
           "首次转移；再对接转移", "任务流程连续性", "舱内任务光",
           "通道场景和道具硬约束", "第3、13场"),
    record("BY-REL-P0-011-梦舟返地构型状态链", "REL", "梦舟月轨—地月转移—再入状态链", "P0",
           "月轨组合体—地月转移点火—三天巡航—服务舱近地分离—返回舱跳跃式再入—群伞／气囊—搜救。",
           "只有返回舱进入大气层。", "完整返地链", "航天器构型连续性", "外部光源随环境切换",
           "梦舟外部与再入资产硬约束", "第14—16场"),
    record("BY-REL-P0-012-月面艺术化光照与声明", "REL", "月面艺术化光照与推演声明关系", "P0",
           "保留2029年4月8日和锁定坐标；画面采用艺术化任务日光；声明承担天文偏差。", "生产光向不得被写成真实太阳方位。",
           "片头声明；月面全段；片尾声明", "光影／包装连续性", "月面艺术化任务日光",
           "阶段2A和阶段3禁止改写项", "镜001、第5—11场、镜114",
           status="用户已确认", phase2="所有月面资产和后期声明必须继承"),
    record("BY-REL-P0-013-返回舱再入搜救状态链", "REL", "返回舱再入、着陆与搜救状态链", "P0",
           "服务舱分离—两次再入—黑障—通信恢复—开伞—气囊着陆—安全检查—开舱—医学与样品接收。",
           "不把航天员落地立即站立庆祝。", "完整回收链", "状态连续性", "近地／大气／地面光影连续",
           "再入与搜救资产硬约束", "第15—16场"),
    record("BY-REL-P1-004-地面测控接力链", "REL", "北京—佳木斯—喀什—VLBI测控接力链", "P1",
           "北京总协调，佳木斯主链路，喀什备份与双目标，VLBI独立校核。", "近月正面着陆区以直达链路为主。",
           "交会；下降；月面；起飞；再交会；返回", "系统关系", "不适用",
           "地面场景、声音和镜头装配约束", "第1—15场"),
    record("BY-REL-P1-005-小天AI权限边界", "REL", "小天AI权限边界", "P1",
           "只做融合、预测、候选排序和异常提示；最终授权、选择与中止权属于乘组和北京。", "禁止全自动AI决策。",
           "交会；下降；复压；起飞；再入", "对白与界面连续性", "不适用",
           "所有出现小天的镜头硬约束", "全片"),
    record("BY-REL-P1-006-月面科学路线与样品链", "REL", "月面科学路线与样品编号链", "P1",
           "月球车路线、地面地质建议、编号采样、封装、主容器和回收接收闭环。", "地质结论保持审慎。",
           "路线；采样；封装；转移；接收", "道具／场景／后期连续性", "艺术化任务日光",
           "月面科学任务装配约束", "第9—10、13、16场"),
]


def load_assets():
    with OLD_ASSETS.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        asset_id = row["生产资产ID"]
        if asset_id in RETIRED:
            row["确认状态"] = "历史停用（V1.2不调用）"
            row["阶段2处理建议"] = RETIRED[asset_id]
            row["关联场次或段落"] = "历史V1.1"
        else:
            row["剧本出处"] = "V1.2逐镜映射见data/阶段1_114镜资产调用映射_V1.2.csv"
            row["确认状态"] = row["确认状态"] or "继承待复核"
        if asset_id in UPDATES:
            row.update(UPDATES[asset_id])
    rows.extend(NEW)
    return rows


SCENE_BLOCKS = [23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, 67, 71, 75, 79, 83]
SCENE_NAMES = [
    "月轨相遇", "环月对接", "人员与任务转移", "分离与降轨", "动力下降", "触月确认", "出舱准备", "第一步与国旗",
    "月面科学任务", "返舱与起飞准备", "月面起飞", "环月再交会", "三人重聚与揽月处置", "踏上归程", "跳跃式再入", "平安归来",
]


def add(target, *ids):
    target.update(x for x in ids if x)


def base_scene_assets(scene, shot):
    # Visual assets are assigned from what is actually visible in the current shot.
    # Do not inject a whole scene's default environment into title cards, interiors,
    # control-room inserts, or other shots where that environment is not on screen.
    return set(), set(), set(), set()


def classify_shot(scene, row):
    number, timecode, seconds, camera, image, audio, control = row
    shot = int(number)
    visual_text = " ".join((camera, image))
    all_text = " ".join((camera, image, audio, control))
    text = visual_text
    visual, voice, sound, post = base_scene_assets(scene, shot)

    # Scene and vehicle anchors.
    lunar_orbit_exterior_shots = {2, 8, 10, 11, 20, 21, 24, 25, 78, 84, 85, 87, 93, 95, 96, 98}
    lunar_surface_visible_shots = {
        27, 30, 32, 33, 34, 37, 38, 39, 42, 47, 48, 49, 50, 51, 52,
        53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 64, 66, 67, 68, 69, 74, 75,
    }
    reentry_visible_shots = {102, 104, 105, 106, 108}
    recovery_visible_shots = set(range(109, 115))
    if shot in lunar_orbit_exterior_shots:
        add(visual, "BY-SCN-P1-006-环月轨道外部环境", "BY-LGT-P1-004-环月轨道太阳光")
    if shot in lunar_surface_visible_shots:
        add(visual, "BY-SCN-P0-004-月面着陆与作业区", "BY-LGT-P0-004-月面艺术化任务日光")
    if shot in {58, 59, 60, 61, 62, 64, 66, 67}:
        add(visual, "BY-SCN-P1-005-月面后段科考区")
    if shot in reentry_visible_shots:
        add(visual, "BY-SCN-P0-007-返回舱再入视觉环境")
    if shot in recovery_visible_shots:
        add(visual, "BY-SCN-P0-008-预定着陆区与搜救现场", "BY-LGT-P1-007-搜救着陆区日间自然光")
    if any(k in text for k in ("梦舟舱内", "梦舟返回舱广角", "三把座椅", "三人固定", "返航构型")):
        add(visual, "BY-SCN-P0-001-梦舟舱内三座布局", "BY-LGT-P0-001-梦舟舱内任务光", "BY-PRP-P0-001-梦舟三座椅与束缚系统")
    if any(k in text for k in ("梦舟工作位", "轨道工作位", "返回舱前上部紧凑工作位", "梦舟交会界面")):
        add(visual, "BY-SCN-P0-005-梦舟环月工作位", "BY-LGT-P0-001-梦舟舱内任务光", "BY-PRP-P1-006-舱内操作界面与任务屏")
    if any(k in text for k in ("通道", "两侧舱门", "对接通道", "压差归零")) and scene in {3, 13}:
        add(visual, "BY-SCN-P0-002-梦舟对接通道与舱门区", "BY-PRP-P1-005-两器舱门与对接锁止结果件")
    if any(k in text for k in ("揽月舱内", "揽月双人", "舱内双人", "登月服准备", "舱压曲线", "舱内中景")) and scene in {1, 2, 3, 4, 5, 6, 7, 10, 11, 12}:
        add(visual, "BY-SCN-P0-003-揽月登月舱舱内", "BY-LGT-P0-002-揽月下降任务光", "BY-PRP-P1-006-舱内操作界面与任务屏")
    if scene in {2, 3, 4, 5, 6, 7, 10, 11, 12} and any(k in camera for k in ("舱内", "舱压", "舱门", "工具与清单")):
        add(visual, "BY-SCN-P0-003-揽月登月舱舱内", "BY-LGT-P0-002-揽月下降任务光")
    if any(k in text for k in ("北京飞控", "飞控多屏", "飞控广角", "长城：", "飞控屏幕", "各席位")):
        add(visual, "BY-SCN-P0-006-北京飞控大厅与任务主屏", "BY-LGT-P1-003-飞控大厅任务光", "BY-CRO-P1-001-北京飞控任务团队")
        add(sound, "BY-SND-P1-008-飞控与测控大厅底噪")
    if "飞控" in camera and not any(k in camera for k in ("媒体区", "地质席")):
        add(visual, "BY-SCN-P0-006-北京飞控大厅与任务主屏", "BY-LGT-P1-003-飞控大厅任务光", "BY-CRO-P1-001-北京飞控任务团队")
        add(sound, "BY-SND-P1-008-飞控与测控大厅底噪")
    if "媒体区" in text:
        add(visual, "BY-SCN-P1-003-飞控中心媒体区", "BY-CST-P1-004-林知夏记者服装")
    if any(k in text for k in ("佳木斯", "林海：")):
        add(visual, "BY-SCN-P1-007-佳木斯66米深空测控站", "BY-LGT-P1-006-深空测控站任务光", "BY-CRO-P1-002-深空测控值班团队")
    if any(k in text for k in ("喀什", "叶河：")):
        add(visual, "BY-SCN-P1-008-喀什35米深空测控站", "BY-LGT-P1-006-深空测控站任务光", "BY-CRO-P1-002-深空测控值班团队")
    if any(k in camera for k in ("天衡", "VLBI")):
        add(visual, "BY-SCN-P1-009-VLBI测轨席", "BY-LGT-P1-006-深空测控站任务光")
    if "地质席" in text:
        add(visual, "BY-SCN-P1-010-北京飞控地质席")
    if "搜救指挥" in text:
        add(visual, "BY-SCN-P1-011-搜救指挥中心")

    if shot in {2, 5, 8, 10, 11, 20, 21, 84, 85, 87, 93, 95, 96, 98}:
        add(visual, "BY-VEH-P0-005-梦舟月轨组合体")
    if shot in {2, 5, 8, 10, 11, 20, 21, 24, 25}:
        add(visual, "BY-VEH-P0-002-揽月完整构型")
    if shot == 25:
        add(visual, "BY-VEH-P1-003-揽月推进舱分离状态")
    if shot in {25, 27, 33, 37, 38, 39, 42, 47, 51, 54, 55, 57, 58, 67, 68, 74, 75}:
        add(visual, "BY-VEH-P0-003-揽月登月舱")
    if shot in {74, 75, 78}:
        add(visual, "BY-VEH-P1-004-揽月月面起飞状态")
    if shot in {84, 85, 87}:
        add(visual, "BY-VEH-P1-005-揽月月轨再对接状态", "BY-VEH-P0-005-梦舟月轨组合体")
    if scene == 13 and shot in {93, 95}:
        add(visual, "BY-VEH-P1-006-揽月受控处置状态", "BY-VFX-P1-006-揽月受控处置轨迹")
    if scene == 14 and shot in {96, 98}:
        add(visual, "BY-VEH-P0-005-梦舟月轨组合体", "BY-VFX-P1-003-月地转移点火与月球远离")
    if shot == 102:
        add(visual, "BY-VEH-P1-007-梦舟服务舱近地分离状态", "BY-VEH-P0-006-梦舟返回舱独立再入构型")
    if shot in {104, 105, 106, 108}:
        add(visual, "BY-VEH-P0-006-梦舟返回舱独立再入构型")
    if shot in {108, 109}:
        add(visual, "BY-VEH-P0-007-返回舱群伞气囊着陆构型")
    if scene == 16:
        add(visual, "BY-VEH-P0-007-返回舱群伞气囊着陆构型", "BY-CRO-P1-003-搜救与医疗团队")
    if shot == 110:
        add(visual, "BY-VEH-P1-008-搜救直升机与地面车辆")

    # Characters, clothing, props.
    lunar_suit_shots = set(range(44, 77))
    if "杨凛" in text or (scene in {6, 7, 8, 9, 10, 11, 12} and any(k in image for k in ("两人", "双人", "航天员"))):
        add(visual, "BY-CHR-P0-001-杨凛")
        add(visual, "BY-CST-P0-004-杨凛望宇登月服" if shot in lunar_suit_shots else "BY-CST-P0-001-杨凛舱内飞行服")
    if "陈砚" in text or (scene in {6, 7, 8, 9, 10, 11, 12} and any(k in image for k in ("两人", "双人", "航天员"))):
        add(visual, "BY-CHR-P0-002-陈砚")
        add(visual, "BY-CST-P0-005-陈砚望宇登月服" if shot in lunar_suit_shots else "BY-CST-P0-002-陈砚舱内飞行服")
    if "刘定槎" in text or (scene in {14, 15} and "三人" in image):
        add(visual, "BY-CHR-P0-003-刘定槎", "BY-CST-P0-003-刘定槎舱内飞行服")
    if scene == 13 and any(k in image for k in ("杨凛", "陈砚", "三人")):
        add(visual, "BY-CST-P1-001-杨凛登月服轻度月尘状态", "BY-CST-P1-002-陈砚登月服轻度月尘状态")
    if "林知夏" in text:
        add(visual, "BY-CHR-P1-002-林知夏", "BY-CST-P1-004-林知夏记者服装")

    if "月球车" in text:
        add(visual, "BY-VEH-P0-004-探索载人月球车", "BY-VFX-P1-007-月球车轮迹与低重力扬尘")
    if any(k in text for k in ("采样", "B-03", "样品袋")):
        add(visual, "BY-PRP-P1-001-月面采样工具", "BY-PRP-P1-002-月壤样品容器", "BY-SYM-P1-005-样品编号与封签模板")
    if any(k in text for k in ("主样品容器", "样品容器", "采样箱", "样品柜")):
        add(visual, "BY-PRP-P0-005-密封样品转移容器", "BY-PRP-P1-008-主样品容器编号与固定座")
    if "样品柜" in text:
        add(visual, "BY-PRP-P1-010-返回舱样品柜与锁止")
    if "污染控制" in text or "擦拭" in text:
        add(visual, "BY-PRP-P1-009-污染控制用品")
    if any(k in text for k in ("任务数据盒", "救生包")):
        add(visual, "BY-PRP-P1-007-任务数据盒与随身救生包")
    if any(k in text for k in ("国旗", "旗杆", "旗面")):
        add(visual, "BY-PRP-P0-004-工程化国旗展示装置", "BY-SYM-P0-001-中华人民共和国国旗图形")
    if any(k in text for k in ("科学载荷", "仪器布设", "载荷一号")):
        add(visual, "BY-PRP-P1-003-月面科学观测设备")
    if any(k in text for k in ("舷梯", "梯口", "下梯", "梯子")):
        add(visual, "BY-PRP-P0-002-揽月舷梯与扶手系统")
    if any(k in text for k in ("相机", "月面视频")) and scene in {7, 8, 9, 11}:
        add(visual, "BY-PRP-P0-003-便携式月面摄像机")
    if any(k in text for k in ("安全索", "应急返回索")):
        add(visual, "BY-PRP-P1-004-月面工具包与载荷固定系统")
    if scene == 16 and any(k in text for k in ("安全检查", "舱体温度", "信标")):
        add(visual, "BY-PRP-P1-011-返回舱信标与现场安全工具")

    # Physical effects.
    if any(k in text for k in ("接近", "姿控喷流", "分离")) and scene in {2, 4, 12, 13, 15}:
        add(visual, "BY-VFX-P1-004-姿控喷流")
    if shot in {5, 8, 10, 11, 84, 85, 87}:
        add(visual, "BY-VFX-P1-002-环月轨道交会与对接")
    if shot in {47, 48}:
        add(visual, "BY-LGT-P1-005-揽月开舱门月面反射")
    if scene == 5 and shot in {27, 37}:
        add(visual, "BY-VFX-P0-001-月面下降羽流与贴地月尘")
    if shot in {38, 39}:
        add(visual, "BY-VFX-P0-002-触月关机与月尘回落")
    if shot == 50:
        add(visual, "BY-VFX-P0-003-第一足印月壤形变")
    if scene == 11 and shot in {74, 75}:
        add(visual, "BY-VFX-P0-004-月面起飞羽流与留场余景")
    if shot in {104, 106, 108}:
        add(visual, "BY-VFX-P0-005-返回舱等离子辉光与黑障视觉", "BY-LGT-P0-005-返回舱再入等离子辉光")
    if shot in {104, 105, 106}:
        add(visual, "BY-VFX-P1-005-半弹道跳跃式再入轨迹")
    if shot == 108:
        add(visual, "BY-VFX-P0-006-稳定伞与主伞展开")
    if shot == 109:
        add(visual, "BY-VFX-P0-007-气囊触地滚摆")

    # Voice assets.
    voice_map = {
        "杨凛": "BY-VOI-P0-001-杨凛声音", "陈砚": "BY-VOI-P0-002-陈砚声音", "刘定槎": "BY-VOI-P0-003-刘定槎声音",
        "林知夏": "BY-VOI-P1-002-林知夏声音", "北京": "BY-VOI-P1-004-北京飞控主调度声音", "长城": "BY-VOI-P1-004-北京飞控主调度声音",
        "林海": "BY-VOI-P1-005-林海深空测控声音", "叶河": "BY-VOI-P1-006-叶河深空测控声音", "天衡": "BY-VOI-P1-007-天衡测轨声音",
        "搜救指挥": "BY-VOI-P1-008-搜救指挥声音", "小天": "BY-VOI-P1-009-小天任务智能体声音",
        "北京地质席": "BY-VOI-P1-010-北京地质席声音", "现场指挥": "BY-VOI-P1-011-现场指挥声音",
    }
    for key, asset_id in voice_map.items():
        if key == "北京" and "北京地质席" in audio:
            continue
        if key in audio:
            voice.add(asset_id)

    # Synchronous sound constraints.
    text = all_text
    if any(k in visual_text for k in ("舱内", "工作位", "返回舱广角", "返回舱内", "舱内反应", "梦舟交会界面")):
        sound.add("BY-SND-P0-001-舱内生命保障与设备底噪")
    mission_speakers = ("杨凛", "陈砚", "刘定槎", "北京", "长城", "林海", "叶河", "天衡", "小天", "地质席")
    if any(k in audio for k in mission_speakers) or any(k in audio for k in ("任务通信", "无线电")):
        sound.add("BY-SND-P0-002-地月无线电通信质感")
    if any(k in visual_text for k in ("对接口", "捕获特写", "舱门", "通道")) or "结构传导声" in audio:
        sound.add("BY-SND-P1-001-舱门对接机构结构传导")
    if shot != 43 and scene in {7, 8, 9, 10, 11} and (
        any(k in audio for k in ("呼吸", "杨凛", "陈砚"))
        or any(k in visual_text for k in ("航天员", "两人", "登月服", "杨凛", "陈砚", "靴底"))
    ):
        sound.add("BY-SND-P1-002-登月服内部呼吸与结构声")
    if any(k in text for k in ("发动机", "推力", "点火")) and (
        "舱内" in visual_text or "舱内" in audio
    ):
        sound.add("BY-SND-P1-003-发动机舱内结构振动")
    if shot in {102, 103, 104, 105, 106, 108}:
        sound.add("BY-SND-P1-004-再入结构与通信衰减")
    if shot in {108, 109}:
        sound.add("BY-SND-P1-005-降落伞与着陆冲击")
    if scene == 16:
        sound.add("BY-SND-P1-006-搜救现场声")
    if "月球车" in text:
        sound.add("BY-SND-P1-007-月球车设备链路结构声")

    # Post-production graphic assets.
    text = visual_text
    if shot == 65:
        for asset_id in (
            "BY-PRP-P0-005-密封样品转移容器",
            "BY-PRP-P1-001-月面采样工具",
            "BY-PRP-P1-002-月壤样品容器",
            "BY-PRP-P1-008-主样品容器编号与固定座",
            "BY-SYM-P1-005-样品编号与封签模板",
        ):
            visual.discard(asset_id)
    if "字幕" in text and shot != 114:
        post.add("BY-SYM-P1-003-任务阶段与时间跳跃标牌")
    if any(k in text for k in ("轨道图", "路线图", "轨迹图", "坐标", "界面", "主屏", "屏幕", "状态屏", "参数", "曲线", "点云")):
        post.add("BY-SYM-P1-004-任务轨迹与相位图模板")
    if shot in {1, 114}:
        post.add("BY-SYM-P0-002-艺术化光照偏差推演声明")
        post.add("BY-SYM-P1-001-未来纪实推演标识")
    return {
        "镜号": number, "场次": str(scene), "场名": SCENE_NAMES[scene - 1], "时间码": timecode,
        "景别／机位": camera, "画面动作摘要": image,
        "所需视觉资产ID": ";".join(sorted(visual)), "所需人物音色ID": ";".join(sorted(voice)),
        "同步声音约束ID": ";".join(sorted(sound)), "后期文字／图形资产ID": ";".join(sorted(post)),
        "资产状态": "V1.2提取已终审；待阶段2B设计与确认可调用", "专业控制": control,
    }


def build_shots():
    data = json.loads(SCRIPT_JSON.read_text(encoding="utf-8"))
    shots = []
    for scene, block_number in enumerate(SCENE_BLOCKS, 1):
        for row in data["blocks"][block_number - 1]["rows"][1:]:
            shots.append(classify_shot(scene, row))
    assert len(shots) == 114
    assert [int(x["镜号"]) for x in shots] == list(range(1, 115))
    return shots


VIEWS = [
    ("BY-SCN-P0-001-梦舟舱内三座布局", "梦舟返回舱三座承力区", "SV1", "局部母图只锁座椅／材料／控制关系", "是", "MASTER;SEAT-BACK;RETURN-THREE", "CONTROL-LOCAL", "否", "人物入座局部;约束系统特写", "已确认推荐口径"),
    ("BY-SCN-P0-005-梦舟环月工作位", "梦舟返回舱环月工作位", "SV1", "留守、目标捕获和再交会反复使用", "是", "MASTER;WORK-FRONT;WORK-OTS", "DISPLAY-LOCAL", "否", "刘定槎操作手部;生命体征页面后期", "已确认推荐口径"),
    ("BY-SCN-P0-002-梦舟对接通道与舱门区", "梦舟—揽月轴向对接转移通道", "SV1", "两次转移需轴线双向和交接局部", "是", "MASTER;AXIS-DREAM;AXIS-LANYUE;TRANSFER", "LOCK-LOCAL", "否", "样品转移架;舱门压差局部", "已确认推荐口径"),
    ("BY-SCN-P0-003-揽月登月舱舱内", "揽月登月舱舱内", "SV2", "下降、EVA、起飞和再交会状态复杂", "是", "MASTER;FRONT;BACK;LEFT;RIGHT;TOP", "HATCH;LOAD-BAY", "是", "双人约束;登月服检查;样品固定", "继承已确认"),
    ("BY-SCN-P0-006-北京飞控大厅与任务主屏", "北京飞控大厅与任务主屏", "SV1", "多场复用但机位集中于大厅、主屏和核心席", "是", "MASTER;FLOOR;MAIN-SCREEN;CONSOLE", "MEDIA-LINK", "否", "手部;眼神;状态闭合局部", "已确认推荐口径"),
    ("BY-SCN-P1-007-佳木斯66米深空测控站", "佳木斯66米深空测控站", "SV1", "需要天线长焦与值班工作区", "是", "MASTER;ANTENNA-LONG;OPS", "SCREEN-LOCAL", "否", "天线结构局部", "已确认推荐口径"),
    ("BY-SCN-P1-008-喀什35米深空测控站", "喀什35米深空测控站", "SV1", "需要与佳木斯可区分的天线跟踪状态", "是", "MASTER;ANTENNA-LONG;OPS", "", "否", "双目标跟踪屏后期", "已确认推荐口径"),
    ("BY-SCN-P1-009-VLBI测轨席", "VLBI测轨席／天衡界面", "SV0", "只作席位和界面局部切入", "是", "MASTER", "CONSOLE", "否", "屏幕局部", "已确认推荐口径"),
    ("BY-SCN-P1-010-北京飞控地质席", "北京飞控地质席", "SV0", "只用于地质席与月面分屏", "是", "MASTER", "SPLIT-SCREEN", "否", "路线标注局部", "已确认推荐口径"),
    ("BY-SCN-P1-003-飞控中心媒体区", "飞控中心媒体区", "SV0", "记者正面单向使用", "是", "MASTER", "", "否", "记者近景;背景屏局部", "继承已确认"),
    ("BY-SCN-P0-004-月面着陆与作业区", "月面着陆与作业区", "SV2", "覆盖下降、着陆、EVA、国旗、返舱与起飞", "是", "MASTER;FRONT;BACK;LEFT;RIGHT;TOP", "FLAG;LADDER;LANDING-CAMERA", "是", "足印;羽流低机位;国旗区;外平台", "继承视图等级；光影重新校准"),
    ("BY-SCN-P1-005-月面后段科考区", "月面科学任务路线与采样点", "SV1", "路线、采样点和载荷布设需连续", "是", "MASTER;PATH-FRONT;PATH-SIDE;PATH-TOP", "SAMPLE-POINT", "否", "车轮局部;手部采样", "已确认推荐口径"),
    ("BY-SCN-P1-006-环月轨道外部环境", "环月轨道外部环境", "SV1", "两次交会、分离、处置和地月转移共用", "是", "MASTER;DOCK-AXIS;MOON-LIMB;SEPARATION", "EARTH-DOT", "否", "对接口;服务舱点火", "继承已确认"),
    ("BY-SCN-P0-007-返回舱再入视觉环境", "返回舱再入视觉环境", "SV1", "需覆盖两次再入和开伞前后状态", "是", "MASTER;FIRST-ENTRY;SKIP;SECOND-ENTRY;PARACHUTE", "PLASMA-LOCAL", "否", "防热大底;辉光局部", "已确认推荐口径"),
    ("BY-SCN-P1-011-搜救指挥中心", "返回器搜救指挥中心", "SV0", "只用于落点和空地调度", "是", "MASTER", "MAIN-SCREEN", "否", "调度席局部", "已确认推荐口径"),
    ("BY-SCN-P0-008-预定着陆区与搜救现场", "预定着陆区与搜救现场", "SV1", "航拍、长焦、开舱和终景方向明确", "是", "MASTER;AERIAL;LONG-LENS;HATCH-MEDICAL", "FINAL-WIDE", "否", "气囊触地;舱体检查;样品接收", "已确认推荐口径"),
]


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    assets = load_assets()
    shots = build_shots()

    usage = defaultdict(lambda: {"scenes": set(), "shots": []})
    for shot in shots:
        for column in ("所需视觉资产ID", "所需人物音色ID", "同步声音约束ID", "后期文字／图形资产ID"):
            for asset_id in filter(None, shot[column].split(";")):
                usage[asset_id]["scenes"].add(int(shot["场次"]))
                usage[asset_id]["shots"].append(shot["镜号"])
    for row in assets:
        asset_id = row["生产资产ID"]
        if asset_id in usage and asset_id not in RETIRED:
            scenes = sorted(usage[asset_id]["scenes"])
            row["关联场次或段落"] = "场" + ",".join(str(x) for x in scenes) + "；镜" + ",".join(usage[asset_id]["shots"])

    change_rows = []
    for asset_id, reason in RETIRED.items():
        change_rows.append({"旧生产资产ID": asset_id, "V1.2处置": "历史停用", "新生产资产ID": "", "原因": reason})
    change_rows.extend([
        {"旧生产资产ID": "BY-SCN-P1-004-北京飞控中心大厅", "V1.2处置": "升级并替代", "新生产资产ID": "BY-SCN-P0-006-北京飞控大厅与任务主屏", "原因": "V1.2贯穿关键节点，升级为P0"},
        {"旧生产资产ID": "BY-LGT-P0-003-月面固定太阳光", "V1.2处置": "语义失效并替代", "新生产资产ID": "BY-LGT-P0-004-月面艺术化任务日光", "原因": "保留日期并显式承担天文偏差"},
        {"旧生产资产ID": "BY-REL-P0-004-刘定槎与两张空座椅", "V1.2处置": "叙事关系失效并替代", "新生产资产ID": "BY-REL-P0-009-梦舟三座返航承载与环月工作位", "原因": "空座椅仅等待乘组归位"},
    ])

    view_rows = []
    for asset_id, name, level, reason, master, required, extra, five, sv3, status in VIEWS:
        prefix = asset_id + "-V"
        ids = []
        for code in filter(None, required.split(";")):
            ids.append(f"{prefix}-{code}")
        view_rows.append({
            "场景生产资产ID": asset_id, "场景名称": name, "视图ID前缀": prefix,
            "视图需求等级建议": level, "建议原因": reason, "母图是否必需": master,
            "指定必需视图": required, "建议补充视图": extra, "是否建议标准五视图": five,
            "阶段3可能追加专项视图": sv3, "用户确认的视图需求等级": level,
            "用户确认的视图清单": required, "用户确认的场景视图ID清单": ";".join(ids), "确认状态": status,
        })

    scene_rows = []
    for scene in range(1, 17):
        scene_shots = [s for s in shots if int(s["场次"]) == scene]
        visual = sorted({x for s in scene_shots for x in s["所需视觉资产ID"].split(";") if x})
        voices = sorted({x for s in scene_shots for x in s["所需人物音色ID"].split(";") if x})
        sounds = sorted({x for s in scene_shots for x in s["同步声音约束ID"].split(";") if x})
        posts = sorted({x for s in scene_shots for x in s["后期文字／图形资产ID"].split(";") if x})
        scene_rows.append({
            "场次编号": str(scene), "场名": SCENE_NAMES[scene - 1],
            "镜号范围": f"{scene_shots[0]['镜号']}-{scene_shots[-1]['镜号']}",
            "所需视觉资产ID": ";".join(visual), "所需人物音色ID": ";".join(voices),
            "同步声音约束ID": ";".join(sounds), "后期文字／图形资产ID": ";".join(posts),
            "阶段2B资产状态": "需求已映射；资产尚待逐项设计并确认可调用",
        })

    write_csv(DATA / "阶段1_资产统计表_V1.2.csv", assets, FIELDS)
    write_csv(DATA / "阶段1_资产变更映射表_V1.2.csv", change_rows, ["旧生产资产ID", "V1.2处置", "新生产资产ID", "原因"])
    write_csv(DATA / "阶段1_场景视图需求表_V1.2.csv", view_rows, list(view_rows[0].keys()))
    write_csv(DATA / "阶段1_114镜资产调用映射_V1.2.csv", shots, list(shots[0].keys()))
    write_csv(DATA / "阶段1_场次资产需求映射_V1.2.csv", scene_rows, list(scene_rows[0].keys()))

    all_ids = {row["生产资产ID"] for row in assets}
    referenced_ids = set()
    for shot in shots:
        for column in ("所需视觉资产ID", "所需人物音色ID", "同步声音约束ID", "后期文字／图形资产ID"):
            referenced_ids.update(filter(None, shot[column].split(";")))
    missing_ids = sorted(referenced_ids - all_ids)
    retired_referenced = sorted(referenced_ids & set(RETIRED))
    assert not missing_ids, f"shot mapping references missing IDs: {missing_ids}"
    assert not retired_referenced, f"shot mapping references retired IDs: {retired_referenced}"

    counts = defaultdict(int)
    active = 0
    retired = 0
    for row in assets:
        counts[f"{row['资产类型']}_{row['资产级别']}"] += 1
        if row["确认状态"].startswith("历史停用"):
            retired += 1
        else:
            active += 1
    report = {
        "asset_total": len(assets), "active_assets": active, "retired_assets": retired,
        "new_assets": len(NEW), "shot_rows": len(shots), "scene_rows": len(scene_rows),
        "view_rows": len(view_rows), "referenced_asset_ids": len(referenced_ids),
        "missing_referenced_ids": missing_ids, "retired_referenced_ids": retired_referenced,
        "counts_by_type_and_level": dict(sorted(counts.items())),
    }
    out = Path(__file__).with_name("asset_counts.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
