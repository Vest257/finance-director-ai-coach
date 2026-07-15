"""Integrated three-statement and liquidity contract for Scenario 002."""

from __future__ import annotations

from dataclasses import dataclass, field
from textwrap import dedent

from finance_director_coach.models import (
    ContentSection,
    FinancialPackTable,
    FinancialPackTableLayout,
    RecommendationRoute,
    ScenarioContent,
)
from finance_director_coach.scenarios.contracts import ScenarioMetadata

MONEY_TOLERANCE = 0.05
PERCENTAGE_TOLERANCE = 0.2
MONETARY_INPUT_GUIDANCE = "Enter monetary answers in GBP millions. 1.00 = GBP 1,000,000."

COMPANY_PNL = {
    "Revenue": (40.00, 48.00),
    "Gross profit": (18.00, 18.24),
    "EBITDA": (4.80, 3.36),
}
COMPANY_RECEIVABLES = 12.00
NORTHSTAR_REVENUE = 9.00
NORTHSTAR_DIRECT_COST = 6.00
NORTHSTAR_RECEIVABLES = 3.00
NORTHSTAR_OVERDUE_RECEIVABLES = 1.20
PAYMENT_TERMS_DAYS = 45
COMPANY_CONTRACT_ASSETS = 4.50
NORTHSTAR_CONTRACT_ASSETS = 1.80
COMPANY_DEFERRED_REVENUE = 3.20
NORTHSTAR_DEFERRED_REVENUE = 0.60
NORTHSTAR_CAPITALISED_IMPLEMENTATION = 1.00
CAPITALISED_IMPLEMENTATION_RECOVERABLE_PERCENT = 70.0
SERVICE_CREDIT_TRANSITION_PROVISION = 0.50
COMPANY_CASH = 3.80
GROSS_DEBT = 8.00
UNDRAWN_RCF = 4.00
BOARD_CASH_FLOOR = 3.50

CASH_BRIDGE = {
    "EBITDA": 3.36,
    "Increase in trade receivables": -2.40,
    "Increase in contract assets": -1.20,
    "Increase in deferred revenue": 0.40,
    "Provision cash payments": -0.30,
    "Capitalised implementation cash expenditure": -0.80,
    "Interest": -0.35,
    "Tax": -0.25,
}

ROUTE_LABELS = ("Renew as proposed", "Renegotiate to target economics", "Exit and redeploy")
REQUESTED_DISCOUNT_PERCENT = 5.0
TARGET_CONTRIBUTION_MARGIN_PERCENT = 45.0
PRICE_UPLIFT_CASH_REALISATION_PERCENT = 70.0
EXIT_AVOIDABLE_DIRECT_COST = 5.00
EXIT_REPLACEMENT_CONTRIBUTION = 3.70
ROUTE_CASH_COMPONENTS = {
    "renew": {"Additional discount cash effect": -0.45, "Further receivable and unbilled-work build": -0.90},
    "exit": {"Foregone customer cash receipts": -7.00, "Avoidable cash costs": 5.00, "Receivable recovery": 2.40, "Contract-asset recovery": 0.90, "Transition cash costs": -1.10, "Replacement cash contribution": 1.00},
}
BASELINE_MONTHLY_CASH = {"Jul": 4.10, "Aug": 3.90, "Sep": 3.70, "Oct": 3.60, "Nov": 3.80, "Dec": 4.00}
ROUTE_MONTHLY_CASH_ADJUSTMENTS = {
    "renew": {"Jul": -0.10, "Aug": -0.20, "Sep": -0.35, "Oct": -0.45, "Nov": -0.45, "Dec": -0.45},
    "renegotiate": {"Jul": -0.25, "Aug": -0.10, "Sep": 0.10, "Oct": 0.35, "Nov": 0.55, "Dec": 0.70},
    "exit": {"Jul": -0.65, "Aug": -0.55, "Sep": -0.35, "Oct": 0.15, "Nov": 0.55, "Dec": 0.85},
}

