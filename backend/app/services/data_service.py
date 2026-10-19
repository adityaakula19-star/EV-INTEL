from functools import lru_cache

import pandas as pd

from app.config import settings

COUNTRY_ALIASES = {
    "india": "India",
    "china": "China",
    "germany": "Germany",
    "norway": "Norway",
    "uk": "UK",
    "united kingdom": "UK",
    "britain": "UK",
    "usa": "USA",
    "us": "USA",
    "united states": "USA",
    "united states of america": "USA",
}


@lru_cache(maxsize=1)
def load_cleaned_dataset() -> pd.DataFrame:
    if not settings.dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {settings.dataset_path}")
    df = pd.read_excel(settings.dataset_path, sheet_name="Cleaned_Data")
    df["date"] = pd.to_datetime(df["date"])
    df["country"] = df["country"].astype(str).str.strip()
    df["vehicle_category"] = df["vehicle_category"].astype(str).str.strip()
    return df


def available_countries() -> list[str]:
    return sorted(load_cleaned_dataset()["country"].unique().tolist())


def available_years() -> list[int]:
    years = load_cleaned_dataset()["year"].dropna().astype(int).unique().tolist()
    return sorted(years)


def extract_countries(text: str) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    for alias, canonical in sorted(COUNTRY_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias in lowered and canonical not in found:
            found.append(canonical)
    return found


def extract_years(text: str, default_years: list[int] | None = None) -> list[int]:
    years_in_data = set(available_years())
    found = [int(token) for token in __import__("re").findall(r"\b(20\d{2})\b", text) if int(token) in years_in_data]
    unique: list[int] = []
    for year in found:
        if year not in unique:
            unique.append(year)
    if unique:
        return unique
    return default_years or available_years()


def country_year_metrics(country: str, year: int) -> dict | None:
    df = load_cleaned_dataset()
    subset = df[(df["country"] == country) & (df["year"] == year)]
    if subset.empty:
        return None

    total_sales = int(subset["total_new_vehicle_sales"].sum())
    ev_sales = int(subset["ev_units_sold"].sum())
    penetration = round((ev_sales / total_sales) * 100, 2) if total_sales else None

    latest = (
        subset.sort_values("date")
        .groupby("region", as_index=False)
        .tail(1)
    )
    charging = float(latest["charging_stations_cumulative"].sum())

    if ev_sales:
        avg_price = float((subset["avg_ev_price_usd"] * subset["ev_units_sold"]).sum() / ev_sales)
    else:
        avg_price = float(subset["avg_ev_price_usd"].mean())

    subsidy_share = round(float(subset["subsidy_active"].mean()) * 100, 2)

    return {
        "country": country,
        "year": year,
        "rows": int(len(subset)),
        "regions": int(subset["region"].nunique()),
        "total_new_vehicle_sales": total_sales,
        "ev_units_sold": ev_sales,
        "ev_market_share_pct": penetration,
        "charging_stations_latest_region_sum": charging,
        "avg_ev_price_usd": round(avg_price, 2),
        "subsidy_active_share_pct": subsidy_share,
        "vehicle_categories": sorted(subset["vehicle_category"].unique().tolist()),
    }


def country_trend(country: str) -> list[dict]:
    return [
        metrics
        for year in available_years()
        if (metrics := country_year_metrics(country, year)) is not None
    ]


def build_evidence(question: str) -> tuple[str, list[str], list[int], list[str]]:
    countries = extract_countries(question)
    years = extract_years(question)
    evidence: list[str] = []

    if not countries:
        countries = available_countries()
        evidence.append(
            "No country was named in the question. Dataset countries: "
            + ", ".join(available_countries())
        )
        question_type = "factor_or_general"
    elif len(countries) >= 2:
        question_type = "country_comparison"
    elif any(word in question.lower() for word in ["trend", "changed", "over time", "growth"]):
        question_type = "trend_analysis"
    else:
        question_type = "data_lookup"

    lowered = question.lower()
    if any(word in lowered for word in ["correlat", "related", "relationship", "statist"]):
        question_type = "statistical_analysis"
    if any(word in lowered for word in ["predict", "forecast"]):
        question_type = "prediction"
    if any(word in lowered for word in ["factor", "why", "influence", "affect"]):
        question_type = "factor_analysis"

    for country in countries:
        if question_type == "trend_analysis":
            for metrics in country_trend(country):
                evidence.append(_format_metrics(metrics))
        else:
            for year in years:
                metrics = country_year_metrics(country, year)
                if metrics is None:
                    evidence.append(f"No dataset rows for {country} in {year}.")
                else:
                    evidence.append(_format_metrics(metrics))

    if len(countries) >= 2 and years:
        year = years[0]
        a = country_year_metrics(countries[0], year)
        b = country_year_metrics(countries[1], year)
        if a and b:
            ev_diff = a["ev_units_sold"] - b["ev_units_sold"]
            share_diff = round(a["ev_market_share_pct"] - b["ev_market_share_pct"], 2)
            evidence.append(
                f"Backend comparison for {year}: {countries[0]} minus {countries[1]} "
                f"EV sales = {ev_diff}; EV new-sales share difference = {share_diff} percentage points."
            )

    return question_type, countries, years, evidence


def _format_metrics(metrics: dict) -> str:
    return (
        f"Country: {metrics['country']}; Year: {metrics['year']}; "
        f"rows={metrics['rows']}; regions={metrics['regions']}; "
        f"total_new_vehicle_sales={metrics['total_new_vehicle_sales']}; "
        f"ev_units_sold (EV sales)={metrics['ev_units_sold']}; "
        f"ev_market_share_pct (new-sales share, computed as sum(ev_units_sold)/sum(total_new_vehicle_sales)*100)="
        f"{metrics['ev_market_share_pct']}; "
        f"charging_stations_latest_region_sum={metrics['charging_stations_latest_region_sum']}; "
        f"avg_ev_price_usd={metrics['avg_ev_price_usd']}; "
        f"subsidy_active_share_pct={metrics['subsidy_active_share_pct']}; "
        f"vehicle_categories={metrics['vehicle_categories']}. "
        f"Note: charging_stations_latest_region_sum is the sum of each region's last observed "
        f"cumulative station count in that year; it is not a national official total."
    )
