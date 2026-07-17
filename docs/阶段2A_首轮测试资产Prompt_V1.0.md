# 阶段2A｜《奔月》首轮测试资产Prompt V1.0

执行方式：内置GPT Image生成；每条Prompt只服务一个生产资产ID。输出均为横向16:9视觉测试图，不生成文字、徽标、水印或不准确国旗。

Prompt正文执行“所见即所得”：只写当前机位能够直接看见并能从生成图中核验的画面结果。工程原理、任务用途、设计动机、隐藏机构、另一机位／状态、资产登记、继承关系以及事实／艺术补全说明只保留在Prompt外的记录字段中，不进入生图正文。

## BY-2A-TST-001｜杨凛人物剧照验证图

```text
Prompt编号：BY-2A-TST-001
Prompt版本：V1.0
关联生产资产ID：BY-CHR-P0-001-杨凛
上游生产包编号：BY-PKG-01
风格锁定包版本：V1.0-DRAFT
执行小组：阶段2A主控
资产类型：P0角色
资产名称：杨凛人物剧照验证图
生成目的：确认脸、年龄感、真人质感和决策型气质；不固化舱内飞行服
建议模型：GPT Image内置生成模式
参考素材：无人物参考图
必须继承：38-45岁范围；虚构中国航天员；精干训练体型；稳定、决策型、低幅度表情；不绑定现实人物
允许创作补充：具体骨相、眉眼、鼻唇、皮肤细节和鬓角灰比例
禁止改变：角色性别、年龄段、职业气质；禁止现实航天员／演员相似性；禁止英雄摆拍
输出规格：横向16:9，胸部以上，眼平，约85mm等效，中性低反差结构光
确认状态：待主创确认
```

Prompt正文：

```text
Use case: photorealistic-natural
Asset type: Stage 2A P0 fictional character casting still and identity proof for BY-CHR-P0-001-杨凛
Primary request: create a completely fictional Chinese male astronaut commander, about 41 years old, credible as a long-trained crew commander, calm and decisive without heroic posing
Scene/backdrop: seamless warm charcoal-gray studio background, clean and quiet, no spacecraft set
Subject: chest-up portrait; lean trained build; medium-width forehead; slightly square jaw with a gentle taper; straight dark eyebrows; restrained inner-double eyelids; steady dark eyes; straight practical nose; medium lips with low-amplitude expression; short natural black hair with a small amount of gray at the temples; visible pores, slight under-eye structure, subtle facial asymmetry and natural skin color variation
Wardrobe: plain dark gray technical crew-neck base layer only, matte functional fabric, no flight-suit structure, no insignia, no flag, no badge
Style/medium: photorealistic professional casting photograph, believable live-action human, not concept art
Composition/framing: horizontal 16:9, chest-up, eye-level, 85mm portrait perspective, shoulders relaxed, looking slightly beside the lens as if listening to a mission briefing
Lighting/mood: large soft key from 45 degrees front-side, very gentle fill, neutral 5000K, no rim light; restrained, precise, quiet
Color palette: natural warm skin, charcoal gray, muted neutral background
Materials/textures: real pores, individual eyebrow and hair strands, matte fabric weave, no beauty retouching
Constraints: original fictional face; must not resemble any real Chinese astronaut, actor, celebrity or public figure; face fully visible; correct human anatomy; no text; no logo; no watermark
Avoid: wax skin, plastic CGI face, fashion model glamour, overly handsome idol styling, square-jawed propaganda hero, smile for camera, dramatic backlight, cinematic teal-orange, uniform, helmet, medals, flags, spacecraft props
```

检查要点：年龄约41；中国真人感；三庭五眼自然；低幅度表情；无现实人物联想；皮肤与头发不塑料；无服装资产串入。

## BY-2A-TST-002｜梦舟舱内三座布局母图

