# loggy


# 1. Introduction and Background

# 项目介绍与背景

**loggy** 是一个工业用：

**Data Logger（数据记录器）**

这种设备也经常被称为：

**DAQ**

发音为：

**“dack”**

DAQ 是：

**Data Acquisition（数据采集）**

的缩写。

简单来说，Data Logger 是一种能够从：

**多个 Sensor Channels（传感器通道）**

记录数据，并长期跟踪这些数据变化的设备。

部分 Data Logger 还具有额外功能，例如：

* Alarm 报警
* 内置数学运算
* 数据处理
* 其他分析功能

通常还会配套 PC Software，使用户能够方便地查看和分析数据。

---

这种设备经常用于：

* 工业环境中的故障排查
* 工业过程监控
* 科学研究
* 实验数据记录
* 不同物理现象监测

市场上的典型产品包括：

* NI mioDAQ
* Pico Technology PicoLog
* LabJack
* Keysight DAQ973A

---

## 常见应用示例

### 1. 工业生产监测

调查、故障排除和监控 Manufacturing Process。

例如：

使用 Temperature Sensor 长期监测一桶牛奶的温度，从而确认：

**UHT（Ultra-high-temperature）超高温灭菌工艺**

是否正确完成。

### 2. 地震/振动监测

使用 Accelerometer：

监测 Ground Vibration

从而检测：

* Earth Tremor
* Earthquake

发生的时间和强度。

这种仪器也称为：

**Seismometer（地震仪）**

### 3. 噪声污染监测

记录一段时间内的：

**Peak Sound Level**

用于测量：

**Noise Pollution**

### 4. 内燃机监测

使用：

* Chemical Sensors
* Temperature Sensors

长期监测 Internal Combustion Engine 的：

* Combustion Efficiency
* Pollution Output

### 5. 桥梁和建筑监测

使用：

**Strain Gauge（应变计）**

长期监测：

* Bridges
* Buildings

的 Mechanical Strain。

---

一般来说，Data Logger 主要测量：

**Voltage 随时间的变化。**

但是，并不是所有 Sensor 都直接输出 Voltage。

因此通常需要使用针对传感器设计的：

**Signal Conditioning Circuit**

将 Sensor Output 转换成与其物理量成比例的 Voltage。

---

# 2. Device Details

# 设备详细要求

---

# 2.1 Constant Current Source

# 恒流源

测量 Resistive Sensor 的一个简单方法是：

将电阻的一端连接到：

**Constant Current Source**

另一端连接：

**Ground**

然后测量恒流源输出的 Voltage。

通过：

**Ohm's Law（欧姆定律）**

就可以计算被测电阻值。

---

设备必须提供：

**两个 Screw Terminals（螺丝端子）**

分别连接两个恒流源：

### 恒流源 1

**10 μA**

### 恒流源 2

**200 μA**

每个 Current Source 的精度必须达到：

**±5%**

同时恒流源必须能够至少输出：

**3 V**

这些 Terminal 应放置在：

**Measurement Input Terminals 附近。**

---

# 2.2 Sensing and Measurement

# 传感与测量

设备必须能够测量：

**4 个独立 Voltage Channels**

分别称为：

* CH1
* CH2
* CH3
* CH4

每个 Voltage Channel 的 Resolution 必须：

**≥16 bit**

---

## Voltage Range

完整的 16-bit Resolution 必须能够分别应用于两个输入范围：

### Range 1

**±1 V**

### Range 2

**±10 V**

用户必须能够通过：

**User Interface**

动态选择使用哪个 Range。

---

例如：

如果选择：

**±1 V**

那么整个 16-bit Resolution 必须分布在：

**-1 V 到 +1 V**

之间。

也就是说：

Range Switching 必须通过：

**Analog Circuitry**

完成。

不能仅仅测量 ±10 V 后，再通过：

**Digital Scaling**

变成 ±1 V。

---

无论目前选择哪个 Range：

设备的 Voltage Input 都必须能够承受：

**±11 V**

而不会损坏。

---

## Input Impedance

Voltage Input 的输入阻抗必须：

**> 1 MΩ**

因此：

每个 Channel Input Circuit 中的第一个 Component 应该是：

* Voltage Buffer
* Voltage Follower
* 或类似电路

---

## Voltage Accuracy

Voltage Reading 的 Accuracy 必须在：

**Full-scale Range 的 5% 总范围内，即 ±2.5%**

例如：

### ±10 V Range

误差必须：

**≤ ±500 mV**

### ±1 V Range

误差必须：

**≤ ±50 mV**

---

## Range Switching

Voltage Range 是：

**整个设备统一选择**

不能让：

* CH1 使用 ±1 V
* CH2 使用 ±10 V

这种混合配置。

也就是说 CH1～CH4 必须同时使用同一个 Range。

---

# 2.3 Voltage Input Screw Terminals

4 个 Measurement Channels 必须通过：

**8 个 Screw Terminals**

引出。

排列如下：

1. CH1
2. GND
3. CH2
4. GND
5. CH3
6. GND
7. CH4
8. GND

也就是说，每个 Voltage Channel 都有自己的：

* Signal
* Ground

