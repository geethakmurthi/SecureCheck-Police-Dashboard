import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(
    page_title="SecureCheck Dashboard",
    page_icon="🚔",
    layout="wide"
)

# Title
#st.title("SecureCheck: Police CheckPost Dashboard")
st.title("🚔 SecureCheck Dashboard")

st.markdown("""
### Project Objective

SecureCheck is a Traffic Stop Analytics Dashboard built using:

- PostgreSQL
- SQL
- Python
- Pandas
- Streamlit

The system analyzes traffic stop records, arrests,
vehicle searches, violations, demographics, and
drug-related incidents to support law enforcement
decision-making.
""")


# Connect to PostgreSQL
engine = create_engine('postgresql://postgres:geethasri@localhost:5432/police_logs')

# Load Data
@st.cache_data
def load_data():
    query = "SELECT * FROM traffic_stops"
    df = pd.read_sql(query, engine)
    return df

df = load_data()


# Show Raw Data
if st.checkbox("Show raw data"):
    st.dataframe(df)

st.sidebar.title("🚔 SecureCheck")

# Filters
st.sidebar.markdown("---")
st.sidebar.header("🔎 Dashboard Filters")

country = st.sidebar.selectbox("Country", ["All"] + sorted(df['country_name'].dropna().unique().tolist()))
gender = st.sidebar.selectbox("Driver Gender", ["All", "M", "F"])

filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[filtered_df['country_name'] == country]
if gender != "All":
    filtered_df = filtered_df[filtered_df['driver_gender'] == gender]

analysis = st.sidebar.selectbox(
    "Choose Analysis",
    [
    "Summary",
    "Top Drug Related Vehicles",
    "Most Searched Vehicles",
    "Drug Related Stops",
    "Arrest Analysis",
    "Violation Breakdown",
    "Most Frequently Searched Violations",
    "Arrest Rate by Age Group",
    "Gender Distribution",
    "Race Gender Search Rate",
    "Peak Stop Hours",
    "Stop Duration Analysis",
    "Day vs Night Arrests",
    "Young Driver Violations",
    "Rare Violations",
    "Country Arrest Analysis",
    "Country Search Analysis",
    "Complex Queries"
    ]
)



# Summary Stats
if analysis == "Summary":
    st.subheader("📊 Summary Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Stops",
        len(filtered_df)
    )

    col2.metric(
        "Arrests",
        filtered_df['is_arrested'].sum()
    )

    col3.metric(
        "Drug Stops",
        filtered_df['drugs_related_stop'].sum()
    )

    col4.metric(
        "Searches",
        filtered_df['search_conducted'].sum()
    )

    # Chart: Violations
    st.subheader("🛑 Violations Breakdown")
    violation_counts = filtered_df['violation'].value_counts()
    st.bar_chart(violation_counts)

    # Chart: Arrests by Age Group
    st.subheader("👮 Arrests by Age Group")
    filtered_df['age_group'] = pd.cut(filtered_df['driver_age'], bins=[0, 18, 25, 35, 50, 100],
                                    labels=['<18', '18-25', '26-35', '36-50', '50+'])
    arrest_by_age = filtered_df.groupby(
        'age_group',
        observed=False
    )['is_arrested'].sum()
    st.bar_chart(arrest_by_age)

    st.success("✅Dashboard loaded successfully!")

    st.markdown("---")
#QUERY 1 : TOP DRUG RELATED VEHICLES
if analysis == "Top Drug Related Stops":

    st.subheader("🌍 Countries with Most Drug-Related Stops")

    query = """
    SELECT
        country_name,
        COUNT(*) AS stop_count
    FROM traffic_stops
    WHERE drugs_related_stop = TRUE
    GROUP BY country_name
    ORDER BY stop_count DESC;
    """

    result = pd.read_sql(query, engine)

    st.bar_chart(result.set_index("country_name"))