```text
Prompt编号：BY-2A-TST-002
Prompt版本：V1.0
关联生产资产ID：BY-SCN-P0-001-梦舟舱内三座布局
场景视图ID：BY-SCN-P0-001-梦舟舱内三座布局-V-MASTER
上游生产包编号：BY-PKG-01／BY-PKG-04
风格锁定包版本：V1.0-DRAFT
资产类型：P0场景母图
生成目的：确认三座椅、对接轴、控制区、材料与工程密度
参考素材：无公开舱内设计图；全部内部细节为功能性艺术补全
必须继承：三座椅；座位归属可固定；轴向对接通道方向清楚；空间紧凑；文字后期添加
允许创作补充：未公开内衬、储物、屏幕底图、扶手和接口形制
禁止改变：三座布局、紧凑尺度、无可读文字；不得宣称官方复原
输出规格：横向16:9，MASTER母图，24-28mm受控广角，空舱
确认状态：待主创确认
```

Prompt正文：

```text
Use case: stylized-concept
Asset type: photorealistic production-design master image for BY-SCN-P0-001-梦舟舱内三座布局, scene view BY-SCN-P0-001-梦舟舱内三座布局-V-MASTER
Primary request: a credible near-future Chinese crewed lunar spacecraft return-capsule interior, designed as functional art completion because the real interior is not public; exactly three adjacent contoured crew seats and a clear axial docking-tunnel relationship
Scene/backdrop: compact conical pressure-cabin interior; camera positioned at the docking-tunnel opening looking forward into the cabin; the circular tunnel rim lightly frames the foreground; exactly three slightly reclined seats occupy the central volume; beyond and around them are a compact control and display zone, restraint hardware, storage, handholds and life-support access panels
Subject: empty spacecraft interior, no people; three seat shells clearly separated and equal in engineering family, central seat plus two flanking seats; fixed mounting rails and harness geometry; two restrained side window openings at most; every visible component has a plausible function
Style/medium: photorealistic live-action production design and engineering documentation image, realistic materials, not a glossy sci-fi concept painting
Composition/framing: horizontal 16:9, centered MASTER view, eye-level relative to seated crew, 24-28mm controlled wide angle, enough depth to read all three seats and the axial passage without fisheye distortion
Lighting/mood: neutral 4500K practical ceiling and side lights, low-intensity cool display reflection, controlled medium contrast, no dramatic rim light
Color palette: warm off-white and light gray cabin panels, graphite-gray seats, muted blue-gray fabric, aluminum hardware, very small restrained red safety accents
Materials/textures: matte composite panels, functional woven fabric, aluminum rails, rubber seals, restrained thermal lining, assembly seams and minor realistic use marks
Constraints: exactly three seats, compact believable pressure-cabin volume, docking axis visually clear, no readable interface text, no numbers, no mission logo, no flag, no watermark; functional artistic interpretation only, not an official reconstruction
Avoid: Orion or Crew Dragon copy, Shenzhou copy, luxury cabin, giant empty volume, white consumer-electronics minimalism, holograms, transparent screens, neon strips, excessive random buttons, all-blue lighting, red-alert wash, fisheye, people, loose floating objects
```

检查要点：恰好三座；对接轴可读；座椅、控制区和通道不互相穿插；空间紧凑；无随机文字；无已知外国飞船直接套型。

### BY-2A-TST-002修订记录与V1.1执行Prompt

```text
修订版本：V1.1
修订原因：V1.0的三座椅与轴向通道成立，但控制／显示区不足，尚未清楚表达三岗位如何操作飞船
新增依据：神舟返回舱指挥控制中心功能；中国空间站与神舟公开舱内的面板、扶手、织物、固定和实体控制语言
继承边界：继承V1.0紧凑尺度、恰好三座和轴向通道；不复制天和或神舟的几何布局
```

Prompt正文：

