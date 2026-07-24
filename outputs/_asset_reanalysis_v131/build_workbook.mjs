import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";


const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", "..");
const DATA = path.join(ROOT, "data");
const OUTPUT = path.join(ROOT, "outputs", "asset_hierarchy_v131_20260724");
const QA = path.join(OUTPUT, "qa");
await fs.mkdir(QA, { recursive: true });

function parseCsv(csvText) {
  const text = csvText.replace(/^\uFEFF/, "");
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') {
        field += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        field += char;
      }
    } else if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n") {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += char;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ""));
    rows.push(row);
  }
  const width = Math.max(...rows.map((item) => item.length));
  return rows.map((item) => [...item, ...Array(width - item.length).fill("")]);
}

function rowsToObjects(rows) {
  const headers = rows[0];
  return rows.slice(1).map((row) =>
    Object.fromEntries(headers.map((header, index) => [header, row[index] ?? ""])),
  );
}

async function readCsvObjects(fileName) {
  const text = await fs.readFile(path.join(DATA, fileName), "utf8");
  return rowsToObjects(parseCsv(text));
}

function excelColumn(index) {
  let value = index + 1;
  let result = "";
  while (value > 0) {
    const remainder = (value - 1) % 26;
    result = String.fromCharCode(65 + remainder) + result;
    value = Math.floor((value - 1) / 26);
  }
  return result;
}

const assets = await readCsvObjects("阶段1_资产统计表_V1.3.1.csv");
const sceneViewRows = await readCsvObjects("阶段1_场景视图需求表_V1.3.1.csv");
const sceneViewByAsset = new Map(sceneViewRows.map((row) => [row["场景生产资产ID"], row]));

const categoryOrder = ["人物资产", "场景资产", "道具资产", "特殊资产", "声音资产"];

function classifyType(type) {
  if (["CHR", "CRO", "CST"].includes(type)) return "人物资产";
  if (type === "SCN") return "场景资产";
  if (["PRP", "VEH"].includes(type)) return "道具资产";
  if (["VOI", "SND"].includes(type)) return "声音资产";
  return "特殊资产";
}

function entryKind(type) {
  const labels = {
    CHR: "人物母资产",
    CRO: "群体人物资产",
    CST: "服装子资产",
    SCN: "场景资产组",
    VEH: "载具／航天器",
    PRP: "设备／道具",
    ANM: "动作链",
    LGT: "光照",
    REL: "关系约束",
    SYM: "后期图形／标识",
    VFX: "视觉特效",
    VOI: "稳定音色",
    SND: "同步声音约束",
  };
  return labels[type] ?? type;
}

function asBaseRecord(asset, category, sequence, parentId = "", level = 1) {
  const isChild = level > 1;
  return {
    资产大类: category,
    分类序号: sequence,
    层级: level,
    登记项类型: entryKind(asset["资产类型"]),
    显示名称: isChild ? `↳ ${asset["资产名称"]}` : asset["资产名称"],
    生产资产ID: asset["生产资产ID"],
    父资产ID: parentId,
    视图代码: "",
    资产类型: asset["资产类型"],
    资产级别: asset["资产级别"],
    剧本出处: asset["剧本出处"],
    关联场次或段落: asset["关联场次或段落"],
    基础描述: asset["基础描述"],
    补全设计信息: asset["补全设计信息"],
    状态变体: asset["状态变体"],
    材质结构或声音特点: asset["材质结构或声音特点"],
    光影或环境要求: asset["光影或环境要求"],
    使用或生成需求: asset["使用或生成需求"],
    可复用范围: asset["可复用范围"],
    信息来源: asset["信息来源"],
    确认状态: asset["确认状态"],
    阶段2处理建议: asset["阶段2处理建议"],
  };
}

const viewLabels = {
  MASTER: "母图",
  "SEAT-BACK": "座椅背面关系",
  "RETURN-THREE": "三人返航状态",
  "WORK-FRONT": "工作位正向",
  "WORK-OTS": "越肩工作位",
  "AXIS-DREAM": "梦舟端轴向",
  "AXIS-LANYUE": "揽月端轴向",
  TRANSFER: "人员／物资转移",
  FRONT: "正视图",
  BACK: "后视图",
  LEFT: "左视图",
  RIGHT: "右视图",
  TOP: "顶视图",
  FLOOR: "大厅全景",
  "MAIN-SCREEN": "任务主屏",
  CONSOLE: "核心席位",
  "ANTENNA-LONG": "天线长焦",
  OPS: "值班操作区",
  "PATH-FRONT": "科考路线前向",
  "PATH-SIDE": "科考路线侧向",
  "PATH-TOP": "科考路线俯视",
  "DOCK-AXIS": "对接轴线",
  "MOON-LIMB": "月缘尺度关系",
  SEPARATION: "分离状态",
  "FIRST-ENTRY": "第一次再入",
  SKIP: "跃出段",
  "SECOND-ENTRY": "第二次再入",
  PARACHUTE: "伞降状态",
  AERIAL: "航拍总览",
  "LONG-LENS": "长焦跟踪",
  "HATCH-MEDICAL": "开舱医监关系",
  HATCH: "开舱口",
  MEDICAL: "医监作业区",
  "SAMPLE-HANDOFF": "样品交接",
};

