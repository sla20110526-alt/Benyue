from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "_asset_reanalysis_v131"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
HANDOFF = ROOT / "handoff"
sys.path.insert(0, str(ROOT / "outputs" / "_script_revision_v131"))

import v131_content as v131  # noqa: E402


ASSET_COLUMNS = [
    "生产资产ID",
    "资产类型",
    "资产名称",
    "资产级别",
    "剧本出处",
    "关联场次或段落",
    "基础描述",
    "补全设计信息",
    "状态变体",
    "材质结构或声音特点",
    "光影或环境要求",
    "使用或生成需求",
    "可复用范围",
    "信息来源",
    "确认状态",
    "阶段2处理建议",
]

MAPPING_COLUMNS = [
    "镜号",
    "场次",
    "场名",
    "时间码",
    "时长秒",
    "景别／机位",
    "画面动作摘要",
    "关键状态／变体",
    "摄影来源等级",
    "所需视觉资产ID",
    "所需人物音色ID",
    "同步声音约束ID",
    "后期文字／图形资产ID",
    "资产状态",
    "专业控制",
]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def asset_row(
    asset_id: str,
    asset_type: str,
    name: str,
    priority: str,
    source: str,
    scenes: str,
    base: str,
    design: str,
    states: str,
    material: str,
    light: str,
    use: str,
    reuse: str,
    info: str = "V1.3.1正式分镜稿＋公开资料边界内艺术推演",
    status: str = "阶段1已确认生产方向",
    stage2: str = "阶段2B建立母资产并按镜头状态派生",
) -> dict[str, str]:
    return dict(
        zip(
            ASSET_COLUMNS,
            [
                asset_id,
                asset_type,
                name,
                priority,
                source,
                scenes,
                base,
                design,
                states,
                material,
                light,
                use,
                reuse,
                info,
                status,
                stage2,
            ],
        )
    )


UPDATES: dict[str, dict[str, str]] = {
    "BY-SCN-P0-001-梦舟舱内三座布局": {
        "资产名称": "梦舟返回舱三座承力区与四种乘员状态",
        "关联场次或段落": "第1—3、5、11、14—15场",
        "补全设计信息": "同一三座承力布局保持几何不变，以人物占位、束缚状态、样品固定和着陆姿态区分四种叙事状态。",
        "状态变体": "A三座满员对接前；B一人工作两座空置；C三人重聚含样品；D三人返航承载／再入／着陆",
        "使用或生成需求": "必须建立一张统一母图和四种状态图；座椅方向、间距、工作界面和舱门轴线不得漂移。",
        "阶段2处理建议": "阶段2B优先生成母资产与四状态对照板",
    },
    "BY-SCN-P0-005-梦舟环月工作位": {
        "关联场次或段落": "第1—3、5、11场",
        "状态变体": "三人协同；刘定槎单人环月值守；三人重聚",
        "使用或生成需求": "工作位与三座承力区必须属于同一返回舱空间，不生成宽阔独立驾驶舱。",
    },
    "BY-SCN-P0-008-预定着陆区与搜救现场": {
        "资产名称": "东风着陆场与搜救现场",
        "关联场次或段落": "第13—15场",
        "基础描述": "东风着陆场荒漠回收区、预报走廊、直升机与车组、警戒区、返回舱开舱区。",
        "状态变体": "再入待命；目标跟踪；返回舱着陆；搜救抵达；安全处置；开舱与转移",
        "光影或环境要求": "黎明至清晨的自然光连续；风沙、尘土和远距能见度真实。",
    },
    "BY-LGT-P1-007-搜救着陆区日间自然光": {
        "资产名称": "东风着陆场黎明—清晨自然光",
        "关联场次或段落": "第13—15场",
        "基础描述": "东风着陆场从黎明低照度到清晨自然光的连续光线。",
        "状态变体": "待命黎明；下降可见；着陆扬尘；搜救清晨",
    },
    "BY-PRP-P0-001-梦舟三座椅与束缚系统": {
        "关联场次或段落": "第1—3、5、11、14—15场",
        "状态变体": "三座满员；两座空置锁定；三人重聚；再入载荷承载；着陆缓冲",
        "使用或生成需求": "同一套座椅保持承力骨架、基座和朝向稳定，四种状态只改变人员、束缚、靠背角度与载荷状态。",
        "阶段2处理建议": "与梦舟舱内母资产同步设计，禁止独立生成三张互不兼容座椅图",
    },
    "BY-PRP-P0-003-便携式月面摄像机": {
        "关联场次或段落": "第8—11场",
        "补全设计信息": "折叠三脚架、可戴手套操作的锁止件、服外图像链路确认界面；部署于揽月侧前方安全距离。",
        "状态变体": "舱外取出；双人部署；固定全景；延时记录；起飞留场空镜",
        "使用或生成需求": "镜60部署后，镜61、63—64、69、76、81必须复用同一机位与同一设备。",
    },
    "BY-PRP-P1-006-舱内操作界面与任务屏": {
        "关联场次或段落": "梦舟、揽月与飞控任务镜头",
        "补全设计信息": "显示轨道、姿态、相对导航、生命保障、样品固定与再入参数；信息密度真实但不伪造官方界面。",
        "使用或生成需求": "建立可读但非官方复刻的统一任务UI组件库；屏幕保持工作状态。",
    },
    "BY-VOI-P1-008-搜救指挥声音": {
        "资产名称": "东风着陆场调度／搜救指挥稳定音色",
        "关联场次或段落": "第13—15场",
        "基础描述": "直播呼号“东风”的着陆场调度、目标跟踪和搜救指挥通话。",
        "使用或生成需求": "独立音色资产；正式镜头中的通话随视频同步生成。",
    },
    "BY-SYM-P1-003-任务阶段与时间跳跃标牌": {
        "关联场次或段落": "第1、4、7、10—13、15场",
        "状态变体": "日期；T+06:00；T+13:40；T+28:00；离月约三天；搜救时间压缩",
        "使用或生成需求": "时间标牌必须与119镜时间线一致，并显式区分直播、延时和视觉重建。",
    },
    "BY-REL-P0-009-梦舟三座返航承载与环月工作位": {
        "资产名称": "梦舟三座四种乘员状态与环月工作位关系",
        "关联场次或段落": "第1—3、5、11、14—15场",
        "基础描述": "同一返回舱内三座承力区、环月工作位、舱门轴线和样品固定位置的连续关系。",
        "状态变体": "三座满员→一人值守两座空置→三人重聚→三人返航承载",
        "使用或生成需求": "作为梦舟所有镜头的强连续性约束；不得生成三人并排占满通道或座椅朝向漂移。",
    },
    "BY-REL-P0-006-月面摄像机摄影来源": {
        "关联场次或段落": "第8—11场",
        "状态变体": "部署前：揽月／宇航服任务相机；部署后：同一便携相机；科研：月球车与宇航服相机",
        "使用或生成需求": "任何第三视角都必须能追溯到已部署设备或显式遥测视觉重建。",
    },
}