```text
Use case: photorealistic-natural
Asset type: revised Stage 2A production-design master for BY-SCN-P0-001-梦舟舱内三座布局, scene view BY-SCN-P0-001-梦舟舱内三座布局-V-MASTER, version V1.1
Input images: Image 1 is the existing V1.0 Dream return-cabin master and is the composition/three-seat continuity reference. Image 2 is an official Tianhe core-module interior photograph; use only its restrained Chinese panel families, warm-white equipment surfaces, blue handholds, gray functional fabric, fixed stowage and practical lighting language, never its large spatial scale. Image 3 is an official Shenzhou orbital-cabin photograph; use only its dense physical controls and compact equipment organization, never copy its exact layout or broadcast graphics.
Primary request: redesign the existing fictional near-future Chinese lunar return-cabin interior so that exactly three adjacent crashworthy seats, the axial docking-transfer passage and a credible three-person command-and-control zone are all readable in the same image
Scene geometry: compact conical pressure cabin; camera at the axial docking-tunnel opening looking into the cabin; circular hatch rim lightly frames the foreground; exactly three slightly reclined seats sit side by side on fixed rails; preserve clear centerline access to the axial passage; no fourth seat and no large unused cavity
Command-and-control zone: create a restrained wraparound instrument zone above and beside the three seats, within gloved reach: one shared central mission display, two smaller side displays, grouped alarm/status/lighting/communications/environment controls, guarded physical switches, and at least one clearly visible hand controller; screens show only abstract dark interface blocks with no legible text or numbers
Secondary systems: fixed soft stowage, cable restraint, life-support access panels, audio unit, handholds, harness hardware and foot restraints arranged by plausible function; nothing floats loose
Design language: original Dream artistic completion grounded in Chinese human-spaceflight ergonomics; warm off-white modular panels, pale gray quilted liners, graphite seat fabric, aluminum rails, restrained blue handholds and tiny red guarded controls; clean but densely functional
Style/medium: photorealistic live-action practical set and aerospace engineering documentation, not glossy concept art
Composition/framing: horizontal 16:9 centered MASTER, 24-28mm controlled wide angle without fisheye; all three seats fully readable and the operating zone clearly more prominent than V1.0
Lighting: neutral 4500K practical ceiling and side lights, faint cool display reflection only, controlled medium contrast, no rim light and no all-blue wash
Constraints: exactly three seats; no people; compact believable pressure volume; docking axis unobstructed; human-scale controls; no readable text, no numbers, no logo, no flag, no watermark; this is a scientifically constrained fictional design, not an official reconstruction
Avoid: copying Tianhe geometry, copying Shenzhou geometry, Orion, Crew Dragon, luxury cabin, panoramic windows, giant tablet wall, transparent holograms, neon strips, random-button wallpaper, consumer-electronics minimalism, red-alert wash, fisheye, loose objects
```

V1.1检查重点：三座与轴向通道不丢失；中央共享屏＋两侧岗位屏清楚；关键实体控制可读；天和语言只体现在材料与面板组织，不放大成空间站舱段。

### BY-2A-TST-002重新设计记录与V2.0执行Prompt

```text
修订版本：V2.0
修订日期：2026-07-15
修订原因：V1.x三座横排形成座椅墙；后续轨道状态尝试先误读为左右壁挂座椅加中央折叠床，再过度纠偏为双座大空舱和地面走廊。以上方向全部淘汰。
当前可见设计：恰好三张低矮深度后仰座椅；2＋1错位；三座同向；锥顶小尺度轴向舱门；座椅上方和脚端形成开敞体积；紧凑连续控制面板；高密度侧壁。
执行规则：从零生成，不引用失败图；Prompt正文只写当前机位可见信息。
确认状态：待重新生成并由主创确认
```

Prompt正文：