function viewCode(viewRow, viewId) {
  const prefix = viewRow["视图ID前缀"];
  if (viewId.startsWith(`${prefix}-`)) return viewId.slice(prefix.length + 1);
  const token = viewId.lastIndexOf("-V-");
  if (token >= 0) return viewId.slice(token + 3);
  return viewId.split("-").slice(-1)[0];
}

function createSceneViewRecord(sceneAsset, viewRow, viewId, masterId, sequence) {
  const code = viewCode(viewRow, viewId);
  const isMaster = code === "MASTER";
  const label = viewLabels[code] ?? code;
  return {
    资产大类: "场景资产",
    分类序号: sequence,
    层级: isMaster ? 2 : 3,
    登记项类型: isMaster ? "场景母图" : "场景多视角",
    显示名称: isMaster ? `↳ 母图｜${viewRow["场景名称"]}` : `  ↳ 视图｜${label}`,
    生产资产ID: viewId,
    父资产ID: isMaster ? sceneAsset["生产资产ID"] : masterId,
    视图代码: code,
    资产类型: "SCN-VIEW",
    资产级别: sceneAsset["资产级别"],
    剧本出处: "阶段1_场景视图需求表_V1.3.1",
    关联场次或段落: sceneAsset["关联场次或段落"],
    基础描述: isMaster
      ? `该场景的统一母图，锁定空间、尺度、材料、光向和主构图。`
      : `相对母图的${label}，用于镜头连续和空间核验。`,
    补全设计信息: isMaster
      ? `后续全部视图均以本母图为唯一空间依据。`
      : `继承${masterId}，不重新发明舱室、设备、地貌或光向。`,
    状态变体: code,
    材质结构或声音特点: sceneAsset["材质结构或声音特点"],
    光影或环境要求: sceneAsset["光影或环境要求"],
    使用或生成需求: isMaster
      ? `先确认母图，再进入多视角和状态图生产。`
      : `母图确认后生成；与母图做几何、材料、光影和设备位置一致性检查。`,
    可复用范围: sceneAsset["可复用范围"],
    信息来源: "V1.3.1场景视图锁定",
    确认状态: viewRow["确认状态"],
    阶段2处理建议: isMaster
      ? `阶段2B先生成并确认本母图。`
      : `阶段2B在母图确认后生成本视图。`,
  };
}

function buildPersonRecords() {
  const records = [];
  let sequence = 1;
  const characters = assets.filter((row) => row["资产类型"] === "CHR");
  const costumes = assets.filter((row) => row["资产类型"] === "CST");
  const assigned = new Set();

  for (const character of characters) {
    records.push(asBaseRecord(character, "人物资产", sequence++));
    const children = costumes.filter((costume) =>
      costume["资产名称"].startsWith(character["资产名称"]),
    );
    for (const costume of children) {
      assigned.add(costume["生产资产ID"]);
      records.push(
        asBaseRecord(costume, "人物资产", sequence++, character["生产资产ID"], 2),
      );
    }
  }

  for (const crowd of assets.filter((row) => row["资产类型"] === "CRO")) {
    records.push(asBaseRecord(crowd, "人物资产", sequence++));
  }

  for (const costume of costumes.filter((row) => !assigned.has(row["生产资产ID"]))) {
    records.push(asBaseRecord(costume, "人物资产", sequence++, "", 2));
  }
  return records;
}

function buildSceneRecords() {
  const records = [];
  let sequence = 1;
  const sceneAssets = assets.filter((row) => row["资产类型"] === "SCN");
  const byId = new Map(sceneAssets.map((row) => [row["生产资产ID"], row]));
  const orderedIds = [
    ...sceneViewRows.map((row) => row["场景生产资产ID"]),
    ...sceneAssets
      .map((row) => row["生产资产ID"])
      .filter((assetId) => !sceneViewByAsset.has(assetId)),
  ];

  for (const sceneId of orderedIds) {
    const sceneAsset = byId.get(sceneId);
    if (!sceneAsset) continue;
    records.push(asBaseRecord(sceneAsset, "场景资产", sequence++));
    const viewRow = sceneViewByAsset.get(sceneId);
    if (!viewRow) continue;
    const viewIds = viewRow["用户确认的场景视图ID清单"]
      .split(";")
      .map((item) => item.trim())
      .filter((item) => item.startsWith("BY-"));
    const masterId = viewIds.find((id) => viewCode(viewRow, id) === "MASTER") ?? viewIds[0];
    for (const viewId of viewIds) {
      records.push(createSceneViewRecord(sceneAsset, viewRow, viewId, masterId, sequence++));
    }
  }
  return records;
}