#QUERY 2 : "Most Searched Vehicles",
if analysis == "Most Searched Vehicles":

    st.subheader("🚗 Most Frequently Searched Vehicles")

    query = """
    SELECT vehicle_number,
           COUNT(*) AS search_count
    FROM traffic_stops
    WHERE search_conducted = TRUE
    GROUP BY vehicle_number
    ORDER BY search_count DESC
    LIMIT 10;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)
#QUERY 3 : "Drug Related Stops",
if analysis == "Drug Related Stops":

    st.subheader("🌍 Countries with Most Drug Related Stops")

    query = """
    SELECT country_name,
           COUNT(*) AS stop_count
    FROM traffic_stops
    WHERE drugs_related_stop = TRUE
    GROUP BY country_name
    ORDER BY stop_count DESC;
    """

    result = pd.read_sql(query, engine)

    st.bar_chart(result.set_index("country_name"))
#QUERY 4 : "Arrest Analysis",
if analysis == "Arrest Analysis":

    st.subheader("👮 Arrests by Driver Age Group")

    query = """
    SELECT
        CASE
            WHEN driver_age < 18 THEN '<18'
            WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
            WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
            WHEN driver_age BETWEEN 36 AND 50 THEN '36-50'
            ELSE '50+'
        END AS age_group,
        COUNT(*) AS arrest_count
    FROM traffic_stops
    WHERE is_arrested = TRUE
    GROUP BY age_group
    ORDER BY arrest_count DESC;
    """

    result = pd.read_sql(query, engine)

    st.bar_chart(result.set_index("age_group"))
#QUERY 5 : "Violation Breakdown",
if analysis == "Violation Breakdown":

    st.subheader("🚔 Top Violations in Drug Related Stops")

    query = """
    SELECT violation,
           COUNT(*) AS stop_count
    FROM traffic_stops
    WHERE drugs_related_stop = TRUE
    GROUP BY violation
    ORDER BY stop_count DESC;
    """

    result = pd.read_sql(query, engine)

    st.bar_chart(result.set_index("violation"))
#QUERY 6 : "Most Frequently Searched Violations",
if analysis == "Most Frequently Searched Violations":

    st.subheader("🔍 Most Frequently Searched Violations")

    query = """
    SELECT violation,
           COUNT(*) AS searches
    FROM traffic_stops
    WHERE search_conducted = TRUE
    GROUP BY violation
    ORDER BY searches DESC;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)
#QUERY 7 : "Arrest Rate by Age Group",
if analysis == "Arrest Rate by Age Group":

    st.subheader("👮 Arrest Rate by Age Group")

    query = """
    SELECT
        CASE
            WHEN driver_age < 18 THEN '<18'
            WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
            WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
            WHEN driver_age BETWEEN 36 AND 50 THEN '36-50'
            ELSE '50+'
        END AS age_group,
        COUNT(*) AS arrests
    FROM traffic_stops
    WHERE is_arrested = TRUE
    GROUP BY age_group
    ORDER BY arrests DESC;
    """

    result = pd.read_sql(query, engine)

    st.bar_chart(result.set_index("age_group"))
#QUERY 8 : "Gender Distribution",
if analysis == "Gender Distribution":

    st.subheader("👨‍👩‍👧 Gender Distribution by Country")

    query = """
    SELECT country_name,
           driver_gender,
           COUNT(*) AS total_stops
    FROM traffic_stops
    GROUP BY country_name, driver_gender
    ORDER BY country_name;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)
#QUERY 9 :  "Race Gender Search Rate",
if analysis == "Race Gender Search Rate":

    st.subheader("👥 Race and Gender Combination with Highest Search Rate")

    query = """
    SELECT driver_race,
           driver_gender,
           COUNT(*) AS search_count
    FROM traffic_stops
    WHERE search_conducted = TRUE
    GROUP BY driver_race, driver_gender
    ORDER BY search_count DESC;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)
#QUERY 10 : "Peak Stop Hours",
if analysis == "Peak Stop Hours":

    st.subheader("🕒 Peak Traffic Stop Hours")

    query = """
    SELECT EXTRACT(HOUR FROM stop_time) AS stop_hour,
           COUNT(*) AS total_stops
    FROM traffic_stops
    GROUP BY stop_hour
    ORDER BY stop_hour;
    """

    result = pd.read_sql(query, engine)

    st.line_chart(result.set_index("stop_hour"))
#QUERY 11 : "Stop Duration Analysis",
if analysis == "Stop Duration Analysis":

    st.subheader("⌛ Stop Duration Analysis")

    query = """
    SELECT violation,
           stop_duration,
           COUNT(*) AS total
    FROM traffic_stops
    GROUP BY violation, stop_duration
    ORDER BY total DESC;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)
#QUERY 12 : "Day vs Night Arrests",
if analysis == "Day vs Night Arrests":

    st.subheader("🌙 Day vs Night Arrest Analysis")

    query = """
    SELECT
        CASE
            WHEN EXTRACT(HOUR FROM stop_time)
                 BETWEEN 6 AND 18
            THEN 'Day'
            ELSE 'Night'
        END AS period,

        COUNT(*) FILTER
        (
            WHERE is_arrested = TRUE
        ) AS arrests

    FROM traffic_stops

    GROUP BY period;
    """

    result = pd.read_sql(query, engine)

    st.bar_chart(result.set_index("period"))
#QUERY 13 : "Young Driver Violations",
if analysis == "Young Driver Violations":

    st.subheader("👦 Violations Among Drivers Under 25")

    query = """
    SELECT violation,
           COUNT(*) AS total
    FROM traffic_stops
    WHERE driver_age < 25
    GROUP BY violation
    ORDER BY total DESC;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)