```text
梦舟载人飞船返回舱内部，近未来中国航天器工程实拍质感，舱内没有人物，横向16:9。

相机位于舱体宽端后上方、略偏画面右侧，高于座椅头枕，朝锥形舱体前上方拍摄。镜头看见三张座椅的背面、前方控制区和锥顶对接舱门。32mm等效焦段，透视自然，全景深，画面边缘清晰。

暖白色舱壁从相机所在宽端向前上方明显收拢。锥顶中央是一扇关闭的圆形对接舱门，舱门直径约为舱内最大宽度的四分之一。暖白色金属门板周围可见深灰密封圈、环形框架、机械锁扣和四个蓝色抓握扶手。

三张石墨灰承力座椅安装在舱内下半部。座椅背面与承力地板之间形成约35度夹角，三张椅背在画面中呈低矮、明显后仰的斜面，头枕全部位于画面中线以下。

两张座椅位于前方左中和右中位置，第三张座椅位于左后方，比前方两张后退约半个座椅长度。三张座椅方向一致，形成不对称的三角形排列，不组成横向直线。

镜头只看到三张椅背。每张椅背都有窄型石墨灰缓冲垫、低矮凹形头枕、哑光铝合金后框、两根纵向承力杆、横向连接件、铰链和锁止销。三组底部支架分别固定在深灰色交叉承力梁和短导轨上。

可见地板只形成座椅框架之间和舱壁边缘的窄条区域。三张低矮椅背上方至锥顶舱门之间保持开敞，可见暖白舱壁、蓝色扶手和深色开放空间。座椅之间没有大型水平平台。

前方斜舱壁偏左安装一组浅灰色梯形控制台。控制台上并排安装三块中等尺寸实体显示器，屏幕下方有两排数量克制的实体按键和旋钮。左右两张前方座椅外侧各有一只黑色短手控器。对接舱门正下方只见暖白色舱壁、两个检修盖和蓝色扶手。

三块显示器处于工作状态，深灰黑色画面上只有稀疏的青蓝色细线、简洁曲线和少量无标签矩形状态块，不出现文字、字母、数字或符号。

左右锥形舱壁各有一扇小型圆形耐压舷窗，玻璃呈深黑色，带有微弱舱内灯光反射。舱壁紧凑分布暖白色检修面板、浅灰绗缝内衬、窄型灰色收纳袋、通风格栅、金属固定点和蓝色扶手。侧壁与座椅框架之间距离很小，设备密度高，左右细节存在自然差异。

顶部和左右上侧可见四盏小型矩形舱内灯，4300—4800K中性暖白色。显示器产生极弱的冷色反光。舱壁、座椅和承力结构共享同一组舱内光源，中等对比，高光受控，暗部保留结构。

照片级真实材质：暖白色低反光金属面板、浅灰功能织物、石墨灰座椅、哑光铝合金承力框架、深灰地板梁和蓝色扶手。表面可见细小装配缝、紧固点和轻微使用痕迹。无可读文字，无标识，无徽标，无国旗，无水印。3840×2160，4K。
```

V2.0检查重点：恰好三座且全部可见；三座低矮后仰而非竖直高背；2＋1错位而非横排座椅墙；没有地面大厅式走廊；没有中央折叠床／担架／平台；锥形舱体和小尺度锥顶舱门清楚；控制区不复制两套或三套独立模拟器；屏幕无伪文字。

### BY-2A-TST-002 V3.0局部母图重置Prompt

```text
修订版本：V3.0
修订日期：2026-07-17
上游状态：V1.x、V2.0及梦舟舱内01—05全部淘汰
当前目标：只建立三张椅背、紧凑控制区和贴身弧形舱壁的局部母图
执行规则：从零生成，不上传任何既有梦舟图；只复制下方Prompt正文
确认状态：待生成并由主创确认
```

Prompt正文：

```text
3840×2160，16:9横幅，真实航天器工程样机摄影。近未来中国三人载人月球飞船返回舱内部，空舱。40毫米直线镜头，摄影机贴近三张座椅后方，处于座椅肩部高度，朝前方控制区拍摄。

三张薄型深灰色航天座椅紧密并列，占据画面下半部。三张座椅尺寸相同、方向相同，金属侧梁相互平行，三个头部支撑排列在同一条浅弧线上。镜头清楚看到深灰色织物椅背、完整的刚性背部框架、独立头部支撑和少量铝合金连接件，画面下沿裁切座椅底座。

左右两张座椅的内侧扶手各有一只小型黑色操纵手柄。三张座椅前方紧邻一组紧凑控制面，控制面下沿接近头部支撑。三块尺寸相同的中型显示器沿浅弧排列，屏幕呈现简洁的蓝青色月球轨道、飞船姿态、推进状态、电源状态和生命保障状态。显示器下方是一条窄控制带，带有少量旋钮、保护框开关和状态灯。

弧形压力舱壁紧密包围三张座椅，左右舱壁贴近外侧座椅框架，并向前方控制区逐渐收拢。舱壁由米白色喷涂铝合金面板组成，表面清楚可见螺钉、铆钉、接缝、锁扣和检修盖板。局部覆盖浅灰色绗缝防护软包，侧面固定灰色织物收纳袋、小型通风格栅和短蓝色金属扶手。

材料表面呈哑光质感，面板之间存在轻微色差，金属边缘带有细小磨损，织物有自然褶皱。舱顶暖白色任务灯照亮座椅和控制区，显示器发出微弱冷蓝光。空间紧凑、密实，真实曝光，清晰自然，载人航天工程纪录片质感。
```