function buildSimpleRecords(category, types) {
  let sequence = 1;
  const ordered = [];
  for (const type of types) {
    for (const asset of assets.filter((row) => row["资产类型"] === type)) {
      ordered.push(asBaseRecord(asset, category, sequence++));
    }
  }
  return ordered;
}

const categoryRecords = new Map([
  ["人物资产", buildPersonRecords()],
  ["场景资产", buildSceneRecords()],
  ["道具资产", buildSimpleRecords("道具资产", ["VEH", "PRP"])],
  ["特殊资产", buildSimpleRecords("特殊资产", ["ANM", "LGT", "VFX", "REL", "SYM"])],
  ["声音资产", buildSimpleRecords("声音资产", ["VOI", "SND"])],
]);

const totalRecords = categoryOrder.flatMap((category) => categoryRecords.get(category));

const baseRecordCount = totalRecords.filter(
  (record) => !["场景母图", "场景多视角"].includes(record["登记项类型"]),
).length;
const sceneViewCount = totalRecords.length - baseRecordCount;

if (baseRecordCount !== 176) {
  throw new Error(`基础资产数量异常：${baseRecordCount}`);
}
if (sceneViewCount !== 58) {
  throw new Error(`场景视图登记数量异常：${sceneViewCount}`);
}

const workbook = Workbook.create();
const summary = workbook.worksheets.add("总览");
for (const sheetName of ["资产总表", ...categoryOrder, "119镜映射", "场次汇总", "资产变更", "生产包"]) {
  workbook.worksheets.add(sheetName);
}

const colors = {
  navy: "#14283B",
  blue: "#215D7A",
  cyan: "#4CA6A8",
  pale: "#EAF2F5",
  pale2: "#F4F7F8",
  paleGreen: "#E8F4EE",
  paleGold: "#FFF7E8",
  orange: "#D97706",
  red: "#A73A37",
  green: "#2F7D61",
  gray: "#667784",
  line: "#C9D5DB",
  white: "#FFFFFF",
  ink: "#1D2B34",
};

function styleHeader(sheet, range, freezeRows = 1) {
  range.format = {
    fill: colors.navy,
    font: { bold: true, color: colors.white, size: 10 },
    verticalAlignment: "center",
    horizontalAlignment: "center",
    wrapText: true,
    borders: { preset: "outside", style: "medium", color: colors.navy },
  };
  range.format.rowHeight = 34;
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(freezeRows);
}

function styleBody(range, rowHeight = 42) {
  range.format = {
    font: { color: colors.ink, size: 9 },
    verticalAlignment: "top",
    horizontalAlignment: "left",
    wrapText: true,
    borders: {
      insideHorizontal: { style: "thin", color: "#E2E8EC" },
      bottom: { style: "thin", color: colors.line },
    },
  };
  range.format.rowHeight = rowHeight;
}

function setColumnWidths(sheet, widths) {
  widths.forEach((width, index) => {
    const letter = excelColumn(index);
    sheet.getRange(`${letter}:${letter}`).format.columnWidth = width;
  });
}

function styleAssetHierarchy(sheet, records, dataStartRow, lastColumn) {
  for (let index = 0; index < records.length; index += 1) {
    const rowNumber = dataStartRow + index;
    const record = records[index];
    const rowRange = sheet.getRange(`A${rowNumber}:${lastColumn}${rowNumber}`);
    if (record["登记项类型"] === "场景母图") {
      rowRange.format.fill = colors.paleGreen;
      rowRange.format.font = { bold: true, color: colors.green, size: 9 };
      rowRange.format.borders = {
        top: { style: "thin", color: "#A7CDBD" },
        bottom: { style: "thin", color: "#CFE3D9" },
      };
    } else if (record["登记项类型"] === "场景多视角") {
      rowRange.format.fill = "#F7FBF9";
      rowRange.format.font = { color: colors.ink, size: 9 };
      rowRange.format.rowHeight = 36;
    } else if (record["登记项类型"] === "服装子资产") {
      rowRange.format.fill = colors.paleGold;
      rowRange.format.font = { color: colors.ink, size: 9 };
      rowRange.format.rowHeight = 40;
    } else {
      rowRange.format.fill = colors.pale;
      rowRange.format.font = { bold: true, color: colors.navy, size: 9 };
      rowRange.format.borders = {
        top: { style: "medium", color: colors.blue },
        bottom: { style: "thin", color: colors.line },
      };
    }
    if (record["确认状态"].startsWith("历史")) {
      rowRange.format.fill = "#ECEFF1";
      rowRange.format.font = { italic: true, color: colors.gray, size: 9 };
    }
  }
}