QUALITY_OPTIONS = {
    "growth_cash_divergence": "Revenue growth and reported EBITDA are not converting into cash because receivables, unbilled work, and implementation cash are absorbing liquidity.",
    "growth_proves_quality": "Revenue growth proves quality of earnings because EBITDA is positive.",
    "deferred_revenue_is_a_loss": "Deferred revenue is an accounting loss and therefore explains the cash decline.",
}
CASH_ABSORBER_OPTIONS = {
    "receivables": "Increase in trade receivables",
    "contract_assets": "Increase in contract assets or unbilled work",
    "capitalised_implementation": "Capitalised implementation cash expenditure",
    "interest": "Interest",
}
CLASSIFICATION_OPTIONS = {
    "implementation_cash": "Capitalised implementation cash expenditure: cash and balance sheet, not current P&L",
    "receivables": "Increase in receivables: cash and balance sheet, not current P&L",
    "provision_creation": "Creating or increasing a service-credit or transition provision: current-period P&L and balance sheet",
    "provision_settlement": "Settling an existing service-credit or transition provision: cash and balance sheet, not current-period P&L",
    "provision_release": "Releasing an unused service-credit or transition provision: current-period P&L and balance sheet",
    "deferred_revenue": "Increase in deferred revenue: cash and balance sheet, before revenue recognition",
    "overhead": "Allocated head-office overhead: current P&L allocation, not automatically avoidable cash",
}
EXPECTED_CLASSIFICATIONS = frozenset({"implementation_cash", "receivables", "provision_creation", "provision_settlement", "provision_release", "deferred_revenue"})
ROUTE_SAFEGUARD_OPTIONS = {
    RecommendationRoute.APPROVE: {"collections": "Weekly collections cadence for the overdue balance", "exposure": "Customer credit limit and unbilled-work exposure cap", "liquidity": "Board-floor and RCF-draw trigger while the renewal starts"},
    RecommendationRoute.CONDITIONALLY_APPROVE: {"economics": "Signed target-margin price, scope, and change-control terms", "billing": "Milestone billing with payment protection before renewal", "repair": "Commercial recovery plan for overdue receivables and unbilled work"},
    RecommendationRoute.DELAY: {"period": "Time-limited negotiation window with named exit date", "validation": "Validate collections, recovery actions, and revised target economics", "alternative": "Validate capacity-redeployment cash timing before committing"},
    RecommendationRoute.REJECT: {"transition": "Transition plan that protects service delivery and cash", "recovery": "Recover outstanding receivables and contract assets before exit", "redeployment": "Redeploy delivery capacity with a tracked replacement-contribution plan"},
}
REQUIRED_ROUTE_SAFEGUARDS = {route: frozenset(options) for route, options in ROUTE_SAFEGUARD_OPTIONS.items()}
ROUTE_PROTECTION_OPTIONS = {
    RecommendationRoute.APPROVE: {"liquidity": "Weekly board-floor forecast and RCF-draw trigger", "credit": "Freeze further exposure if overdue receivables worsen"},
    RecommendationRoute.CONDITIONALLY_APPROVE: {"billing": "Collect an upfront or milestone invoice before additional delivery", "exposure": "Cap unbilled work and require recovery of the overdue balance"},
    RecommendationRoute.DELAY: {"liquidity": "Reserve RCF capacity during the time-limited negotiation period", "exposure": "Stop incremental unbilled work until recovery and pricing are validated"},
    RecommendationRoute.REJECT: {"cash": "Weekly transition cash forecast with board-floor intervention", "recovery": "Ring-fence receivable and contract-asset recovery ownership"},
}
REQUIRED_ROUTE_PROTECTIONS = {route: frozenset(options) for route, options in ROUTE_PROTECTION_OPTIONS.items()}
ROUTE_DECISION_ASSUMPTION_OPTIONS = {
    RecommendationRoute.APPROVE: {"collection": "Overdue receivables return to the weekly collection plan", "exposure": "The customer does not create additional unbilled-work exposure"},
    RecommendationRoute.CONDITIONALLY_APPROVE: {"acceptance": "Northstar accepts target economics and milestone billing", "recovery": "The overdue balance and contract assets can be recovered"},
    RecommendationRoute.DELAY: {"negotiation": "A time-limited negotiation produces enforceable revised economics", "redeployment": "The capacity-redeployment alternative converts to cash on time"},
    RecommendationRoute.REJECT: {"recovery": "Exit does not materially impair receivable and contract-asset recovery", "redeployment": "Released capacity produces the planned replacement contribution"},
}
REQUIRED_ROUTE_ASSUMPTIONS = {route: frozenset(options) for route, options in ROUTE_DECISION_ASSUMPTION_OPTIONS.items()}