NEW_ASSETS = [
    asset_row(
        "BY-CHR-P1-004-何文澜",
        "CHR",
        "何文澜",
        "P1",
        "镜20、48—50、79、113",
        "第3、7、11、15场",
        "载人航天与航天医学方向专家。",
        "媒体区采访状态严谨、平实，医学解释可作画外。",
        "媒体区出镜；专家画外",
        "真实人物皮肤、自然职业妆发",
        "媒体区中性任务光",
        "建立正面、三分之四与双人采访构图",
        "媒体区采访与医学解释",
    ),
    asset_row(
        "BY-CHR-P1-005-孙亦川",
        "CHR",
        "孙亦川",
        "P1",
        "镜35、88、93、100",
        "第6、12—14场",
        "轨道动力学与返回再入方向专家。",
        "通过轨迹图解释下降、月地返回和跳跃式再入。",
        "媒体区出镜；轨迹图前出镜；专家画外",
        "真实人物皮肤、自然职业妆发",
        "媒体区中性任务光",
        "与历史停用角色“孙屹川”严格区分，不复用旧脸与旧音色",
        "轨迹、下降与再入解释",
    ),
    asset_row(
        "BY-CHR-P1-006-顾青岚",
        "CHR",
        "顾青岚",
        "P1",
        "镜66—67、72",
        "第9—10场",
        "月球地质与月面科学方向专家。",
        "结合艺术锁定着陆点解释地质单元和短程科学路线。",
        "媒体区出镜；地质图卡画外",
        "真实人物皮肤、自然职业妆发",
        "媒体区中性任务光",
        "建立与地质图双人采访和指图动作",
        "月面科学解释",
    ),
    asset_row(
        "BY-CST-P1-006-何文澜专家服装",
        "CST",
        "何文澜专家服装",
        "P1",
        "镜20、48、113",
        "第3、7、15场",
        "深色或中性低饱和职业正装。",
        "不使用夸张科幻制服。",
        "站立采访；医学画外无画面",
        "哑光织物",
        "媒体区中性任务光",
        "与何文澜人物资产绑定",
        "同一直播日采访",
    ),
    asset_row(
        "BY-CST-P1-007-孙亦川专家服装",
        "CST",
        "孙亦川专家服装",
        "P1",
        "镜35、88、93",
        "第6、12—13场",
        "低饱和职业正装。",
        "能与深蓝轨迹图分离轮廓。",
        "下降讲解；返回讲解；再入讲解",
        "哑光织物",
        "媒体区中性任务光",
        "与孙亦川人物资产绑定",
        "多段直播采访",
    ),
    asset_row(
        "BY-CST-P1-008-顾青岚专家服装",
        "CST",
        "顾青岚专家服装",
        "P1",
        "镜66",
        "第9场",
        "专业、简洁的地质专家采访服装。",
        "色彩不与月面地质图冲突。",
        "媒体区采访",
        "哑光织物",
        "媒体区中性任务光",
        "与顾青岚人物资产绑定",
        "月面科学采访",
    ),
    asset_row(
        "BY-VOI-P1-012-何文澜声音",
        "VOI",
        "何文澜稳定音色",
        "P1",
        "镜20、48—50、79、113",
        "第3、7、11、15场",
        "冷静、温和、医学解释清楚的中年专家音色。",
        "采访和画外保持同一身份。",
        "媒体区原声；专家画外",
        "无夸张播音腔",
        "近讲收音，轻媒体区底噪",
        "独立制作、确认和登记；正式镜头对白同步生成",
        "何文澜所有台词",
    ),
    asset_row(
        "BY-VOI-P1-013-孙亦川声音",
        "VOI",
        "孙亦川稳定音色",
        "P1",
        "镜35、88、93、100",
        "第6、12—14场",
        "逻辑清晰、节奏克制的轨道动力学专家音色。",
        "与历史停用“孙屹川”音色彻底隔离。",
        "媒体区原声；专家画外",
        "不使用激昂新闻腔",
        "近讲收音",
        "独立制作、确认和登记；正式镜头对白同步生成",
        "孙亦川所有台词",
    ),
    asset_row(
        "BY-VOI-P1-014-顾青岚声音",
        "VOI",
        "顾青岚稳定音色",
        "P1",
        "镜66—67、72",
        "第9—10场",
        "清晰、沉稳的月球地质专家音色。",
        "采访与科学画外连续。",
        "媒体区原声；专家画外",
        "自然语言节奏",
        "近讲收音",
        "独立制作、确认和登记；正式镜头对白同步生成",
        "顾青岚所有台词",
    ),
    asset_row(
        "BY-VOI-P1-015-医监人员声音",
        "VOI",
        "东风医监人员稳定音色",
        "P1",
        "镜114",
        "第15场",
        "现场医监人员的短句程序口令。",
        "与现场指挥、东风调度保持可辨识差异。",
        "舱门开启前后",
        "现场对讲质感",
        "东风清晨户外",
        "独立登记；正式镜头通话同步生成",
        "开舱医学评估",
    ),
    asset_row(
        "BY-SCN-P1-012-东风医监开舱作业区",
        "SCN",
        "东风医监医保与开舱作业区",
        "P1",
        "镜112—117",
        "第15场",
        "返回舱外警戒、开舱、人员评估、支撑转移与样品交接的连续工作区。",
        "保持返回舱、医监点、座椅／担架、样品接收和车辆通道的空间关系。",
        "安全处置；开舱；逐人评估；座椅／担架转移；样品交接",
        "荒漠地表、专业救援器材、低反射工作服",
        "黎明至清晨自然光",
        "建立俯视总图、开舱侧视、医疗转移和样品交接四类视图",
        "东风回收段",
    ),
    asset_row(
        "BY-LGT-P1-008-飞控媒体区直播光",
        "LGT",
        "飞控媒体区直播任务光",
        "P1",
        "记者与专家直播镜头",
        "第1、3、5—9、12—13、15场",
        "中性、可信的新闻现场光，兼顾记者肤色、专家和任务大屏。",
        "三段直播保持连续，允许大屏亮度随任务阶段变化。",
        "记者单人；记者专家双人；片尾收束",
        "柔和主光、轻轮廓、屏幕补光",
        "室内稳定光",
        "建立统一灯位，不随每次生成漂移",
        "全部媒体区镜头",
    ),
    asset_row(
        "BY-PRP-P0-006-东风医监转移设备",
        "PRP",
        "东风医监支撑座椅、担架与生命体征设备",
        "P0",
        "镜113—116",
        "第15场",
        "航天员出舱后的循环、平衡和运动状态评估及转移设备。",
        "座椅、担架、便携生命体征监测、遮护和固定带属于同一现场套装。",
        "舱外待命；逐人评估；座椅转移；担架转移；坐姿挥手",
        "医疗级织物、轻质金属、易消毒表面",
        "东风清晨自然光",
        "人物状态决定座椅或担架，不允许航天员立即自行步行出舱",
        "返回舱医监回收",
    ),
    asset_row(
        "BY-PRP-P1-012-月球车任务相机组",
        "PRP",
        "月球车前向与侧后固定相机组",
        "P1",
        "镜68、70、72、74—75",
        "第9—10场",
        "探索载人月球车的前向导航相机与侧后任务记录相机。",
        "机位与车体结构绑定，视野高度、畸变和遮挡稳定。",
        "前向行驶；侧后科研；返程",
        "航天级相机外壳与防尘镜罩",
        "月面艺术化任务日光",
        "所有月球车视角复用同一标定参数",
        "月面科研镜头",
    ),
    asset_row(
        "BY-PRP-P1-013-东风样品接收设备",
        "PRP",
        "东风样品接收箱、封签与交接设备",
        "P1",
        "镜94、117",
        "第13、15场",
        "月球样品密封转运的现场接收箱、编号、封签和交接记录件。",
        "与主样品容器编号链一致。",
        "待命检查；编号交接；转运",
        "密封箱、标识牌、封签和记录终端",
        "东风清晨自然光",
        "与BY-SYM-P1-005共同使用",
        "样品回收段",
    ),
    asset_row(
        "BY-PRP-P1-014-宇航服任务相机",
        "PRP",
        "望宇登月服任务相机与图像链路",
        "P1",
        "镜55、57、60、62、71、73—74",
        "第8—10场",
        "固定于登月服的第一视角任务记录相机。",
        "随人物绑定，保持视野高度、手套遮挡和运动节奏一致。",
        "扶梯；安全检查；采样；钻取；载荷部署",
        "航天级相机壳体",
        "月面艺术化任务日光",
        "分别绑定杨凛与陈砚服装资产",
        "月面第一视角",
    ),
    asset_row(
        "BY-PRP-P1-015-航天器任务相机组",
        "PRP",
        "梦舟／揽月任务相机组",
        "P1",
        "对接口、下视、着陆腿、外部固定及返回外部任务镜头",
        "第2、5—8、11、14场",
        "对接口监视、揽月下视与着陆腿、舱外固定、梦舟外部返回任务相机。",
        "每类相机固定在可解释位置，画面畸变、遮挡和相对运动一致。",
        "对接；分离；下降；触月；出舱；再对接；返回",
        "航天级相机外壳与光学窗口",
        "随载具环境变化",
        "任务证据视角优先于视觉重建",
        "航天器关键动作证明",
    ),
    asset_row(
        "BY-VFX-P1-008-遥测视觉重建合成",
        "VFX",
        "基于实时遥测的视觉重建合成",
        "P1",
        "所有标注“视觉重建”的镜头",
        "第1—2、4—7、11—14场",
        "以轨道、姿态、距离和时间数据重建无法由实体任务相机直接拍到的外部全景。",
        "画面角落始终保留统一来源标识，运动克制，不模拟追逐摄影机。",
        "环月对接；分离下降；着陆全景；月面上升；再入",
        "与载具母资产和轨迹数据绑定",
        "环月、月面与再入环境",
        "不得替代接触、触月、出舱、再对接等任务证据镜头",
        "全片视觉重建",
    ),
    asset_row(
        "BY-SYM-P1-006-视觉重建来源标识",
        "SYM",
        "“基于实时遥测的视觉重建”来源标识",
        "P1",
        "所有视觉重建镜头",
        "第1—2、4—7、11—14场",
        "明确区分艺术重建与任务相机实拍逻辑的角标。",
        "位置、字号、显隐时长全片统一。",
        "常驻角标；镜头起始淡入；结束淡出",
        "简洁中性图形",
        "适配深空、月面和等离子高亮背景",
        "后期叠加，不写入载具屏幕",
        "所有遥测视觉重建",
    ),
    asset_row(
        "BY-SYM-P1-007-直播进口出口与倒计时",
        "SYM",
        "三段直播进口、出口与任务倒计时图形",
        "P1",
        "镜3、22、27、47、51、87、92、118",
        "三段直播",
        "记者开场、阶段提示、五分钟倒计时和直播收束的统一图形系统。",
        "不包装成娱乐综艺；不使用新闻提示音。",
        "直播开始；任务阶段；倒计时；直播结束",
        "中性、克制、可读",
        "媒体区大屏与后期字幕",
        "与任务时间标牌统一设计语言",
        "直播结构",
    ),
    asset_row(
        "BY-SYM-P1-008-东风搜救时间压缩",
        "SYM",
        "东风搜救抵达时间压缩标牌",
        "P1",
        "镜110",
        "第15场",
        "明确提示搜救分队抵达和安全处置为时间压缩。",
        "避免观众误解为落地后数秒即开舱。",
        "黑场文字；任务画面转接",
        "高可读文字",
        "黑场",
        "给足阅读时间",
        "回收段",
    ),
    asset_row(
        "BY-SND-P1-009-媒体区直播现场声",
        "SND",
        "飞控媒体区直播现场声",
        "P1",
        "记者与专家镜头",
        "三段直播",
        "低声工作环境、轻空调底噪、现场掌声与人物近讲。",
        "关键任务动作期间不以媒体区声覆盖无线电。",
        "开场安静；采访；克制掌声；片尾收束",
        "真实室内空间声",
        "飞控媒体区",
        "无配乐、无新闻提示音",
        "媒体区镜头",
    ),
    asset_row(
        "BY-REL-P1-007-摄影来源证据层级",
        "REL",
        "任务相机、地面直播、遥测重建与图卡证据层级",
        "P1",
        "119镜全片",
        "全片",
        "A任务证据机位、B地面直播机位、C显式遥测视觉重建、D后期图卡四层来源。",
        "不可逆节点优先A层；C层必须标识；D层只解释。",
        "四层摄影来源",
        "关系资产",
        "全片",
        "写入每镜摄影来源等级",
        "镜头设计与后期合成",
    ),
    asset_row(
        "BY-REL-P1-008-三段直播结构链",
        "REL",
        "三段直播进口、关键动作链、采访解释与出口",
        "P1",
        "第1—15场",
        "全片",
        "记者事件前解释、任务关键动作、事件后采访、字幕跳时四种结构单元。",
        "采访不覆盖不可逆任务节点；重复确认可由采访或图卡压缩。",
        "直播一；直播二；直播三",
        "关系资产",
        "全片",
        "作为剪辑与声音节奏约束",
        "全片直播结构",
    ),
    asset_row(
        "BY-REL-P1-009-东风医监与样品双线",
        "REL",
        "东风人员医监转移与样品交接双线",
        "P1",
        "镜110—118",
        "第15场",
        "人员安全处置、逐人评估、座椅／担架转移与样品编号交接并行闭合。",
        "任务完成必须同时满足乘组三人安全与样品完成交接。",
        "安全处置；医学评估；人员转移；样品交接；任务闭合",
        "关系资产",
        "东风回收现场",
        "镜117合流",
        "回收段",
    ),
    asset_row(
        "BY-REL-P1-010-地月视觉尺度连续性",
        "REL",
        "地球、月球与飞行器视觉尺度连续性",
        "P1",
        "镜2、4、23、31、33、46、83、89—90、96—101",
        "深空与轨道镜头",
        "环月轨道中的地球表现为有清晰直径的蓝白圆盘，接近地球时逐步扩大。",
        "禁止把环月视角的地球画成静止小蓝点。",
        "环月；离月；接近地球；再入",
        "关系资产",
        "深空、月轨、近地",
        "与每个视觉重建镜头的镜头尺度绑定",
        "深空连续性",
    ),
    asset_row(
        "BY-ANM-P0-001-梦舟四种乘员状态",
        "ANM",
        "梦舟三座四种乘员状态动作链",
        "P0",
        "镜5、8、12、17、19、25、82、86、97—109",
        "第1—3、5、11、14—15场",
        "三座满员、两座空置、一人环月值守、三人重聚与返航承载的动作连续。",
        "人物离座、锁座、归位、样品固定和再入约束动作连续。",
        "A满员；B一人值守；C重聚；D再入着陆",
        "人物与座椅绑定动画",
        "梦舟舱内",
        "不得改变舱内几何和座椅朝向",
        "梦舟全片",
    ),
    asset_row(
        "BY-ANM-P0-002-揽月下降出舱起飞链",
        "ANM",
        "揽月下降、着陆、单人出舱与月面起飞动作链",
        "P0",
        "镜24、32—60、77—85",
        "第5—8、11场",
        "下降约束、着陆检查、单人通行出舱、回舱增压、起飞与再对接。",
        "舱口和扶梯一次只容纳一人，样品和工具先于人员回舱。",
        "下降；触月；六小时准备；杨凛先出；陈砚后出；回舱；起飞；再对接",
        "人物、舱门、扶梯与载具绑定动画",
        "揽月舱内与月面",
        "关键动作按镜头证据链制作",
        "登月主流程",
    ),
    asset_row(
        "BY-ANM-P1-001-月面科研时间压缩",
        "ANM",
        "月面科研与时间压缩动作链",
        "P1",
        "镜61—76",
        "第9—10场",
        "相机部署后国旗、月球车、采样、钻取、载荷部署和返程。",
        "固定相机、宇航服相机和月球车相机之间保持空间与时间连续。",
        "T+06:20；T+08:20；T+10:40；T+12:50；T+13:40",
        "低重力人物与车辆动作",
        "月面艺术化任务日光",
        "无外部空气传播声",
        "月面科研段",
    ),
    asset_row(
        "BY-ANM-P1-002-东风搜救开舱转移",
        "ANM",
        "东风搜救、安全处置、开舱与人员转移动作链",
        "P1",
        "镜107—117",
        "第15场",
        "着陆、时间压缩、搜救抵达、安全检测、开舱评估、座椅／担架转移和样品交接。",
        "先安全后开舱，先评估后转移，航天员不立即独立站立。",
        "着陆；搜救抵达；安全处置；开舱；评估；转移；挥手；样品交接",
        "返回舱、人员、车辆和医疗器材绑定动画",
        "东风黎明至清晨",
        "保持专业工作节奏",
        "返回回收段",
    ),
]