Terminal。

PCB 上必须：

**清晰标注每一个 Screw Terminal 应连接的 Signal。**

---

# 2.4 Accelerometer

设备必须包含：

**3-axis Accelerometer（三轴加速度计）**

用于 Data Logging。

每一个 Axis 的 Resolution 必须：

**≥8 bit**

三个 Axis 分别作为独立 Channel：

* X → CH5
* Y → CH6
* Z → CH7

---

# 2.5 Temperature Sensor

设备必须包含一个：

**Onboard Temperature Sensor**

用于测量：

**Ambient Temperature（环境温度）**

Temperature Resolution 必须：

**≤1°C**

即能够分辨 1°C 或更小的变化。

这个 Temperature Sensor 是系统的：

**CH8**

---

# 2.6 Sampling Rate

每个 Channel 的 Sample Rate 必须：

**≥2 Hz**

各个 Channel 不要求完全在同一瞬间进行 Sampling。

但是：

**所有 8 个 Channel 必须在 100 ms 的 Window 内完成一次采样。**

平均下来大约：

**12.5 ms / Channel**

---

CH1～CH4 中的每一个 Voltage Channel：

都可以独立配置成：

**Resistive Temperature Measurement Mode**

配合前面的 Constant Current Source 测量 Resistive Temperature Sensor。

后面会进一步说明。

---

# 3. Display, Physical Controls and Indicators

# 显示、实体控制和指示灯

设备必须至少使用以下 Components 向用户显示设备状态。

---

## 3.1 Power LED

必须有：

**Power LED**

* Device Active → LED On
* Device 没有 Power → LED Off

---

## 3.2 LCD

必须使用：

**20×4 Character LCD**

ETSG Part：

**24-05-10**

---

## 3.3 Sampling LED

必须有一个：

**Sampling LED**

设备进行 Channel Sampling 时：

**闪烁。**

如果 Sampling Window 太短，可以人为延长 LED 的点亮时间。

例如：

如果所有 Sampling 在：

**100 μs**

内完成，那么 Sampling LED 可能非常暗，甚至看起来没有亮。

此时可以将 LED 点亮时间人为延长到：

**约 100 ms**

---

# 3.4 Alarm LEDs

必须有：

**16 个红色 LED**

每一个 Channel：

**2 个 LED**

共：

8 Channels × 2 = **16 LEDs**

这些 LED 用来显示某个 Channel 是否发生 Alarm。

如果某个 Channel 已经配置了 Alarm：

两个 Alarm LED 中：

**应该始终至少有一个亮起**

用于表示：

* Alarm 正在发生
* Alarm 未发生

PCB 上必须清楚标注：

**哪个 LED 表示 Alarm 正在发生。**

---

# 3.5 Buttons

最多允许：

**10 个 Momentary Push Buttons**

用于控制 Device Function。

也可以使用：

**Multi-position Momentary Joystick-like Switch**

替代其中部分 Buttons。

例如：

Digikey EG4561-ND。

---

# 3.6 Debug LEDs

允许增加额外 LED 用于：

**Debugging**

但在：

**Final Demonstration**

中，这些 LED 必须：

* 被禁用
* 或移除

---

# 3.7 LCD Mechanical Mounting

Display Module 必须使用：

**Mechanical Fasteners**

例如：

* Standoffs
* Screws

机械固定在：

**PCB**

上。

---

# 4. Alarms

# 报警系统

每一个 Channel 都必须能够设置两个：

**Alarm Threshold**

分别为：

* High Threshold
* Low Threshold

---

发生以下情况时认为出现 Alarm：

### High Alarm

Measurement：

**> High Threshold**

### Low Alarm

Measurement：

**< Low Threshold**

---

软件必须阻止用户设置：

**High Threshold < Low Threshold**

这种不合理配置。

---

Threshold 必须使用：

**该 Channel 的实际物理单位**

来配置。

不能使用：

**ADC Counts**

例如 CH1 应使用 Voltage，而不是 ADC Raw Value。

---

每个 Channel 的两个 Alarm LEDs：

必须显示当前：

**Alarm 是否发生。**

---

# 4.1 Alarm Modes

Alarm 可以设置为三种 State：

### Disabled

禁用

### Live

实时模式

### Latching

锁存模式

---

## Disabled Mode

该 Channel 的：

**所有 Alarm LEDs 都关闭。**

---

## Live Mode

Alarm State 根据：

**最新一次 Sample**

实时更新。

也就是说：

是否 Alarm 只取决于：

**Most Recent Sample**

前面是否发生过 Alarm 不重要。

---

## Latching Mode

每一次 Sampling 都会更新 Alarm Condition。

但是：

一旦 Alarm Condition 被触发：

**Alarm 将永久保持 On。**

这种状态称为：

**Latched**

直到用户执行 Un-latch 操作。

---

# 5. PC Communication

# PC 通信

设备与 PC 通信只能使用：

**Seeeduino Xiao**

ETSG Part：

**24-01-01**

并运行：

**polyglot-turtle-xiao firmware**

这是：

**唯一允许的 PC Communication 方式。**

---

# 6. Power Supply

# 电源

设备必须使用：