def operating_cash_flow() -> float:
    return round(sum(CASH_BRIDGE.values()), 2)


def cash_conversion_percent() -> float:
    return round(operating_cash_flow() / CASH_BRIDGE["EBITDA"] * 100, 1)


def northstar_dso() -> float:
    return round(NORTHSTAR_RECEIVABLES / NORTHSTAR_REVENUE * 365, 1)


def northstar_receivable_concentration() -> float:
    return round(NORTHSTAR_RECEIVABLES / COMPANY_RECEIVABLES * 100, 1)


def net_customer_working_capital() -> float:
    return round(NORTHSTAR_RECEIVABLES + NORTHSTAR_CONTRACT_ASSETS - NORTHSTAR_DEFERRED_REVENUE - SERVICE_CREDIT_TRANSITION_PROVISION, 2)


def customer_balance_sheet_exposure() -> float:
    return round(net_customer_working_capital() + NORTHSTAR_CAPITALISED_IMPLEMENTATION, 2)


def customer_exposure_at_risk() -> float:
    unrecovered_receivables = NORTHSTAR_RECEIVABLES * 0.20
    unrecovered_contract_assets = NORTHSTAR_CONTRACT_ASSETS * 0.50
    impaired_implementation = NORTHSTAR_CAPITALISED_IMPLEMENTATION * (1 - CAPITALISED_IMPLEMENTATION_RECOVERABLE_PERCENT / 100)
    return round(unrecovered_receivables + unrecovered_contract_assets + impaired_implementation + SERVICE_CREDIT_TRANSITION_PROVISION, 2)


def renegotiated_target_revenue() -> float:
    return round(NORTHSTAR_DIRECT_COST / (1 - TARGET_CONTRIBUTION_MARGIN_PERCENT / 100), 2)


def renegotiation_cash_realised() -> float:
    """Return forecast-period collections from the renegotiated price uplift."""
    revenue_uplift = renegotiated_target_revenue() - NORTHSTAR_REVENUE
    return round(revenue_uplift * PRICE_UPLIFT_CASH_REALISATION_PERCENT / 100, 2)


ROUTE_CASH_COMPONENTS["renegotiate"] = {
    "Cash from price and scope reset": renegotiation_cash_realised(),
    "Implementation and support cash control": 0.50,
    "Payment protection": 0.30,
}


def route_ebitda(route: str) -> float:
    current_ebitda = COMPANY_PNL["EBITDA"][1]
    if route == "renew":
        return round(current_ebitda - NORTHSTAR_REVENUE * REQUESTED_DISCOUNT_PERCENT / 100, 2)
    if route == "renegotiate":
        return round(current_ebitda + renegotiated_target_revenue() - NORTHSTAR_REVENUE, 2)
    if route == "exit":
        return round(current_ebitda - NORTHSTAR_REVENUE + EXIT_AVOIDABLE_DIRECT_COST + EXIT_REPLACEMENT_CONTRIBUTION, 2)
    raise KeyError(f"Unknown Scenario 002 route: {route}")


ROUTE_EBITDA = {route: route_ebitda(route) for route in ("renew", "renegotiate", "exit")}


def route_operating_cash(route: str) -> float:
    return round(operating_cash_flow() + sum(ROUTE_CASH_COMPONENTS[route].values()), 2)


def route_monthly_cash(route: str) -> dict[str, float]:
    return {month: round(BASELINE_MONTHLY_CASH[month] + adjustment, 2) for month, adjustment in ROUTE_MONTHLY_CASH_ADJUSTMENTS[route].items()}