VOICE_MAP = {
    "杨凛": "BY-VOI-P0-001-杨凛声音",
    "陈砚": "BY-VOI-P0-002-陈砚声音",
    "刘定槎": "BY-VOI-P0-003-刘定槎声音",
    "林知夏": "BY-VOI-P1-002-林知夏声音",
    "北京": "BY-VOI-P1-004-北京飞控主调度声音",
    "林海": "BY-VOI-P1-005-林海深空测控声音",
    "东风": "BY-VOI-P1-008-搜救指挥声音",
    "小天": "BY-VOI-P1-009-小天任务智能体声音",
    "现场指挥": "BY-VOI-P1-011-现场指挥声音",
    "何文澜": "BY-VOI-P1-012-何文澜声音",
    "孙亦川": "BY-VOI-P1-013-孙亦川声音",
    "顾青岚": "BY-VOI-P1-014-顾青岚声音",
    "医监人员": "BY-VOI-P1-015-医监人员声音",
}

CHAR_ASSETS = {
    "杨凛": ("BY-CHR-P0-001-杨凛", "BY-CST-P0-001-杨凛舱内飞行服"),
    "陈砚": ("BY-CHR-P0-002-陈砚", "BY-CST-P0-002-陈砚舱内飞行服"),
    "刘定槎": ("BY-CHR-P0-003-刘定槎", "BY-CST-P0-003-刘定槎舱内飞行服"),
    "林知夏": ("BY-CHR-P1-002-林知夏", "BY-CST-P1-004-林知夏记者服装"),
    "何文澜": ("BY-CHR-P1-004-何文澜", "BY-CST-P1-006-何文澜专家服装"),
    "孙亦川": ("BY-CHR-P1-005-孙亦川", "BY-CST-P1-007-孙亦川专家服装"),
    "顾青岚": ("BY-CHR-P1-006-顾青岚", "BY-CST-P1-008-顾青岚专家服装"),
}


def add(target: set[str], *items: str) -> None:
    target.update(item for item in items if item)


def source_grade(camera: str, image: str, note: str) -> str:
    text = camera + image + note
    if "视觉重建" in text:
        return "C｜显式遥测视觉重建"
    if any(k in camera for k in ["后期字幕", "图卡", "轨迹仿真", "黑场"]):
        return "D｜后期字幕／解释图卡"
    if any(
        k in camera
        for k in ["媒体区", "飞控", "佳木斯", "东风", "搜救", "地面", "现场", "医监", "空中", "开舱"]
    ):
        return "B｜地面直播／测控任务机位"
    return "A｜航天器／宇航服／月面真实任务机位推演"