**Bench Power Supply（实验室台式电源）**

供电。

连接使用：

**3-pin Molex KK Connector**

这个 Connector 提供：

* Positive Voltage Rail
* Negative Voltage Rail

实际电压由你在 Bench Power Supply 上选择。

---

提交产品时：

必须提供一根用于连接：

**Device ↔ Bench Power Supply**

的 Cable。

Cable 一端：

**Molex KK Connector**

另一端：

**3 根 Bare Wires**

以便连接 Bench Power Supply。

根据 TP-STD 的要求：

还必须提供这根 Cable 的：

**Schematic。**

---

# 6.1 USB Power

设备可以使用：

**USB Cable 的 5 V**

但是：

**Microcontroller 必须运行在 3.3 V。**

USB Power 可能来自：

* PC
* USB Power Supply
* Power Bank

如果 Power Bank 没有 Data Connection：

PC Communication 无法使用。

但设备本身：

**仍然必须能够正常工作。**

---

# 6.2 Polyglot Turtle 3.3 V

可以将：

**polyglot-turtle 的 3.3 V Output**

连接到 Device。

但不能从中获取大量 Current。

最大：

**50 mA**

因为这个 Output 并不是用于大功率供电。

---

# 6.3 Other Power Sources

**禁止使用任何其他 Power Source。**

---

# 7. PC Software and User Interface

# PC 软件和用户界面

---

# 7.1 On-device Interface

# 设备本地界面

设备必须能够在本地 Display 上显示：

**任意 Channel 的最新 Reading。**

单位：

### CH1～CH4

**V**

### CH5～CH7

**m/s²**

### CH8

**°C**

---

Reading 必须至少显示：

**小数点后 3 位**

同时必须显示：

**对应单位。**

---

设备 Display 必须能够：

**同时至少显示 2 个 Channels。**

并且必须能够通过 Device 上的 Buttons：

**Scroll 浏览其他 Channels。**

---

Display 只需要按照 Channel 顺序显示。

例如：

可以：

CH1 → CH2 → CH3 → CH4

不需要支持：

CH1 → CH4 → CH7 → CH3

这种乱序显示。

---

# 7.2 Voltage Range Selection

Device 上必须具有一个：

**On-device Interface**

允许用户选择：

* ±1 V
* ±10 V

同时当前选择的 Range：

**必须显示在 LCD 上。**

---

# 7.3 Alarm Un-latch

Device 必须提供：

**On-device Interface**

允许用户：

**Un-latch 已经锁存的 Alarm。**

---

# 7.4 PC Connection Status Icon

LCD 必须显示：

**PC Software 当前是否连接。**

必须在：

* Connected
* Disconnected

两种情况下都显示对应的 Status Icon。

必须使用：

**Pictographic Symbol（图形符号）**

例如：

类似 USB Logo。

不能只使用：

* 数字
* 字母
* 文本

来表示。

---

LCD 还必须具有：

**Alarm Status 的图形 Icon**

用于表示：

是否存在任何 Alarm。

---

# 7.5 Standalone Operation

Device 上的所有 On-device Function：

**无论 PC Software 是否打开或连接，都必须能够工作。**

---

# 8. PC Software

必须开发：

**PC GUI Application**

通过 USB 与 Device Communication。

该程序有两个主要用途：

### 1. Configure Device

配置 Device。

### 2. View Measurements

实时查看 Device Measurement。

---

下面两种功能必须在 Device Connected 时才能使用：

* Configure Parameters
* Live Data Viewing

但是：

**Replay Mode**

必须能够在：

**Device 没有连接**

的情况下使用。

---

# 8.1 GUI Configuration

PC Application 必须能够查看和配置：

### Alarm Parameters

每一个 Channel 的：

* High Threshold
* Low Threshold
* Alarm Type

GUI 还必须以：

**Read-only**

形式显示：

**所有 Channel 当前 Alarm State。**

---

### Input Range

配置：

* ±10 V
* ±1 V

---

# 8.2 Parameter Synchronisation

如果 GUI 修改了任何 Configurable Parameter：

Device 必须在：

**1 秒以内**

更新。

反过来：

如果用户通过 Device 修改参数：

GUI 也必须在：

**1 秒以内**

同步更新。

---

所有这些参数必须存储在 Device 的：

**Non-volatile Memory**

中。

因此：

即使设备断电再开机：

设置仍然必须保留。

---

PC Software 第一次连接 Device 时：

必须：

1. 读取 Device 当前 Existing State
2. 根据 Device State 更新 GUI Controls

而不是直接用软件 Default Value 覆盖设备设置。

---

# 9. Plotting

# 实时绘图

GUI 必须显示：

**Device 当前 Measurement 的 Live Plots**

每当收到新的 Measurements：

Plot 必须更新。

---

用户必须可以选择显示以下三种 Plot：

### Plot 1

Voltage Channels

CH1～CH4

### Plot 2

Acceleration Channels

CH5～CH7

### Plot 3

Temperature Channel

CH8

---

# 9.1 Y-axis

每一个 Plot 都必须允许用户配置：

**Visible Y-axis Range**

---

# 9.2 Maximum Number of Points