def route_low_cash(route: str) -> float:
    return min(route_monthly_cash(route).values())


def route_rcf_draw(route: str) -> float:
    return round(max(0.0, BOARD_CASH_FLOOR - route_low_cash(route)), 2)


def route_liquidity_headroom(route: str) -> float:
    return round(UNDRAWN_RCF - route_rcf_draw(route), 2)


EXPECTED_OPERATING_CASH = operating_cash_flow()
EXPECTED_CASH_CONVERSION = cash_conversion_percent()
EXPECTED_DSO = northstar_dso()
EXPECTED_RECEIVABLE_CONCENTRATION = northstar_receivable_concentration()
EXPECTED_NET_WORKING_CAPITAL = net_customer_working_capital()
EXPECTED_BALANCE_SHEET_EXPOSURE = customer_balance_sheet_exposure()
EXPECTED_EXPOSURE_AT_RISK = customer_exposure_at_risk()


@dataclass(frozen=True)
class Scenario002Answers:
    quality_interpretation: str | None = None
    operating_cash_flow: float | None = None
    cash_conversion_percent: float | None = None
    largest_cash_absorber: str | None = None
    northstar_dso: float | None = None
    receivable_concentration_percent: float | None = None
    net_working_capital: float | None = None
    balance_sheet_exposure: float | None = None
    exposure_at_risk: float | None = None
    route_ebitda: dict[str, float] = field(default_factory=dict)
    route_operating_cash: dict[str, float] = field(default_factory=dict)
    route_low_cash: dict[str, float] = field(default_factory=dict)
    route_rcf_draw: dict[str, float] = field(default_factory=dict)
    route_headroom: dict[str, float] = field(default_factory=dict)
    classifications: frozenset[str] = field(default_factory=frozenset)
    recommendation: RecommendationRoute | None = None
    safeguards: frozenset[str] = field(default_factory=frozenset)
    protections: frozenset[str] = field(default_factory=frozenset)
    assumptions: frozenset[str] = field(default_factory=frozenset)
    ceo_response: str = ""


EVIDENCE_TITLES = {
    "SCN-002-E-001": "Quality of earnings", "SCN-002-E-002": "Operating cash flow", "SCN-002-E-003": "Cash conversion", "SCN-002-E-004": "Cash absorber", "SCN-002-E-005": "Northstar DSO", "SCN-002-E-006": "Receivable concentration", "SCN-002-E-007": "Net customer working capital", "SCN-002-E-008": "Balance-sheet exposure", "SCN-002-E-009": "Route EBITDA and operating cash", "SCN-002-E-010": "Monthly liquidity low point", "SCN-002-E-011": "RCF draw and headroom", "SCN-002-E-012": "Financial classification", "SCN-002-E-013": "Recommendation route", "SCN-002-E-014": "Route safeguards", "SCN-002-E-015": "Cash protections and decision assumptions"
}
BASIC_PNL_EVIDENCE_IDS = frozenset({"SCN-002-E-001"})
CRITICAL_OMISSION_LABELS = {"SCN-002-CO-001": "Integrated cash-flow evidence was materially incorrect.", "SCN-002-CO-002": "Balance-sheet exposure was materially incorrect.", "SCN-002-CO-003": "No explicit recommendation route was provided.", "SCN-002-CO-004": "Minimum route controls were not selected."}
SCENARIO_METADATA = ScenarioMetadata(("Commercial Finance", "Balance Sheet", "Cash Flow", "Liquidity"), "35 minutes", "advanced", "Synthetic FinanceOS scenario", "2.0", "Connect renewal economics, customer exposure, cash conversion, and liquidity.")