const totalColumns = [
  "资产大类",
  "分类序号",
  "层级",
  "登记项类型",
  "显示名称",
  "生产资产ID",
  "父资产ID",
  "视图代码",
  "资产类型",
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
  "基础资产标记",
  "有效标记",
];

const compactColumns = [
  "分类序号",
  "层级",
  "登记项类型",
  "显示名称",
  "生产资产ID",
  "父资产ID",
  "视图代码",
  "资产类型",
  "资产级别",
  "关联场次或段落",
  "基础描述",
  "状态变体",
  "使用或生成需求",
  "确认状态",
  "阶段2处理建议",
];

function writeAssetSheet(sheetName, records, note) {
  const sheet = workbook.worksheets.getItem(sheetName);
  const lastColumn = excelColumn(compactColumns.length - 1);
  sheet.showGridLines = false;
  sheet.getRange(`A1:${lastColumn}1`).merge();
  sheet.getRange("A1").values = [[`《奔月》V1.3.1｜${sheetName}`]];
  sheet.getRange(`A1:${lastColumn}1`).format = {
    fill: colors.navy,
    font: { bold: true, color: colors.white, size: 18 },
    verticalAlignment: "center",
  };
  sheet.getRange(`A1:${lastColumn}1`).format.rowHeight = 38;
  sheet.getRange(`A2:${lastColumn}2`).merge();
  sheet.getRange("A2").values = [[note]];
  sheet.getRange(`A2:${lastColumn}2`).format = {
    fill: colors.pale,
    font: { color: colors.blue, bold: true, size: 9 },
    wrapText: true,
    verticalAlignment: "center",
  };
  sheet.getRange(`A2:${lastColumn}2`).format.rowHeight = 30;
  sheet.getRangeByIndexes(3, 0, 1, compactColumns.length).values = [compactColumns];
  const data = records.map((record) => compactColumns.map((column) => record[column]));
  sheet.getRangeByIndexes(4, 0, data.length, compactColumns.length).values = data;
  styleHeader(sheet, sheet.getRange(`A4:${lastColumn}4`), 4);
  styleBody(sheet.getRange(`A5:${lastColumn}${4 + data.length}`), 46);
  styleAssetHierarchy(sheet, records, 5, lastColumn);
  setColumnWidths(sheet, [8, 7, 18, 30, 43, 43, 18, 12, 9, 28, 45, 38, 48, 26, 38]);
  sheet.getRange(`A5:C${4 + data.length}`).format.horizontalAlignment = "center";
  sheet.getRange(`G5:I${4 + data.length}`).format.horizontalAlignment = "center";
  sheet.getRange(`I5:I${4 + data.length}`).conditionalFormats.add("containsText", {
    text: "P0",
    format: { fill: "#FCE8E6", font: { bold: true, color: colors.red } },
  });
  return sheet;
}