用户必须能够配置：

**图中最大显示数据点数量**

范围：

**10～1000 Points**

---

# 9.3 Axis Units

Y-axis 必须显示：

**正确的物理单位。**

X-axis 必须显示：

**Relative Time**

相对时间起点是：

以下两者中较晚发生的那个：

* Device 连接 PC Software 的时间
* Data 上一次被 Clear 的时间

---

# 9.4 Plot Layout

所有 Plot 必须拥有：

**完全相同的 X-axis。**

GUI 中的 Plot 必须排列在：

**Single Column**

也就是：

一个在上，一个在下。

Plots 应占据 GUI：

**大部分 Screen Space。**

---

# 9.5 Mouse Hover

如果 Mouse Hover 在任意一个 Plot 上：

GUI 中必须有一个区域，以：

**Text Format**

显示该时间点：

**全部 8 个 Channel Measurements**

如果没有完全相同时间的 Sample：

则显示距离 Mouse 对应时间：

**最近的 Sample。**

---

# 9.6 Plot Appearance

Plot 必须具有：

**Legend**

所有 Measurement Points 都应该显示：

### Marker

例如：

**X**

同时：

相邻 Points 之间必须通过：

**Line**

连接。

每一条 Line 必须具有：

**Unique Colour。**

---

# 9.7 Clear Data

GUI 必须具有一个：

**Button**

用于：

**Clear 所有 Plot Data。**

---

# 10. Recording

# 数据记录

PC Application 必须能够：

* Start Recording
* Stop Recording

Device Sampling Data。

---

# 10.1 CSV Format

每完成：

**全部 8 Channels**

的一轮 Sampling 后：

System 必须将 Readings 写入：

**CSV File**

每一行格式：

```text
YYYY-MM-DD_HH-MM-SS.sss,CH1,CH2,CH3,...
```

其中：

`YYYY-MM-DD_HH-MM-SS.sss`

表示：

**Current Date and Time**

精度需要达到：

**1 millisecond**

`CHx`

表示：

对应 Channel 的 Reading。

使用与 User Interface 相同的实际单位数值：

但是：

**CSV 中不需要写单位字符。**

---

# 10.2 CSV Header

CSV 第一行必须包含：

**Appropriate Headings**

每个 Channel Heading 必须包括：

* Channel Name，例如 CH1
* Channel Unit

---

# 10.3 Filename

Recording 开始时：

使用：

**First Sample 的 Timestamp**

作为 File Name。

格式：

```text
YYYY-MM-DD_HH-MM-SS.csv
```

注意：

Filename 中：

**Milliseconds 被删除。**

例如 Sample Timestamp 如果是：

```text
2025-05-07_12-30-15.123
```

则 File Name 类似：

```text
2025-05-07_12-30-15.csv
```

之后所有 Samples 都必须继续写入：

**同一个 CSV File**

直到：

**Recording Stop。**

---

# 10.4 Recording 时禁止修改 Configuration

Recording 正在运行时：

**不能修改 Channel Configuration。**

例如：

* Voltage Range
* 其他 Channel Settings

---

# 11. Replay

# 回放模式

PC Software 必须具有：

**Replay Mode**

用于查看之前 Recorded CSV File。

---

如果 CSV 中的 Samples 数量：

大于用户设置的：

**Maximum Number of Points**

那么软件只显示：

**最近的 Samples**

数量不能超过用户设置的 Limit。

---

File Load 完成以后：

所有可见 Samples 应当：

**立刻显示。**

不能像 Live Mode 那样一点一点播放。

---

Replay Mode 必须根据：

**CSV File Headings**

自动判断某些 Channels 是否处于：

**Resistive Temperature Measurement Mode**

并以正确方式 Plot Data。

---

Replay Mode 中：

X-axis 应显示：

**Relative Time**

时间起点是：

**CSV 第一条 Sample 的 Timestamp。**

---

# 12. Resistive Temperature Measurement Mode

# 电阻式温度测量模式

通过：

**PC Software**

CH1～CH4 中每一个 Voltage Channel：

都可以：

**独立配置**

成 Resistive Temperature Channel。

---

用户必须能够选择：

## Current Source

* 10 μA
* 200 μA

以及：

## Temperature Sensor Type

两种类型：

### 1. Thermistor

热敏电阻

### 2. Platinum RTD

铂电阻温度传感器

---

如果某个 Voltage Channel 被配置成：

**Resistive Temperature Channel**

那么该 Channel：

**不再作为 Voltage Plot。**

而是：

1. 测量 Voltage
2. 根据 Constant Current 计算 Resistance
3. 使用对应 Sensor Equation
4. 将 Resistance 转换为 Temperature

最终显示：

**Temperature**

---

这些 Temperature Data：

必须与：

**Ambient Temperature CH8**

画在：

**同一个 Temperature Plot / Axis**

上。

---

# 12.1 Device LCD 不转换 Temperature

需要特别注意：

Resistive Temperature Channel 的配置：

**只存在于 PC Software 中。**

Device 上的 LCD：

仍然必须显示：

**Voltage Measurement**

而不是 Temperature。

---

# 12.2 Sensor Parameters

