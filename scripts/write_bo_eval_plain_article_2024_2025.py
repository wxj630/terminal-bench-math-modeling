#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write a plain-language Chinese article explaining the BO-Eval results."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import math
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
JOBS_ROOT = REPO_ROOT / "jobs"
ARTICLE_PATH = JOBS_ROOT / "terminus2-bo-eval-plain-language-article-2024-2025.md"
ARTICLE_PATH_2023_2025 = JOBS_ROOT / "terminus2-bo-eval-plain-language-article-2023-2025.md"
sys.path.insert(0, str(SCRIPTS_ROOT))


MODEL_ORDER = ["flash", "pro", "glm", "kimi", "gpt", "opus5", "gemini37flash"]
ANSWER_MODEL_ORDER = ["pro", "glm", "kimi", "gpt", "opus5", "gemini37flash"]
SHORT_MODEL_LABEL = {
    "flash": "v4 flash",
    "pro": "v4 pro",
    "glm": "GLM-5.3",
    "kimi": "Kimi K3",
    "gpt": "GPT-5.6 Sol",
    "opus5": "Claude Opus 5",
    "gemini37flash": "Gemini 3.7 Flash",
    "qwen": "Qwen3.8 27B",
    "qwenflash": "Qwen3.8 Flash (Bailian)",
    "oxalpha": "ox-alpha",
    "hy4": "Hy4 Preview",
}
CHINESE_TITLE = {
    "cumcm-2023-a-heliostat-field": "定日镜场布局优化",
    "cumcm-2023-b-multibeam-lines": "多波束测线布设",
    "cumcm-2023-c-vegetable-pricing": "蔬菜类商品定价",
    "cumcm-2024-a-dragon-dance": "板凳龙调头",
    "cumcm-2024-b-production-decision": "生产过程抽检与决策",
    "cumcm-2024-c-crop-planting": "农作物种植策略",
    "cumcm-2025-a-smoke-screen": "烟幕遮蔽导弹",
    "cumcm-2025-b-sic-thickness": "外延层厚度反演",
    "cumcm-2025-c-nipt": "女胎 NIPT 异常判定",
    "mcm-2024-a-lamprey": "七鳃鳗生态影响",
    "mcm-2024-b-submersible-search": "潜水器搜索迁移",
    "mcm-2024-c-tennis-momentum": "网球势头预警",
    "mcm-2023-a-plant-community": "植物群落抗旱韧性",
    "mcm-2023-b-maasai-mara": "马赛马拉保护区",
    "mcm-2023-c-wordle": "Wordle 难度评估",
    "mcm-2025-a-stair-wear": "楼梯磨损反推人流",
    "mcm-2025-b-juneau-tourism": "朱诺旅游可持续政策",
    "mcm-2025-c-olympic-medals": "奥运奖牌与强教练效应",
}
GEOMETRY_IMAGE = {
    "cumcm-2024-a-dragon-dance": "../docs/assets/geometry/cumcm-2024-a-dragon-dance.svg",
    "cumcm-2025-a-smoke-screen": "../docs/assets/geometry/cumcm-2025-a-smoke-screen.svg",
    "cumcm-2025-b-sic-thickness": "../docs/assets/geometry/cumcm-2025-b-sic-thickness.svg",
    "mcm-2024-b-submersible-search": "../docs/assets/geometry/mcm-2024-b-submersible-search.svg",
    "mcm-2025-a-stair-wear": "../docs/assets/geometry/mcm-2025-a-stair-wear.svg",
}
DIRECTION_LABEL = {
    "higher_is_better": "越高越好",
    "lower_is_better": "越低越好",
    "target_value": "越接近越好",
    "exact_value": "必须完全命中",
}
ROBUST_GAP_FLOOR = 0.10
ROBUST_SATURATED_GAIN_CLIP = 0.10
ROBUST_RATIO_CLIP = 1.0
KNOWN_NUMERIC_LIBS = {
    "numpy",
    "pandas",
    "scipy",
    "sklearn",
    "statsmodels",
    "matplotlib",
    "seaborn",
    "openpyxl",
    "xlrd",
    "xlsxwriter",
    "cvxpy",
    "pulp",
    "ortools",
    "networkx",
    "sympy",
    "shapely",
    "lightgbm",
    "xgboost",
    "catboost",
    "torch",
}
LIB_DISPLAY = {
    "sklearn": "scikit-learn",
    "ortools": "OR-Tools",
}
TASK_MODEL_FAMILY = {
    "cumcm-2023-a-heliostat-field": "解析几何/方程 + 物理仿真 + 运筹优化",
    "cumcm-2023-b-multibeam-lines": "解析几何/方程 + 运筹优化",
    "cumcm-2023-c-vegetable-pricing": "数据建模 + 运筹优化",
    "cumcm-2024-a-dragon-dance": "解析几何/方程 + 运动学",
    "cumcm-2024-b-production-decision": "统计推断 + 运筹优化/决策",
    "cumcm-2024-c-crop-planting": "运筹优化 + 不确定性仿真",
    "cumcm-2025-a-smoke-screen": "解析几何/方程 + 运动学 + 运筹优化",
    "cumcm-2025-b-sic-thickness": "解析几何/物理反演 + 数据拟合",
    "cumcm-2025-c-nipt": "数据建模/统计推断 + 综合评价/决策",
    "mcm-2023-a-plant-community": "微分方程/动力系统 + 生态仿真",
    "mcm-2023-b-maasai-mara": "空间规划/图论网络 + 运筹优化 + 动力系统",
    "mcm-2023-c-wordle": "数据建模/时间序列 + 分类/聚类",
    "mcm-2024-a-lamprey": "微分方程/动力系统 + 生态仿真",
    "mcm-2024-b-submersible-search": "随机仿真/贝叶斯搜索 + 综合评价/路径规划",
    "mcm-2024-c-tennis-momentum": "数据建模/时间序列 + 统计检验/分类预警",
    "mcm-2025-a-stair-wear": "解析几何/物理反演 + 数据估计",
    "mcm-2025-b-juneau-tourism": "系统动力学 + 动态规划/多目标优化",
    "mcm-2025-c-olympic-medals": "数据建模/机器学习 + Monte Carlo 仿真",
}
TASK_ROLE_METHOD_CN = {
    "cumcm-2023-a-heliostat-field": {
        "B": "太阳高度角和 DNI 大气辐照模型 + 镜面余弦、遮挡、截断效率的几何光学模型；用坐标附件做数值复现。",
        "O": "几何光学效率代理 + O 奖目标校准 + 固定、优化、可变布局的镜场设计汇总。",
        "Agent": "太阳轨迹采样 + 向量反射/圆柱接收器射线追踪 + 镜场遮挡校正。",
    },
    "cumcm-2023-b-multibeam-lines": {
        "B": "局部平面海底上的多波束扇形覆盖几何；按等深线和重叠率规则做贪心测线布设。",
        "O": "多波束覆盖宽度公式 + 贪心线距 + 模拟退火对比，并按 O 奖测线长度、漏测率和重叠率校准。",
        "Agent": "局部平面射线-海底相交模型 + 不对称半幅覆盖 + 区间重叠计算 + 贪心测线搜索。",
    },
    "cumcm-2023-c-vegetable-pricing": {
        "B": "线性需求回归 + 利润最大化的定价/补货优化。",
        "O": "K-means++ 商品聚类 + 销量/加价率相关分析 + 线性价格-需求回归 + 网格搜索定价。",
        "Agent": "K-means 聚类 + OLS 需求定价回归 + 非线性/混合整数约束利润优化。",
    },
    "cumcm-2024-a-dragon-dance": {
        "B": "阿基米德螺线弧长参数化 + 刚体板凳运动学 + 速度约束反推。",
        "O": "等距螺线弧长反解 + 把手递推 + 非相邻碰撞检测 + 螺距搜索 + 速度比例缩放。",
        "Agent": "非线性弧长反解 + 刚性弦长约束 + 多边形碰撞检测。",
    },
    "cumcm-2024-b-production-decision": {
        "B": "二项分布抽样检验 + 期望利润递推/枚举 + 拆解决策搜索。",
        "O": "二项假设检验 + 期望利润枚举 + 状态-决策遗传搜索 + Beta 后验更新。",
        "Agent": "Clopper-Pearson 单侧二项置信规则 + 检验功效设计 + 期望利润/返修拆解决策优化。",
    },
    "cumcm-2024-c-crop-planting": {
        "B": "模式化种植组合优化 + Monte Carlo 场景仿真，用来评估收益和风险。",
        "O": "附件清洗 + 候选种植组合 + 贪心/风险调整优化 + Monte Carlo 情景 + CVaR 风险度量 + Spearman 相关性。",
        "Agent": "七年混合整数线性规划（MILP）：地块-季次-作物面积连续变量、种植选择二元变量和模式变量，目标是利润最大化。",
    },
    "cumcm-2025-a-smoke-screen": {
        "B": "三维运动学轨迹 + 视线-烟球相交判定 + 紧凑搜索投放参数。",
        "O": "三维运动学 + 圆柱目标视线遮蔽判定 + 随机搜索 + 多弹贪心分配。",
        "Agent": "弹道释放 + 下沉烟球 + 采样圆柱视线并集优化，目标为有效遮蔽时间并集。",
    },
    "cumcm-2025-b-sic-thickness": {
        "B": "双光束干涉测厚 + Airy 多光束修正。",
        "O": "Snell/Fresnel 光学 + Cauchy 色散模型 + FFT 初值 + 非线性最小二乘 + Airy 多光束修正。",
        "Agent": "广义 Airy 多光束反射率模型 + 光谱非线性拟合 + 外延层厚度反演。",
    },
    "cumcm-2025-c-nipt": {
        "B": "男胎 Y 浓度 logit 线性模型 + 女胎 Z 值阈值判别 + BMI 分组时点决策。",
        "O": "胎儿浓度 logit 混合效应近似 + BMI 时点优化 + 女胎异常分类器。",
        "Agent": "REML 随机截距线性混合模型拟合 logit(Y 浓度) + BMI 分组风险时点预测 + 留一验证。",
    },
    "mcm-2023-a-plant-community": {
        "B": "Lotka-Volterra 竞争动力系统 + 物种功能性状/干旱敏感性参数化。",
        "O": "Lotka-Volterra 启发的差分生态仿真 + 干旱脉冲 + 多样性稳定性校准。",
        "Agent": "离散年度群落动力学：物种生物量、干旱记忆和性状参数共同递推。",
    },
    "mcm-2023-b-maasai-mara": {
        "B": "元胞/格点空间分配的多目标规划 + Lotka-Volterra 生态动态 + 多准则决策。",
        "O": "6x6 空间规划评分 + Dijkstra 交互距离 + 经济/生态场景效益校准。",
        "Agent": "100 格点多目标功能分区 + 离散 logistic 野生动物、旅游和经济动态。",
    },
    "mcm-2023-c-wordle": {
        "B": "带星期效应的对数线性时间序列预测 + 词特征 KNN 难度估计。",
        "O": "移动平均差分预测 + 单词词汇特征 + K-means 难度聚类 + 树模型分类。",
        "Agent": "峰后对数幂律衰减预测 + 星期效应 + 滚动校准 + 词特征难度分类。",
    },
    "mcm-2024-a-lamprey": {
        "B": "分阶段确定性常微分方程（ODE）种群模型 + Euler 数值积分。",
        "O": "资源驱动性别比 + 分阶段种群动力学 + Lotka-Volterra/Nicholson-Bailey 生态模型 + 稳定性指标。",
        "Agent": "四仓室食物网常微分方程（ODE）+ 四阶 Runge-Kutta（RK4）数值积分。",
    },
    "mcm-2024-b-submersible-search": {
        "B": "SIR 粒子滤波 + 平流扩散漂移模型 + 多准则装备评价 + 贝叶斯搜索更新。",
        "O": "RK4 动力漂移 + Monte Carlo 粒子群 + 熵权装备评分 + Bayesian 搜索更新 + 类蚁群路径排序。",
        "Agent": "5 万粒子 Monte Carlo 位置后验 + 海流漂移/扩散不确定性 + 搜索区域规划。",
    },
    "mcm-2024-c-tennis-momentum": {
        "B": "发球校正 EWMA 势头指标 + 游程/Ljung-Box 随机性检验 + Markov 链 + 预警分类。",
        "O": "发球校正残差 + 双时间 EWMA 势头指标 + Ljung-Box/游程检验 + Bayesian 转移预警。",
        "Agent": "发球和破发点基准胜率 + EWMA 残差势头 + Ljung-Box/游程检验 + 转折预警。",
    },
    "mcm-2025-a-stair-wear": {
        "B": "磨损体积反演交通量模型。",
        "O": "磨损体积模型（WVM）+ 磨损分布模型（WDM）。",
        "Agent": "WVM/WDM 反演楼梯交通量：由踏面磨损形态推日均和峰值人流。",
    },
    "mcm-2025-b-juneau-tourism": {
        "B": "系统动力学反馈模型 + 有限期动态规划优化。",
        "O": "游客需求、经济收益、环境压力、社会接受度耦合的动态规划。",
        "Agent": "游客需求-冰川健康-居民接受度耦合系统动力学 + 有限期动态规划。",
    },
    "mcm-2025-c-olympic-medals": {
        "B": "历史加权平均 + 主办国效应 + Monte Carlo 奖牌仿真。",
        "O": "运动员能力特征工程 + 随机森林 + Monte Carlo 奖牌分配 + Poisson 项目弹性。",
        "Agent": "按项目训练随机森林二分类器预测金牌/奖牌 + Monte Carlo 2028 奖牌表投影。",
    },
}


