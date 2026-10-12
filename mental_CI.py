import pandas as pd
import numpy as np
# Sheet 1
df = pd.read_excel(
    "Prevalence-and-impact-of-mental-illness.xlsx",
    sheet_name="Prevalence.6",
    skiprows=4   
)

df.to_json("mental_CI.json", orient="records", indent=2, force_ascii=False)

# For ridgeline

df = pd.read_json("mental_CI.json")

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df = df.dropna(subset=["Year"])          # drop rows where Year wasn't a real number
df["Year"] = df["Year"].astype(int)      # back to clean integers

subset = df[
    (df["Response"] == "Has a long-term mental health condition") &
    (df["Year"] == df["Year"].max())
]

# pick the slice you want ridges over — adjust these filters as needed
subset = df[
    (df["Response"] == "Has a long-term mental health condition") &
    (df["Year"] == df["Year"].max())      # most recent year available
]

x_vals = np.linspace(0, subset["Upper 95% confidence limit"].max() * 1.3, 200)

rows = []
for _, r in subset.iterrows():
    lower = r["Lower 95% confidence limit"]
    upper = r["Upper 95% confidence limit"]
    est   = r["Per cent"]
    sd    = (upper - lower) / (2 * 1.96)     # 95% CI -> implied std dev

    for x in x_vals:
        density = (1 / (sd * np.sqrt(2*np.pi))) * np.exp(-0.5 * ((x - est) / sd) ** 2)
        rows.append({
            "Age group": r["Age group"],
            "Sex": r["Sex"],
            "x": x,
            "density": density
        })

pd.DataFrame(rows).to_json("ridgeline_data.json", orient="records", indent=2, force_ascii=False)

# Sheet 2
df = pd.read_excel(
    "hysterectomy-hospitalisations-data-file.xlsx",
    sheet_name="Hospitalisations (State)",
    skiprows=1 
)

df.to_json("hysterectomy_state.json", orient="records", indent=2, force_ascii=False)


# Sheet 3
df = pd.read_excel(
    "aihw-phe357-data-table-Endometriosis-hospital-procedures.xlsx",
    sheet_name="Table 3",
    skiprows=3
)

df.to_json("Selected_procedures.json", orient="records", indent=2, force_ascii=False)


# Sheet 4

df = pd.read_excel(
    "aihw-phe-239-male-and-female-health-data-tables_8.xlsx",
    sheet_name="Table S7",
    skiprows=13,        # <- the row index where real data starts, from step 1
    header=None,
    names=[
        "drop0", "Age group", "drop2",
        "Males_Number", "Males_Rate_per_1000", "drop5",
        "Females_Number", "Females_Rate_per_1000", "drop8"
    ]
)

df = df.drop(columns=[c for c in df.columns if c.startswith("drop")])

df_long = df.melt(id_vars="Age group", var_name="measure", value_name="value")
df_long[["sex", "metric"]] = df_long["measure"].str.split("_", n=1, expand=True)
df_long = df_long.drop(columns="measure")
df_long["metric"] = df_long["metric"].replace({"Number": "Number", "Rate_per_1000": "Rate per 1,000"})

df_long.to_json("Dementia.json", orient="records", indent=2, force_ascii=False)



# Sheet 5
import pandas as pd
df = pd.read_json("Selected_procedures.json")

# rename each block to something explicit and unambiguous
rename_map = {
    "Under 25": "Under 25 (Number)", "25–34": "25-34 (Number)", "35–44": "35-44 (Number)",
    "45 and over": "45 and over (Number)", "Private": "Private (Number)", "Public": "Public (Number)", "Total": "Total (Number)",

    "Under 25.1": "Under 25 (Per cent)", "25–34.1": "25-34 (Per cent)", "35–44.1": "35-44 (Per cent)",
    "45 and over.1": "45 and over (Per cent)", "Total.1": "Total (Per cent)",

    "Under 25.2": "Under 25 (Rate)", "25–34.2": "25-34 (Rate)", "35–44.2": "35-44 (Rate)",
    "45 and over.2": "45 and over (Rate)", "Private.1": "Private (Rate)", "Public.1": "Public (Rate)", "Total.2": "Total (Rate)"
}
df = df.rename(columns=rename_map)

df.to_json("Selected_procedures.json", orient="records", indent=2, force_ascii=False)



# Sheet 6
df = pd.read_excel(
    "Prevalence-and-impact-of-mental-illness.xlsx",
    sheet_name="Prevalence.5",
    skiprows=4
)

df.to_json("reported_mental_health.json", orient="records", indent=2, force_ascii=False)


# Sheet 7
df = pd.read_excel(
    "Prevalence-and-impact-of-mental-illness.xlsx",
    sheet_name="Prevalence.4",
    skiprows=4
)

df.to_json("tested_mental_health.json", orient="records", indent=2, force_ascii=False)


# Sheet 8
df = pd.read_excel(
    "Prevalence-and-impact-of-mental-illness.xlsx",
    sheet_name="Prevalence.2",
    skiprows=4
)

df.to_json("mental_health_population.json", orient="records", indent=2, force_ascii=False)


# Sheet 9
df = pd.read_excel(
    "hysterectomy-hospitalisations-data-file.xlsx",
    sheet_name="Hospitalisations (SA3)",
    skiprows=2
)

df.to_json("hysterectomy_sa3_based.json", orient="records", indent=2, force_ascii=False)



# Sheet 10
df = pd.read_excel(
    "aihw-phe357-data-table-Endometriosis-hospital-procedures.xlsx",
    sheet_name="Table 6",
    skiprows=2
)

df.to_json("common_procedures_endometriosis.json", orient="records", indent=2, force_ascii=False)