V3.0检查重点：三张椅背是否平行且紧密；画面是否裁掉大厅式地板；外侧座椅是否贴近弧形舱壁；控制面是否紧邻头枕；材料是否为喷涂金属、真实紧固件、织物与局部软包，而非洁净塑料科幻舰桥。

## BY-2A-TST-003｜月面着陆与作业区母图

```text
Prompt编号：BY-2A-TST-003
Prompt版本：V1.0
关联生产资产ID：BY-SCN-P0-004-月面着陆与作业区
场景视图ID：BY-SCN-P0-004-月面着陆与作业区-V-MASTER
上游生产包编号：BY-PKG-01／BY-PKG-06
风格锁定包版本：V1.0-DRAFT
资产类型：P0场景母图
生成目的：确认地貌、太阳方向、揽月尺度、舷梯朝向和作业空间
参考素材：通过后的BY-VEH-P0-003揽月登月舱首轮测试图；无正式着陆点资料
必须继承：月面固定太阳光；无大气；单一主空间；无地球；无国旗；无人物
允许创作补充：缓坡、浅洼、碎石密度和远景低起伏地貌
禁止改变：太阳从MASTER左前方进入、阴影右后；不得出现雾、蓝天、尘烟和奇观地貌
输出规格：横向16:9，MASTER母图，28mm等效，略高于人物视线的稳定机位
确认状态：待主创确认
```

Prompt正文：

```text
Use case: stylized-concept
Asset type: photorealistic lunar production-design master image for BY-SCN-P0-004-月面着陆与作业区, scene view BY-SCN-P0-004-月面着陆与作业区-V-MASTER
Input images: Image 1 is the generated BY-VEH-P0-003-揽月登月舱 structural reference; preserve its overall silhouette, landing-leg geometry, hatch and ladder side, materials and scale
Primary request: establish one physically credible lunar landing and activity zone for a future Chinese crewed landing documentary simulation
Scene/backdrop: gently uneven gray lunar regolith with a shallow depression, low ridges and sparse small rocks; deep black sky; no atmosphere; broad safe working area around the lander; low distant terrain, not mountains
Subject: the confirmed Lanyue landing craft stands firmly on four landing pads, slightly left of center; the hatch-and-ladder operations side faces the open work zone; show a clear safe corridor from ladder foot to the foreground and enough open space for a later portable camera, flag apparatus, sampling, science equipment and rover route, but do not place those assets yet
Style/medium: photorealistic live-action lunar mission photography and practical production design, restrained future documentary realism
Composition/framing: horizontal 16:9 MASTER view; camera south of the site looking north, approximately 2.2 meters high, 28mm controlled wide angle; horizon low enough to read terrain and working relationships; no fisheye and no hero poster angle
Lighting/mood: single hard neutral sunlight from local southwest azimuth 225 degrees at elevation 22 degrees, appearing from frame-left and slightly forward; shadows cast clearly toward frame-right and deeper into the scene; only very weak gray regolith bounce; no fill light, no atmospheric haze
Color palette: mineral gray regolith, deep black sky, restrained off-white, aluminum and pale-gold lander materials
Materials/textures: fine dry regolith, small angular rocks, crisp contact shadows, subtle disturbed dust around landing pads without suspended dust
Constraints: no people, no flag, no rover, no camera, no science instruments, no footprints, no readable markings, no Earth, no stars visible at surface exposure, no text, no logo, no watermark
Avoid: blue or purple sky, fog, atmospheric perspective, clouds, blowing dust, smoke, hovering dust cloud, wet sand, Sahara dunes, dramatic mountains, giant crater wall, colorful nebula, Apollo landing site copy, cinematic anamorphic flare
```

