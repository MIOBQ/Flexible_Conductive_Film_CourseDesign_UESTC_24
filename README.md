# 基于 COMSOL 的压阻式压力传感器课程设计

本仓库对应电子科技大学（UESTC）2024 级《柔性导电薄膜制备与仿真》课程设计。项目以 COMSOL Multiphysics 5.6 官方 **Piezoresistive Pressure Sensor, Shell** 案例为基准，围绕压阻式压力传感器的几何、材料参数、材料类型及工作偏置条件建立对照模型，并完成压力响应仿真与比较。

> 本仓库中的结果均为 COMSOL 数值仿真结果，并非实物测试数据。

## 研究思路

1. 以原始模型 A 为统一基准，在 `p1=100 kPa`、偏置电压 3 V 下验证工作电流和差分输出电压。
2. 在不改变硅薄膜承压结构、压力范围和四端测量原理的前提下，分别研究几何宽度、互连区掺杂输入和偏置电压的影响。
3. 通过 A/B/C/D 的 2×2 对照区分几何因素、材料参数因素及二者的交互作用。
4. 以 n 型单晶硅和蛇形导电路径扩展材料类型与真实几何轮廓对照。
5. 在 0–200 kPa、25 kPa 步长的九个压力点下，对比工作电流、差分输出电压、功耗、灵敏度和线性度。

## 仿真环境与共同条件

- 软件：COMSOL Multiphysics 5.6
- 力学接口：Shell
- 电学接口：Electric Currents, Single Layer Shell
- 耦合：Piezoresistive Effect
- 默认压力扫描：`p1 = 0, 25, ..., 200 kPa`
- 默认偏置：Terminal 1 = 3 V（E 模型除外）
- 压敏区掺杂输入：`1.32e19[1/cm^3]`
- 压敏层厚度：`400[nm]`

## 模型说明

| 标识 | 推荐 `.mph` 文件 | 对照内容 | 说明 |
|---|---|---|---|
| A | `Pressure_Sensor_Original.mph` | 原始基准 | 官方 Shell 压阻传感器模型，3 V。 |
| B | `Pressure_Sensor_GeometryOnly.mph` | 仅几何 | X 形压敏电阻臂 r1/r2 宽度由 10/20 μm 调整为 11/22 μm；互连区掺杂保持原值。 |
| C | `Pressure_Sensor_MaterialOnly.mph` | 仅材料参数 | 几何保持 A；互连区掺杂输入由 `1.45e20` 调整为 `1.8e20[1/cm^3]`。 |
| D | `Pressure_Sensor_Modified.mph` | 几何 + 材料参数 | 同时采用 B 的宽度调整和 C 的互连区掺杂输入。 |
| E | `Pressure_Sensor_Original_2V.mph` | 仅工作条件 | 几何、材料和载荷保持 A；Terminal 1 由 3 V 调整为 2 V。 |
| F | `Pressure_Sensor_NType_SingleCrystal_Sweep.mph` | 探索性材料类型 | 导电区域由 p 型单晶硅改为 n 型单晶硅，保持原有掺杂输入和几何。应注意：COMSOL 内置轻掺杂材料模型用于当前高掺杂输入时，仅作探索性数值对照。 |
| G | `Pressure_Sensor_Serpentine_Sweep.mph` | 蛇形真实几何 | 在保留四端测量结构的基础上，通过 Difference 槽形成蛇形导电路径，用于几何轮廓改变对照。 |

`*_100kPa.mph` 为对应模型的 100 kPa 单点验证版本；`*_pre_*.mph`、`*_pending.mph`、`Diagnostics/`、`TaperedX*` 和 `*Exploratory*.mph` 为备份、诊断或未作为最终 A–G 对照结论依据的中间文件。

## 目录结构

```text
.
├─ Automation/           COMSOL Java API 自动化、断点续算与启动脚本
├─ COMSOL_Models/        A–G 正式模型、单点验证版本及必要备份
├─ Figures/              几何图、应力/位移/电势云图和曲线图
├─ References/           课程任务与模型说明等参考资料
├─ Simulation_Results/   真实求解 CSV、拟合汇总、比较表和求解日志
├─ Report_Draft/         课程设计报告及图 3-1 的导出核验记录
├─ .gitignore            Git 忽略规则
└─ README.md             本说明文件
```

### `Simulation_Results/` 与 `Figures/` 子目录

- `Original/`：A 模型的压力扫描、基准结果和图件。
- `GeometryOnly/`、`MaterialOnly/`、`Modified/`：B、C、D 的对应结果和图件。
- `Controlled_Comparison/`：A–D 四模型的因素效应、交互项和性能汇总。
- `Extended_Design/`：E 模型 2 V 工况结果及 2 V/3 V 对比。
- `Material_Replacement/`：F 模型的材料审计、单点验证和压力扫描结果。
- `Serpentine_Design/`：G 模型的几何审计、单点验证、九点扫描及 A/G 比较。
- `Comparison/`：早期原始/联合修改模型的直接比较结果。

## 主要输出指标

- 工作电流：`ecs.I0_1`
- 差分输出电压：`ecs.V0_2-ecs.V0_3`
- 工作功耗：`P = Vbias × I`
- 电压灵敏度：对 `Vout-p` 九点数据进行线性拟合的斜率
- 线性度：拟合决定系数 `R²`

输出电压始终保留 COMSOL 的原始符号；比较幅值时会另行说明，不能将不同偏置电压下的绝对输出直接用于结构优劣排名。

## 复现建议

1. 使用 COMSOL 5.6 打开需要的 A–G `.mph` 文件。
2. 核对 `p1`、Terminal 1 电压及 `std1` 的稳态/参数化扫描设置。
3. 使用已提供的 `Automation/` 脚本时，先启动 COMSOL Multiphysics Server，并避免多个客户端同时写入同一模型或 CSV。
4. 结果分析优先读取 `Simulation_Results/` 中的 CSV，而非手工抄录图上数据。
5. 若重新求解，保存到新的独立模型或结果文件，避免覆盖本仓库的已验证 A–G 数据。

## 数据解释限制

- F 模型是高掺杂输入条件下使用 COMSOL 内置轻掺杂 n-Si 材料模型的探索性对照，不能替代经实验或高掺杂参数标定后的器件预测。
- E 为 2 V 偏置，其功耗与信号幅值不应直接作为与其余 3 V 结构模型的同条件性能排序依据。
- 所有结论反映当前模型、边界条件、网格和扫描范围下的数值响应；尚未包含制造偏差、噪声、温漂、接触效应等实验因素。

## Git 使用说明

`.gitignore` 会保留正式 A–G `.mph`、CSV 和 PNG 结果，同时忽略 COMSOL 锁文件、自动化编译产物、临时备份和诊断模型。单个正式 `.mph` 文件低于 GitHub 的 100 MB 单文件限制；若后续大量增加二进制模型，建议使用 Git LFS。