def load_eval_module() -> Any:
    path = SCRIPTS_ROOT / "write_direction_aware_flash_baseline_eval_2024_2025.py"
    spec = importlib.util.spec_from_file_location("direction_eval", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_all_model_module() -> Any:
    path = SCRIPTS_ROOT / "write_all_models_boeval_2023_2025.py"
    spec = importlib.util.spec_from_file_location("all_model_boeval_2023_2025", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fmt_number(value: Any, *, digits: int = 6) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, bool):
        return str(value)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return "N/A"
    if abs(number) >= 1_000_000:
        return f"{number:,.2f}".rstrip("0").rstrip(".")
    if abs(number) >= 10_000:
        return f"{number:,.3f}".rstrip("0").rstrip(".")
    if abs(number) >= 100:
        return f"{number:,.4f}".rstrip("0").rstrip(".")
    if abs(number) >= 10:
        return f"{number:.4f}".rstrip("0").rstrip(".")
    if abs(number) >= 1:
        return f"{number:.5f}".rstrip("0").rstrip(".")
    return f"{number:.{digits}g}"


def pct(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value * 100:.2f}%"


def pp(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value * 100:+.2f} pp"


def money(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"¥{value:,.2f}"


def md_cell(value: Any) -> str:
    text = str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def compact_text(value: Any, *, limit: int = 140) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        if value.get("name"):
            value = value["name"]
        else:
            value = ", ".join(f"{key}={val}" for key, val in value.items() if val not in (None, "", [], {}))
    elif isinstance(value, list):
        value = "；".join(str(item) for item in value[:4])
    text = re.sub(r"\s+", " ", str(value)).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def method_from_result(data: dict[str, Any] | None) -> str:
    if not isinstance(data, dict):
        return ""
    preferred: list[Any] = []
    selected = data.get("selected_model")
    if isinstance(selected, dict):
        preferred.append(selected.get("name"))
    elif selected:
        preferred.append(selected)
    for key in ("methods", "model", "model_summary", "reproduction_scope", "approach", "method"):
        if data.get(key):
            preferred.append(data[key])
    seen: set[str] = set()
    parts: list[str] = []
    for item in preferred:
        text = compact_text(item, limit=120)
        if text and text not in seen:
            seen.add(text)
            parts.append(text)
    return "；".join(parts[:2])


def method_family_cn(slug: str, method_text: str = "") -> str:
    if slug in TASK_MODEL_FAMILY:
        return TASK_MODEL_FAMILY[slug]
    text = method_text.lower()
    families: list[str] = []
    keyword_families = [
        (("ode", "differential", "lotka", "dynamics", "rk4", "euler"), "微分方程/动力系统"),
        (("milp", "linear programming", "dynamic programming", "optimization", "profit", "greedy"), "运筹优化"),
        (("regression", "classifier", "random forest", "kmeans", "time-series", "arima", "ewma"), "数据建模"),
        (("geometry", "ray", "kinematic", "trajectory", "interference", "wear"), "解析几何/方程"),
        (("bayesian", "entropy", "multi-criteria", "topsis", "ahp"), "综合评价/决策"),
        (("dijkstra", "network", "path"), "图论网络"),
        (("monte carlo", "particle", "simulation"), "随机仿真"),
    ]
    for keywords, family in keyword_families:
        if any(keyword in text for keyword in keywords) and family not in families:
            families.append(family)
    return " + ".join(families[:3]) if families else "综合建模"


def generic_method_cn(method_text: str, fallback: str) -> str:
    text = re.sub(r"\s+", " ", method_text).strip()
    if not text:
        return fallback
    if re.search(r"[\u4e00-\u9fff]", text):
        return compact_text(text, limit=220)
    lower = text.lower()
    phrases: list[str] = []
    keyword_methods = [
        (("milp", "mixed integer"), "混合整数线性规划（MILP）"),
        (("linear programming", "profit maximization"), "线性规划/利润最大化"),
        (("dynamic programming",), "动态规划"),
        (("greedy",), "贪心搜索"),
        (("simulated annealing",), "模拟退火"),
        (("genetic",), "遗传算法"),
        (("ode", "differential equation"), "常微分方程（ODE）"),
        (("rk4", "runge"), "Runge-Kutta 数值积分"),
        (("lotka",), "Lotka-Volterra 生态动力系统"),
        (("monte carlo",), "Monte Carlo 随机仿真"),
        (("particle",), "粒子滤波/粒子群仿真"),
        (("bayesian", "bayes"), "贝叶斯更新/搜索"),
        (("kmeans", "k-means"), "K-means 聚类"),
        (("random forest",), "随机森林"),
        (("regression", "ols"), "回归建模"),
        (("logit", "logistic"), "logit/Logistic 统计模型"),
        (("ewma",), "指数加权移动平均（EWMA）"),
        (("markov",), "Markov 链"),
        (("geometry", "geodesic", "ray", "line-of-sight", "trajectory"), "解析几何/运动学"),
        (("interference", "airy", "fresnel", "snell"), "光学干涉反演"),
        (("wear",), "磨损反演模型"),
        (("dijkstra",), "Dijkstra 路径/距离模型"),
    ]
    for keywords, phrase in keyword_methods:
        if any(keyword in lower for keyword in keywords) and phrase not in phrases:
            phrases.append(phrase)
    if phrases:
        return " + ".join(phrases[:4])
    return fallback


def role_method_cn(slug: str, role: str, method_text: str = "") -> str:
    if slug in TASK_ROLE_METHOD_CN and role in TASK_ROLE_METHOD_CN[slug]:
        return TASK_ROLE_METHOD_CN[slug][role]
    return generic_method_cn(method_text, "未在 artifact 中明确记录数学模型；需回看轨迹或报告。")


def read_json_maybe(path: Path | str | None) -> dict[str, Any] | None:
    if path is None:
        return None
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def external_lib_names(modules: set[str]) -> list[str]:
    libs = sorted(name for name in modules if name in KNOWN_NUMERIC_LIBS)
    return [LIB_DISPLAY.get(name, name) for name in libs]


def libs_from_python(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return []
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    return external_lib_names(modules)


def trial_dir_from_artifact(path: str | None) -> Path | None:
    if not path:
        return None
    artifact_path = Path(path)
    for parent in artifact_path.parents:
        if parent.name == "artifacts":
            return parent.parent
    return None


def libs_from_agent_artifact(path: str | None) -> list[str]:
    trial_dir = trial_dir_from_artifact(path)
    if trial_dir is None:
        return []
    text_parts: list[str] = []
    for candidate in [
        trial_dir / "agent" / "trajectory.json",
        trial_dir / "agent" / "terminus_2.pane",
        trial_dir / "artifacts" / "root" / "results" / "report.md",
    ]:
        try:
            text_parts.append(candidate.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            pass
    text = "\n".join(text_parts)
    modules: set[str] = set()
    for match in re.finditer(r"(?m)^[>\s]*(?:from|import)\s+([A-Za-z_][\w]*)", text):
        modules.add(match.group(1).split(".")[0])
    for match in re.finditer(r"(?:pip3?|python3?\s+-m\s+pip)\s+install\s+([^\n\r;&|]+)", text):
        for token in re.split(r"\s+", match.group(1)):
            token = token.strip().strip("'\"")
            if not token or token.startswith("-"):
                continue
            package = re.split(r"[<>=!~\[]", token)[0].replace("_", "-").lower()
            normalized = {"scikit-learn": "sklearn", "sklearn": "sklearn", "python-docx": "docx"}.get(package, package)
            modules.add(normalized)
    return external_lib_names(modules)


def libs_cell(libs: list[str]) -> str:
    if libs:
        return "、".join(libs)
    return "未显式记录；可能只用 Python 标准库或未在轨迹中留下安装/import 线索"


def artifact_data_and_libs(record: dict[str, Any], model: str) -> tuple[dict[str, Any] | None, list[str]]:
    details = record["details"].get(model)
    if not isinstance(details, dict):
        return None, []
    artifact_path = details.get("artifact_path")
    return read_json_maybe(artifact_path), libs_from_agent_artifact(artifact_path)


def oracle_data_and_libs(case: Any) -> tuple[dict[str, Any] | None, list[str]]:
    expected_path = REPO_ROOT / "tasks" / case.contest_dir / case.slug / "tests" / "expected_result.json"
    solution_path = REPO_ROOT / "tasks" / case.contest_dir / case.slug / "solution" / "oracle" / case.solution_rel
    return read_json_maybe(expected_path), libs_from_python(solution_path)


def best_agent_summary(record: dict[str, Any], model_summaries: list[Any]) -> Any | None:
    candidates = [summary for summary in model_summaries if summary.model != "flash"]
    if not candidates:
        return None
    return max(candidates, key=lambda summary: record["o"].get(summary.model) if record["o"].get(summary.model) is not None else float("-inf"))


def role_method_table_all(record: dict[str, Any], spec: Any, model_summaries: list[Any]) -> list[str]:
    case = record["case"]
    b_data, b_libs = artifact_data_and_libs(record, "flash")
    o_data, o_libs = oracle_data_and_libs(case)
    agent_summary = best_agent_summary(record, model_summaries)
    agent_data: dict[str, Any] | None = None
    agent_libs: list[str] = []
    if agent_summary is not None:
        agent_data, agent_libs = artifact_data_and_libs(record, agent_summary.model)

    b_method = method_from_result(b_data) or spec.baseline_model_summary
    o_method = method_from_result(o_data) or spec.final_answer_summary
    if agent_summary is None:
        agent_label = "Agent"
        agent_method = "无可读 agent artifact"
        agent_note = "没有找到非 baseline agent 结果"
    else:
        agent_label = f"Agent：{model_display(agent_summary.model, agent_summary.short)}"
        agent_method = method_from_result(agent_data) or "result.json 未显式写出模型；需看轨迹/报告细节"
        agent_note = f"本题 O-Eval {pct(record['o'].get(agent_summary.model))}，这里取非 baseline 中本题最高者"

    b_family = method_family_cn(case.slug, b_method)
    o_family = method_family_cn(case.slug, o_method)
    agent_family = method_family_cn(case.slug, agent_method)
    b_method_cn = role_method_cn(case.slug, "B", b_method)
    o_method_cn = role_method_cn(case.slug, "O", o_method)
    agent_method_cn = role_method_cn(case.slug, "Agent", agent_method)
    rows = [
        "| 角色 | 题型大类 | 中文数学模型 | 主要库/求解器 | 备注 |",
        "|---|---|---|---|---|",
        f"| B：v4 flash baseline | {md_cell(b_family)} | {md_cell(b_method_cn)} | {md_cell(libs_cell(b_libs))} | {md_cell('实际 baseline agent artifact；题目基准描述：' + spec.baseline_model_summary)} |",
        f"| O：O 奖复现 | {md_cell(o_family)} | {md_cell(o_method_cn)} | {md_cell(libs_cell(o_libs))} | {md_cell('来自 O 奖论文 ' + str(case.paper_id) + ' 的可运行复现/expected_result')} |",
        f"| {md_cell(agent_label)} | {md_cell(agent_family)} | {md_cell(agent_method_cn)} | {md_cell(libs_cell(agent_libs))} | {md_cell(agent_note)} |",
    ]
    return rows


def answer_cell(details: dict[str, Any] | None, metric_path: str) -> str:
    if details is None:
        return "无 artifact"
    item = next((m for m in details.get("metrics", []) if m.get("path") == metric_path), None)
    if item is None:
        return "不评分"
    if item.get("excluded"):
        return "本轮排除"
    if not item.get("found"):
        return "缺失"
    if item.get("nonnumeric"):
        return "非数值"
    actual = item.get("actual")
    scoring_actual = item.get("scoring_actual")
    text = fmt_number(actual)
    try:
        if actual is not None and scoring_actual is not None and abs(float(actual) - float(scoring_actual)) > 1e-9:
            text = f"{fmt_number(actual)}→{fmt_number(scoring_actual)}"
    except (TypeError, ValueError):
        pass
    reward = item.get("reward")
    if reward is not None:
        text += f" / 分 {fmt_number(reward, digits=4)}"
    if item.get("invalid_reason"):
        text += f"<br>无效: {md_cell(item['invalid_reason'])}"
    if item.get("review_warning"):
        text += f"<br>需复核: {md_cell(item['review_warning'])}"
    return text


def scored_metric_items(oracle_details: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    for item in oracle_details.get("metrics", []):
        if item.get("excluded"):
            continue
        if float(item.get("score_weight", 0.0)) <= 0:
            continue
        items.append(item)
    return items


def make_records(evalmod: Any) -> tuple[Any, list[dict[str, Any]]]:
    builder = evalmod._load_builder()
    cases = [case for case in builder.CASES if case.year in (2024, 2025)]
    records: list[dict[str, Any]] = []
    for case in cases:
        score_config = evalmod._score_config(case)
        oracle_details = evalmod.score_artifact_direction_aware(evalmod._expected_result(case), score_config)
        raw: dict[str, float | None] = {"oracle": evalmod._raw(oracle_details)}
        details: dict[str, dict[str, Any] | None] = {"oracle": oracle_details}
        for model in evalmod.MODELS:
            model_details = evalmod._score_model_artifact_direction_aware(model, case, case.output_name, score_config)
            details[model] = model_details
            raw[model] = evalmod._raw(model_details) if model_details is not None else 0.0
        b = {
            model: evalmod._b_eval(raw[model], raw["flash"])
            for model in evalmod.MODELS
            if model != "flash"
        }
        bo = {
            model: evalmod._bo_eval(raw[model], raw["flash"], raw["oracle"])
            for model in evalmod.MODELS
            if model != "flash"
        }
        bo_defined = raw["flash"] is not None and raw["oracle"] is not None and raw["oracle"] - raw["flash"] > evalmod.BO_DENOM_EPS
        records.append(
            {
                "case": case,
                "spec": builder.final_question_spec(case),
                "score_config": score_config,
                "details": details,
                "raw": raw,
                "b": b,
                "bo": bo,
                "bo_defined": bo_defined,
            }
        )
    return builder, records


def overall_bo(records: list[dict[str, Any]], model: str) -> float | None:
    values = [r["bo"][model] for r in records if r["bo"].get(model) is not None]
    if not values:
        return None
    return sum(values) / len(values)


def overall_raw(records: list[dict[str, Any]], model: str) -> float:
    values = [r["raw"][model] for r in records if r["raw"].get(model) is not None]
    return sum(values) / len(values)


def artifact_count(records: list[dict[str, Any]], model: str) -> int:
    return sum(1 for r in records if r["details"].get(model) is not None)


def task_heading(record: dict[str, Any]) -> str:
    case = record["case"]
    title = CHINESE_TITLE.get(case.slug, case.title)
    return f"{case.contest.upper()} {case.year} {case.code}: {title}"


def task_bo_sentence(record: dict[str, Any]) -> str:
    raw = record["raw"]
    if not record["bo_defined"]:
        return (
            f"这题不进入 BO-Eval：flash raw={fmt_number(raw['flash'])}，"
            f"O raw={fmt_number(raw['oracle'])}，flash 已经达到或超过 O，分母不为正。"
        )
    denom = raw["oracle"] - raw["flash"]
    return (
        f"这题进入 BO-Eval。分母是 O raw - flash raw = "
        f"{fmt_number(raw['oracle'])} - {fmt_number(raw['flash'])} = {fmt_number(denom)}。"
        f"某模型本题 BO-Eval 就是 max(0, (模型 raw - flash raw) / 这个分母)。"
    )


def task_score_table(record: dict[str, Any]) -> list[str]:
    raw = record["raw"]
    lines = [
        "| 模型 | 本题 raw | B-Eval vs flash | 本题 BO-Eval |",
        "|---|---:|---:|---:|",
        f"| O 奖复现答案 | {fmt_number(raw['oracle'])} | N/A | N/A |",
        f"| v4 flash baseline | {fmt_number(raw['flash'])} | +0.00 pp | 0.00% |",
    ]
    for model in ANSWER_MODEL_ORDER:
        lines.append(
            f"| {SHORT_MODEL_LABEL[model]} | {fmt_number(raw[model])} | {pp(record['b'][model])} | {pct(record['bo'][model])} |"
        )
    return lines


def metric_answer_table(record: dict[str, Any]) -> list[str]:
    details = record["details"]
    rows = [
        "| 评测指标 | 方向 | BO/O 答案 | v4 flash | v4 pro | GLM | Kimi K3 | GPT-5.6 Sol | Gemini |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in scored_metric_items(details["oracle"]):
        path = item["path"]
        direction = DIRECTION_LABEL.get(str(item.get("direction")), str(item.get("direction")))
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{md_cell(path)}`",
                    direction,
                    answer_cell(details["oracle"], path),
                    answer_cell(details["flash"], path),
                    answer_cell(details["pro"], path),
                    answer_cell(details["glm"], path),
                    answer_cell(details["kimi"], path),
                    answer_cell(details["gpt"], path),
                    answer_cell(details["gemini37flash"], path),
                ]
            )
            + " |"
        )
    return rows


def bo_breakdown_table(records: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| 赛题 | v4 pro | GLM-5.3 | Kimi K3 | GPT-5.6 Sol | Gemini 3.7 Flash |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in records:
        case = r["case"]
        label = f"{case.contest.upper()} {case.year} {case.code}"
        if not r["bo_defined"]:
            note = "N/A"
            lines.append(f"| {label} | {note} | {note} | {note} | {note} | {note} |")
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    label,
                    pct(r["bo"]["pro"]),
                    pct(r["bo"]["glm"]),
                    pct(r["bo"]["kimi"]),
                    pct(r["bo"]["gpt"]),
                    pct(r["bo"]["gemini37flash"]),
                ]
            )
            + " |"
        )
    lines.append(
        "| **最终平均** | "
        + " | ".join(
            [
                f"**{pct(overall_bo(records, 'pro'))}**",
                f"**{pct(overall_bo(records, 'glm'))}**",
                f"**{pct(overall_bo(records, 'kimi'))}**",
                f"**{pct(overall_bo(records, 'gpt'))}**",
                f"**{pct(overall_bo(records, 'gemini37flash'))}**",
            ]
        )
        + " |"
    )
    return lines


def model_display(model: str, fallback: str | None = None) -> str:
    return SHORT_MODEL_LABEL.get(model, fallback or model)


def bo_defined_all(record: dict[str, Any]) -> bool:
    flash_raw = record["raw"].get("flash")
    oracle_raw = record.get("oracle_raw")
    return flash_raw is not None and oracle_raw is not None and oracle_raw - flash_raw > 1e-12


def overall_bo_all(records: list[dict[str, Any]], model: str) -> float | None:
    values = [r["bo"][model] for r in records if r["bo"].get(model) is not None]
    return sum(values) / len(values) if values else None


def overall_effect_all(records: list[dict[str, Any]], model: str) -> float | None:
    values = [r["effect"][model] for r in records if r["effect"].get(model) is not None]
    return sum(values) / len(values) if values else None


def overall_o_all(records: list[dict[str, Any]], model: str) -> float | None:
    values = [r["o"][model] for r in records if r["o"].get(model) is not None]
    return sum(values) / len(values) if values else None


def overall_hard_gated_o_all(records: list[dict[str, Any]], model: str) -> float | None:
    values = [r["gated_o"][model] for r in records if r["gated_o"].get(model) is not None]
    return sum(values) / len(values) if values else None


def overall_hard_gated_effect_all(records: list[dict[str, Any]], model: str) -> float | None:
    if model == "flash":
        return 0.0 if records else None
    values = [r["gated_effect"][model] for r in records if r["gated_effect"].get(model) is not None]
    return sum(values) / len(values) if values else None


def task_bo_sentence_all(record: dict[str, Any]) -> str:
    raw = record["raw"]
    oracle_raw = record["oracle_raw"]
    gain_text = "gain = 模型 raw - flash raw"
    gap = oracle_raw - raw["flash"] if oracle_raw is not None and raw.get("flash") is not None else None
    if gap is None or gap <= 1e-12:
        return (
            f"这题鲁棒辅助口径失效：flash raw={fmt_number(raw['flash'])}，"
            f"O raw={fmt_number(oracle_raw)}，flash 已经达到或超过 O，分母不为正。"
            f"Robust 辅助指标改用 clipped B-Eval：把 {gain_text} 截到 ±{ROBUST_SATURATED_GAIN_CLIP * 100:.0f}pp 再进平均。"
        )
    if gap < ROBUST_GAP_FLOOR:
        return (
            f"这题分母太小：O raw - flash raw = {fmt_number(oracle_raw)} - {fmt_number(raw['flash'])} = {fmt_number(gap)}，"
            f"小于 {ROBUST_GAP_FLOOR:.2f}。所以 Robust 辅助指标不用比例放大，改用 clipped B-Eval：把 {gain_text} 截到 ±{ROBUST_SATURATED_GAIN_CLIP * 100:.0f}pp。"
        )
    return (
        f"这题进入 Robust 比例口径。分母是 O raw - flash raw = "
        f"{fmt_number(oracle_raw)} - {fmt_number(raw['flash'])} = {fmt_number(gap)}。"
        f"Robust 辅助指标用 (模型 raw - flash raw) / 这个分母，但最终截到 ±{ROBUST_RATIO_CLIP * 100:.0f}%，所以超大离群值不会继续放大。"
    )


def bo_breakdown_table_all(records: list[dict[str, Any]], model_summaries: list[Any]) -> list[str]:
    labels = [model_display(summary.model, summary.short) for summary in model_summaries]
    lines = [
        "| 赛题 | " + " | ".join(labels) + " |",
        "|---" + "|---:" * len(labels) + "|",
    ]
    for record in records:
        case = record["case"]
        label = f"{case.contest.upper()} {case.year} {case.code}"
        if not bo_defined_all(record):
            lines.append("| " + " | ".join([label, *["N/A" for _ in model_summaries]]) + " |")
            continue
        values = [pct(record["bo"].get(summary.model)) for summary in model_summaries]
        lines.append("| " + " | ".join([label, *values]) + " |")
    final_values = [f"**{pct(overall_bo_all(records, summary.model))}**" for summary in model_summaries]
    lines.append("| " + " | ".join(["**最终平均**", *final_values]) + " |")
    return lines


def effect_breakdown_table_all(records: list[dict[str, Any]], model_summaries: list[Any]) -> list[str]:
    labels = [model_display(summary.model, summary.short) for summary in model_summaries]
    lines = [
        "| 赛题 | " + " | ".join(labels) + " |",
        "|---" + "|---:" * len(labels) + "|",
    ]
    for record in records:
        case = record["case"]
        label = f"{case.contest.upper()} {case.year} {case.code}"
        values = [pct(record["effect"].get(summary.model)) for summary in model_summaries]
        lines.append("| " + " | ".join([label, *values]) + " |")
    final_values = [f"**{pct(overall_effect_all(records, summary.model))}**" for summary in model_summaries]
    lines.append("| " + " | ".join(["**最终平均**", *final_values]) + " |")
    return lines


def o_breakdown_table_all(records: list[dict[str, Any]], model_summaries: list[Any]) -> list[str]:
    labels = [model_display(summary.model, summary.short) for summary in model_summaries]
    lines = [
        "| 赛题 | " + " | ".join(labels) + " |",
        "|---" + "|---:" * len(labels) + "|",
    ]
    for record in records:
        case = record["case"]
        label = f"{case.contest.upper()} {case.year} {case.code}"
        values = [pct(record["o"].get(summary.model)) for summary in model_summaries]
        lines.append("| " + " | ".join([label, *values]) + " |")
    final_values = [f"**{pct(overall_o_all(records, summary.model))}**" for summary in model_summaries]
    lines.append("| " + " | ".join(["**最终平均**", *final_values]) + " |")
    return lines


def hard_gated_leaderboard_table(model_summaries: list[Any]) -> list[str]:
    rows = sorted(
        model_summaries,
        key=lambda summary: summary.hard_gated_o_mean if summary.hard_gated_o_mean is not None else float("-inf"),
        reverse=True,
    )
    lines = [
        "| 模型 | Hard-gated O-Eval | Hard-gated Robust | 原始 O-Eval | gate 数 | 成本 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for summary in rows:
        lines.append(
            f"| {model_display(summary.model, summary.short)} | {pct(summary.hard_gated_o_mean)} | "
            f"{pct(summary.hard_gated_effect_mean)} | {pct(summary.o_mean)} | {summary.hard_gate_count} | {money(summary.cost_rmb)} |"
        )
    return lines


def hard_gate_decision_table(records: list[dict[str, Any]], model_summaries: list[Any]) -> list[str]:
    order = ["flash", *[summary.model for summary in model_summaries]]
    lines = [
        "| 模型 | 赛题 | 原 O-Eval | gated O-Eval | 原 Robust | gated Robust | 原因 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for record in records:
        for model in order:
            reason = record["hard_gate"].get(model)
            if not reason:
                continue
            lines.append(
                f"| {model_display(model)} | `{record['case'].slug}` | {pct(record['o'].get(model))} | "
                f"{pct(record['gated_o'].get(model))} | {pct(record['effect'].get(model))} | "
                f"{pct(record['gated_effect'].get(model))} | {md_cell(reason)} |"
            )
    if len(lines) == 2:
        lines.append("| 无 | 无 | N/A | N/A | N/A | N/A | 无 hard gate |")
    return lines


def task_score_table_all(record: dict[str, Any], model_summaries: list[Any]) -> list[str]:
    raw = record["raw"]
    lines = [
        "| 模型 | 本题 raw | O-Eval 主分 | B-Eval vs flash | Robust BO-Eval 辅助 |",
        "|---|---:|---:|---:|---:|",
        f"| O 奖复现答案 | {fmt_number(record['oracle_raw'])} | 100.00% | N/A | N/A |",
        f"| v4 flash baseline | {fmt_number(raw['flash'])} | {pct(record['o'].get('flash'))} | +0.00 pp | 0.00% |",
    ]
    for summary in model_summaries:
        model = summary.model
        lines.append(
            f"| {model_display(model, summary.short)} | {fmt_number(raw.get(model))} | {pct(record['o'].get(model))} | "
            f"{pp(record['b'].get(model))} | {pct(record['effect'].get(model))} |"
        )
    return lines


def metric_answer_table_all(record: dict[str, Any], model_summaries: list[Any]) -> list[str]:
    details = record["details"]
    oracle_details = details.get("oracle")
    if oracle_details is None:
        return ["没有找到 O 奖复现答案的逐指标明细。"]
    header = ["评测指标", "方向", "BO/O 答案", "v4 flash"]
    header.extend(model_display(summary.model, summary.short) for summary in model_summaries)
    rows = [
        "| " + " | ".join(header) + " |",
        "|---|---|---:" + "|---:" * (len(header) - 3) + "|",
    ]
    for item in scored_metric_items(oracle_details):
        path = item["path"]
        direction = DIRECTION_LABEL.get(str(item.get("direction")), str(item.get("direction")))
        values = [
            f"`{md_cell(path)}`",
            direction,
            answer_cell(oracle_details, path),
            answer_cell(details.get("flash"), path),
        ]
        values.extend(answer_cell(details.get(summary.model), path) for summary in model_summaries)
        rows.append("| " + " | ".join(values) + " |")
    return rows


def split_tables_all(allmod: Any, records: list[dict[str, Any]], model_summaries: list[Any]) -> list[str]:
    lines = [
        "## 分年份和赛制看",
        "",
        "同一个 O-Eval 总分拆开看，会发现 2023、2024、2025 的难点不一样；CUMCM 和 MCM 也不是同一种口味。",
        "",
        "| 模型 | 2023 | 2024 | 2025 |",
        "|---|---:|---:|---:|",
    ]
    for summary in model_summaries:
        lines.append(
            f"| {model_display(summary.model, summary.short)} | "
            f"{pct(allmod.split_o_mean(records, summary.model, year=2023))} | "
            f"{pct(allmod.split_o_mean(records, summary.model, year=2024))} | "
            f"{pct(allmod.split_o_mean(records, summary.model, year=2025))} |"
        )
    lines.extend(
        [
            "",
            "| 模型 | CUMCM | MCM | CUMCM artifacts | MCM artifacts |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for summary in model_summaries:
        lines.append(
            f"| {model_display(summary.model, summary.short)} | "
            f"{pct(allmod.split_o_mean(records, summary.model, suite='cumcm'))} | "
            f"{pct(allmod.split_o_mean(records, summary.model, suite='mcm'))} | "
            f"{allmod.artifact_count(records, summary.model, suite='cumcm')} | "
            f"{allmod.artifact_count(records, summary.model, suite='mcm')} |"
        )
    return lines


def write_article_2023_2025() -> Path:
    allmod = load_all_model_module()
    base, _, records, summaries = allmod.compute()
    builder = base._load_builder()
    o_ranked_non_baseline = sorted(
        [summary for summary in summaries if summary.model != "flash"],
        key=lambda summary: summary.o_mean if summary.o_mean is not None else float("-inf"),
        reverse=True,
    )
    robust_ranked_non_baseline = sorted(
        [summary for summary in summaries if summary.model != "flash"],
        key=lambda summary: summary.effect_mean if summary.effect_mean is not None else float("-inf"),
        reverse=True,
    )
    hard_gated_ranked_non_baseline = sorted(
        [summary for summary in summaries if summary.model != "flash"],
        key=lambda summary: summary.hard_gated_o_mean if summary.hard_gated_o_mean is not None else float("-inf"),
        reverse=True,
    )
    non_baseline = o_ranked_non_baseline
    flash = next(summary for summary in summaries if summary.model == "flash")
    bo_defined_count = sum(1 for record in records if bo_defined_all(record))
    robust_ratio_count = sum(
        1
        for record in records
        if record["raw"].get("flash") is not None
        and record.get("oracle_raw") is not None
        and record["oracle_raw"] - record["raw"]["flash"] >= ROBUST_GAP_FLOOR
    )
    saturated_count = len(records) - robust_ratio_count
    top_o = o_ranked_non_baseline[0]
    top_robust = robust_ranked_non_baseline[0]
    top_hard_gated = hard_gated_ranked_non_baseline[0]
    qwen = next((summary for summary in summaries if summary.model == "qwen"), None)
    qwenflash = next((summary for summary in summaries if summary.model == "qwenflash"), None)
    kimi = next((summary for summary in summaries if summary.model == "kimi"), None)
    gemini = next((summary for summary in summaries if summary.model == "gemini37flash"), None)
    oxalpha = next((summary for summary in summaries if summary.model == "oxalpha"), None)
    hy4 = next((summary for summary in summaries if summary.model == "hy4"), None)
    example_records = [record for record in records if record["effect"].get(top_robust.model) is not None]
    example = max(example_records, key=lambda record: record["effect"].get(top_robust.model) or 0.0)
    example_case = example["case"]
    example_denom = example["oracle_raw"] - example["raw"]["flash"]

    lines: list[str] = [
        "# 用大白话看 terminal-bench-math-modeling 的 18 题 O-Eval / Robust BO-Eval",
        "",
        f"生成日期：{date.today().isoformat()}",
        "",
        "这篇文章解释 2023、2024、2025 三年共 18 道 terminal-bench-math-modeling 题。它不重新跑模型，只读取已经保存的 artifact，再用同一套 direction-aware scoring 重新算 O-Eval 主指标、Robust BO-Eval 辅助指标、token 和粗略成本。",
        "",
        "## 先说结论",
        "",
        "这个 benchmark 看的不是模型会不会写一篇像样的建模论文，而是：给它完整赛题和附件后，它最后交出来的关键数字，能不能追上优秀论文复现答案。",
        "",
        "最终主指标现在是 O-Eval：`clamp(模型 direction-aware raw / O raw, 0, 1)`，再对 18 题取平均。大白话说，100% 就是平均达到 O 奖复现答案的 raw 水平；超过 O 奖锚点的部分不再继续加分。",
        "",
        "这也是为什么 O-Eval 和 Robust BO-Eval 会出现排序不一致：O-Eval 看的是离 O 有多近，Robust 看的是比 flash 多追回了多少。一个是绝对分，一个是相对进步分，所以它们是互补的，不是二选一。",
        "",
        f"18 题总排名按 O-Eval 算是：{' > '.join(f'{model_display(summary.model, summary.short)} ({pct(summary.o_mean)})' for summary in o_ranked_non_baseline)}。",
        "",
        f"另外新增一个温和版 hard-gated leaderboard：只把“明显不是可行解”的模型-题目格子整题清零，不把所有 needs-review/proxy 题一刀切。按这个谨慎口径，Hard-gated O-Eval 排名是：{' > '.join(f'{model_display(summary.model, summary.short)} ({pct(summary.hard_gated_o_mean)})' for summary in hard_gated_ranked_non_baseline)}。",
        "",
        f"Robust BO-Eval 仍然保留做辅助解释：正常题用 `(模型 raw - flash raw) / (O raw - flash raw)`，而且赢很多和输很多都一起截到 ±{ROBUST_RATIO_CLIP * 100:.0f}%；分母小于 {ROBUST_GAP_FLOOR:.2f} 的已完成题，改用 clipped B-Eval，也就是把 `模型 raw - flash raw` 截到 ±{ROBUST_SATURATED_GAIN_CLIP * 100:.0f}pp。若 trial 没有产出可评分结果，就直接记 -100%。它回答的是“相对便宜 flash baseline 多追回多少”，并且不会让 841% 这种小分母离群值主导结论。",
        "",
        "如果两个排名冲突，正式主榜以 O-Eval 为准，Robust 只做辅榜和解释。GLM-5.3-Flash 和 DeepSeek flash 的差别也属于这一类：一个可能在相对追赶上更猛，另一个可能在绝对接近 O 上更好。",
        "",
        f"按 Robust 辅助口径排序是：{' > '.join(f'{model_display(summary.model, summary.short)} ({pct(summary.effect_mean)})' for summary in robust_ranked_non_baseline)}。",
        "",
        "| 模型 | artifacts | 平均 raw | O-Eval 主分 | Hard-gated O-Eval | Robust BO-Eval 辅助 | Hard-gated Robust | tokens input/cache/output | 估算成本 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in [flash, *non_baseline]:
        lines.append(
            f"| {model_display(summary.model, summary.short)} | {summary.artifacts}/18 | "
            f"{fmt_number(summary.raw_mean)} | {pct(summary.o_mean)} | {pct(summary.hard_gated_o_mean)} | "
            f"{pct(summary.effect_mean)} | {pct(summary.hard_gated_effect_mean)} | "
            f"{summary.input_tokens:,} / {summary.cache_tokens:,} / {summary.output_tokens:,} | {money(summary.cost_rmb)} |"
        )

    lines.extend(
        [
            "",
            "## 温和版 hard-gated 怎么算",
            "",
            "hard-gated 不是把所有可疑题都删掉。它只惩罚三类很硬的失败：第一，score_config 已经标出 `invalid_reason` 的硬无效字段；第二，独立重放后确定几何/物理结果为零的高分；第三，明显量纲越界或结构缺失但被开放式“越高越好”指标错误奖励的高分。",
            "",
            "被 hard gate 的格子，O-Eval 按 raw 0 进入 18 题平均；Robust BO-Eval 按 -100% 进入 18 题平均。只是 needs-review、proxy-score、还缺更强 replay verifier 的格子，先保留原分，但报告里会标注不能拿来 claim “强于 O”。",
            "",
            *hard_gated_leaderboard_table([flash, *non_baseline]),
            "",
            "这版最大的变化是：Kimi K3 的朱诺旅游和奥运教练效应高分被扣掉，ox-alpha 的烟幕高分被扣掉；七鳃鳗里凡是把原始种群量写成 0-1 归一化指数的格子，也按整题不可行处理。",
            "",
            *hard_gate_decision_table(records, non_baseline),
            "",
            "## 图怎么读",
            "",
            f"第一组图看温和版 hard-gated O-Eval：它回答“把明显不可行解扣掉以后，谁还稳”。{model_display(top_hard_gated.model, top_hard_gated.short)} 在这张榜上排第一；Hy4 Preview 因新增的生产抽检阈值/旅游可持续性越界 gate 回落，Kimi K3 因朱诺旅游和奥运教练效应两个高杠杆坏题明显下滑；ox-alpha 因烟幕几何重放为零，也从原 O-Eval 里掉下来。",
            "",
            "![Hard-gated O-Eval 主效果柱状图](figures/aa-style-2023-2025-hard-gated-o-eval-bar.png)",
            "",
            "![Hard-gated O-Eval vs Cost](figures/aa-style-2023-2025-hard-gated-o-eval-cost-scatter.png)",
            "",
            "第二组图看原始 O-Eval 主效果；它仍然有意义，因为它展示 verifier 当前定义下的可评分数值表现，但需要和 hard-gated 榜一起读。",
            "",
            "![O-Eval 主效果柱状图](figures/aa-style-2023-2025-o-eval-bar.png)",
            "",
            "![O-Eval vs Cost](figures/aa-style-2023-2025-o-eval-cost-scatter.png)",
            "",
            "Robust 图保留下来，用来看“相对 v4 flash baseline 的增益”是不是稳定；token 和成本图用来解释为什么同样分数会有不同价格。没有可评分 artifact 的 trial 现在按 -100% 记分，不会再被当成普通小分母题。",
            "",
            "![Robust 辅助效果柱状图](figures/aa-style-2023-2025-boeval-effect-bar.png)",
            "",
            "![Robust vs Cost](figures/aa-style-2023-2025-boeval-score-cost.png)",
            "",
            "token 和成本图用来解释为什么同样 O-Eval 分数会有不同价格。",
            "",
            "![Token usage](figures/aa-style-2023-2025-token-usage.png)",
            "",
            "![Cost](figures/aa-style-2023-2025-cost.png)",
            "",
            f"成本统一优先按 OpenRouter 当前 catalog 里的 `prompt`、`input_cache_read`、`input_cache_write`、`completion` 价格算，再用 USD/CNY={allmod.OPENROUTER_USD_TO_RMB} 转成人民币/百万 tokens。价格快照写在 `openrouter-pricing-used-2023-2025.json`；当前 `result.json` 只有 input/cache/output 三类 token，没有单独的 cache write/create 字段，所以显式缓存创建费用不额外拆账。",
            "",
        ]
    )
    if qwen is not None:
        if getattr(qwen, "cache_imputed_from_peer_avg", False) and qwen.cache_hit_rate is not None:
            lines.extend(
                [
                    f"为了横向可比，Qwen3.8 27B 的 cache 命中率不用日志里的 0，而是用其他非 Qwen 模型的等权平均命中率 {qwen.cache_hit_rate * 100:.2f}%。这相当于把 Qwen 的 input tokens 里 {qwen.cache_tokens:,} 记为 cached-read，原始 Qwen `result.json` 记录的 cache tokens 是 {qwen.raw_cache_tokens:,}。",
                    "",
                ]
            )
        lines.append(
            f"按这个口径，Qwen3.8 27B 是 {pct(qwen.o_mean)} O-Eval、{pct(qwen.effect_mean)} Robust 辅助、{money(qwen.cost_rmb)} 估算成本；它不会再被 841% 这类小分母离群值抬高。"
        )
        lines.append("")
    if kimi is not None:
        lines.append(
            f"Kimi K3 是 {pct(kimi.o_mean)} O-Eval、{pct(kimi.effect_mean)} Robust 辅助、{money(kimi.cost_rmb)} 估算成本。Kimi 2023 的汇总 `result.json` 已经回到 3 completed / 0 error 的状态，所以这里不会再因为旧 error 计数低估 artifacts。"
        )
        lines.append("")
    if oxalpha is not None:
        lines.append(
            f"GLM-5.3-Flash (ox-alpha) 已完成 17/18 个有效任务；`cumcm-2023-a-heliostat-field` 因正常模型推理超时记为最终失败，不再重试。目录级 artifact 记录为 {oxalpha.artifacts}/18，O-Eval 按可评分的有效结果计算。"
        )
        lines.append("")
    if qwenflash is not None:
        lines.append(
            f"Qwen3.8 Flash (Bailian) 有 {qwenflash.valid_tasks}/18 个有效完成、{qwenflash.error_tasks} 个正常模型推理超时的最终 error；目录级 artifact 记录为 {qwenflash.artifacts}/18，错误题不进入有效结果。"
        )
        lines.append("")

    if hy4 is not None:
        hy4_cost_text = (
            f"按 OpenRouter `tencent/hy4-preview` 价格估算成本为 {money(hy4.cost_rmb)}。"
            if hy4.cost_rmb is not None
            else "当前没有纳入统一价格表，所以效果图和 token 图会展示 Hy4，分数-cost 图里先不把它放到横轴上。"
        )
        lines.append(
            f"Hy4 Preview 已完成 {hy4.valid_tasks}/18 个有效任务，O-Eval 是 {pct(hy4.o_mean)}、Robust 辅助是 {pct(hy4.effect_mean)}。{hy4_cost_text}"
        )
        lines.append("")

    lines.extend(
            [
                "## B、O、Agent 各自是什么",
                "",
                "为了别把三个角色混在一起，后面的逐题表会把它们拆开：",
                "",
                "- **B**：v4 flash baseline 的实际提交答案。它是 Robust 里的便宜参考点，不一定是人工写死的 baseline。表里的模型和库优先从它自己的 `result.json` 和 agent 轨迹里抽取。",
                "- **O**：O 奖论文复现答案，也就是 scoring 的 oracle 锚点。表里的模型来自 `expected_result.json`，库来自对应 oracle `solution.py` 的 imports。",
                "- **Agent**：该题当前主表里 O-Eval 最高的非 baseline agent。也就是说，它不是固定某一个模型，而是每道题选“这题做得最接近 O 的那个 agent”来说明模型路线和求解库。",
                "",
                "逐题表里的“题型大类”沿用 `intro-mathmodel/数学建模题型-解法速查.md` 的决策树口径，比如解析几何/方程、微分方程/动力系统、运筹优化、数据建模、综合评价/决策、图论网络。复杂题会写成组合类，因为真实赛题常常是“先数据建模，再优化决策”。",
                "",
                "这些方法/库不是重新评判答案，只是给读者解释：同一个分数背后，大家到底把赛题抽象成了什么数学问题，又大概靠什么 Python 数值栈求出来。NumPy、Pandas、SciPy 这类是实现工具，不是数学模型；抽不到明确库时，我会写“未显式记录”，不强行脑补。",
                "",
                "## O-Eval 到底怎么算",
                "",
                "先把每道题最后答案里的关键数字拆出来，比如定日镜场的年平均输出功率、网球势头题的预测准确率、烟幕题的遮蔽时长。每个数字根据方向算 reward：该高的越高越好，该低的越低越好，该贴目标值的就越接近越好。",
                "",
                "多个指标平均起来，就是这道题的 direction-aware raw。然后 O-Eval 用 O 奖复现答案做分母：",
                "",
                "```text",
                "本题 O-Eval = clamp(模型 raw / O raw, 0, 1)",
                "```",
                "",
                "最后对 18 道题取平均。它最像“绝对成绩单”：不关心 flash baseline 有多强或多弱，只问模型答案离 O 奖复现锚点有多近。缺失 artifact 仍按 raw 0 计入，所以覆盖不完整会直接掉分。",
                "",
                "下面这张表是 18 道题的 O-Eval 展开。",
                "",
                *o_breakdown_table_all(records, non_baseline),
                "",
                "## Robust BO-Eval 怎么辅助解释",
                "",
                "有了每题的 direction-aware raw 以后，Robust BO-Eval 额外放进一个便宜 baseline：v4 flash。",
                "",
                "它的公式还是先看相对 flash 的比例；如果 flash 已经很接近 O，或者分母不够大，就改用 clipped B-Eval，避免小分母把结果放大到离谱。",
                "",
                f"所以 Robust BO-Eval 辅助指标这样算：如果 `O raw - flash raw >= {ROBUST_GAP_FLOOR:.2f}`，用比例但截到 ±{ROBUST_RATIO_CLIP * 100:.0f}%；如果分母太小，完成了的题就用 clipped B-Eval 但截到 ±{ROBUST_SATURATED_GAIN_CLIP * 100:.0f}pp；如果 trial 压根没跑出可评分结果，直接记 -100%。直白说，正常题看追回比例，没做出来的题按最坏值算，而且赢很多和输很多都不会冲破上限。",
                "",
                f"18 道题里有 {bo_defined_count} 道题满足 `O raw > flash raw`，完成但分母太小或失效的 {saturated_count} 类题会用 clipped B-Eval 进入最终平均；如果某个 trial 没有产出可评分结果，它会直接记 -100% 而不是躲进平均里。",
                "",
                f"举个真实例子：{example_case.contest.upper()} {example_case.year} {example_case.code} `{example_case.slug}` 里，flash raw={fmt_number(example['raw']['flash'])}，O raw={fmt_number(example['oracle_raw'])}，分母是 {fmt_number(example_denom)}。{model_display(top_robust.model, top_robust.short)} raw={fmt_number(example['raw'][top_robust.model])}，但进入 Robust 辅助分的是 {pct(example['effect'][top_robust.model])}。",
                "",
                "下面这张表是 18 道题的 Robust 辅助指标展开。这里没有 `N/A` 逃逸口：完成但分母太小的题会用 clipped B-Eval 进入平均，最终失败或缺失的 trial 则直接记 -100%。",
                "",
                *effect_breakdown_table_all(records, non_baseline),
                "",
                *split_tables_all(allmod, records, non_baseline),
                "",
                "## 18 道题逐题看",
                "",
            ]
        )

    for record in records:
        case = record["case"]
        spec = builder.final_question_spec(case)
        lines.extend(
            [
                f"### {task_heading(record)}",
                "",
                f"任务 slug：`{case.slug}`",
                "",
                f"**这题在问什么：**{spec.plain_question}",
                "",
                f"**BO/O 答案是什么：**{spec.final_answer_summary}",
                "",
                f"**baseline 解法大概是什么：**{spec.baseline_model_summary}",
                "",
                "**B / O / Agent 用的题型大类、数学模型和库：**",
                "",
                *role_method_table_all(record, spec, non_baseline),
                "",
                f"**这题怎么换成 O-Eval / Robust：**O-Eval 直接用 `clamp(模型 raw / O raw, 0, 1)`；{task_bo_sentence_all(record)}",
                "",
                "**本题 raw、O-Eval、B-Eval vs flash 和 Robust 辅助指标：**",
                "",
                *task_score_table_all(record, non_baseline),
                "",
                "**评测问题和模型答案：**下面表里的“/ 分”是单指标 reward，不是整题分。`a→b` 表示评测器做了单位换算或百分比归一化后用 `b` 计分。",
                "",
                *metric_answer_table_all(record, non_baseline),
                "",
                "**一句话带走：**这题真正看的不是模型有没有写出漂亮过程，而是最后几个关键数值能不能落在正确方向上。",
                "",
            ]
        )

    lines.extend(
        [
            "## 为什么排名会长这样",
            "",
            f"O-Eval 第一的是 {model_display(top_o.model, top_o.short)}，主分是 {pct(top_o.o_mean)}。这说明它在 18 题平均 raw 上最接近 O 奖复现锚点，不是靠某一道小分母题爆表冲上去。",
            "",
            f"Robust 辅助第一的是 {model_display(top_robust.model, top_robust.short)}，辅助分是 {pct(top_robust.effect_mean)}。这个口径说明它在 flash 弱项上追回 gap 的能力强，但它不再是唯一主表，因为它仍然依赖 flash 和 O 之间那段尺子的形状。",
            "",
            f"温和版 hard-gated 第一的是 {model_display(top_hard_gated.model, top_hard_gated.short)}，主分是 {pct(top_hard_gated.hard_gated_o_mean)}。这张榜不是新的数学分数，而是给公开解读加了一道保守阀门：明显不可行的高分不再继续抬平均数。",
            "",
            "GLM-5.3 和 v4 pro 的位置很接近，说明它们在 flash 弱项上整体有稳定增益；GPT-5.6 Sol high、Kimi K3、Qwen3.8 27B 都有强题，但 O-Eval 会把强题、弱题、缺失题放到同一张绝对成绩单里平均。",
            "",
        ]
    )
    if gemini is not None and gemini.artifacts < 18:
        lines.extend(
            [
                f"Gemini 3.7 Flash 只有 {gemini.artifacts}/18 个 artifact，所以缺失题按 raw 0 进入统计；这会直接压低它的 O-Eval 主分。",
                "",
            ]
        )
    lines.extend(
        [
            "所以这套结果要分三眼看：O-Eval 是最终主排名，Robust BO-Eval 是相对 flash 的辅助口径，score-cost 图再加一眼：同样的分，到底花了多少钱。",
            "",
        ]
    )

    ARTICLE_PATH_2023_2025.write_text("\n".join(lines), encoding="utf-8")
    return ARTICLE_PATH_2023_2025


def write_article() -> Path:
    evalmod = load_eval_module()
    _, records = make_records(evalmod)
    bo_defined_count = sum(1 for r in records if r["bo_defined"])
    saturated_count = len(records) - bo_defined_count

    lines: list[str] = [
        "# 用大白话看 terminal-bench-math-modeling 的 BO-Eval",
        "",
        f"生成日期：{date.today().isoformat()}",
        "",
        "这篇文章只解释 2024-2025 的 12 道 terminal-bench-math-modeling 题。它不是重新跑模型，而是读已经保存下来的模型答案 artifact，再用同一套 direction-aware scoring 重新算分。",
        "",
        "## 先说结论",
        "",
        "这个 benchmark 想测的不是“模型会不会背数学公式”，而是：给模型一整道数学建模赛题、附件和输出格式，它能不能把最后一问做成一组可检验的数字。评测器不会读完整论文文采，它抓最后答案里的关键数字，看这些数字离 O 奖复现答案有多近，或者在正确方向上有没有比 O 答案还好。",
        "",
        "这里的 BO/O 答案，可以理解成“优秀论文复现出来的锚点答案”。v4 flash 是便宜 baseline。BO-Eval 做的事就是问：某个模型从 v4 flash 往 O 答案方向追，追上了多少？追过头也会继续计分，所以会出现超过 100% 的 BO-Eval。",
        "",
        "| 模型 | artifacts | 平均 raw | 最终 BO-Eval |",
        "|---|---:|---:|---:|",
    ]
    for model in ANSWER_MODEL_ORDER:
        lines.append(
            f"| {SHORT_MODEL_LABEL[model]} | {artifact_count(records, model)}/12 | {fmt_number(overall_raw(records, model))} | {pct(overall_bo(records, model))} |"
        )
    lines.extend(
        [
            "",
            "BO-Eval 的 raw/effect 大图不再单独展示，避免和 O-Eval 主指标混在一起；这里保留 token 和成本图，方便对照“做得好”和“花了多少”。",
            "",
            "![Token usage](figures/aa-style-token-usage.png)",
            "",
            "![Cost](figures/aa-style-cost.png)",
            "",
            "## BO-Eval 到底怎么算",
            "",
            "先把每道题的最后答案拆成几个数字指标。比如烟幕题会拆成 M1、M2、M3、总遮蔽时长；楼梯题会拆成日均人数、短时峰值、分散到 10 小时的人数节奏。",
            "",
            "每个指标先算一个 reward。越高越好的指标，达到 O 答案是 1 分，比 O 更高可以超过 1；越低越好的指标，达到 O 答案是 1 分，比 O 更低也可以超过 1；目标值指标则是越接近 O 越好。多个指标平均起来，就是这道题的 direction-aware raw。",
            "",
            "然后 BO-Eval 用 v4 flash 和 O 答案拉一把尺子：",
            "",
            "```text",
            "本题 BO-Eval = max(0, (模型 raw - v4 flash raw) / (O raw - v4 flash raw))",
            "```",
            "",
            f"12 道题里有 {bo_defined_count} 道题的 `O raw > flash raw`，这些题进入 BO-Eval。另有 {saturated_count} 道题 flash 已经达到或超过 O，分母不为正，所以只保留 raw/B-Eval，不进入 BO-Eval。",
            "",
            "举个小例子：CUMCM 2025 A 烟幕题里，flash raw=0.727946，O raw=1.000000，分母是 0.272054。GPT-5.6 Sol raw=3.416382，所以本题 BO-Eval = (3.416382 - 0.727946) / 0.272054 = 988.20%。这不是写错了，而是它在这个方向-aware 计分下远远超过了 O 锚点。",
            "",
            "最终 BO-Eval 就是把这些进入 BO-Eval 的题目百分比取平均。下面这张表就是最终值的展开。",
            "",
            *bo_breakdown_table(records),
            "",
            "注意：Gemini 这轮只有 10/12 个 artifact。它缺的 `mcm-2024-c-tennis-momentum` 在 BO-defined 集合里，所以该题贡献 0；缺的 `mcm-2025-c-olympic-medals` 是 saturated 题，不进入 BO-Eval。",
            "",
            "## 12 道题逐题看",
            "",
        ]
    )

    for r in records:
        case = r["case"]
        spec = r["spec"]
        title = task_heading(r)
        lines.extend(
            [
                f"### {title}",
                "",
                f"任务 slug：`{case.slug}`",
                "",
            ]
        )
        if case.slug in GEOMETRY_IMAGE:
            lines.extend([f"![{title}]({GEOMETRY_IMAGE[case.slug]})", ""])
        lines.extend(
            [
                f"**这题在问什么：**{spec.plain_question}",
                "",
                f"**BO/O 答案是什么：**{spec.final_answer_summary}",
                "",
                f"**baseline 解法大概是什么：**{spec.baseline_model_summary}",
                "",
                f"**这题怎么换成 BO-Eval：**{task_bo_sentence(r)}",
                "",
                "**本题 raw 和 BO-Eval：**",
                "",
                *task_score_table(r),
                "",
                "**评测问题和模型答案：**下面表里的“/ 分”是这个单指标的 reward，不是整题分。`a→b` 表示评测器做了单位换算或百分比归一化后用 `b` 计分。",
                "",
                *metric_answer_table(r),
                "",
                "**一句话带走：**这题真正看的不是模型有没有写出漂亮建模过程，而是最后几个关键数值能不能落在正确方向上。",
                "",
            ]
        )

    lines.extend(
        [
            "## 为什么最终排名会长这样",
            "",
            "GPT-5.6 Sol 的 BO-Eval 最高，主要是 CUMCM 2025 A 烟幕题给了一个极高的正贡献；BO-Eval 不封顶，所以这一题能把平均值明显拉上去。",
            "",
            "Kimi K3 的 12 题 raw 均值最高，说明它在全体题目上很强，尤其在 saturated 题上也拿了很高分。但 BO-Eval 只看 flash 还没追上 O 的 9 道题，所以它的 BO-Eval 略低于 GPT-5.6 Sol。",
            "",
            "v4 pro 中规中矩，很多题比 flash 有进步，但没有特别大的超额项。GLM-5.3 在 MCM 2024 B 潜水器搜索上很好，但整体被若干题拉低。Gemini 3.7 Flash 在烟幕和朱诺旅游上有亮点，可是两个 MCM C artifact 缺失，其中网球势头题直接给 BO-Eval 带来 0 贡献。",
            "",
            "所以这套表要分两眼看：raw 像“总成绩”，BO-Eval 像“在 flash 弱项上追回 O 答案的比例”。两者都重要，只是回答的问题不同。",
            "",
        ]
    )
    ARTICLE_PATH.write_text("\n".join(lines), encoding="utf-8")
    return ARTICLE_PATH


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", choices=["2024-2025", "2023-2025"], default="2024-2025")
    args = parser.parse_args()
    path = write_article_2023_2025() if args.scope == "2023-2025" else write_article()
    print(path)


if __name__ == "__main__":
    main()