不同的：

* Thermistor
* RTD

具有不同的参数。

这些参数必须用于：

**Resistance → Temperature**

转换。

---

你们必须：

选择：

* 1 种具体 Thermistor
* 1 种具体 RTD

并根据：

**这两个具体 Component 的正确参数**

配置 System。

---

Final Demo 时：

必须提供：

**这两个 Temperature Sensors**

供测试人员使用。

---

# 12.3 RTD 类型

RTD 必须从以下两种类型中选择一个：

* Pt100
* Pt1000

---

RTD 和 Thermistor 都必须选择：

**Through-hole Style**

这样更方便连接：

**Screw Terminals。**

如果 Sensor 已经自带 Wire：

也可以接受。

---

如果 Sensor 没有自带足够长的 Wire：

建议在提交产品前：

增加合适的 Wire。

长度至少：

**100 mm**

方便 Final Demo Testing。

---

# 13. Construction and Physical Dimensions

# 产品结构

Final Product 必须使用：

**一个或多个自行设计的 Custom PCB**

构建。

---

所有 Components，例如：

* Display
* Buttons
* Batteries
* 其他元件

必须：

**安装在 PCB 上或固定到 PCB。**

---

禁止使用其他额外 Mounting Frame，例如：

* 3D Printed
* Laser Cut
* 其他结构框架

---

# 13.1 Breadboard

如果最终提交的 Product 使用：

**Breadboard**

那么：

**Final Demo 最高成绩限制为 50%。**

---

# 13.2 Approved Breakout Boards

以下 Breakout Boards 可以使用，而且不会触发 Course Profile 中的 Grade Hurdles：

### 1.

Seeeduino Xiao

只能运行：

**polyglot-turtle-xiao Firmware**

### 2.

前面规定的 Display Module

### 3.

只包含以下元件的 Breakout：

* Accelerometer
* Decoupling Capacitors

### 4.

只包含以下元件的 Breakout：

* Op-amp
* Decoupling Capacitors

### 5.

只包含以下元件的 Breakout：

* ADC
* Decoupling Capacitors

---

# 14. Budget / Bill of Materials

# BOM 与预算

Final Product 的 BOM 总价格必须：

**≤ 100 AUD**

不包括：

**GST**

---

团队拥有：

**200 AUD ETSG Development Budget**

可以使用以下三种方式消费：

### 1. ETSG Store

校内位置：

**50-S309**

### 2. Pinecone

用于：

**Order PCB**

### 3. Hazelnut

用于：

**从 DigiKey Order Parts**

---

也可以直接从：

**TP-STD Approved Suppliers**

购买。

也允许从 Non-approved Supplier 购买，但前提是：

Approved Supplier 中存在：

**Equivalent Part**

但是：

这种自行购买：

**不能 Reimbursement。**

---

# 14.1 BOM 不计入的物品

以下物品：

**不需要计入 BOM Cost**

### USB Cable

### 两个 Resistive Temperature Sensors

### Power Supply Cable

但是：

虽然不计入 BOM：

**提交作品时仍然必须提供这些物品。**

---

# 15. Components Included in Locker

# Locker 提供的元件

团队 Locker 中已经包含：

### 1. Display Module

前面规定的 LCD Module。

### 2. Seeeduino Xiao

用于：

**polyglot-turtle Firmware**

### 3. Jumper Wires

各种 Jumper Wires。

### 4. ATMEGA328P

ETSG Part：

**10-03-03**

### 5. AVR ISP Breakout

ETSG Part：

**16-56-01**

---

# 16. Other Notes and Recommendations

# 其他说明和建议

下面的内容：

**不一定是项目强制要求。**

而是：

**Hints and Tips**

目的是帮助开发过程更加顺利。

---

## Alarm LED 建议

建议 Alarm LEDs 使用：

**Surface Mount LEDs（贴片 LED）**

例如：

ETSG Part：

**63-07-03**

对应：

**0805 Package LED**

原因是：

这些 LED 可以在 PCB Assembly 时：

**一次性通过 Reflow / Oven Soldering 焊接。**

---

# 整个 loggy 项目的核心结构总结

最终的 loggy 实际上是一个：

**8 Channel Industrial Data Acquisition System（工业数据采集系统）**

---

## CH1～CH4

4 个外部：

**Voltage Input Channels**

要求：

* ≥16-bit Resolution
* ±1 V / ±10 V 可切换
* > 1 MΩ Input Impedance
* ±11 V Input Protection
* Voltage Accuracy 满足规定
* 也可以通过 Constant Current Source 测量 Resistive Temperature Sensor

---

## CH5～CH7

来自：

**3-axis Accelerometer**

分别：

* CH5 = X
* CH6 = Y
* CH7 = Z

Resolution：

**≥8 bit**

单位：

**m/s²**

---

## CH8

来自：

**Onboard Ambient Temperature Sensor**

单位：

**°C**

Resolution：

**1°C 或更好**

---

## Sampling

每个 Channel：

**≥2 Hz**

全部 8 Channels：

必须在：

**100 ms**

以内完成一轮 Sampling。

---

## Constant Current Sources

必须提供：