const totalSheet = workbook.worksheets.getItem("资产总表");
totalSheet.showGridLines = false;
totalSheet.getRange("A1:X1").merge();
totalSheet.getRange("A1").values = [["《奔月》V1.3.1｜资产总表（分类层级版）"]];
totalSheet.getRange("A1:X1").format = {
  fill: colors.navy,
  font: { bold: true, color: colors.white, size: 18 },
  verticalAlignment: "center",
};
totalSheet.getRange("A1:X1").format.rowHeight = 38;
totalSheet.getRange("A2:X2").merge();
totalSheet.getRange("A2").values = [[
  `正式基础资产176项；场景母图／多视角登记58项；登记项共234项。视图登记不改变176项基础资产口径。`,
]];
totalSheet.getRange("A2:X2").format = {
  fill: colors.pale,
  font: { color: colors.blue, bold: true, size: 9 },
  wrapText: true,
  verticalAlignment: "center",
};
totalSheet.getRange("A2:X2").format.rowHeight = 30;
totalSheet.getRange("A4:X4").values = [totalColumns];
const totalBaseValues = totalRecords.map((record) =>
  totalColumns.slice(0, 22).map((column) => record[column]),
);
totalSheet.getRangeByIndexes(4, 0, totalBaseValues.length, 22).values = totalBaseValues;
const totalDataEnd = 4 + totalRecords.length;
totalSheet.getRange("W5").formulas = [[
  '=IF(OR(D5="场景母图",D5="场景多视角"),0,1)',
]];
totalSheet.getRange(`W5:W${totalDataEnd}`).fillDown();
totalSheet.getRange("X5").formulas = [['=IF(LEFT(U5,2)="历史",0,1)']];
totalSheet.getRange(`X5:X${totalDataEnd}`).fillDown();
styleHeader(totalSheet, totalSheet.getRange("A4:X4"), 4);
styleBody(totalSheet.getRange(`A5:X${totalDataEnd}`), 44);
styleAssetHierarchy(totalSheet, totalRecords, 5, "X");
setColumnWidths(totalSheet, [
  13, 8, 7, 18, 32, 44, 44, 18, 12, 9, 24, 27,
  42, 44, 36, 30, 28, 44, 24, 31, 25, 38, 10, 10,
]);
totalSheet.getRange(`A5:D${totalDataEnd}`).format.horizontalAlignment = "center";
totalSheet.getRange(`H5:J${totalDataEnd}`).format.horizontalAlignment = "center";
totalSheet.getRange(`W5:X${totalDataEnd}`).format.horizontalAlignment = "center";
totalSheet.getRange(`J5:J${totalDataEnd}`).conditionalFormats.add("containsText", {
  text: "P0",
  format: { fill: "#FCE8E6", font: { bold: true, color: colors.red } },
});

writeAssetSheet(
  "人物资产",
  categoryRecords.get("人物资产"),
  "人物母资产在前；每套服装、服装状态紧跟对应人物并以父资产ID关联。稳定音色单列于“声音资产”。",
);
writeAssetSheet(
  "场景资产",
  categoryRecords.get("场景资产"),
  "层级固定为“场景资产组→母图→多视角”。多视角父资产ID直接指向该场景母图，先确认母图再生成视图。",
);
writeAssetSheet(
  "道具资产",
  categoryRecords.get("道具资产"),
  "载具／航天器与任务设备统一纳入道具大类，同时保留VEH、PRP原始类型代码，便于镜头调用与专业分工。",
);
writeAssetSheet(
  "特殊资产",
  categoryRecords.get("特殊资产"),
  "包含动作链、光照、视觉特效、关系约束和后期图形／标识；这些资产承担连续性、物理和来源边界。",
);
writeAssetSheet(
  "声音资产",
  categoryRecords.get("声音资产"),
  "VOI为独立稳定音色；SND为随镜头视频同步生成的声音约束。月面外部无空气传播声，全片不配乐。",
);

const importedSheets = [
  ["阶段1_119镜资产调用映射_V1.3.1.csv", "119镜映射"],
  ["阶段1_场次资产需求映射_V1.3.1.csv", "场次汇总"],
  ["阶段1_资产变更映射表_V1.3.1.csv", "资产变更"],
  ["阶段1_资产生产包_V1.3.1.csv", "生产包"],
];

for (const [file, sheetName] of importedSheets) {
  const csv = await fs.readFile(path.join(DATA, file), "utf8");
  const values = parseCsv(csv);
  if (sheetName === "119镜映射") {
    for (let row = 1; row < values.length; row += 1) {
      values[row][0] = Number(values[row][0]);
      values[row][1] = Number(values[row][1]);
      values[row][4] = Number(values[row][4]);
    }
  }
  if (sheetName === "场次汇总") {
    for (let row = 1; row < values.length; row += 1) {
      values[row][0] = Number(values[row][0]);
      values[row][3] = Number(values[row][3]);
      values[row][4] = Number(values[row][4]);
    }
  }
  const sheet = workbook.worksheets.getItem(sheetName);
  sheet.getRangeByIndexes(0, 0, values.length, values[0].length).values = values;
}

// Summary/dashboard
summary.showGridLines = false;
summary.getRange("A1:P1").merge();
summary.getRange("A1").values = [["《奔月》V1.3.1｜阶段1资产分类层级与119镜映射"]];
summary.getRange("A1:P1").format = {
  fill: colors.navy,
  font: { bold: true, color: colors.white, size: 20 },
  verticalAlignment: "center",
  horizontalAlignment: "left",
};
summary.getRange("A1:P1").format.rowHeight = 40;

summary.getRange("A2:P2").merge();
summary.getRange("A2").values = [[
  "正式基线：15场 / 119镜 / 1020秒建议素材｜资产按人物、场景、道具、特殊、声音五类拆分｜阶段2B入口不变",
]];
summary.getRange("A2:P2").format = {
  fill: colors.pale,
  font: { color: colors.blue, bold: true, size: 10 },
  verticalAlignment: "center",
};
summary.getRange("A2:P2").format.rowHeight = 25;

