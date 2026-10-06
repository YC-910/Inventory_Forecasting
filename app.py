import streamlit as st
import pandas as pd
import numpy as np
import joblib

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
# LOAD TRAINED MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("demand_model.pkl")

def prepare_model_input(input_data, model_bundle, category):

    data = input_data.copy()

    # ============================================================
    # 1. LOAD SAVED CATEGORY MAPPINGS
    # ============================================================

    mappings = model_bundle['category_mappings']

    categorical_columns = model_bundle['categorical_columns']

    # ============================================================
    # 2. CONVERT CATEGORICAL COLUMNS TO TRAINING CODES
    # ============================================================

    for col in categorical_columns:

        if col in data.columns:

            if col not in mappings:
                raise ValueError(
                    f"No saved mapping found for '{col}'."
                )

            # Convert the user's selected value
            # into the same integer code used during training
            data[col] = (
                data[col]
                .astype(str)
                .map(mappings[col])
            )

            # Check for unknown values
            if data[col].isna().any():

                original_value = input_data[col].iloc[0]

                raise ValueError(
                    f"Unknown value '{original_value}' "
                    f"for column '{col}'."
                )

            data[col] = data[col].astype(int)

    # ============================================================
    # 3. CONVERT HOLIDAY/PROMOTION TO 0/1
    # ============================================================

    if 'Holiday/Promotion' in data.columns:

        if data['Holiday/Promotion'].dtype == bool:

            data['Holiday/Promotion'] = (
                data['Holiday/Promotion']
                .astype(int)
            )

        else:

            data['Holiday/Promotion'] = (
                data['Holiday/Promotion']
                .astype(str)
                .str.strip()
                .str.lower()
                .map({
                    'true': 1,
                    'false': 0,
                    '1': 1,
                    '0': 0,
                    'yes': 1,
                    'no': 0
                })
            )

    # ============================================================
    # 4. CONVERT NUMERIC COLUMNS
    # ============================================================

    numeric_columns = [
        'Inventory Level',
        'Units Ordered',
        'Demand Forecast',
        'Price',
        'Discount',
        'Competitor Pricing',
        'Price_Discount',
        'Price_Gap',
        'Month',
        'Holiday/Promotion'
    ]

    for col in numeric_columns:

        if col in data.columns:

            data[col] = pd.to_numeric(
                data[col],
                errors='coerce'
            )

    # ============================================================
    # 5. FORCE EXACT SAME FEATURE ORDER AS TRAINING
    # ============================================================

    data = data[
        model_bundle['feature_columns']
    ].copy()

    # ============================================================
    # 6. CHECK FOR MISSING VALUES
    # ============================================================

    if data.isnull().any().any():

        bad_columns = data.columns[
            data.isnull().any()
        ].tolist()

        raise ValueError(
            f"Invalid or missing values in: {bad_columns}"
        )

    # ============================================================
    # 7. FINAL NUMERIC CONVERSION
    # ============================================================

    for col in data.columns:

        data[col] = pd.to_numeric(
            data[col],
            errors='raise'
        )

    # ============================================================
    # 8. DEBUG CHECK
    # ============================================================

    print("\n" + "=" * 70)
    print("FINAL MODEL INPUT CHECK")
    print("=" * 70)

    print("\nColumns:")
    print(data.columns.tolist())

    print("\nData types:")
    print(data.dtypes)

    print("\nValues:")
    print(data)

    print("\nNon-numeric columns:")
    print(
        data.select_dtypes(
            exclude=np.number
        ).columns.tolist()
    )

    return data

try:
    model = load_model()
    model_loaded = True
    model_error = None