* 10 μA
* 200 μA

Accuracy：

**±5%**

Output：

**至少 3 V**

---

## Alarm

每个 Channel：

* High Threshold
* Low Threshold

Alarm Modes：

* Disabled
* Live
* Latching

共：

**16 个 Red Alarm LEDs**

---

## LCD

必须使用：

**20×4 Character LCD**

至少同时显示：

**2 Channels**

并显示：

* Measurement
* Unit
* Voltage Range
* PC Connection Icon
* Alarm Icon

---

## PC GUI

必须实现：

* USB Communication
* Configure Alarm
* Configure Voltage Range
* 实时同步 Settings
* Live Plot
* Voltage Plot
* Acceleration Plot
* Temperature Plot
* Mouse Hover 查看 8 Channels
* Clear Data
* Recording
* CSV 保存
* Replay Mode
* Resistive Temperature Conversion

---

## CSV Recording

每轮 8 Channels Sampling 后保存：

```text
YYYY-MM-DD_HH-MM-SS.sss,CH1,CH2,CH3,...
```

File Name：

```text
YYYY-MM-DD_HH-MM-SS.csv
```

---

## Resistive Temperature

CH1～CH4 可以在 PC Software 中独立转换为：

**Temperature Channel**

支持：

* Thermistor
* Pt100 / Pt1000 RTD
* 10 μA / 200 μA Current Source

但 Device LCD 仍显示：

**Voltage。**

---

## Hardware

最终必须：

* Custom PCB
* 20×4 LCD
* Accelerometer
* Temperature Sensor
* ≥16-bit ADC
* Constant Current Circuit
* Alarm LEDs
* Buttons
* Seeeduino Xiao
* Bench Power Supply Interface

Final Product：

**不能使用 Breadboard**

否则最高只有：

**50%。**

---

## BOM

Final Product：

**≤100 AUD，不含 GST**

团队开发预算：

**200 AUD**

loggy

Investigating/troubleshooting/monitoring processes in manufacturing - for example, using a temperature sensor to monitor the temperature of a vat of milk over time to ensure that the UHT process has been correctly implemented.
Monitoring ground vibrations with an accelerometer to detect the onset and magnitude of earth tremors/earthquakes (also known as a seismometer)
Measuring peak sound levels over time when measuring sound/noise pollution
Monitoring combustion efficiency and pollution output of an internal combustion engine over time using various chemical and temperature sensors
Monitoring mechanical strain in bridges and buildings over time using strain gauges
Data logger devices generally only measure voltage over time (though there are some notable exceptions). Not all sensors will generate an output voltage, and as such they are typically used with some sensor-specific conditioning electronics to turn the sensor output into a proportional voltage.

Device details
Constant current source
A simple way to measure a resistive sensor is to connect one side of the resistor to a constant current source, and the other side to ground. Then, by monitoring the voltage being output by the constant current source, one can use Ohm's law to calculate the resistance under test.

Your device must provide two screw terminals that are connected to constant current sources - one which is 10uA and one which is 200uA. Each current should be accurate to within +/- 5% and this current source must be able to output at least 3V. These terminals should be located near the measurement input terminals on the device.

Sensing and measurement
Your device must be able to measure four separate voltage channels with a resolution of 16 bits or higher - these channels are hereafter referred to as channels 1 to 4 (CH1-CH4). The full resolution must be distributed over two ranges, either +/- 1V or +/- 10V, with the user able to dynamically select which range they would like to use through the user interface. Thus, if the user selects the +/-1V range, the 16 bit resolution should be spread over only the +/- 1V range (ie the range switching must be done using analog circuitry, not using digital scaling). Regardless of which range is selected, the device should be able to withstand +/- 11V being applied to the inputs. Your voltage inputs must have an input impedance of greater than 1 MOhm - to do this, the first component in your channel input circuitry should be a voltage buffer, voltage follower or similar circuit.

Voltage accuracy of the reading must be within 5% (+/-2.5%) of the full-scale range. This means that for the +/- 10V range, the voltage must be accurate to within +/- 500mV, and in the 1V range it must be accurate to +/- 50mV.

The range switching selection applies to the entire device - it is not possible to configure one channel in the +/- 1V while another is in the +/- 10V range.

The four measurement channels must be exposed using 8 screw terminals - every second terminal connects to one of the measurement channels, and every other terminal is connected together and to GND:

CH1
GND
CH2
GND
CH3
GND
CH4
GND
You must clearly label on your PCB the signal which is expected to be connected to a given screw terminal.

Your device must contain a 3 axis accelerometer for logging purposes. Each axis must have a resolution of at least 8 bits, and each axis will be considered a channel in your acquisition system (X = CH5, Y = CH6, Z = CH7).

Your device must contain an onboard temperature sensor that measures the ambient temperature to a resolution of 1C or better. This temperature sensor should be considered to be the eighth measurement channel (CH8) of your system.

Each channel must be sampled at a rate of 2Hz or higher, but the channels do not need to be sampled at exactly the same instant - all channels must be sampled within a 100ms window (average 12.5ms per channel).

Each of these four channels may independently be configured into a resistive temperature measurement mode in combination with the constant current sources. This will be described further in this document.