检查要点：黑天空；无雾；固定光向；地貌可作业；揽月尺度可信；舷梯面向开放区；不提前加入后续道具。

### BY-2A-TST-003修订记录

```text
修订版本：V1.1
修订原因：V1.0中的载具过高、过窄，与独立揽月结构验证图的宽扁低重心方向不一致
本次修改：把载具限制为宽大于高、低矮上舱、宽设备体、中央矩形舱门、短梯、四支腿和顶部对接环；保留原月面地貌与光向规则
当前结果：V1.1作为月面空间候选；仍需在参考图链可用后完成精确载具继承
```

## BY-2A-TST-004｜揽月登月舱结构验证图

```text
Prompt编号：BY-2A-TST-004
Prompt版本：V1.0
关联生产资产ID：BY-VEH-P0-003-揽月登月舱
上游生产包编号：BY-PKG-01／BY-PKG-05
风格锁定包版本：V1.0-DRAFT
资产类型：P0载具
生成目的：确认推进舱分离后登月舱的整体形制、支腿、舷梯、舱门、材料和着陆／起飞一体逻辑
建议模型：GPT Image内置生成模式
参考素材：两张中国载人航天工程网2025年揽月着陆起飞综合验证试验照片，只用于公开试验工程语言，不复制试验塔、吊索、伞具或地面环境
必须继承：两人往返、可携月球车与科学载荷、登月舱＋推进舱体系中的登月舱、无留月下降级
允许创作补充：未公开表面分区、舱门、舷梯、支腿细节和隔热材料拼接
禁止改变：一体着陆／驻留／起飞逻辑；禁止阿波罗复制、Starship构型和装饰性科幻件
输出规格：横向16:9，完整载具三分之四前视，50mm等效，月面中性结构验证环境
确认状态：待主创确认
```

Prompt正文：

```text
Use case: product-mockup
Asset type: photorealistic engineering validation still for BY-VEH-P0-003-揽月登月舱
Input images: Image 1 and Image 2 are official public photographs of the 2025 Lanyue landing-and-takeoff verification test; use them only as factual engineering-lineage references; do not copy the test tower, suspension cables, red parachute system, ground rig or terrestrial background
Primary request: create a credible artistic completion of the Lanyue crewed lunar landing cabin after separation from its propulsion module, designed as one integrated craft that lands, supports two astronauts on the surface, takes off again with its landing gear still attached, and docks in lunar orbit; no separate descent stage is left on the Moon
Scene/backdrop: neutral gray lunar surface with a low horizon and deep black sky, no atmosphere; no other vehicles or people
Subject: complete compact landing craft in a stable three-quarter front view; low center of mass; pressurized central cabin; four widely splayed landing legs with broad pads; functional external equipment bays; one clearly identifiable side hatch and deployable ladder/handrail path; upper docking interface; restrained propulsion and attitude-control hardware; geometry must support landing, EVA access, ascent and later docking
Style/medium: photorealistic aerospace engineering documentation image, plausible near-future Chinese design language, realistic scale and materials, not concept-art spectacle
Composition/framing: horizontal 16:9, whole craft visible with generous margin, three-quarter front at approximately 50mm perspective, camera slightly below cabin center but not a hero angle
Lighting/mood: single hard neutral sunlight from frame-left/front at 22-degree elevation, crisp shadow toward frame-right/back, extremely weak regolith bounce, no fill or rim light
Color palette: restrained warm off-white, aluminum silver, graphite gray, muted pale-gold thermal blankets, tiny functional red accents only if structurally necessary
Materials/textures: matte insulated panels, restrained multilayer insulation, metal struts, composite covers, seals, fasteners and slight assembly variation; no glossy toy surfaces
Constraints: preserve integrated landing-and-ascent logic; four landing legs remain part of the craft; realistic hatch, ladder and human scale; no readable text, no flag, no mission patch, no logo, no watermark; artistic interpretation within public information limits, not an official reconstruction
Avoid: Apollo lunar module copy, American LM descent stage, Starship, flying saucer, military armor, giant panoramic windows, wings, decorative fins, neon lights, holograms, excessive gold foil, random antennas, exposed impossible plumbing, test tower, suspension cables, parachutes, terrestrial sky
```