def shot_state(number: int, image: str, camera: str) -> str:
    if number in {5, 8, 12, 17}:
        return "梦舟A｜三座满员／对接前"
    if number in {19, 25, 82}:
        return "梦舟B｜刘定槎值守／两座空置锁定"
    if number == 86:
        return "梦舟C｜三人重聚／样品归舱"
    if 97 <= number <= 109:
        return "梦舟D｜三人返航承载／再入着陆"
    if "视觉重建" in camera + image:
        return "遥测视觉重建｜角标常驻"
    if number < 60 and "月面" in image:
        return "月面相机部署前｜不得使用便携相机第三视角"
    if number >= 61 and "便携月面相机" in camera:
        return "同一便携月面相机｜机位连续"
    if 69 <= number <= 81:
        return "月面T+时间线连续"
    if 110 <= number <= 117:
        return "东风回收｜时间压缩后专业处置"
    return "常规任务状态"


def build_mapping() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    elapsed = 0
    shot_no = 1
    for scene_no, scene in enumerate(v131.SCENES, start=1):
        for duration, camera, image, sound, note in scene["shots"]:
            visual_text = "｜".join([camera, image])
            text = "｜".join([camera, image, sound, note])
            visual: set[str] = set()
            voices: set[str] = set()
            snd: set[str] = {"BY-REL-P1-003-声音来源真实性"}
            sym: set[str] = set()

            for name, voice_id in VOICE_MAP.items():
                if re.search(rf"{re.escape(name)}(?:画外|在延迟后)?：", sound):
                    voices.add(voice_id)

            # Visible named people only. Voice-over names do not create visual calls.
            for name, (character, costume) in CHAR_ASSETS.items():
                if name in visual_text and f"{name}画外" not in camera:
                    add(visual, character, costume)

            if "媒体区" in visual_text:
                add(
                    visual,
                    "BY-SCN-P1-003-飞控中心媒体区",
                    "BY-LGT-P1-008-飞控媒体区直播光",
                    "BY-REL-P1-008-三段直播结构链",
                )
                snd.add("BY-SND-P1-009-媒体区直播现场声")
                if any(k in camera + image for k in ["记者", "专家", "林知夏"]):
                    add(visual, *CHAR_ASSETS["林知夏"])
                for expert in ["何文澜", "孙亦川", "顾青岚"]:
                    if expert in image + camera:
                        add(visual, *CHAR_ASSETS[expert])

            if "飞控" in visual_text or "北京席位" in visual_text:
                add(
                    visual,
                    "BY-SCN-P0-006-北京飞控大厅与任务主屏",
                    "BY-LGT-P1-003-飞控大厅任务光",
                    "BY-CRO-P1-001-北京飞控任务团队",
                )
                snd.add("BY-SND-P1-008-飞控与测控大厅底噪")

            if "佳木斯" in visual_text:
                add(
                    visual,
                    "BY-SCN-P1-007-佳木斯66米深空测控站",
                    "BY-LGT-P1-006-深空测控站任务光",
                    "BY-CRO-P1-002-深空测控值班团队",
                    "BY-REL-P1-004-地面测控接力链",
                )
                snd.add("BY-SND-P1-008-飞控与测控大厅底噪")

            dream_inside = (
                any(k in camera for k in ["梦舟舱内", "梦舟工作位", "梦舟返回舱"])
                or any(k in image for k in ["三把座椅", "三名航天员全部固定在梦舟", "刘定槎独自坐回工作位", "两张空座"])
            )
            if dream_inside:
                add(
                    visual,
                    "BY-SCN-P0-001-梦舟舱内三座布局",
                    "BY-SCN-P0-005-梦舟环月工作位",
                    "BY-PRP-P0-001-梦舟三座椅与束缚系统",
                    "BY-PRP-P1-006-舱内操作界面与任务屏",
                    "BY-LGT-P0-001-梦舟舱内任务光",
                    "BY-REL-P0-009-梦舟三座返航承载与环月工作位",
                    "BY-ANM-P0-001-梦舟四种乘员状态",
                )
                snd.add("BY-SND-P0-001-舱内生命保障与设备底噪")

            if "梦舟" in visual_text:
                visual.add("BY-VEH-P0-001-梦舟载人飞船")
            if any(k in visual_text for k in ["梦舟—揽月", "对接通道", "舱门依次开启", "转移清单"]):
                add(
                    visual,
                    "BY-SCN-P0-002-梦舟对接通道与舱门区",
                    "BY-PRP-P1-005-两器舱门与对接锁止结果件",
                    "BY-REL-P0-010-梦舟轴向转移顺序",
                    "BY-REL-P1-002-两侧舱门顺序",
                )
                snd.add("BY-SND-P1-001-舱门对接机构结构传导")

            if any(k in visual_text for k in ["环月", "月球轨道", "月轨", "深空", "月球弧面"]):
                add(
                    visual,
                    "BY-SCN-P1-006-环月轨道外部环境",
                    "BY-LGT-P1-004-环月轨道太阳光",
                    "BY-REL-P1-010-地月视觉尺度连续性",
                )

            if "揽月" in visual_text:
                if shot_no <= 32:
                    visual.add("BY-VEH-P0-002-揽月完整构型")
                visual.add("BY-VEH-P0-003-揽月登月舱")
                visual.add("BY-REL-P0-005-揽月构型状态链")
            if "揽月舱内" in visual_text:
                add(
                    visual,
                    "BY-SCN-P0-003-揽月登月舱舱内",
                    "BY-PRP-P1-006-舱内操作界面与任务屏",
                    "BY-LGT-P0-002-揽月下降任务光",
                    "BY-ANM-P0-002-揽月下降出舱起飞链",
                )
                snd.add("BY-SND-P0-001-舱内生命保障与设备底噪")

            if any(k in camera for k in ["对接口监视", "着陆器下视", "着陆腿相机", "揽月外部固定", "梦舟外部任务", "返回舱外部任务"]):
                visual.add("BY-PRP-P1-015-航天器任务相机组")

            if any(k in visual_text for k in ["对接", "交会", "接触捕获", "硬连接"]):
                add(
                    visual,
                    "BY-VFX-P1-002-环月轨道交会与对接",
                    "BY-PRP-P1-005-两器舱门与对接锁止结果件",
                )
                snd.add("BY-SND-P1-001-舱门对接机构结构传导")

            if "姿控喷气" in visual_text or "姿态控制" in visual_text:
                visual.add("BY-VFX-P1-004-姿控喷流")

            if "推进舱" in visual_text:
                visual.add("BY-VEH-P1-003-揽月推进舱分离状态")

            if any(k in visual_text for k in ["下降", "着陆区", "月面", "舱外", "扶梯", "足印", "国旗", "采样", "月球车"]):
                add(
                    visual,
                    "BY-SCN-P0-004-月面着陆与作业区",
                    "BY-LGT-P0-004-月面艺术化任务日光",
                    "BY-REL-P0-012-月面艺术化光照与声明",
                    "BY-REL-P1-001-月面空间总图",
                )
            if any(k in text for k in ["下降", "着陆", "触月", "发动机", "上升级", "起飞"]):
                snd.add("BY-SND-P1-003-发动机舱内结构振动")
            if any(k in visual_text for k in ["尘埃", "月尘", "喷流扩散"]):
                visual.add("BY-VFX-P0-001-月面下降羽流与贴地月尘")
            if any(k in visual_text for k in ["接触月面", "触月", "尘埃沉降", "尘埃落定"]):
                visual.add("BY-VFX-P0-002-触月关机与月尘回落")
            if "踏上月面" in visual_text or "一只脚接触月面" in visual_text or "脚印" in visual_text:
                visual.add("BY-VFX-P0-003-第一足印月壤形变")

            if 53 <= shot_no <= 78:
                # These shots either show or directly support the suited lunar EVA chain.
                if any(k in visual_text for k in ["杨凛", "两人", "航天员", "宇航服", "陈砚"]):
                    add(
                        visual,
                        "BY-CHR-P0-001-杨凛",
                        "BY-CHR-P0-002-陈砚",
                        "BY-CST-P0-004-杨凛望宇登月服",
                        "BY-CST-P0-005-陈砚望宇登月服",
                    )
                if shot_no >= 62:
                    add(
                        visual,
                        "BY-CST-P1-001-杨凛登月服轻度月尘状态",
                        "BY-CST-P1-002-陈砚登月服轻度月尘状态",
                    )
                snd.add("BY-SND-P1-002-登月服内部呼吸与结构声")

            if "宇航服相机" in camera:
                visual.add("BY-PRP-P1-014-宇航服任务相机")
            if "舷梯" in visual_text or "扶梯" in visual_text:
                visual.add("BY-PRP-P0-002-揽月舷梯与扶手系统")
            if "安全绳" in visual_text or "工具包" in visual_text:
                visual.add("BY-PRP-P1-004-月面工具包与载荷固定系统")
            if "便携月面相机" in visual_text or "折叠三脚架" in visual_text or (shot_no in {60, 61, 63, 64, 69, 76, 81}):
                add(
                    visual,
                    "BY-PRP-P0-003-便携式月面摄像机",
                    "BY-REL-P0-006-月面摄像机摄影来源",
                )
            if "国旗" in visual_text:
                add(
                    visual,
                    "BY-PRP-P0-004-工程化国旗展示装置",
                    "BY-SYM-P0-001-中华人民共和国国旗图形",
                    "BY-REL-P0-007-国旗装置部署链",
                )
            if "月球车" in visual_text:
                add(
                    visual,
                    "BY-VEH-P0-004-探索载人月球车",
                    "BY-PRP-P1-012-月球车任务相机组",
                    "BY-VFX-P1-007-月球车轮迹与低重力扬尘",
                )
                snd.add("BY-SND-P1-007-月球车设备链路结构声")
            if any(k in visual_text for k in ["采样", "样品", "岩芯", "科学载荷", "科研", "地质"]):
                add(
                    visual,
                    "BY-SCN-P1-005-月面后段科考区",
                    "BY-REL-P1-006-月面科学路线与样品链",
                )
            if "表层样品" in visual_text or "采样工具" in visual_text:
                visual.add("BY-PRP-P1-001-月面采样工具")
            if "岩芯" in visual_text or "样品袋" in visual_text:
                visual.add("BY-PRP-P1-002-月壤样品容器")
            if "科学载荷" in visual_text or "观测设备" in visual_text:
                visual.add("BY-PRP-P1-003-月面科学观测设备")
            if "样品箱" in visual_text or "样品固定" in visual_text or "密封样品" in visual_text:
                add(
                    visual,
                    "BY-PRP-P0-005-密封样品转移容器",
                    "BY-PRP-P1-008-主样品容器编号与固定座",
                    "BY-REL-P0-008-样品转移链",
                )
                sym.add("BY-SYM-P1-005-样品编号与封签模板")
            if any(k in visual_text for k in ["清洁隔离", "污染控制", "月尘处置"]):
                visual.add("BY-PRP-P1-009-污染控制用品")
            if 61 <= shot_no <= 76:
                visual.add("BY-ANM-P1-001-月面科研时间压缩")
            if shot_no in {81, 83, 85}:
                visual.add("BY-VEH-P1-004-揽月月面起飞状态")
            if shot_no in {83, 85}:
                visual.add("BY-VEH-P1-005-揽月月轨再对接状态")
            if shot_no == 81:
                visual.add("BY-VFX-P0-004-月面起飞羽流与留场余景")

            if "视觉重建" in camera + image + note:
                add(
                    visual,
                    "BY-VFX-P1-008-遥测视觉重建合成",
                    "BY-REL-P1-007-摄影来源证据层级",
                )
                sym.add("BY-SYM-P1-006-视觉重建来源标识")
            else:
                visual.add("BY-REL-P1-007-摄影来源证据层级")

            if any(k in visual_text for k in ["轨迹", "走廊", "相位", "高度、速度", "速度标尺"]):
                sym.add("BY-SYM-P1-004-任务轨迹与相位图模板")

            if any(k in camera + image for k in ["后期字幕", "时间码", "倒计时", "直播结束", "字幕"]):
                sym.add("BY-SYM-P1-003-任务阶段与时间跳跃标牌")
            if "媒体区" in visual_text or shot_no in {3, 22, 27, 47, 51, 87, 92, 118}:
                sym.add("BY-SYM-P1-007-直播进口出口与倒计时")
            if shot_no in {1, 119}:
                add(
                    sym,
                    "BY-SYM-P1-001-未来纪实推演标识",
                    "BY-SYM-P0-002-艺术化光照偏差推演声明",
                )
            if shot_no == 110:
                sym.add("BY-SYM-P1-008-东风搜救时间压缩")

            if any(k in visual_text for k in ["离开月球轨道", "月地", "地月返回", "离月"]):
                add(
                    visual,
                    "BY-VEH-P0-005-梦舟月轨组合体",
                    "BY-VFX-P1-003-月地转移点火与月球远离",
                    "BY-REL-P0-011-梦舟返地构型状态链",
                )

            if any(k in visual_text for k in ["再入", "黑障", "等离子", "大气层", "入口走廊"]):
                add(
                    visual,
                    "BY-SCN-P0-007-返回舱再入视觉环境",
                    "BY-VEH-P0-006-梦舟返回舱独立再入构型",
                    "BY-LGT-P0-005-返回舱再入等离子辉光",
                    "BY-VFX-P0-005-返回舱等离子辉光与黑障视觉",
                    "BY-VFX-P1-005-半弹道跳跃式再入轨迹",
                    "BY-REL-P0-011-梦舟返地构型状态链",
                    "BY-REL-P0-013-返回舱再入搜救状态链",
                )
                snd.add("BY-SND-P1-004-再入结构与通信衰减")
            if "服务舱" in visual_text:
                visual.add("BY-VEH-P1-007-梦舟服务舱近地分离状态")
            if any(k in visual_text for k in ["主伞", "引导伞", "群伞"]):
                add(
                    visual,
                    "BY-VEH-P0-007-返回舱群伞气囊着陆构型",
                    "BY-VFX-P0-006-稳定伞与主伞展开",
                )
                snd.add("BY-SND-P1-005-降落伞与着陆冲击")

            if any(k in visual_text for k in ["东风", "着陆场", "搜救", "医监", "开舱", "返回舱接地", "直升机", "地面车队"]):
                add(
                    visual,
                    "BY-SCN-P0-008-预定着陆区与搜救现场",
                    "BY-LGT-P1-007-搜救着陆区日间自然光",
                    "BY-CRO-P1-003-搜救与医疗团队",
                    "BY-REL-P0-013-返回舱再入搜救状态链",
                    "BY-REL-P1-009-东风医监与样品双线",
                )
                snd.add("BY-SND-P1-006-搜救现场声")
            if any(k in visual_text for k in ["直升机", "地面车辆", "车队"]):
                visual.add("BY-VEH-P1-008-搜救直升机与地面车辆")
            if any(k in visual_text for k in ["现场安全", "危险源", "信标"]):
                visual.add("BY-PRP-P1-011-返回舱信标与现场安全工具")
            if 110 <= shot_no <= 117:
                add(
                    visual,
                    "BY-SCN-P1-012-东风医监开舱作业区",
                    "BY-ANM-P1-002-东风搜救开舱转移",
                )
            if any(k in visual_text for k in ["座椅、担架", "支撑座椅", "生命体征", "逐人评估", "医学"]):
                visual.add("BY-PRP-P0-006-东风医监转移设备")
            if any(k in visual_text for k in ["样品接收", "样品箱完成交接", "样品交接"]):
                visual.add("BY-PRP-P1-013-东风样品接收设备")
                sym.add("BY-SYM-P1-005-样品编号与封签模板")

            if shot_no in {109}:
                add(
                    visual,
                    "BY-VEH-P0-007-返回舱群伞气囊着陆构型",
                    "BY-VFX-P0-007-气囊触地滚摆",
                )
                snd.add("BY-SND-P1-005-降落伞与着陆冲击")

            # If astronaut names only occur in action without an explicit full name list.
            if "三名航天员" in visual_text or "三人" in visual_text:
                for name in ["杨凛", "陈砚", "刘定槎"]:
                    add(visual, *CHAR_ASSETS[name])
            if "两名航天员" in visual_text or "两人" in visual_text:
                for name in ["杨凛", "陈砚"]:
                    add(visual, CHAR_ASSETS[name][0])

            start = elapsed
            end = elapsed + duration
            rows.append(
                {
                    "镜号": f"{shot_no:03d}",
                    "场次": f"{scene_no:02d}",
                    "场名": scene["title"],
                    "时间码": f"{fmt_time(start)}–{fmt_time(end)}",
                    "时长秒": str(duration),
                    "景别／机位": camera,
                    "画面动作摘要": image,
                    "关键状态／变体": shot_state(shot_no, image, camera),
                    "摄影来源等级": source_grade(camera, image, note),
                    "所需视觉资产ID": ";".join(sorted(visual)),
                    "所需人物音色ID": ";".join(sorted(voices)),
                    "同步声音约束ID": ";".join(sorted(snd)),
                    "后期文字／图形资产ID": ";".join(sorted(sym)),
                    "资产状态": "阶段1映射完成｜阶段2B按镜头状态调用",
                    "专业控制": note,
                }
            )
            elapsed = end
            shot_no += 1

    return rows