SCENARIO_002_PRESENTATION = (
    FinancialPackTable("Company performance", ("Metric", "FY2025", "FY2026 forecast"), (("Revenue", "40.00", "48.00"), ("Gross profit", "18.00", "18.24"), ("EBITDA", "4.80", "3.36"))),
    FinancialPackTable("EBITDA-to-cash bridge inputs", ("Cash bridge item", "GBP m"), (("Current EBITDA", "3.36"), ("Increase in trade receivables", "(2.40)"), ("Increase in contract assets", "(1.20)"), ("Increase in deferred revenue", "0.40"), ("Provision cash payments", "(0.30)"), ("Capitalised implementation cash expenditure", "(0.80)"), ("Interest", "(0.35)"), ("Tax", "(0.25)"))),
    FinancialPackTable("Northstar commercial inputs", ("Input", "Value"), (("Reported annual revenue", "GBP 9.00m"), ("Standard price", "GBP 10.50m"), ("Direct cost-to-serve", "GBP 6.00m"), ("Target contribution margin", "45.0%"), ("Requested additional discount", "5.0%"), ("Contractual payment terms", "45 days")), layout=FinancialPackTableLayout.KEY_VALUE),
    FinancialPackTable("Customer working capital and balance-sheet exposure", ("Input", "Value"), (("Company trade receivables", "GBP 12.00m"), ("Northstar receivables", "GBP 3.00m"), ("Northstar overdue receivables", "GBP 1.20m"), ("Company contract assets", "GBP 4.50m"), ("Northstar unbilled implementation work", "GBP 1.80m"), ("Company deferred revenue", "GBP 3.20m"), ("Northstar deferred revenue", "GBP 0.60m"), ("Capitalised Northstar implementation cost", "GBP 1.00m"), ("Expected recoverable portion", "70.0%"), ("Service-credit and transition provision", "GBP 0.50m")), layout=FinancialPackTableLayout.KEY_VALUE),
    FinancialPackTable("Liquidity inputs", ("Input", "Value"), (("Cash", "GBP 3.80m"), ("Gross debt", "GBP 8.00m"), ("Undrawn RCF", "GBP 4.00m"), ("Board minimum operating cash", "GBP 3.50m")), layout=FinancialPackTableLayout.KEY_VALUE),
    FinancialPackTable("Baseline monthly cash", ("Month", "Baseline closing cash"), (("Jul", "4.10"), ("Aug", "3.90"), ("Sep", "3.70"), ("Oct", "3.60"), ("Nov", "3.80"), ("Dec", "4.00"))),
    FinancialPackTable("Renew as proposed", ("Assumption", "Value"), (("Requested additional discount", "5.0%"), ("Annual revenue and cash reduction", "0.45"), ("Further receivable and unbilled-work build", "0.90"), ("Direct cost-to-serve base", "No immediate repair to the 6.00 base")), layout=FinancialPackTableLayout.KEY_VALUE),
    FinancialPackTable("", ("Month", "Cash adjustment"), (("Jul", "(0.10)"), ("Aug", "(0.20)"), ("Sep", "(0.35)"), ("Oct", "(0.45)"), ("Nov", "(0.45)"), ("Dec", "(0.45)"))),
    FinancialPackTable("Renegotiate to target economics", ("Assumption", "Value"), (("Target contribution margin", "45.0%"), ("Direct cost-to-serve base", "6.00"), ("Price-uplift cash timing", "70% of the price uplift is billed and collected within the forecast period."), ("Implementation and support cash control", "0.50"), ("Payment protection releases", "0.30")), layout=FinancialPackTableLayout.KEY_VALUE),
    FinancialPackTable("", ("Month", "Cash adjustment"), (("Jul", "(0.25)"), ("Aug", "(0.10)"), ("Sep", "0.10"), ("Oct", "0.35"), ("Nov", "0.55"), ("Dec", "0.70"))),
    FinancialPackTable("Exit and redeploy", ("Assumption", "Value"), (("Customer revenue", "Ends"), ("Avoidable direct cost", "5.00"), ("Direct cost remaining", "1.00"), ("Allocated head-office overhead remaining", "0.80"), ("Replacement contribution", "3.70"), ("Foregone customer cash receipts", "7.00"), ("Avoidable cash costs", "5.00"), ("Receivable recovery", "2.40"), ("Contract-asset recovery", "0.90"), ("Transition cash costs", "1.10"), ("Replacement cash contribution", "1.00")), layout=FinancialPackTableLayout.KEY_VALUE),
    FinancialPackTable("", ("Month", "Cash adjustment"), (("Jul", "(0.65)"), ("Aug", "(0.55)"), ("Sep", "(0.35)"), ("Oct", "0.15"), ("Nov", "0.55"), ("Dec", "0.85"))),
    FinancialPackTable("Definitions", ("Term", "Definition"), (("Operating cash flow", "The EBITDA-to-cash bridge total."), ("Cash conversion", "Operating cash flow / EBITDA."), ("Net customer working capital", "Northstar receivables + Northstar contract assets - Northstar deferred revenue - service-credit and transition provision."), ("Total customer balance-sheet exposure", "Net customer working capital + capitalised implementation."), ("Exposure at risk", "Assumes 20% of Northstar receivables, 50% of contract assets, the non-recoverable implementation balance, and the provision."), ("Provision creation or increase", "Affects current-period P&L and the balance sheet."), ("Provision settlement", "Affects cash and the balance sheet, not current-period P&L."), ("Provision release", "Affects current-period P&L and the balance sheet."), ("RCF draw required", "Maximum of zero and board cash floor less the route low point."), ("Remaining liquidity headroom", "Undrawn RCF less required draw.")), layout=FinancialPackTableLayout.KEY_VALUE),
)