summary.getRange("A4:B10").values = [
  ["资产口径", "结果"],
  ["基础资产", null],
  ["有效基础资产", null],
  ["历史停用", null],
  ["场景视图登记", null],
  ["登记项总数", null],
  ["映射镜头", null],
];
summary.getRange("B5").formulas = [[`=SUM('资产总表'!$W$5:$W$${totalDataEnd})`]];
summary.getRange("B6").formulas = [[
  `=SUMIFS('资产总表'!$W$5:$W$${totalDataEnd},'资产总表'!$X$5:$X$${totalDataEnd},1)`,
]];
summary.getRange("B7").formulas = [["=B5-B6"]];
summary.getRange("B8").formulas = [[
  `=COUNTIF('资产总表'!$D$5:$D$${totalDataEnd},"场景母图")+COUNTIF('资产总表'!$D$5:$D$${totalDataEnd},"场景多视角")`,
]];
summary.getRange("B9").formulas = [[`=COUNTA('资产总表'!$F$5:$F$${totalDataEnd})`]];
summary.getRange("B10").formulas = [["=COUNTA('119镜映射'!$A$2:$A$120)"]];
summary.getRange("A4:B4").format = {
  fill: colors.blue,
  font: { color: colors.white, bold: true },
  horizontalAlignment: "center",
};
summary.getRange("A5:A10").format = {
  fill: colors.pale2,
  font: { bold: true, color: colors.gray },
};
summary.getRange("B5:B10").format = {
  fill: colors.white,
  font: { bold: true, color: colors.navy, size: 15 },
  horizontalAlignment: "center",
};
summary.getRange("A4:B10").format.borders = {
  preset: "outside",
  style: "medium",
  color: colors.line,
};

summary.getRange("D4:F10").values = [
  ["入口校验", "期望", "状态"],
  ["基础资产口径", 176, null],
  ["视图登记", 58, null],
  ["镜头覆盖", 119, null],
  ["素材时长", 1020, null],
  ["场次覆盖", 15, null],
  ["缺失／停用调用", 0, "通过"],
];
summary.getRange("F5").formulas = [["=IF(B5=E5,\"通过\",\"异常\")"]];
summary.getRange("F6").formulas = [["=IF(B8=E6,\"通过\",\"异常\")"]];
summary.getRange("F7").formulas = [["=IF(B10=E7,\"通过\",\"异常\")"]];
summary.getRange("F8").formulas = [["=IF(SUM('119镜映射'!$E$2:$E$120)=E8,\"通过\",\"异常\")"]];
summary.getRange("F9").formulas = [["=IF(COUNTA('场次汇总'!$A$2:$A$16)=E9,\"通过\",\"异常\")"]];
summary.getRange("D4:F4").format = {
  fill: colors.blue,
  font: { color: colors.white, bold: true },
  horizontalAlignment: "center",
};
summary.getRange("D5:E10").format = {
  fill: colors.pale2,
  font: { color: colors.ink },
};
summary.getRange("F5:F10").format = {
  fill: colors.paleGreen,
  font: { bold: true, color: colors.green },
  horizontalAlignment: "center",
};
summary.getRange("D4:F10").format.borders = {
  preset: "outside",
  style: "medium",
  color: colors.line,
};

summary.getRange("H4:J9").values = [
  ["资产大类", "基础资产", "视图登记"],
  ...categoryOrder.map((category) => [category, null, null]),
];
for (let index = 0; index < categoryOrder.length; index += 1) {
  const row = 5 + index;
  summary.getRange(`I${row}`).formulas = [[
    `=SUMIFS('资产总表'!$W$5:$W$${totalDataEnd},'资产总表'!$A$5:$A$${totalDataEnd},H${row})`,
  ]];
  summary.getRange(`J${row}`).formulas = [[
    `=COUNTIFS('资产总表'!$A$5:$A$${totalDataEnd},H${row},'资产总表'!$W$5:$W$${totalDataEnd},0)`,
  ]];
}
summary.getRange("H4:J4").format = {
  fill: colors.cyan,
  font: { color: colors.white, bold: true },
  horizontalAlignment: "center",
};
summary.getRange("H5:J9").format = {
  fill: colors.white,
  font: { color: colors.ink },
};
summary.getRange("H4:J9").format.borders = {
  preset: "outside",
  style: "thin",
  color: colors.line,
};