检查要点：整器可着陆又可起飞；四腿、舱门、舷梯、对接口关系合理；不出现留月下降级；不复制试验设施；材料克制；无文字与不准确标识。

### BY-2A-TST-004修订记录与V1.1执行Prompt

```text
修订版本：V1.1
修订原因：V1.0的一体起降逻辑成立，但整体仍偏通用登月器，设备舱与承力关系不够清楚
新增依据：官方公开的“两人往返、携带月球车／科学载荷、登月舱＋推进舱、着陆起飞综合验证”功能边界
继承边界：保留宽扁低重心、四腿、舱门／舷梯、顶部对接区；不把试验塔、吊索、伞系统写入飞行构型
```

Prompt正文：

```text
Use case: product-mockup
Asset type: revised photorealistic engineering validation still for BY-VEH-P0-003-揽月登月舱, version V1.1
Input images: Image 1 and Image 2 are official public photographs from the 2025 Lanyue landing-and-takeoff verification test; use them only as evidence of a compact integrated landing/takeoff test article and Chinese engineering restraint, never copy the tower, cables, parachute system, terrestrial background or test rig. Image 3 is the existing V1.0 fictional Lanyue image; preserve only its broad low silhouette, four-leg stance, central hatch/ladder side and upper docking region, then redesign the generic details.
Primary request: create an original, scientifically credible artistic completion of the Lanyue crewed lunar landing cabin after propulsion-module separation: one integrated two-person craft that lands, supports surface operations, carries interfaces for a lunar rover and science payload, takes off with the landing legs still attached, and docks again in lunar orbit; no descent stage is left behind
Overall architecture: broad shallow faceted pressure cabin over a clear central load-bearing lower structure; width visibly greater than main body height; low center of mass; four widely spaced landing legs tied into visible structural hardpoints; broad pads and believable shock struts; adequate ground clearance for the central propulsion group
Operations side: one human-scale rectangular EVA hatch with rounded corners, outward handholds and a short rigid deployable ladder reaching a safe first step; two suited astronauts could pass one at a time; the hatch/ladder path must not cross thrusters or fragile equipment
Orbital-return functions: compact upper docking collar and restrained rendezvous sensor mounting zone; attitude-control clusters positioned with clear fields of fire and away from the hatch; propulsion hardware integrated into the craft instead of a separate Apollo-style descent stage
Payload and service organization: two or three disciplined external equipment bays integrated into the broad side body, including a plausible rover/science-payload carrier interface and thermal-control surfaces; panels form a consistent modular family, not random boxes
Design language and materials: restrained near-future Chinese aerospace engineering; warm off-white and light-gray insulated panels, matte aluminum, graphite structural members, limited pale-gold multilayer insulation only where needed, very small red safety handhold accents; clean, functional, maintainable, no decorative national styling
Scene: complete craft alone on neutral gray lunar regolith, low horizon, deep black sky, no atmosphere, no people and no other vehicle
Composition: horizontal 16:9, full craft with generous margin, stable three-quarter front view at about 50mm perspective, camera near lower-cabin height, not a hero poster angle
Lighting: one hard neutral sun from frame-left/front at 22-degree elevation, crisp shadow to frame-right/back, extremely weak gray regolith bounce, no fill, no rim light
Constraints: exactly four landing legs remain attached; integrated landing-and-ascent logic; realistic human scale; hatch, ladder, legs, docking collar and propulsion do not conflict; no readable text, no flag, no insignia, no logo, no watermark; fictional completion inside public facts, not official reconstruction
Avoid: Apollo lunar module silhouette, separate descent stage, Starship cylinder, flying saucer, faceted military armor, gold-foil-heavy body, giant windows, decorative fins, wings, neon lights, excessive antennas, impossible exposed plumbing, test tower, suspension cables, parachutes, Earth sky
```