SCENARIO_002 = ScenarioContent(
    scenario_id="SCN-002", title="Growth at Any Price: Should We Renew the Contract?", learner_role="Finance Director of Atlas Bridge, a fictional UK B2B technology and implementation-services company.", company_context="Northstar is strategically visible, but its renewal combines weak contribution, overdue cash, unbilled implementation work, and a constrained liquidity position.",
    financial_pack=(
        ContentSection("Company performance and cash bridge - GBP m", dedent("""FY2025 revenue 40.00; FY2026 forecast revenue 48.00. Gross profit moves from 18.00 to 18.24 and EBITDA from 4.80 to 3.36.\n\nCurrent EBITDA 3.36; increase in trade receivables (2.40); increase in contract assets (1.20); increase in deferred revenue 0.40; provision cash payments (0.30); capitalised implementation cash expenditure (0.80); interest (0.35); tax (0.25)."""), SCENARIO_002_PRESENTATION[:2]),
        ContentSection("Northstar customer, balance-sheet and liquidity inputs - GBP m unless stated", dedent("""Reported annual revenue 9.00; standard price 10.50; direct cost-to-serve 6.00; target contribution margin 45.0%; requested additional discount 5.0%.\n\nCompany trade receivables 12.00; Northstar receivables 3.00, including 1.20 overdue; contractual payment terms 45 days. Company contract assets 4.50; Northstar unbilled implementation work 1.80. Company deferred revenue 3.20; Northstar deferred revenue 0.60. Capitalised Northstar implementation cost 1.00, with 70.0% expected recoverable. Service-credit and transition provision 0.50.\n\nCash 3.80; gross debt 8.00; undrawn RCF 4.00; board minimum operating cash 3.50."""), SCENARIO_002_PRESENTATION[2:5]),
        ContentSection("Route and monthly-cash assumptions", dedent(f"""Baseline closing cash: Jul 4.10, Aug 3.90, Sep 3.70, Oct 3.60, Nov 3.80, Dec 4.00.\n\nRenew as proposed: the 5.0% requested discount reduces annual revenue and cash by 0.45; further receivable and unbilled-work build is 0.90. Monthly cash adjustments: Jul (0.10), Aug (0.20), Sep (0.35), Oct (0.45), Nov (0.45), Dec (0.45). There is no immediate repair to the 6.00 direct cost-to-serve base.\n\nRenegotiate to target economics: target contribution margin is 45.0% on the 6.00 direct cost-to-serve base. {PRICE_UPLIFT_CASH_REALISATION_PERCENT:.0f}% of the price uplift is billed and collected within the forecast period; implementation and support cash control is 0.50 and payment protection releases 0.30. Monthly cash adjustments: Jul (0.25), Aug (0.10), Sep 0.10, Oct 0.35, Nov 0.55, Dec 0.70.\n\nExit and redeploy: customer revenue ends; avoidable direct cost is 5.00 while 1.00 of direct cost and 0.80 allocated head-office overhead are retained. Replacement contribution is 3.70. Cash movements are foregone customer cash receipts (7.00), avoidable cash costs 5.00, receivable recovery 2.40, contract-asset recovery 0.90, transition cash costs (1.10), and replacement cash contribution 1.00. Monthly cash adjustments: Jul (0.65), Aug (0.55), Sep (0.35), Oct 0.15, Nov 0.55, Dec 0.85."""), SCENARIO_002_PRESENTATION[5:12]),
        ContentSection("Definitions", "Operating cash flow is the EBITDA-to-cash bridge total. Cash conversion is operating cash flow / EBITDA. Net customer working capital = Northstar receivables + Northstar contract assets - Northstar deferred revenue - service-credit and transition provision. Total customer balance-sheet exposure = net customer working capital + capitalised implementation. Exposure at risk assumes 20% of Northstar receivables, 50% of contract assets, the non-recoverable implementation balance, and the provision. Creating or increasing a provision affects current-period P&L and the balance sheet; settling an existing provision affects cash and the balance sheet; releasing an unused provision affects current-period P&L and the balance sheet. RCF draw required = maximum of zero and board cash floor less the route low point. Remaining liquidity headroom = undrawn RCF less required draw.", SCENARIO_002_PRESENTATION[12:]),
    ),
    initial_question="Do you approve, conditionally approve, delay, or reject Northstar's renewal when its commercial terms are weakening earnings quality, customer working capital, and liquidity?",
    model_answer="Conditionally approve only with signed target-margin pricing, milestone billing, a receivable and contract-asset recovery plan, and a board-floor RCF trigger. The account can be commercially repaired, but the cash bridge and exposure mean revenue retention alone is not a Finance Director answer.",
    debrief="Profit does not equal cash. Northstar's receivables, unbilled work, capitalised implementation cash, and transition uncertainty create a balance-sheet exposure that must be considered alongside contribution. Renegotiation has the strongest modelled liquidity path, while exit remains defensible if recoveries and redeployment can be validated.",
    self_review_checklist=("Did I reconcile EBITDA to operating cash?", "Did I distinguish working-capital exposure from P&L?", "Did I compare lowest cash points and RCF capacity, not only year-end economics?", "Did my controls cover both commercial repair and liquidity?"),
    action_plan=("Validate Northstar collections and contract-asset recovery weekly.", "Agree pricing, scope, milestone billing, and change-control protections.", "Maintain a capacity-redeployment and transition-cash downside case."),
    reconciliation_summary=f"Operating cash flow is GBP {EXPECTED_OPERATING_CASH:.2f}m and cash conversion is {EXPECTED_CASH_CONVERSION:.1f}%. Northstar DSO is {EXPECTED_DSO:.1f} days, net working-capital exposure is GBP {EXPECTED_NET_WORKING_CAPITAL:.2f}m, total customer balance-sheet exposure is GBP {EXPECTED_BALANCE_SHEET_EXPOSURE:.2f}m, and exposure at risk is GBP {EXPECTED_EXPOSURE_AT_RISK:.2f}m. The renegotiated target revenue is GBP {renegotiated_target_revenue():.2f}m, so the GBP {renegotiation_cash_realised():.2f}m forecast cash from the price uplift reflects {PRICE_UPLIFT_CASH_REALISATION_PERCENT:.0f}% collection. Route annual operating cash outcomes are renew GBP {route_operating_cash('renew'):.2f}m, renegotiate GBP {route_operating_cash('renegotiate'):.2f}m, and exit GBP {route_operating_cash('exit'):.2f}m. Low cash points are renew GBP {route_low_cash('renew'):.2f}m, renegotiate GBP {route_low_cash('renegotiate'):.2f}m, and exit GBP {route_low_cash('exit'):.2f}m; required RCF draws are GBP {route_rcf_draw('renew'):.2f}m, GBP {route_rcf_draw('renegotiate'):.2f}m, and GBP {route_rcf_draw('exit'):.2f}m.",
)