Display, physical controls and indicators
Your device must use at least the following items to inform the user of the device state:

A power LED (on when the device is active, and off when the device has no power)
A 20x4 character LCD (ETSG part 24-05-10)
A sampling LED (that blinks while the device is sampling the channels)
16 red LEDs (two per channel) that indicate if an alarm is occurring on a given channel (one or the other should always be on if the alarm has been configured, and it must be clearly labelled on the PCB which LED indicates that the alarm is occurring)
The sampling LED may be time-extended if the sampling window on the device is extremely short. For example, if all sampling occurs within 100us, then the sampling LED will be very dim or look as though it is not turned on. In this case, you should artificially increase the LED on-time to something more reasonable (like 100ms).

You are permitted to have up to 10 momentary push buttons to allow the user to control the functions on the device. You may optionally use a multi-position momentary joystick-like switch as some of these buttons (for example, Digikey part EG4561-ND).

You may have additional LEDs for debugging purposes but these must be disabled or removed for the final demonstration.

You must use mechanical fasteners (standoffs, etc) to mechanically attach the display module to your PCB.

Alarms
Each channel must be able to be configured with two alarm thresholds, hereafter referred to as the high and low thresholds. An alarm is considered to occur if the measurement is greater than the high threshold or lower than the low threshold. The user should be prevented from configuring the high threshold to a value lower than the low threshold.

These thresholds must be set by the user in the actual units of the channel, not in arbitrary ADC counts.

The two alarm LEDs for a given channel should indicate to the user whether an alarm has occurred or not.

An alarm can be configured into one of three states:

Disabled
Live
Latching
In the disabled mode, all alarm LEDs for that channel are off. In the live mode, the alarm state is triggered and updated based on the most recent sample - the alarm will be occurring or not depending on only the most recent sample. In the Latching mode, the alarm is triggered and updated on each sample, but once the alarm condition is triggered, the alarm will be permanently on (in this case, the alarm is said to be "latched").

PC communication
Your device must use the polyglot-turtle-xiao firmware with a Seeeduino Xiao (ETSG part 24-01-01) as the only means of communication with the PC.

Power supply
The device must be powered via the bench power supply and a 3 pin Molex KK connector. This connector will supply a positive and negative voltage rail at a voltage that you select on the bench power supply. You need to provide a cable to connect your device to the power supply as part of your submission - on one end will be the Molex KK connector, and on the other will be three bare wires which can be connected to the bench power supply. As per the TP-STD documents, you must provide a schematic of this cable as part of your submission.

The device may use 5V from the USB cable (but your microcontroller must operate at 3.3V). Note that this power may come from a PC, or it may come from a USB power supply such as a power bank with no data connection present - your device must operate in both cases although PC communication will not be possible if there is no data connection.

It is acceptable to connect the 3.3V output from the polyglot-turtle to your device, but you should not draw any significant current from it (max 50mA) as it is not designed for this purpose.

You are not permitted to use any other sources of power.

PC software and user interface
On-device interface
Your device must be able to locally display the most recent reading on any channel (CH1-4 in volts, CH5-7 in m/s^2 and CH8 in Celsius). The reading must show at least three digits after the decimal point and also show the appropriate units for the channel.

Your device must be capable of showing at least two of the channels at once on the display, and there must be a method for scrolling through these using the on-device buttons.

The display only needs to show consecutive voltage channels and never channels out of order (ie it would never show the channels in the order CH1, CH4, CH7, CH3...).

Your device must have an on-device interface to allow selecting the voltage input range, and the state of this must be visible on the display.

Your device must have an on-device interface for the user to un-latch any alarms that are latched.

The display must show a status icon to indicate whether the PC software is connected or not. An icon should still be present to indicate the negative state (disconnected from PC software). You must use a pictographic symbol (for example, something that looks like the USB logo) and not just alphanumeric characters to indicate this. The display must have a pictographic icon to indicate whether any of the alarms have occurred.

The on-device functionality must function regardless of whether the PC software is opened and connected or not.

PC software
To configure your device, you must have a GUI application that runs on your PC and communicates with the device over the USB connection. This application serves to allow the user the configure the device, but also to view the measurements generated by the device. The configuration of parameters and live viewing of data must only be possible while a device is connected, but the replay mode must be usable regardless of whether a device is connected.

Your application must allow the viewing and configuration of the following parameters on the device:

The alarm high and low thresholds for each channel, as well as their type. The interface should also show (in a read-only format) the current alarm states for all channels.
The input range setting (+/- 10V or +/- 1V)
If any of these configurable parameters are changed, they must be updated on the device within 1 second (and vice versa with any changes on the device). All of these parameters must be stored in non-volatile memory on the device such that they survive any power cycling. When first connecting to the device, the software must read the existing state of the device and set the GUI controls accordingly.

Plotting
The GUI must show a live plots of the measurements being performed by the device, and they must be updated as new measurements arrive. The user must be able to select if any of three plots are visible:

The voltage channels
The acceleration channels
The temperature channel
The user must be able to configure the visible Y axis range of each of these plots, and the maximum number of points visible (in the range of 10-1000 points). The Y axis must show the appropriate units, and the X axis must show the relative time since the device was connected to the software, or since the data was last cleared (whichever is more recent).