V1.1检查重点：四腿随整器起飞；设备舱并入宽扁主体；舱门／舷梯避开推进与姿控喷口；顶部对接结构可读；不依赖国旗或文字形成“中国感”。

## BY-2A-TST-005｜工程化国旗展示装置结构验证图

```text
Prompt编号：BY-2A-TST-005
Prompt版本：V1.0
关联生产资产ID：BY-PRP-P0-004-工程化国旗展示装置
上游生产包编号：BY-PKG-01／BY-PKG-06
风格锁定包版本：V1.0-DRAFT
资产类型：P0关键道具
生成目的：确认折叠基座、立杆、上下横向张紧、锁止与加压手套操作逻辑
参考素材：嫦娥五号官方国旗展开结果照片，只参考平展状态与无风环境；不复制无人探测器安装方式
必须继承：不普通插杆；双人搬运／展开；旗面无风摆动；月面固定太阳光
允许创作补充：基座收纳壳、折叠支臂、足垫、防尘罩、真空兼容铰链和手套锁止件
禁止改变：准确五星红旗图形不由模型生成；不得虚构深钻锚固、风吹旗面或永久悬浮波浪
输出规格：横向16:9，完整装置三分之四结构验证视图，50mm等效，月面中性环境
确认状态：待主创确认
```

Prompt正文：

```text
Use case: product-mockup
Asset type: photorealistic engineering validation still for BY-PRP-P0-004-工程化国旗展示装置
Input image: official Chang'e-5 lunar flag-display result, used only to understand a taut fabric panel in vacuum and the absence of wind; do not copy its spacecraft-mounted mechanism or any logos
Primary request: design a portable human-deployed lunar flag display apparatus for two suited astronauts, scientifically grounded in vacuum, one-sixth gravity, abrasive lunar dust and pressurized-glove operation; it must not be an ordinary pole pushed into the soil
Structure: a low rectangular transport case becomes the central base mass; four fold-out stabilizer arms form a broad cross footprint with wide footpads and shallow anti-slip cleats; a telescoping vertical mast hinges upright from the base; upper and lower horizontal battens extend from the mast and keep a rectangular fabric panel gently tensioned; large over-center locks, guarded release levers and high-contrast grip areas are sized for bulky gloves
Mechanism details: covered hinge gaps, simple hard stops, visible lock confirmation geometry, restrained dust shields and minimal exposed sliding surfaces; plausible vacuum-compatible material pairing and dry-lubricated joints are suggested visually, with no delicate open gears
Fabric state: use a plain solid red rectangular test fabric with absolutely no stars, emblem, letters or symbol; the accurate national-flag graphic will be composited later; fabric is flat between upper and lower battens with only a tiny natural material curvature, completely still with no wind waves
Scene: apparatus fully deployed by itself on level gray lunar regolith, deep black sky, no astronaut and no other object; shallow footpad impressions only, no drilled hole
Style: photorealistic aerospace hardware documentation and live-action prop engineering, restrained Chinese near-future design language, compact and carryable by two suited astronauts
Composition: horizontal 16:9, stable three-quarter view at about 50mm, full apparatus and footprint visible with generous margin; human scale inferred from glove-sized handles
Lighting: one hard neutral sun from frame-left/front at 22-degree elevation, crisp shadow to frame-right/back, weak regolith bounce only
Color/materials: matte aluminum and graphite structure, warm-white transport case, restrained blue grip markers and tiny red safety latches; solid red placeholder fabric; no decorative gold foil
Constraints: freestanding wide base; no ordinary pole planting; no deep auger; no wind; no people; no stars; no flag emblem; no text; no logo; no watermark; all members structurally connected and lockable
Avoid: waving flag, wind ripples, floating cloth, single flimsy pole, terrestrial tripod photography stand, deep drilling machine, exposed gears, decorative sci-fi lights, military styling, inaccurate Chinese flag, readable labels
```

检查要点：基座自立且有宽支撑面；立杆与上下横杆可收纳并锁止；操作件适合手套；旗面静止；图中不生成星位。