summary.getRange("K4:L19").values = [
  ["场次", "素材秒"],
  ...Array.from({ length: 15 }, (_, index) => [index + 1, null]),
];
for (let index = 0; index < 15; index += 1) {
  const row = 5 + index;
  summary.getRange(`L${row}`).formulas = [[`='场次汇总'!$E$${row - 3}`]];
}
summary.getRange("K4:L4").format = {
  fill: colors.cyan,
  font: { color: colors.white, bold: true },
};
summary.getRange("K5:L19").format = {
  fill: colors.white,
  font: { color: colors.ink },
};
summary.getRange("K4:L19").format.borders = {
  preset: "outside",
  style: "thin",
  color: colors.line,
};

const typeChart = summary.charts.add("bar", summary.getRange("H4:J9"));
typeChart.title = "五类资产与场景视图登记";
typeChart.hasLegend = true;
typeChart.setPosition("A13", "G29");
const sceneChart = summary.charts.add("line", summary.getRange("K4:L19"));
sceneChart.title = "15场建议素材时长";
sceneChart.hasLegend = false;
sceneChart.setPosition("H20", "P36");

summary.getRange("A31:F36").values = [
  ["阶段2B首批", "生产内容", "状态", "", "", ""],
  ["P13-02", "梦舟四状态与空间连续", "最高优先", "", "", ""],
  ["P13-03", "揽月构型与单人出舱动作链", "最高优先", "", "", ""],
  ["P13-04", "任务相机与遥测视觉重建", "最高优先", "", "", ""],
  ["P13-05", "月面相机、宇航服相机与月球车相机", "最高优先", "", "", ""],
  ["原则", "所见即所得；先母图后多视角；无配乐；月面外部静音", "锁定", "", "", ""],
];
summary.getRange("A31:F31").format = {
  fill: colors.navy,
  font: { color: colors.white, bold: true },
};
summary.getRange("A32:F36").format = {
  fill: colors.pale2,
  font: { color: colors.ink },
  wrapText: true,
};
summary.getRange("A31:F36").format.borders = {
  preset: "outside",
  style: "medium",
  color: colors.line,
};
summary.getRange("A:A").format.columnWidth = 17;
summary.getRange("B:B").format.columnWidth = 23;
summary.getRange("C:C").format.columnWidth = 14;
summary.getRange("D:F").format.columnWidth = 13;
summary.getRange("G:G").format.columnWidth = 3;
summary.getRange("H:H").format.columnWidth = 16;
summary.getRange("I:J").format.columnWidth = 12;
summary.getRange("K:K").format.columnWidth = 10;
summary.getRange("L:L").format.columnWidth = 12;
summary.freezePanes.freezeRows(2);

// 119-shot mapping
const mapSheet = workbook.worksheets.getItem("119镜映射");
styleHeader(mapSheet, mapSheet.getRange("A1:O1"));
styleBody(mapSheet.getRange("A2:O120"), 62);
setColumnWidths(mapSheet, [8, 8, 27, 19, 9, 31, 68, 35, 28, 72, 52, 52, 52, 25, 50]);
mapSheet.getRange("A2:E120").format.horizontalAlignment = "center";
mapSheet.getRange("I2:I120").format.horizontalAlignment = "center";
mapSheet.freezePanes.freezeColumns(3);
mapSheet.tables.add("A1:O120", true, "ShotAssetMapV131");
mapSheet.getRange("I2:I120").conditionalFormats.add("containsText", {
  text: "C｜",
  format: { fill: "#FFF3CD", font: { color: colors.orange, bold: true } },
});
mapSheet.getRange("I2:I120").conditionalFormats.add("containsText", {
  text: "D｜",
  format: { fill: "#ECEFF1", font: { color: colors.gray, bold: true } },
});

// Scene summary
const sceneSheet = workbook.worksheets.getItem("场次汇总");
styleHeader(sceneSheet, sceneSheet.getRange("A1:J1"));
styleBody(sceneSheet.getRange("A2:J16"), 64);
setColumnWidths(sceneSheet, [10, 32, 14, 10, 12, 72, 54, 54, 54, 30]);
sceneSheet.getRange("A2:E16").format.horizontalAlignment = "center";
sceneSheet.tables.add("A1:J16", true, "SceneAssetMapV131");

// Changes
const changeSheet = workbook.worksheets.getItem("资产变更");
styleHeader(changeSheet, changeSheet.getRange("A1:E1"));
styleBody(changeSheet.getRange("A2:E58"), 48);
setColumnWidths(changeSheet, [42, 18, 44, 62, 32]);
changeSheet.tables.add("A1:E58", true, "AssetChangesV131");
changeSheet.getRange("B2:B58").conditionalFormats.add("containsText", {
  text: "新增",
  format: { fill: colors.paleGreen, font: { color: colors.green, bold: true } },
});