except Exception as e:
    model = None
    model_loaded = False
    model_error = str(e)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GENERAL
    ======================================================== */

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

    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {
        overflow-x: hidden !important;
    }


    /* ========================================================
       SIDEBAR TEXT
    ======================================================== */

    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] .stMarkdown p {
        color: #cbd5e1;
    }

    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

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


    /* ========================================================
       SIDEBAR INPUTS
    ======================================================== */

    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #1e293b;
        border-radius: 8px;
    }

    [data-testid="stSidebar"] [data-baseweb="input"] {
        background-color: #1e293b;
        border-radius: 8px;
    }


    /* ========================================================
       FORECAST BUTTON
    ======================================================== */

    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(
            135deg,
            #2563eb,
            #1d4ed8
        ) !important;

        color: #ffffff !important;
        border: 1px solid #60a5fa !important;
        border-radius: 9px !important;

        font-size: 14px !important;
        font-weight: 650 !important;

        padding: 12px !important;

        box-shadow:
            0px 4px 12px rgba(37, 99, 235, 0.35) !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #3b82f6,
            #2563eb
        ) !important;

        border-color: #93c5fd !important;
        color: #ffffff !important;
    }


    /* ========================================================
       SIDEBAR COLLAPSE / EXPAND BUTTON
    ======================================================== */

    [data-testid="stSidebarCollapseButton"] button {
        background-color: #2563eb !important;
        color: #ffffff !important;

        border: 2px solid #ffffff !important;
        border-radius: 8px !important;

        width: 38px !important;
        height: 38px !important;

        opacity: 1 !important;
        visibility: visible !important;

        box-shadow:
            0px 3px 10px rgba(0, 0, 0, 0.25) !important;
    }

    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarCollapseButton"] button:focus,
    [data-testid="stSidebarCollapseButton"] button:active {
        background-color: #2563eb !important;
        color: #ffffff !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebarCollapseButton"] button svg {
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }


    /* ========================================================
       HEADER
    ======================================================== */

    .dashboard-header {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1e3a8a 100%
        );

        padding: 28px 32px;

        border-radius: 14px;

        margin-bottom: 25px;

        box-shadow:
            0px 4px 12px rgba(15, 23, 42, 0.15);
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


    /* ========================================================
       SECTION HEADERS
    ======================================================== */

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


    /* ========================================================
       SCENARIO CARDS
    ======================================================== */

    .scenario-card {
        background: #ffffff;

        border: 1px solid #dbeafe;

        border-radius: 10px;

        padding: 15px 18px;

        min-height: 75px;

        box-shadow:
            0px 2px 8px rgba(15, 23, 42, 0.04);
    }

    .scenario-label {
        font-size: 12px;
        color: #64748b;

        margin-bottom: 5px;
    }

    .scenario-value {
        font-size: 17px;

        font-weight: 650;

        color: #1e3a8a;
    }


    /* ========================================================
       SUCCESS STATUS
    ======================================================== */

    .forecast-success {
        background: #ecfdf5;

        border: 1px solid #a7f3d0;

        border-left: 5px solid #10b981;

        border-radius: 10px;

        padding: 14px 18px;

        margin-bottom: 20px;
    }

    .forecast-success-title {
        font-size: 14px;

        font-weight: 650;

        color: #047857;
    }

    .forecast-success-text {
        font-size: 12px;

        color: #065f46;

        margin-top: 3px;
    }


    /* ========================================================
       KPI CARDS
    ======================================================== */

    .kpi-card {
        background: #ffffff;

        border: 1px solid #dbeafe;

        border-left: 5px solid #2563eb;

        border-radius: 12px;

        padding: 20px;

        min-height: 125px;

        box-shadow:
            0px 3px 10px rgba(15, 23, 42, 0.06);
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


    /* ========================================================
       RECOMMENDATION
    ======================================================== */

    .recommendation {
        background: #ffffff;

        border: 1px solid #bfdbfe;

        border-left: 5px solid #2563eb;

        border-radius: 12px;

        padding: 20px;

        margin-top: 10px;

        box-shadow:
            0px 3px 10px rgba(15, 23, 42, 0.05);
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


    /* ========================================================
       FOOTER
    ======================================================== */

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
# SESSION STATE
# ============================================================

if "forecast_generated" not in st.session_state:
    st.session_state.forecast_generated = False

if "predicted_demand" not in st.session_state:
    st.session_state.predicted_demand = None

if "input_data" not in st.session_state:
    st.session_state.input_data = None


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


    # ========================================================
    # PRODUCT INFORMATION
    # ========================================================

    st.markdown("### Product & Market")

    store = st.selectbox(
        "Store",
        [
            "S001",
            "S002",
            "S003",
            "S004",
            "S005"
        ]
    )

    category = st.selectbox(
        "Category",
        [
            "Groceries",
            "Toys",
            "Electronics",
            "Furniture",
            "Clothing"
        ]
    )

    region = st.selectbox(
        "Region",
        [
            "North",
            "West",
            "South",
            "East"
        ]
    )

    month = st.selectbox(
        "Month",
        [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12"
        ]
    )


    # ========================================================
    # MARKET CONDITIONS
    # ========================================================

    st.markdown("### Market Conditions")

    holiday = st.selectbox(
        "Holiday / Promotion",
        [
            "False",
            "True"
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
            "Spring",
            "Summer",
            "Autumn",
            "Winter"
        ]
    )


    # ========================================================
    # PRICING & INVENTORY INFORMATION
    # ========================================================

    st.markdown(
        '<div class="sidebar-section">Pricing & Inventory Information</div>',
        unsafe_allow_html=True
    )

    competitor_price = st.number_input(
        "Competitor Price (RM)",
        min_value=0.0,
        max_value=1000.0,
        value=8.00,
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
        value=8.00,
        step=0.10,
        format="%.2f"
    )

    # =======================================================
    # OTHERS
    # =======================================================
    inventory_level = st.number_input(
    "Inventory Level",
    min_value=0.0,
    max_value=100000.0,
    value=100.0,
    step=1.0
    )

    units_ordered = st.number_input(
        "Units Ordered",
        min_value=0.0,
        max_value=100000.0,
        value=100.0,
        step=1.0
    )

    demand_forecast = st.number_input(
        "Demand Forecast",
        min_value=0.0,
        max_value=100000.0,
        value=100.0,
        step=1.0
    )

    price_discount = st.number_input(
        "Price_Discount",
        min_value=-100000.0,
        max_value=100000.0,
        value=0.0,
        step=0.10,
        format="%.2f"
    )

    price_gap = st.number_input(
        "Price_Gap",
        min_value=-100000.0,
        max_value=100000.0,
        value=0.0,
        step=0.10,
        format="%.2f"
    )

    st.divider()


    # ========================================================
    # RUN FORECAST BUTTON
    # ========================================================

    run_forecast = st.button(
        "🔮 Run Demand Forecast",
        type="primary",
        use_container_width=True
    )


# ============================================================
# HEADER
# ============================================================

st.title("Demand Forecasting & Inventory Decision System")

st.caption(
    "Predict demand, evaluate uncertainty, and determine "
    "the recommended reorder point."
)


# ============================================================
# MODEL STATUS
# ============================================================

if not model_loaded:

    st.error(
        "⚠️ The demand model could not be loaded."
    )

    st.code(
        model_error,
        language="text"
    )

    st.stop()


# ============================================================
# CURRENT SCENARIO
# ============================================================

st.subheader("Current Scenario")

st.caption(
    "Selected product and market conditions"
)

scenario_col1, scenario_col2, scenario_col3, scenario_col4 = st.columns(4)

with scenario_col1:
    st.metric(
        label="Store",
        value=store
    )

with scenario_col2:
    st.metric(
        label="Category",
        value=category
    )

with scenario_col3:
    st.metric(
        label="Region",
        value=region
    )

with scenario_col4:
    st.metric(
        label="Month",
        value=month
    )


# ============================================================
# FORECAST CALCULATION
# ============================================================

if run_forecast:

    try:

        # ----------------------------------------------------
        # CREATE MODEL INPUT
        # ----------------------------------------------------

        input_data = pd.DataFrame({
            "Store ID": [store],
            "Region": [region],
            "Inventory Level": [inventory_level],
            "Units Ordered": [units_ordered],
            "Demand Forecast": [demand_forecast],
            "Price": [price],
            "Discount": [discount],
            "Weather Condition": [weather],
            "Holiday/Promotion": [holiday],
            "Competitor Pricing": [competitor_price],
            "Seasonality": [seasonality],
            "Price_Discount": [price_discount],
            "Price_Gap": [price_gap],
            "Month": [int(month)],
        })


        # ----------------------------------------------------
        # SELECT MODEL BASED ON CATEGORY
        # ----------------------------------------------------

        if category == "Furniture":

            selected_model = model["xgb_models"][category]

            selected_model_name = "XGBoost"

        else:

            selected_model = model["lgbm_models"][category]

            selected_model_name = "LightGBM"

        # ============================================================
        # PREPARE INPUT FOR MODEL
        # ============================================================

        model_input = prepare_model_input(
            input_data,
            model,
            category
        )


        # ============================================================
        # DEBUG MODEL INPUT
        # ============================================================

        print("\n" + "=" * 70)
        print("FINAL MODEL INPUT CHECK")
        print("=" * 70)

        print("\nColumns:")
        print(model_input.columns.tolist())

        print("\nData types:")
        print(model_input.dtypes)

        print("\nValues:")
        print(model_input)

        print("\nNon-numeric columns:")
        print(
            model_input.select_dtypes(
                exclude=np.number
            ).columns.tolist()
        )

        # ============================================================
        # PREDICT DEMAND
        # ============================================================

        prediction = selected_model.predict(
            model_input
        )

        predicted_demand = float(
            prediction[0]
        )

        predicted_demand = max(
            0,
            predicted_demand
        )

        # ============================================================
        # CALCULATE UNIT LEFT MANUALLY
        # ============================================================

        calculated_unit_left = (
            inventory_level
            - predicted_demand
            + units_ordered
        )

        calculated_unit_left = max(
            0,
            calculated_unit_left
        )

        # ----------------------------------------------------
        # SAVE RESULTS
        # ----------------------------------------------------

        st.session_state.forecast_generated = True

        st.session_state.predicted_demand = (
            predicted_demand
        )

        st.session_state.calculated_unit_left = (
            calculated_unit_left
        )

        st.session_state.input_data = (
            input_data
        )

        st.session_state.selected_model_name = (
            selected_model_name
        )


    except Exception as e:

        st.session_state.forecast_generated = False

        st.session_state.predicted_demand = None

        st.error(
            "❌ Unable to generate the demand forecast."
        )

        st.markdown(
            "### Model Error"
        )

        st.exception(e)

        st.markdown(
            "### Model Input Used"
        )

        try:

            st.dataframe(
                input_data,
                use_container_width=True,
                hide_index=True
            )

        except:

            pass

# ============================================================
# RESULTS
# ============================================================

if st.session_state.forecast_generated:

    predicted_demand = (
        st.session_state.predicted_demand
    )

    input_data = (
        st.session_state.input_data
    )


    # ========================================================
    # SUCCESS MESSAGE
    # ========================================================

    st.success(
    "✓ Forecast Generated Successfully\n\n"
    "The trained demand model has generated a forecast "
    "based on the selected product, market and pricing conditions."
    )


    # ========================================================
    # TEMPORARY QUANTILE FORECAST
    # ========================================================
    #
    # IMPORTANT:
    # These are temporary approximations for the UI.
    #
    # The final research methodology should generate
    # Q10, Q25, Q50, Q75 and Q90 using actual quantile
    # forecasting models.
    #
    # ========================================================

    q10 = predicted_demand * 0.80

    q25 = predicted_demand * 0.90

    q50 = predicted_demand

    q75 = predicted_demand * 1.10

    q90 = predicted_demand * 1.25


    # ========================================================
    # INVENTORY CALCULATION
    # ========================================================



    # ========================================================
    # FORECAST OVERVIEW
    # ========================================================

    st.subheader("Forecast Overview")
    st.caption("Key demand and inventory indicators")


    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    with kpi1:
        st.metric(
            "Predicted Demand",
            f"{predicted_demand:.0f}"
        )

    with kpi2:
        st.metric(
            "First Quartile Forecast",
            f"{q25:.0f}"
        )

    with kpi3:
        st.metric(
            "Median Forecast",
            f"{q50:.0f}"
        )

    with kpi4:
        st.metric(
            "First Quartile Forecast",
            f"{q75:.0f}"
        )

    with kpi5:
        st.metric(
            "Selected Model",
            st.session_state.selected_model_name
        )

    # ========================================================
    # DEMAND FORECAST
    # ========================================================

    st.subheader("Demand Forecast")
    st.caption(
        "Forecast distribution across different demand scenarios."
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


    # --------------------------------------------------------
    # QUANTILE TABLE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # QUANTILE CHART
    # --------------------------------------------------------

    with forecast_col2:

        st.bar_chart(
            quantile_data.set_index("Quantile"),
            height=300
        )


    # ========================================================
    # INVENTORY DECISION
    # ========================================================

    st.subheader("Inventory Decision")
    st.caption(
        "Determine whether the current inventory level requires replenishment."
    )

    inventory_col1, inventory_col2 = st.columns([1, 1])


    # --------------------------------------------------------
    # INVENTORY TABLE
    # --------------------------------------------------------

    with inventory_col1:

        inventory_data = pd.DataFrame({

            "Inventory Metric": [
                "Current Inventory",
                "Lead-Time Demand",
                "Safety Stock",
                "Reorder Point"
            ],

        })


        st.dataframe(
            inventory_data,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # INVENTORY POSITION
    # ========================================================

    st.markdown(
        '<div class="section-title">Inventory Position</div>',
        unsafe_allow_html=True
    )


    inventory_chart = pd.DataFrame({

        "Inventory Level": [
            "Current Inventory",
            "Reorder Point",
            "Safety Stock"
        ],

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


    st.markdown(
        f"""
        <div class="recommendation">

            <div class="recommendation-title">
                📌 Inventory Recommendation
            </div>

        </div>

        <br>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # FORECAST INPUT DETAILS
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
            border: 1px solid #dbeafe;
            border-radius: 14px;
            padding: 55px 30px;
            text-align: center;
            margin-top: 30px;
            box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.05);
        ">

            <div style="
                font-size: 46px;
                margin-bottom: 8px;
            ">
                📊
            </div>

            <div style="
                font-size: 22px;
                font-weight: 650;
                color: #1e3a8a;
                margin-top: 5px;
            ">
                Ready to Forecast
            </div>

            <div style="
                font-size: 14px;
                color: #64748b;
                margin-top: 10px;
                line-height: 1.6;
            ">
                Configure the product, market and pricing
                conditions using the sidebar.
                <br>
                Click <b>Run Demand Forecast</b> to generate
                the demand prediction.
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
