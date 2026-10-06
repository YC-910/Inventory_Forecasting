import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DemandIQ | Inventory Decision System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GENERAL
    -------------------------------------------------------- */

    .main {
        padding-top: 1rem;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #f1f5f9;
    }

    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] .stMarkdown p {
        color: #cbd5e1;
    }

    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* --------------------------------------------------------
       HEADER
    -------------------------------------------------------- */

    .dashboard-header {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1e3a8a 100%
        );

        padding: 28px 32px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.15);
    }

    .dashboard-title {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .dashboard-subtitle {
        font-size: 15px;
        color: #dbeafe;
    }

    /* --------------------------------------------------------
       KPI CARDS
    -------------------------------------------------------- */

    .kpi-card {
        background: #ffffff;
        border: 1px solid #dbeafe;
        border-left: 5px solid #2563eb;
        border-radius: 12px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.06);
    }

    .kpi-label {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #1e3a8a;
    }

    .kpi-description {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 5px;
    }

    /* --------------------------------------------------------
       SECTION HEADER
    -------------------------------------------------------- */

    .section-title {
        font-size: 20px;
        font-weight: 650;
        color: #0f172a;
        margin-top: 20px;
        margin-bottom: 5px;
        border-left: 4px solid #2563eb;
        padding-left: 10px;
    }

    .section-description {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 15px;
        padding-left: 14px;
    }

    /* --------------------------------------------------------
       RESULT BOX
    -------------------------------------------------------- */

    .recommendation {
        background: #ffffff;
        border: 1px solid #bfdbfe;
        border-left: 5px solid #2563eb;
        border-radius: 12px;
        padding: 20px;
        margin-top: 10px;
        box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.05);
    }

    .recommendation-title {
        font-size: 16px;
        font-weight: 650;
        color: #1e3a8a;
        margin-bottom: 8px;
    }

    .recommendation-text {
        font-size: 14px;
        color: #475569;
        line-height: 1.6;
    }

    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    .sidebar-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
    }

    .sidebar-description {
        font-size: 13px;
        color: #cbd5e1;
        line-height: 1.5;
        margin-bottom: 20px;
    }

    .sidebar-section {
        font-size: 15px;
        font-weight: 600;
        color: #ffffff;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    /* --------------------------------------------------------
       SIDEBAR INPUTS
    -------------------------------------------------------- */

    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #1e293b;
        border-radius: 8px;
    }

    [data-testid="stSidebar"] [data-baseweb="input"] {
        background-color: #1e293b;
        border-radius: 8px;
    }

    /* --------------------------------------------------------
       BUTTON
    -------------------------------------------------------- */

    [data-testid="stSidebar"] .stButton > button {
        background-color: #2563eb;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #1d4ed8;
        color: #ffffff;
    }

    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding: 30px 0px 10px 0px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📦 DemandIQ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-description">
        Demand forecasting and inventory decision-support system.
        Configure the product and market conditions below.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------------
    # PRODUCT INFORMATION
    # --------------------------------------------------------

    st.markdown("### Product & Market")

    store = st.selectbox(
        "Store",
        [
            "Store A",
            "Store B",
            "Store C",
            "Store D"
        ]
    )

    category = st.selectbox(
        "Category",
        [
            "Beverages",
            "Food",
            "Household",
            "Personal Care"
        ]
    )

    region = st.selectbox(
        "Region",
        [
            "Central",
            "Northern",
            "Southern",
            "Eastern"
        ]
    )

    month = st.selectbox(
        "Month",
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
    )

    # --------------------------------------------------------
    # MARKET CONDITIONS
    # --------------------------------------------------------

    st.markdown("### Market Conditions")

    holiday = st.selectbox(
        "Holiday / Promotion",
        [
            "No",
            "Yes"
        ]
    )

    weather = st.selectbox(
        "Weather Condition",
        [
            "Sunny",
            "Cloudy",
            "Rainy"
        ]
    )

    seasonality = st.selectbox(
        "Seasonality",
        [
            "Low",
            "Normal",
            "High"
        ]
    )

    # ============================================================
    # PRICING INPUTS
    # ============================================================

    st.markdown(
        '<div class="sidebar-section">Pricing Information</div>',
        unsafe_allow_html=True
    )

    competitor_price = st.number_input(
        "Competitor Price (RM)",
        min_value=0.0,
        max_value=1000.0,
        value=8.0,
        step=0.10,
        format="%.2f"
    )

    discount = st.number_input(
        "Discount (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0,
        format="%.0f"
    )

    price = st.number_input(
        "Selling Price (RM)",
        min_value=0.0,
        max_value=1000.0,
        value=8.0,
        step=0.10,
        format="%.2f"
    )

    # --------------------------------------------------------
    # INVENTORY PARAMETERS
    # --------------------------------------------------------

    st.markdown("### Inventory Parameters")

    lead_time = st.number_input(
        "Lead Time (days)",
        min_value=1,
        max_value=30,
        value=3,
        step=1
    )

    safety_stock = st.number_input(
        "Safety Stock (units)",
        min_value=0,
        max_value=10000,
        value=50,
        step=10
    )

    current_inventory = st.number_input(
        "Current Inventory (units)",
        min_value=0,
        max_value=100000,
        value=1000,
        step=50
    )

    st.divider()

    run_forecast = st.button(
        "🔮 Run Demand Forecast",
        type="primary",
        use_container_width=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">
        <div class="dashboard-title">
            Demand Forecasting & Inventory Decision System
        </div>
        <div class="dashboard-subtitle">
            Predict demand, evaluate uncertainty, and determine
            the recommended reorder point.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CURRENT SELECTION SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">Current Scenario</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Selected product and market conditions</div>',
    unsafe_allow_html=True
)