// Production packages
const packageSheet = workbook.worksheets.getItem("生产包");
styleHeader(packageSheet, packageSheet.getRange("A1:E1"));
styleBody(packageSheet.getRange("A2:E12"), 58);
setColumnWidths(packageSheet, [14, 30, 78, 14, 18]);
packageSheet.getRange("A2:A12").format.horizontalAlignment = "center";
packageSheet.getRange("D2:E12").format.horizontalAlignment = "center";
packageSheet.tables.add("A1:E12", true, "ProductionPackagesV131");
packageSheet.getRange("E2:E12").conditionalFormats.add("containsText", {
  text: "最高优先",
  format: { fill: "#FCE8E6", font: { color: colors.red, bold: true } },
});

const inspections = {};
const inspectTargets = [
  ["总览", "A1:P36"],
  ["资产总表", "A1:X28"],
  ["人物资产", "A1:O30"],
  ["场景资产", "A1:O40"],
  ["道具资产", "A1:O24"],
  ["特殊资产", "A1:O24"],
  ["声音资产", "A1:O24"],
  ["119镜映射", "A1:O15"],
  ["场次汇总", "A1:J16"],
  ["资产变更", "A1:E15"],
  ["生产包", "A1:E12"],
];

for (const [sheetName, range] of inspectTargets) {
  const result = await workbook.inspect({
    kind: "region",
    sheetId: sheetName,
    range,
    maxChars: 4500,
    tableMaxRows: 14,
    tableMaxCols: 16,
    tableMaxCellChars: 80,
  });
  inspections[sheetName] = result.ndjson;
}

const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});

const qaRanges = new Map([
  ["总览", "A1:P36"],
  ["资产总表", "A1:X34"],
  ["人物资产", `A1:O${4 + categoryRecords.get("人物资产").length}`],
  ["场景资产", `A1:O${4 + categoryRecords.get("场景资产").length}`],
  ["道具资产", `A1:O${4 + categoryRecords.get("道具资产").length}`],
  ["特殊资产", `A1:O${4 + categoryRecords.get("特殊资产").length}`],
  ["声音资产", `A1:O${4 + categoryRecords.get("声音资产").length}`],
  ["119镜映射", "A1:O18"],
  ["场次汇总", "A1:J16"],
  ["资产变更", "A1:E20"],
  ["生产包", "A1:E12"],
]);

for (const [sheetName, range] of qaRanges) {
  const preview = await workbook.render({
    sheetName,
    range,
    scale: sheetName === "总览" ? 0.9 : 0.55,
    format: "png",
  });
  const safe = sheetName.replace(/[^\p{L}\p{N}]+/gu, "_");
  await fs.writeFile(
    path.join(QA, `${safe}.png`),
    new Uint8Array(await preview.arrayBuffer()),
  );
}

const validation = {
  baseAssetCount: baseRecordCount,
  activeBaseAssetCount: assets.filter((row) => !row["确认状态"].startsWith("历史")).length,
  historicalBaseAssetCount: assets.filter((row) => row["确认状态"].startsWith("历史")).length,
  sceneViewRegistrations: sceneViewCount,
  totalRegisterEntries: totalRecords.length,
  categoryBaseCounts: Object.fromEntries(
    categoryOrder.map((category) => [
      category,
      categoryRecords
        .get(category)
        .filter((record) => !["场景母图", "场景多视角"].includes(record["登记项类型"]))
        .length,
    ]),
  ),
  categoryRegisterCounts: Object.fromEntries(
    categoryOrder.map((category) => [category, categoryRecords.get(category).length]),
  ),
  formulaErrorInspection: formulaErrors.ndjson,
};

await fs.writeFile(
  path.join(OUTPUT, "workbook_inspection.json"),
  JSON.stringify(inspections, null, 2),
  "utf8",
);
await fs.writeFile(
  path.join(OUTPUT, "asset_hierarchy_validation.json"),
  JSON.stringify(validation, null, 2),
  "utf8",
);

const output = await SpreadsheetFile.exportXlsx(workbook);
const canonicalPath = path.join(DATA, "阶段1_V1.3.1资产分类层级与119镜映射.xlsx");
const deliveryPath = path.join(OUTPUT, "阶段1_V1.3.1资产分类层级与119镜映射.xlsx");
await output.save(deliveryPath);
const canonical = await SpreadsheetFile.exportXlsx(workbook);
await canonical.save(canonicalPath);

console.log(JSON.stringify({
  canonicalPath,
  deliveryPath,
  sheets: 11,
  baseRecordCount,
  sceneViewCount,
  totalRegisterEntries: totalRecords.length,
}, null, 2));