All plots must have identical X axes, and must be drawn in the GUI in a single column. The plots should take up the majority of the screen space of the application.

If the mouse is hovered over any plot, an area of the user interface must show (in textual format) all eight channel measurements at, or closest to, the corresponding sample time.

The plot must have a legend, and all measurement points should be visible with both markers (for example, an 'X' symbol) and with a line connecting adjacent points to each other. Each line must have a unique colour.

Your interface must have a button to clear all the data in the plots.

Recording
Your application must have a method to start and stop recording of the sampled data.

After all 8 channels are sampled, your system must record the readings in a CSV file with the following format on each line:

YYYY-MM-DD_HH-MM-SS.sss,CH1,CH2,CH3,...
where YYYY-MM-DD_HH-MM-SS.sss is the current date and time (down to a resolution of 1 millisecond), and CHx is the reading (in the same units as the user interface, but without the unit text characters).

The first line of the file should contain appropriate headings for each channel, containing the channel name (ie CH1) and the units of the channel.

When a recording is started, the timestamp of the first sample should be used as the filename, and a .csv suffix appended on the end: YYYY-MM-DD_HH-MM-SS.csv (note the milliseconds have been discarded). All subsequent samples should be written to this same file until the recording is stopped.

While recording is running, it must not be possible to change the configuration of the channels (voltage range, etc).

Replay
It must be possible to use your software in a replay mode, where the contents of a recorded file can be viewed. If there are more samples in the recording than the maximum number of points specified by the user, the software should display only the most recent samples up to this limit. All visible samples should be shown instantly once the file has been loaded. The replay mode must automatically detect if any channels are in the resistive temperature measurement mode using the headings in the CSV file and plot the data accordingly.

In the replay mode, the X axis should show the relative time since the timestamp of the first sample in the CSV file.

Resistive temperature measurement mode
Using the PC software, each of the four voltage channels should be able to be independently configured as a resistive temperature channel. The user should be able to select which current source is being used (10uA or 200uA) and which type of temperature sensor is being used (one of each type: a thermistor and a platinum RTD). The voltage channel should then no longer be plotted as a voltage, and instead converted as a temperature using the appropriate equations to convert the measured voltage into a temperature. The temperature data will be plotted on the same axis as the ambient temperature plot (CH8).

This temperature channel configuration exists in the PC software only - your on-device LCD should still display the measurements in volts.

Note that different thermistors/RTDs have different parameters that need to be used to convert the resistance into temperature. You must select one of each of these types of component and configure your system to work with the correct parameters for these two components. You must provide these two sensors for use during the final demo.

For the RTD, you must select one of the following types: Pt100 or Pt1000. Both the RTD and thermistor you choose must be of the through-hole style to make them easier to connect to your screw terminals. Devices with wires already connected are also acceptable.

If they are not already present, is recommended that you attach appropriate wires (at least 100mm) to your temperature sensors before handing your product in to make testing easier.

Construction and physical dimensions
Your final product must be constructed using one or more custom designed PCBs. All components (display, buttons, batteries, etc) must be mounted on or to the PCB - no other mounting frames (3D printed, laser cut, etc) are permitted.

Submitting your product on breadboard will result in your maximum mark for the final demo being limited to 50%.

The following breakout boards are approved for use without triggering the grade hurdles outlined in the course profile:

Seeeduino Xiao (running the polyglot-turtle-xiao firmware only)
The display module mentioned previously
Any breakout board which contains only an accelerometer and/or decoupling capacitors
Any breakout board which contains only an op-amp and/or decoupling capacitors
Any breakout board which contains only an ADC and/or decoupling capacitors
Budget/Bill Of Materials (BOM)
Your final product must have a BOM total of $100 AUD or less (excluding GST). Your team will have a $200 AUD development budget available at ETSG; you can spend your ETSG development budget in one of three ways:

At the ETSG store (on campus in 50-S309), see also How to use the ETSG store
Using pinecone to order PCBs
Using hazelnut to order parts from DigiKey
Alternatively, you can order directly from any of the approved suppliers in the TP-STD documents (or a non-approved supplier as long as an equivalent part is available at an approved supplier), but reimbursement will not be possible.

You do not need to include the cost of the USB cable, the two resistive temperature sensors or the power supply cable in your BOM, but you must still provide them with your submission.

Components included in your locker
The display module mentioned previously
A Seeeduino Xiao to be used with the polyglot-turtle firmware.
Various jumper wires
ATMEGA328P (ETSG part 10-03-03): https://www.digikey.com.au/product-detail/en/microchip-technology/ATMEGA328P-PU/ATMEGA328P-PU-ND/1914589
AVR ISP breakout (ETSG part 16-56-01): https://www.adafruit.com/product/1465
Other notes and recommendations
The following are not necessarily requirements for the project, rather they are hints and tips that may make things go more smoothly for you.

It is recommended that you use surface mount LEDs for the alarm LEDs (for example, ETSG part number 63-07-03 for an LED in an 0805 package) as they can be oven soldered all at once.