scenario_col1, scenario_col2, scenario_col3, scenario_col4 = st.columns(4)

with scenario_col1:
    st.info(f"**Store**\n\n{store}")

with scenario_col2:
    st.info(f"**Category**\n\n{category}")

with scenario_col3:
    st.info(f"**Region**\n\n{region}")

with scenario_col4:
    st.info(f"**Month**\n\n{month}")


# ============================================================
# DEFAULT STATE
# ============================================================

if "forecast_generated" not in st.session_state:
    st.session_state.forecast_generated = False


# ============================================================
# FORECAST CALCULATION
# ============================================================

if run_forecast:

    st.session_state.forecast_generated = True


# ============================================================
# RESULTS
# ============================================================

if st.session_state.forecast_generated:

    # --------------------------------------------------------
    # MODEL INPUT
    # --------------------------------------------------------

    input_data = pd.DataFrame({
        "Store": [store],
        "Category": [category],
        "Month": [month],
        "Holiday_Promotion": [holiday],
        "Region": [region],
        "Weather_Condition": [weather],
        "Seasonality": [seasonality],
        "Competitor_Price": [competitor_price],
        "Discount_Percentage": [discount],
        "Price": [price]
    })

    # --------------------------------------------------------
    # TEMPORARY ML PREDICTION
    # --------------------------------------------------------
    #
    # Replace this value with:
    #
    # predicted_demand = model.predict(input_data)[0]
    #
    # when your actual trained model is connected.
    #

    predicted_demand = 245

    predicted_demand = max(0, predicted_demand)


    # --------------------------------------------------------
    # TEMPORARY QUANTILE FORECAST
    # --------------------------------------------------------

    q10 = predicted_demand * 0.80
    q25 = predicted_demand * 0.90
    q50 = predicted_demand
    q75 = predicted_demand * 1.10
    q90 = predicted_demand * 1.25


    # --------------------------------------------------------
    # INVENTORY CALCULATION
    # --------------------------------------------------------

    daily_demand = q50

    lead_time_demand = daily_demand * lead_time

    reorder_point = lead_time_demand + safety_stock


    # ========================================================
    # KPI SECTION
    # ========================================================

    st.markdown(
        '<div class="section-title">Forecast Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Key demand and inventory indicators'
        '</div>',
        unsafe_allow_html=True
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)


    with kpi1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">
                    Predicted Demand
                </div>

                <div class="kpi-value">
                    {predicted_demand:.0f}
                </div>

                <div class="kpi-description">
                    units
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with kpi2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">
                    Median Forecast
                </div>

                <div class="kpi-value">
                    {q50:.0f}
                </div>

                <div class="kpi-description">
                    Q50 demand
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with kpi3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">
                    Lead-Time Demand
                </div>

                <div class="kpi-value">
                    {lead_time_demand:.0f}
                </div>

                <div class="kpi-description">
                    units over {lead_time} days
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with kpi4:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">
                    Reorder Point
                </div>

                <div class="kpi-value">
                    {reorder_point:.0f}
                </div>

                <div class="kpi-description">
                    units
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # DEMAND FORECAST
    # ========================================================

    st.markdown(
        '<div class="section-title">Demand Forecast</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Forecast distribution across different demand scenarios.
        </div>
        """,
        unsafe_allow_html=True
    )


    quantile_data = pd.DataFrame({

        "Quantile": [
            "Q10",
            "Q25",
            "Q50",
            "Q75",
            "Q90"
        ],

        "Demand": [
            q10,
            q25,
            q50,
            q75,
            q90
        ]

    })


    quantile_data["Demand"] = (
        quantile_data["Demand"]
        .round()
        .astype(int)
    )


    forecast_col1, forecast_col2 = st.columns([1, 2])


    with forecast_col1:

        st.dataframe(
            quantile_data,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Q50 represents the median demand forecast. "
            "Higher quantiles represent higher-demand scenarios."
        )


    with forecast_col2:

        st.bar_chart(
            quantile_data.set_index("Quantile"),
            height=300
        )


    # ========================================================
    # INVENTORY DECISION
    # ========================================================

    st.markdown(
        '<div class="section-title">Inventory Decision</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Determine whether the current inventory level requires replenishment.
        </div>
        """,
        unsafe_allow_html=True
    )


    inventory_col1, inventory_col2 = st.columns([1, 1])


    with inventory_col1:

        inventory_data = pd.DataFrame({

            "Inventory Metric": [
                "Current Inventory",
                "Lead Time",
                "Lead-Time Demand",
                "Safety Stock",
                "Reorder Point"
            ],

            "Value": [
                f"{current_inventory:.0f} units",
                f"{lead_time} days",
                f"{lead_time_demand:.0f} units",
                f"{safety_stock:.0f} units",
                f"{reorder_point:.0f} units"
            ]

        })


        st.dataframe(
            inventory_data,
            use_container_width=True,
            hide_index=True
        )


    with inventory_col2:

        # ----------------------------------------------------
        # INVENTORY STATUS
        # ----------------------------------------------------

        if current_inventory <= reorder_point:

            st.error(
                "### ⚠️ Reorder Recommended\n\n"
                f"Current inventory is **{current_inventory:.0f} units**, "
                f"which is at or below the reorder point of "
                f"**{reorder_point:.0f} units**."
            )

        else:

            inventory_buffer = (
                current_inventory - reorder_point
            )

            st.success(
                "### ✅ Inventory Sufficient\n\n"
                f"Current inventory is **{current_inventory:.0f} units**, "
                f"which is above the reorder point of "
                f"**{reorder_point:.0f} units**.\n\n"
                f"Current inventory buffer: "
                f"**{inventory_buffer:.0f} units**."
            )


    # ========================================================
    # REORDER POINT VISUALIZATION
    # ========================================================

    st.markdown(
        '<div class="section-title">Inventory Position</div>',
        unsafe_allow_html=True
    )

    inventory_chart = pd.DataFrame({

        "Inventory Level": [
            current_inventory,
            reorder_point,
            safety_stock
        ],

        "Units": [
            current_inventory,
            reorder_point,
            safety_stock
        ]

    })


    st.bar_chart(
        inventory_chart.set_index("Inventory Level"),
        height=250
    )


    # ========================================================
    # BUSINESS RECOMMENDATION
    # ========================================================

    st.markdown(
        '<div class="section-title">Decision Recommendation</div>',
        unsafe_allow_html=True
    )


    if current_inventory <= reorder_point:

        recommendation_text = (
            f"The forecast indicates a median demand of "
            f"{q50:.0f} units. Considering a lead time of "
            f"{lead_time} days and safety stock of "
            f"{safety_stock:.0f} units, the calculated reorder "
            f"point is {reorder_point:.0f} units. "
            f"Since current inventory is {current_inventory:.0f} units, "
            f"which is below the reorder threshold, replenishment "
            f"is recommended."
        )

    else:

        recommendation_text = (
            f"The forecast indicates a median demand of "
            f"{q50:.0f} units. The calculated reorder point is "
            f"{reorder_point:.0f} units. Current inventory of "
            f"{current_inventory:.0f} units remains above the "
            f"reorder threshold, so immediate replenishment "
            f"is not required."
        )


    st.markdown(
        f"""
        <div class="recommendation">

            <div class="recommendation-title">
                📌 Inventory Recommendation
            </div>

            <div class="recommendation-text">
                {recommendation_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # FORECAST DETAILS
    # ========================================================

    with st.expander("View Forecast Input Details"):

        st.dataframe(
            input_data,
            use_container_width=True,
            hide_index=True
        )


else:

    # ========================================================
    # INITIAL EMPTY STATE
    # ========================================================

    st.markdown(
        """
        <div style="
            background: white;
            border: 1px solid #e6e8eb;
            border-radius: 12px;
            padding: 45px;
            text-align: center;
            margin-top: 30px;
        ">

            <div style="font-size: 45px;">
                📊
            </div>

            <div style="
                font-size: 22px;
                font-weight: 650;
                color: #1f2937;
                margin-top: 10px;
            ">
                Ready to Forecast
            </div>

            <div style="
                font-size: 14px;
                color: #6b7280;
                margin-top: 8px;
            ">
                Configure the product, market and inventory
                parameters using the sidebar, then click
                <b>Run Demand Forecast</b>.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        DemandIQ • Demand Forecasting & Inventory Decision Support System
    </div>
    """,
    unsafe_allow_html=True
)