#QUERY 14 : "Rare Violations",
if analysis == "Rare Violations":

    st.subheader("⚠ Violations Rarely Resulting in Search or Arrest")

    query = """
    SELECT violation,
           COUNT(*) AS total
    FROM traffic_stops
    WHERE search_conducted = TRUE
       OR is_arrested = TRUE
    GROUP BY violation
    ORDER BY total ASC;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)
#QUERY 15 : "Country Arrest Analysis",
if analysis == "Country Arrest Analysis":

    st.subheader("🚨 Arrest Rate by Country and Violation")

    query = """
    SELECT country_name,
           violation,
           COUNT(*) AS arrests
    FROM traffic_stops
    WHERE is_arrested = TRUE
    GROUP BY country_name, violation
    ORDER BY arrests DESC;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)
#QUERY 16 : "Country Search Analysis",
if analysis == "Country Search Analysis":

    st.subheader("🔍 Searches by Country")

    query = """
    SELECT country_name,
           COUNT(*) AS searches
    FROM traffic_stops
    WHERE search_conducted = TRUE
    GROUP BY country_name
    ORDER BY searches DESC;
    """

    result = pd.read_sql(query, engine)

    st.bar_chart(result.set_index("country_name"))
#QUERY 17 : "Complex Queries"
if analysis == "Complex Queries":

    st.header("🚀 Advanced SQL Analytics")
    #A QUERY 1 
    st.subheader("1️⃣ Yearly Stops and Arrests by Country")

    query = """
    SELECT
        country_name,
        EXTRACT(YEAR FROM stop_date) AS year,
        COUNT(*) AS total_stops,
        SUM(
            CASE
                WHEN is_arrested = TRUE THEN 1
                ELSE 0
            END
        ) AS arrests
    FROM traffic_stops
    GROUP BY country_name, year
    ORDER BY year, country_name;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)

    st.markdown("---")

    #A QUERY 2
    st.subheader("2️⃣ Driver Violation Trends by Race")

    query = """
    SELECT
        driver_race,
        violation,
        COUNT(*) AS total_cases
    FROM traffic_stops
    GROUP BY driver_race, violation
    ORDER BY total_cases DESC;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)

    st.markdown("---")
    #A QUERY 3
    st.subheader("3️⃣ Traffic Stops Trend by Month")

    query = """
    SELECT
        EXTRACT(MONTH FROM stop_date)::INTEGER AS month,
        COUNT(*) AS total_stops
    FROM traffic_stops
    GROUP BY month
    ORDER BY month;
    """

    result = pd.read_sql(query, engine)

    #st.write("Columns:", result.columns.tolist())

    st.dataframe(result)

    if 'month' in result.columns:
        #st.line_chart(result.set_index('month'))
        st.bar_chart(result.set_index("month"))
        st.info(
            "The dataset contains traffic stop records for January and February. "
            "January recorded significantly more traffic stops than February."
        )
    else:
        st.error("Month column not found")


    st.markdown("---")
    #A QUERY 4
    st.subheader("4️⃣ Traffic Stops Trend by Month")

    query = """
    SELECT
        EXTRACT(MONTH FROM stop_date) AS month,
        COUNT(*) AS total_stops
    FROM traffic_stops
    GROUP BY month
    ORDER BY month;
    """

    result = pd.read_sql(query, engine)

    st.bar_chart(result.set_index("month"))

    st.markdown("---")
    #A QUERY 5
    st.subheader("5️⃣ Violation Ranking using Window Function")

    query = """
    SELECT
        violation,
        COUNT(*) AS total_cases,

        RANK() OVER
        (
            ORDER BY COUNT(*) DESC
        ) AS violation_rank

    FROM traffic_stops

    WHERE search_conducted = TRUE
       OR is_arrested = TRUE

    GROUP BY violation;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)

    st.markdown("---")
    #A QUERY 6
    st.subheader("6️⃣ Driver Demographics by Country")

    query = """
    SELECT
        country_name,
        driver_gender,
        driver_race,

        ROUND(
            AVG(driver_age),
            2
        ) AS average_age,

        COUNT(*) AS total_drivers

    FROM traffic_stops

    GROUP BY
        country_name,
        driver_gender,
        driver_race

    ORDER BY total_drivers DESC;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)

    st.markdown("---")
    #A QUERY 7
    st.subheader("7️⃣ Top 5 Violations with Highest Arrest Rates")

    query = """
    SELECT
        violation,
        COUNT(*) AS arrest_count

    FROM traffic_stops

    WHERE is_arrested = TRUE

    GROUP BY violation

    ORDER BY arrest_count DESC

    LIMIT 5;
    """

    result = pd.read_sql(query, engine)

    st.bar_chart(result.set_index("violation"))
    #BONUS QUERY 8
    st.subheader("🏆 Country Ranking by Arrest Count")

    query = """
    SELECT
        country_name,

        COUNT(*) AS arrests,

        DENSE_RANK() OVER
        (
            ORDER BY COUNT(*) DESC
        ) AS rank

    FROM traffic_stops

    WHERE is_arrested = TRUE

    GROUP BY country_name;
    """

    result = pd.read_sql(query, engine)

    st.dataframe(result)


#end 

hide_menu = """
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
"""

st.markdown(
    hide_menu,
    unsafe_allow_html=True
)