def fmt_time(seconds: int) -> str:
    return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"


def build_scene_map(mapping: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in mapping:
        grouped[row["场次"]].append(row)
    rows = []
    for scene_no in sorted(grouped):
        items = grouped[scene_no]
        rows.append(
            {
                "场次编号": scene_no,
                "场名": items[0]["场名"],
                "镜号范围": f"{items[0]['镜号']}—{items[-1]['镜号']}",
                "镜头数": str(len(items)),
                "素材时长秒": str(sum(int(item["时长秒"]) for item in items)),
                "所需视觉资产ID": join_unique(items, "所需视觉资产ID"),
                "所需人物音色ID": join_unique(items, "所需人物音色ID"),
                "同步声音约束ID": join_unique(items, "同步声音约束ID"),
                "后期文字／图形资产ID": join_unique(items, "后期文字／图形资产ID"),
                "阶段2B资产状态": "可进入阶段2B｜优先按场次资产包生产",
            }
        )
    return rows


def join_unique(rows: list[dict[str, str]], key: str) -> str:
    values: set[str] = set()
    for row in rows:
        values.update(item for item in row[key].split(";") if item)
    return ";".join(sorted(values))


def build_views() -> list[dict[str, str]]:
    old = load_csv(DATA / "阶段1_场景视图需求表_V1.2.csv")
    changes = {
        "BY-SCN-P0-001-梦舟舱内三座布局": {
            "场景名称": "梦舟返回舱三座承力区与四种乘员状态",
            "指定必需视图": "MASTER;SEAT-BACK;FULL-3;EMPTY-2;REUNION-3;REENTRY-3",
            "建议补充视图": "CONTROL-LOCAL;SAMPLE-LOCK",
            "阶段3可能追加专项视图": "ENTRY-GLOAD;LANDING-IMPACT",
            "确认状态": "V1.3.1重校已确认",
        },
        "BY-SCN-P0-005-梦舟环月工作位": {
            "指定必需视图": "MASTER;WORK-FRONT;WORK-OTS;SINGLE-OP",
            "建议补充视图": "DISPLAY-LOCAL;EMPTY-SEAT",
            "确认状态": "V1.3.1重校已确认",
        },
        "BY-SCN-P1-003-飞控中心媒体区": {
            "视图需求等级建议": "SV1",
            "指定必需视图": "MASTER;REPORTER;EXPERT-PAIR;BIG-SCREEN",
            "建议补充视图": "COUNTDOWN;FINAL",
            "确认状态": "V1.3.1重校已确认",
        },
        "BY-SCN-P0-004-月面着陆与作业区": {
            "指定必需视图": "MASTER;FRONT;BACK;LEFT;RIGHT;TOP;LANDING-RECON;PORTABLE-CAMERA",
            "建议补充视图": "FLAG;LADDER;ASCENT;EMPTY-HOLD",
            "确认状态": "V1.3.1重校已确认",
        },
        "BY-SCN-P1-005-月面后段科考区": {
            "指定必需视图": "MASTER;PATH-FRONT;PATH-SIDE;PATH-TOP;ROVER-FRONT;ROVER-SIDE-REAR;SUIT-CAM",
            "建议补充视图": "SAMPLE-POINT;CORE;PAYLOAD",
            "确认状态": "V1.3.1重校已确认",
        },
        "BY-SCN-P1-006-环月轨道外部环境": {
            "指定必需视图": "MASTER;DOCK-AXIS;MOON-LIMB;SEPARATION;EARTH-DISC",
            "建议补充视图": "ASCENT-RENDEZVOUS;EARTH-APPROACH",
            "确认状态": "V1.3.1重校已确认",
        },
        "BY-SCN-P0-007-返回舱再入视觉环境": {
            "指定必需视图": "MASTER;SERVICE-SEPARATION;FIRST-ENTRY;SKIP;SECOND-ENTRY;BLACKOUT;PARACHUTE",
            "建议补充视图": "CABIN-GLOAD;PLASMA-LOCAL;IR-TRACK",
            "确认状态": "V1.3.1重校已确认",
        },
        "BY-SCN-P0-008-预定着陆区与搜救现场": {
            "场景名称": "东风着陆场与搜救现场",
            "指定必需视图": "MASTER;DAWN-AERIAL;LONG-LENS;LANDING;IR;CONVOY;HATCH-MEDICAL;SAMPLE-HANDOFF",
            "建议补充视图": "FINAL-WIDE;HELICOPTER-POV",
            "确认状态": "V1.3.1重校已确认",
        },
    }
    for row in old:
        row.update(changes.get(row["场景生产资产ID"], {}))
    new = {
        "场景生产资产ID": "BY-SCN-P1-012-东风医监开舱作业区",
        "场景名称": "东风医监医保与开舱作业区",
        "视图ID前缀": "BY-SCN-P1-012-SV",
        "视图需求等级建议": "SV1",
        "建议原因": "开舱、评估、座椅／担架转移和样品交接要求严格空间连续。",
        "母图是否必需": "是",
        "指定必需视图": "MASTER;HATCH;MEDICAL;TRANSFER;SAMPLE-HANDOFF",
        "建议补充视图": "AERIAL-RELATION",
        "是否建议标准五视图": "否",
        "阶段3可能追加专项视图": "CREW-CLOSE;SEAT-WAVE",
        "用户确认的视图需求等级": "按推荐口径锁定",
        "用户确认的视图清单": "按推荐必需视图执行",
        "用户确认的场景视图ID清单": "阶段2B生成后登记",
        "确认状态": "V1.3.1新增｜阶段1已确认生产方向",
    }
    old.append(new)
    return old


def build_changes(new_assets: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    old_changes = load_csv(DATA / "阶段1_资产变更映射表_V1.2.csv")
    for row in old_changes:
        rows.append(
            {
                "原生产资产ID": row.get("旧生产资产ID", ""),
                "V1.3.1处置": row.get("V1.2处置", ""),
                "现生产资产ID": row.get("新生产资产ID", ""),
                "原因": row.get("原因", ""),
                "影响镜号": "历史继承",
            }
        )
    update_reasons = {
        "BY-SCN-P0-001-梦舟舱内三座布局": ("语义扩展", "四种乘员状态共用同一舱体几何", "005;008;012;017;019;025;082;086;097—109"),
        "BY-SCN-P0-005-梦舟环月工作位": ("语义扩展", "明确单人值守与两座空置关系", "019;025;082"),
        "BY-SCN-P0-008-预定着陆区与搜救现场": ("正式锁定", "主着陆场改为并锁定东风着陆场", "094;104;107—118"),
        "BY-LGT-P1-007-搜救着陆区日间自然光": ("语义校正", "脚本为黎明至清晨，不再写笼统日间", "107—118"),
        "BY-PRP-P0-003-便携式月面摄像机": ("状态扩展", "同一相机从部署连续复用到起飞空镜", "060—061;063—064;069;076;081"),
        "BY-REL-P0-009-梦舟三座返航承载与环月工作位": ("语义扩展", "建立三座满员—两座空置—三座重聚—返航承载链", "005—019;025;082;086;097—109"),
    }
    for asset_id, (action, reason, shots) in update_reasons.items():
        rows.append(
            {
                "原生产资产ID": asset_id,
                "V1.3.1处置": action,
                "现生产资产ID": asset_id,
                "原因": reason,
                "影响镜号": shots,
            }
        )
    for row in new_assets:
        rows.append(
            {
                "原生产资产ID": "",
                "V1.3.1处置": "新增",
                "现生产资产ID": row["生产资产ID"],
                "原因": row["基础描述"],
                "影响镜号": row["剧本出处"],
            }
        )
    return rows


PRODUCTION_PACKAGES = [
    ("P13-01", "人物、服装与稳定音色", "林知夏、何文澜、孙亦川、顾青岚及三名航天员；先确认三位新增专家脸、服装和独立音色", "P0/P1", "先行"),
    ("P13-02", "梦舟四状态与空间连续", "同一返回舱母图、三座承力区、环月工作位、轴向通道、四种乘员状态", "P0", "最高优先"),
    ("P13-03", "揽月构型与动作链", "无人月轨状态、下降、着陆、单人出舱、回舱、整器起飞、再对接", "P0", "最高优先"),
    ("P13-04", "摄影来源与遥测视觉重建", "任务相机组、视觉重建合成、来源角标、地月尺度连续", "P0/P1", "最高优先"),
    ("P13-05", "月面相机与空间连续", "便携相机部署、同机位复用、宇航服相机、月球车前向和侧后相机", "P0/P1", "最高优先"),
    ("P13-06", "国旗与月面科学任务", "国旗装置、月球车、采样、岩芯、载荷、样品与月尘状态", "P0/P1", "第二优先"),
    ("P13-07", "飞控、媒体区与深空测控", "飞控大厅、媒体区直播、专家采访、佳木斯链路、任务UI与图卡", "P0/P1", "第二优先"),
    ("P13-08", "梦舟返回与再入", "离月、服务舱分离、两段再入、黑障、红外发现和主伞", "P0/P1", "第二优先"),
    ("P13-09", "东风着陆与医监回收", "着陆场、直升机车组、安全处置、开舱、座椅／担架、样品交接", "P0/P1", "第二优先"),
    ("P13-10", "声音与后期图形约束", "无配乐、月面外部静音、独立音色、直播图形、时间码与推演声明", "P0/P1", "贯穿"),
    ("P13-11", "119镜映射与QA", "逐镜ID校验、摄影来源、状态变体、停用资产隔离和场次聚合", "P0", "阶段2B入口"),
]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    def esc(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", "<br>")

    lines = [
        "| " + " | ".join(map(esc, headers)) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    lines.extend("| " + " | ".join(esc(cell) for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def build_analysis_doc(
    assets: list[dict[str, str]],
    mapping: list[dict[str, str]],
    scene_map: list[dict[str, str]],
) -> str:
    active = [row for row in assets if "历史" not in row["确认状态"] and "停止" not in row["确认状态"]]
    historical = [row for row in assets if row not in active]
    type_counts = Counter(row["资产类型"] for row in active)
    priority_counts = Counter(row["资产级别"] for row in active)
    grade_counts = Counter(row["摄影来源等级"].split("｜")[0] for row in mapping)
    scene_rows = [
        [
            row["场次编号"],
            row["场名"],
            row["镜号范围"],
            row["镜头数"],
            row["素材时长秒"],
        ]
        for row in scene_map
    ]
    return f"""# 阶段1｜V1.3.1剧本资产重分析与119镜映射结论

版本：V1.3.1  
正式输入：`文本/奔月_正式分镜稿_V1.3.1.docx`  
分析日期：2026-07-24  
阶段结论：**阶段1重分析完成，119镜均已建立镜头—资产调用关系，可以重入阶段2B。**

## 1. 本次执行结果

- 正式结构：15场、119镜、建议生成素材1020秒；最终剪辑目标仍为约840秒。
- 逐镜覆盖：119/119；镜号连续，无重复、无缺号。
- 资产主表：共{len(assets)}项，其中有效{len(active)}项、历史停用{len(historical)}项。
- 有效资产优先级：P0 {priority_counts.get('P0', 0)}项，P1 {priority_counts.get('P1', 0)}项，P2 {priority_counts.get('P2', 0)}项。
- 本次新增正式资产：{len(NEW_ASSETS)}项；旧资产ID继承，只有语义不足处作状态扩展。
- 摄影来源：A层任务机位{grade_counts.get('A', 0)}镜，B层地面直播／测控{grade_counts.get('B', 0)}镜，C层显式遥测视觉重建{grade_counts.get('C', 0)}镜，D层字幕／图卡{grade_counts.get('D', 0)}镜。

## 2. 资产类型统计

{markdown_table(["类型", "有效数量"], [[key, str(type_counts[key])] for key in sorted(type_counts)])}

## 3. V1.3.1必须新建或重校的核心资产

1. **梦舟四状态**：同一三座承力区必须连续呈现“三座满员→刘定槎一人值守、两座空置→三人重聚、样品归舱→三人返航承载／再入／着陆”。四种状态不能被生成成四个不同舱室。
2. **揽月无人前置状态**：环月对接前揽月无人；三名航天员均在梦舟。推进舱分离、动力下降、着陆、单人出舱、回舱、整器月面起飞和再对接属于一条载具状态链。
3. **摄影来源层级**：关键证据节点优先用对接口、下视、着陆腿、舱外固定、宇航服和月面相机；无实体机位的全景必须标注“基于实时遥测的视觉重建”。
4. **月面第三视角**：镜60以前便携月面相机尚未部署；镜60完成部署后，镜61、63—64、69、76、81必须复用同一机位与同一设备。科研段另调用宇航服和月球车固定相机。
5. **东风回收链**：镜110先以字幕明确时间压缩；随后按“搜救抵达→安全处置→医监设备待命→开舱评估→座椅／担架转移→样品交接”执行。
6. **人物新增**：何文澜、孙亦川、顾青岚均建立独立人物、服装和音色资产。“孙亦川”与历史停用的“孙屹川”不是同一角色，不复用旧资产。
7. **地月尺度**：环月轨道中的地球必须为可分辨蓝白圆盘，接近地球时逐步扩大，禁止回退成静止小蓝点。

## 4. 119镜分场覆盖

{markdown_table(["场次", "场名", "镜号", "镜头数", "素材秒"], scene_rows)}

## 5. 四层摄影来源规则

{markdown_table(
    ["层级", "定义", "使用边界"],
    [
        ["A", "航天器、宇航服、便携月面相机、月球车等任务机位", "接触捕获、触月、出舱、足印、再对接、开伞等不可逆节点优先"],
        ["B", "北京飞控、媒体区、佳木斯、东风着陆场等地面任务机位", "承担直播、解释、遥测和搜救系统视角"],
        ["C", "基于实时遥测的视觉重建", "只补充空间尺度和轨道关系；必须常驻来源角标，不伪装外拍"],
        ["D", "后期字幕、时间码、轨迹仿真与任务图卡", "只承担解释和时间压缩，不替代任务证据"],
    ],
)}

## 6. 声音资产口径

- 杨凛、陈砚、刘定槎、林知夏、何文澜、孙亦川、顾青岚及关键地面岗位的稳定音色独立制作、确认和登记。
- 正式镜头中的对白、无线电、设备声和任务通信随视频同步生成，不单独预制成镜头声音文件。
- 月面外部无空气传播声；只保留服内呼吸、结构传导和无线电。
- 全片不配乐，不使用新闻提示音。

## 7. 阶段2B进入顺序

1. 梦舟母资产与四状态对照板。
2. 揽月构型、舱内、舱外机位和单人出舱动作链。
3. 任务相机体系与遥测视觉重建模板。
4. 月面主场景、便携相机机位、月球车相机、国旗与科学任务资产。
5. 飞控／媒体区／专家人物与直播图形。
6. 梦舟返回、再入、黑障、东风着陆、医监与样品交接。

## 8. 阶段1出口判断

V1.3.1资产主表、资产变更表、场景视图表、119镜调用映射和15场聚合表均已生成；全部镜头引用ID可在资产主表中解析，未调用历史停用资产。阶段2A风格锁定包V1.1继续有效，项目可直接重入阶段2B，按生产包逐项建立具体人物、场景、道具和载具资产。
"""


def build_plan_doc() -> str:
    table = markdown_table(
        ["包号", "生产包", "内容", "级别", "顺序"],
        [list(row) for row in PRODUCTION_PACKAGES],
    )
    return f"""# 阶段1｜V1.3.1资产生产计划

版本：V1.3.1  
执行基线：15场、119镜、1020秒建议素材量  
阶段目标：把逐镜映射转为可直接进入阶段2B的资产生产包。

## 1. 生产包

{table}

## 2. 阶段2B批次门

- 每个生产包先完成母资产，再生成状态变体和局部视图。
- P0资产必须有可复用母图、稳定ID、状态链和镜头调用范围。
- 所有Prompt遵循“所见即所得”：只描述画面中可见的信息，不把背景解释、未入镜功能和资产登记文字写入生图Prompt。
- 视觉重建镜头和任务相机镜头分开生成；角标由后期叠加。
- 梦舟、揽月、月面摄影来源和东风医监链任一连续性未通过时，不批量进入相应镜头Prompt。

## 3. 声音与视频同步

人物稳定音色独立制作并登记；正式镜头对白、无线电、设备声和任务通信随视频同步生成。月面外部无空气传播声，全片无配乐。

## 4. 验收优先级

最高优先：梦舟四状态、揽月状态链、摄影来源与遥测重建、月面相机连续。  
第二优先：科学任务、飞控媒体区、返回再入、东风医监回收。  
贯穿校验：119镜ID引用、时间码、声音边界、历史停用资产隔离。
"""


def build_card_doc(assets: list[dict[str, str]]) -> str:
    active = [row for row in assets if "历史" not in row["确认状态"] and "停止" not in row["确认状态"]]
    sections = [
        "# 阶段1｜V1.3.1生产资产卡索引",
        "",
        "正式输入：`文本/奔月_正式分镜稿_V1.3.1.docx`  ",
        "用途：阶段2B资产Prompt、母资产确认和阶段3镜头调用。历史停用资产只保留追溯，不得调用。",
        "",
    ]
    by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in active:
        by_type[row["资产类型"]].append(row)
    for asset_type in sorted(by_type):
        sections.extend(
            [
                f"## {asset_type}｜{len(by_type[asset_type])}项",
                "",
                markdown_table(
                    ["资产ID", "名称", "级别", "状态变体", "阶段2处理"],
                    [
                        [
                            row["生产资产ID"],
                            row["资产名称"],
                            row["资产级别"],
                            row["状态变体"],
                            row["阶段2处理建议"],
                        ]
                        for row in by_type[asset_type]
                    ],
                ),
                "",
            ]
        )
    return "\n".join(sections)


def build_handoff_doc(assets: list[dict[str, str]], mapping: list[dict[str, str]]) -> str:
    active_count = sum(
        1
        for row in assets
        if "历史" not in row["确认状态"] and "停止" not in row["确认状态"]
    )
    return f"""# 阶段1到阶段2交接包｜V1.3.1资产重分析版

交接日期：2026-07-24
正式剧本：`文本/奔月_正式分镜稿_V1.3.1.docx`
范围：15场、119镜、建议生成素材1020秒，最终剪辑目标约840秒
当前阶段：**阶段1完成，重入阶段2B**

## 1. 已交付

- `docs/阶段1_剧本资产重分析_V1.3.1.md`
- `docs/阶段1_资产生产计划_V1.3.1.md`
- `docs/阶段1_资产卡索引_V1.3.1.md`
- `data/阶段1_资产统计表_V1.3.1.csv`
- `data/阶段1_资产变更映射表_V1.3.1.csv`
- `data/阶段1_场景视图需求表_V1.3.1.csv`
- `data/阶段1_119镜资产调用映射_V1.3.1.csv`
- `data/阶段1_场次资产需求映射_V1.3.1.csv`
- `data/阶段1_资产生产包_V1.3.1.csv`
- `data/阶段1_V1.3.1资产重分析与119镜映射.xlsx`
- `docs/阶段2B_入口与资产重校审计_V1.1.md`

## 2. 完成度

- 资产主表：{len(assets)}项，其中有效{active_count}项。
- 逐镜映射：{len(mapping)}/119。
- 历史停用资产：完整保留追溯，但119镜无调用。
- 摄影来源：每镜已标注A任务机位／B地面直播／C遥测视觉重建／D后期图卡。
- 梦舟四状态、月面相机部署前后、月球车机位、东风医监转移和样品交接已建立独立资产或关系约束。

## 3. 继续有效的锁定项

- 风格锁定包V1.1继续有效，阶段2A不重做。
- 2029年4月8日及艺术化月面光照偏差继续由推演声明承担。
- 主着陆场为东风着陆场。
- 着陆后约6小时完成出舱准备，月面总停留约28小时，主舱外活动约7小时40分。
- 全片无配乐；月面外部无空气传播声；稳定音色独立资产登记，正式声音随视频同步生成。

## 4. 阶段2B首批顺序

1. `P13-02` 梦舟四状态与空间连续。
2. `P13-03` 揽月构型与单人出舱动作链。
3. `P13-04` 任务相机和遥测视觉重建。
4. `P13-05` 月面便携相机、宇航服相机和月球车相机。
5. 其余生产包按`docs/阶段1_资产生产计划_V1.3.1.md`执行。

## 5. 禁止回退

- 不使用V1.3的100镜映射或V1.2的114镜映射作为正式生产依据。
- 不复用失败的梦舟舱旧图作为空间母资产。
- 不把“孙亦川”误绑定到历史停用角色“孙屹川”。
- 不在便携月面相机部署前调用其第三视角。
- 不把遥测视觉重建伪装成真实外拍；不把环月视角地球画成小蓝点。
"""


def validate(
    assets: list[dict[str, str]],
    mapping: list[dict[str, str]],
    scene_map: list[dict[str, str]],
) -> dict[str, object]:
    ids = [row["生产资产ID"] for row in assets]
    duplicate_ids = sorted({asset_id for asset_id in ids if ids.count(asset_id) > 1})
    asset_set = set(ids)
    references: set[str] = set()
    historical = {
        row["生产资产ID"]
        for row in assets
        if "历史" in row["确认状态"] or "停止" in row["确认状态"]
    }
    for row in mapping:
        for key in [
            "所需视觉资产ID",
            "所需人物音色ID",
            "同步声音约束ID",
            "后期文字／图形资产ID",
        ]:
            references.update(item for item in row[key].split(";") if item)
    missing = sorted(references - asset_set)
    historical_called = sorted(references & historical)
    malformed_asset_ids = []
    type_priority_mismatches = []
    pattern = re.compile(r"^BY-([A-Z]{3})-(P[0-2])-\d{3}-.+$")
    for row in assets:
        match = pattern.match(row["生产资产ID"])
        if not match:
            malformed_asset_ids.append(row["生产资产ID"])
        elif match.group(1) != row["资产类型"] or match.group(2) != row["资产级别"]:
            type_priority_mismatches.append(row["生产资产ID"])
    reconstruction_without_label = [
        row["镜号"]
        for row in mapping
        if row["摄影来源等级"].startswith("C")
        and "BY-SYM-P1-006-视觉重建来源标识" not in row["后期文字／图形资产ID"]
    ]
    portable_camera_early_calls = [
        row["镜号"]
        for row in mapping
        if int(row["镜号"]) < 60
        and "BY-PRP-P0-003-便携式月面摄像机" in row["所需视觉资产ID"]
    ]
    portable_required = {"060", "061", "063", "064", "069", "076", "081"}
    portable_camera_missing_calls = sorted(
        portable_required
        - {
            row["镜号"]
            for row in mapping
            if "BY-PRP-P0-003-便携式月面摄像机" in row["所需视觉资产ID"]
        }
    )
    required_expert_voices = {
        "BY-VOI-P1-012-何文澜声音",
        "BY-VOI-P1-013-孙亦川声音",
        "BY-VOI-P1-014-顾青岚声音",
    }
    result = {
        "formal_script": "文本/奔月_正式分镜稿_V1.3.1.docx",
        "scene_count": len(v131.SCENES),
        "shot_count": len(mapping),
        "duration_seconds": sum(int(row["时长秒"]) for row in mapping),
        "shot_ids_contiguous": [int(row["镜号"]) for row in mapping] == list(range(1, 120)),
        "asset_count": len(assets),
        "active_asset_count": len(assets) - len(historical),
        "historical_asset_count": len(historical),
        "duplicate_asset_ids": duplicate_ids,
        "referenced_asset_count": len(references),
        "missing_referenced_ids": missing,
        "historical_ids_called": historical_called,
        "malformed_asset_ids": malformed_asset_ids,
        "type_priority_mismatches": type_priority_mismatches,
        "reconstruction_without_label": reconstruction_without_label,
        "portable_camera_early_calls": portable_camera_early_calls,
        "portable_camera_missing_required_calls": portable_camera_missing_calls,
        "required_expert_voices_registered": required_expert_voices.issubset(asset_set),
        "scene_map_count": len(scene_map),
        "empty_visual_mappings": [row["镜号"] for row in mapping if not row["所需视觉资产ID"]],
        "passed": (
            len(mapping) == 119
            and sum(int(row["时长秒"]) for row in mapping) == 1020
            and not duplicate_ids
            and not missing
            and not historical_called
            and not malformed_asset_ids
            and not type_priority_mismatches
            and not reconstruction_without_label
            and not portable_camera_early_calls
            and not portable_camera_missing_calls
            and required_expert_voices.issubset(asset_set)
            and len(scene_map) == 15
        ),
    }
    return result


def main() -> None:
    assets = load_csv(DATA / "阶段1_资产统计表_V1.2.csv")
    for row in assets:
        row.update(UPDATES.get(row["生产资产ID"], {}))
    assets.extend(NEW_ASSETS)
    mapping = build_mapping()
    scene_map = build_scene_map(mapping)
    views = build_views()
    changes = build_changes(NEW_ASSETS)
    validation = validate(assets, mapping, scene_map)
    if not validation["passed"]:
        raise RuntimeError(json.dumps(validation, ensure_ascii=False, indent=2))

    write_csv(DATA / "阶段1_资产统计表_V1.3.1.csv", assets, ASSET_COLUMNS)
    write_csv(
        DATA / "阶段1_119镜资产调用映射_V1.3.1.csv",
        mapping,
        MAPPING_COLUMNS,
    )
    write_csv(
        DATA / "阶段1_场次资产需求映射_V1.3.1.csv",
        scene_map,
        [
            "场次编号",
            "场名",
            "镜号范围",
            "镜头数",
            "素材时长秒",
            "所需视觉资产ID",
            "所需人物音色ID",
            "同步声音约束ID",
            "后期文字／图形资产ID",
            "阶段2B资产状态",
        ],
    )
    write_csv(
        DATA / "阶段1_场景视图需求表_V1.3.1.csv",
        views,
        list(views[0].keys()),
    )
    write_csv(
        DATA / "阶段1_资产变更映射表_V1.3.1.csv",
        changes,
        ["原生产资产ID", "V1.3.1处置", "现生产资产ID", "原因", "影响镜号"],
    )
    write_csv(
        DATA / "阶段1_资产生产包_V1.3.1.csv",
        [
            {
                "生产包ID": row[0],
                "生产包": row[1],
                "内容": row[2],
                "级别": row[3],
                "顺序": row[4],
            }
            for row in PRODUCTION_PACKAGES
        ],
        ["生产包ID", "生产包", "内容", "级别", "顺序"],
    )
    write_text(
        DOCS / "阶段1_剧本资产重分析_V1.3.1.md",
        build_analysis_doc(assets, mapping, scene_map),
    )
    write_text(DOCS / "阶段1_资产生产计划_V1.3.1.md", build_plan_doc())
    write_text(DOCS / "阶段1_资产卡索引_V1.3.1.md", build_card_doc(assets))
    write_text(
        HANDOFF / "阶段1到阶段2交接包.md",
        build_handoff_doc(assets, mapping),
    )
    write_text(
        OUT / "v131_asset_reanalysis_validation.json",
        json.dumps(validation, ensure_ascii=False, indent=2),
    )
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
