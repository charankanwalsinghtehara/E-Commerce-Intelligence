import streamlit as st
import pandas as pd
import joblib
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Customer Churn Intelligence",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)


# =========================================================
# LOAD MODEL FILES
# =========================================================

@st.cache_resource
def load_model_files():

    model = joblib.load(
        os.path.join(
            MODEL_DIR,
            "churn_prediction_model.pkl"
        )
    )

    scaler = joblib.load(
        os.path.join(
            MODEL_DIR,
            "feature_scaler.pkl"
        )
    )

    feature_names = joblib.load(
        os.path.join(
            MODEL_DIR,
            "feature_names.pkl"
        )
    )

    threshold = joblib.load(
        os.path.join(
            MODEL_DIR,
            "best_threshold.pkl"
        )
    )

    return (
        model,
        scaler,
        feature_names,
        threshold
    )


# Load model
model, scaler, feature_names, threshold = load_model_files()


# =========================================================
# LOAD DASHBOARD DATA
# =========================================================

@st.cache_data
def load_dashboard_data():

    predictions_path = os.path.join(
        DATA_DIR,
        "churn_predictions.csv"
    )

    predictions = pd.read_csv(
        predictions_path
    )

    return predictions


predictions = load_dashboard_data()


# =========================================================
# FEATURE IMPORTANCE FUNCTION
# =========================================================

def get_feature_importance():

    # Random Forest / Gradient Boosting
    if hasattr(model, "feature_importances_"):

        importance_df = pd.DataFrame(
            {
                "Feature": feature_names,
                "Importance": model.feature_importances_
            }
        )

    # Logistic Regression
    elif hasattr(model, "coef_"):

        importance_df = pd.DataFrame(
            {
                "Feature": feature_names,
                "Importance": abs(model.coef_[0])
            }
        )

    else:

        return None

    return importance_df.sort_values(
        "Importance",
        ascending=False
    )


importance_df = get_feature_importance()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Home",
        "Customer Prediction",
        "High-Risk Customers",
        "Project Insights"
    ]
)


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    st.title("📊 Customer Churn Intelligence")

    st.write(
        """
        An end-to-end Data Analytics and Machine Learning
        project for analyzing customer behavior and predicting
        customer churn.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # KPI CALCULATIONS
    # -----------------------------------------------------

    total_customers = len(predictions)

    predicted_churners = int(
        predictions["predicted_churn"].sum()
    )

    churn_rate = (
        predicted_churners
        / total_customers
        * 100
    )

    average_probability = (
        predictions["churn_probability"].mean()
        * 100
    )

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Customers Analyzed",
            total_customers
        )

    with col2:

        st.metric(
            "Predicted Churners",
            predicted_churners
        )

    with col3:

        st.metric(
            "Predicted Churn Rate",
            f"{churn_rate:.2f}%"
        )

    with col4:

        st.metric(
            "Average Churn Risk",
            f"{average_probability:.2f}%"
        )

    st.divider()

    # -----------------------------------------------------
    # CHARTS
    # -----------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.subheader(
            "Customer Risk Distribution"
        )

        risk_counts = (
            predictions["risk_category"]
            .value_counts()
        )

        st.bar_chart(
            risk_counts
        )

    with chart_col2:

        st.subheader(
            "Prediction Distribution"
        )

        prediction_counts = (
            predictions["predicted_churn"]
            .value_counts()
        )

        prediction_counts.index = (
            prediction_counts.index.map(
                {
                    0: "Active",
                    1: "Churn Risk"
                }
            )
        )

        st.bar_chart(
            prediction_counts
        )

    st.divider()

    # -----------------------------------------------------
    # HIGH-RISK CUSTOMERS
    # -----------------------------------------------------

    st.subheader(
        "Top High-Risk Customers"
    )

    high_risk_customers = (
        predictions[
            predictions["risk_category"]
            == "High Risk"
        ]
        .sort_values(
            "churn_probability",
            ascending=False
        )
    )

    if len(high_risk_customers) > 0:

        st.dataframe(
            high_risk_customers.head(10),
            use_container_width=True
        )

    else:

        st.info(
            "No customers are currently classified as High Risk."
        )


# =========================================================
# CUSTOMER PREDICTION PAGE
# =========================================================

elif page == "Customer Prediction":

    st.title("🔮 Customer Churn Prediction")

    st.write(
        """
        Enter customer behavior information below.
        The trained machine learning model will estimate
        the probability that the customer may churn.
        """
    )

    st.divider()

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # LEFT COLUMN
    # -----------------------------------------------------

    with col1:

        total_orders = st.number_input(
            "Total Orders",
            min_value=0,
            value=1
        )

        total_spending = st.number_input(
            "Total Spending",
            min_value=0.0,
            value=1000.0
        )

        average_order_value = st.number_input(
            "Average Order Value",
            min_value=0.0,
            value=1000.0
        )

        average_discount = st.number_input(
            "Average Discount",
            min_value=0.0,
            max_value=1.0,
            value=0.10
        )

        total_quantity = st.number_input(
            "Total Quantity Purchased",
            min_value=0,
            value=1
        )

    # -----------------------------------------------------
    # RIGHT COLUMN
    # -----------------------------------------------------

    with col2:

        unique_products = st.number_input(
            "Unique Products",
            min_value=0,
            value=1
        )

        unique_categories = st.number_input(
            "Unique Categories",
            min_value=0,
            value=1
        )

        historical_recency = st.number_input(
            "Days Since Last Purchase",
            min_value=0,
            value=30
        )

        average_profit = st.number_input(
            "Average Profit",
            value=100.0
        )

    st.divider()

    # -----------------------------------------------------
    # CREATE INPUT DATA
    # -----------------------------------------------------

    input_data = pd.DataFrame(
        [[
            total_orders,
            total_spending,
            average_order_value,
            average_discount,
            total_quantity,
            unique_products,
            unique_categories,
            historical_recency,
            average_profit
        ]],
        columns=[
            "total_orders",
            "total_spending",
            "average_order_value",
            "average_discount",
            "total_quantity",
            "unique_products",
            "unique_categories",
            "historical_recency",
            "average_profit"
        ]
    )

    # Ensure feature order matches the trained model
    # ---------------------------------------------------------
# ALIGN INPUT FEATURES WITH TRAINING FEATURES
# ---------------------------------------------------------

# Create a copy so the original input remains unchanged
aligned_input = input_data.copy()

# Handle features created by pandas merge operations
# (_x and _y suffixes)

for feature in feature_names:

    if feature in aligned_input.columns:
        continue

    if feature.endswith("_x"):

        base_feature = feature[:-2]

        if base_feature in aligned_input.columns:
            aligned_input[feature] = aligned_input[
                base_feature
            ]

    elif feature.endswith("_y"):

        base_feature = feature[:-2]

        if base_feature in aligned_input.columns:
            aligned_input[feature] = aligned_input[
                base_feature
            ]


# Check whether any required features are still missing
missing_features = [
    feature
    for feature in feature_names
    if feature not in aligned_input.columns
]

if missing_features:

    st.error(
        f"Missing model features: {missing_features}"
    )

    st.stop()


# Put features in EXACTLY the same order
# used during model training
input_data = aligned_input[
    feature_names
].copy()
    # -----------------------------------------------------
    # PREDICT BUTTON
    # -----------------------------------------------------
if st.button(
        "🚀 Predict Churn Risk",
        use_container_width=True
    ):

        # Logistic Regression requires scaling
        if model.__class__.__name__ == "LogisticRegression":

            processed_input = scaler.transform(
                input_data
            )

        # Tree models do not require scaling
        else:

            processed_input = input_data

        # -------------------------------------------------
        # GET CHURN PROBABILITY
        # -------------------------------------------------

        churn_probability = model.predict_proba(
            processed_input
        )[0][1]

        # -------------------------------------------------
        # PREDICT CHURN
        # -------------------------------------------------

        predicted_churn = (
            churn_probability >= threshold
        )

        # -------------------------------------------------
        # CREATE RISK CATEGORY
        # -------------------------------------------------

        if churn_probability >= 0.75:

            risk = "High Risk"

        elif churn_probability >= 0.40:

            risk = "Medium Risk"

        else:

            risk = "Low Risk"

        st.divider()

        st.subheader("Prediction Result")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:

            st.metric(
                "Churn Probability",
                f"{churn_probability * 100:.2f}%"
            )

        with result_col2:

            st.metric(
                "Risk Category",
                risk
            )

        with result_col3:

            if predicted_churn:

                prediction_text = "Likely to Churn"

            else:

                prediction_text = "Likely Active"

            st.metric(
                "Model Prediction",
                prediction_text
            )

        st.divider()

        # -------------------------------------------------
        # BUSINESS MESSAGE
        # -------------------------------------------------

        if predicted_churn:

            st.warning(
                """
                ⚠️ This customer is predicted to be at risk
                of churn. Consider a retention strategy such
                as personalized offers or customer engagement.
                """
            )

        else:

            st.success(
                """
                ✅ This customer is predicted to remain active
                based on the current customer behavior.
                """
            )

        # -------------------------------------------------
        # SHOW INPUT FEATURES
        # -------------------------------------------------

        with st.expander(
            "View Customer Feature Data"
        ):

            st.dataframe(
                input_data,
                use_container_width=True
            )


# =========================================================
# HIGH-RISK CUSTOMERS PAGE
# =========================================================

elif page == "High-Risk Customers":

    st.title("⚠️ High-Risk Customer Analysis")

    st.write(
        """
        Customers are ranked based on their predicted
        probability of churn.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # RISK COUNTS
    # -----------------------------------------------------

    high_risk_count = len(
        predictions[
            predictions["risk_category"]
            == "High Risk"
        ]
    )

    medium_risk_count = len(
        predictions[
            predictions["risk_category"]
            == "Medium Risk"
        ]
    )

    low_risk_count = len(
        predictions[
            predictions["risk_category"]
            == "Low Risk"
        ]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "High-Risk Customers",
            high_risk_count
        )

    with col2:

        st.metric(
            "Medium-Risk Customers",
            medium_risk_count
        )

    with col3:

        st.metric(
            "Low-Risk Customers",
            low_risk_count
        )

    st.divider()

    # -----------------------------------------------------
    # SORT CUSTOMERS
    # -----------------------------------------------------

    sorted_customers = (
        predictions.sort_values(
            "churn_probability",
            ascending=False
        )
    )

    st.subheader(
        "Top Customers at Risk"
    )

    st.dataframe(
        sorted_customers.head(20),
        use_container_width=True
    )

    st.divider()

    # -----------------------------------------------------
    # CHURN PROBABILITY CHART
    # -----------------------------------------------------

    st.subheader(
        "Top Customer Churn Probabilities"
    )

    chart_data = (
        sorted_customers
        .head(20)
        .set_index("customer_id")
        [["churn_probability"]]
    )

    st.bar_chart(
        chart_data
    )


# =========================================================
# PROJECT INSIGHTS PAGE
# =========================================================

elif page == "Project Insights":

    st.title("📈 Project Insights")

    st.write(
        """
        This page explains the machine learning features
        and business value of the project.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # FEATURES
    # -----------------------------------------------------

    st.subheader(
        "Machine Learning Features"
    )

    feature_df = pd.DataFrame(
        {
            "Feature": feature_names
        }
    )

    st.dataframe(
        feature_df,
        use_container_width=True
    )

    st.divider()

    # -----------------------------------------------------
    # FEATURE IMPORTANCE
    # -----------------------------------------------------

    st.subheader(
        "Feature Importance"
    )

    if importance_df is not None:

        importance_chart = (
            importance_df
            .set_index("Feature")
        )

        st.bar_chart(
            importance_chart
        )

        st.dataframe(
            importance_df,
            use_container_width=True
        )

    else:

        st.info(
            """
            Feature importance is not directly available
            for the selected model.
            """
        )

    st.divider()

    # -----------------------------------------------------
    # BUSINESS INTERPRETATION
    # -----------------------------------------------------

    st.subheader(
        "Business Interpretation"
    )

    st.write(
        """
        Customers with a high churn probability can be
        prioritized for retention campaigns.

        Possible actions include:

        • Personalized discounts

        • Loyalty rewards

        • Targeted marketing campaigns

        • Customer engagement strategies

        • Special offers for high-value customers
        """
    )

    st.divider()

    # -----------------------------------------------------
    # ML PIPELINE
    # -----------------------------------------------------

    st.subheader(
        "Machine Learning Workflow"
    )

    st.code(
        """
Historical Customer Data
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
RFM Segmentation
        ↓
Feature Engineering
        ↓
Temporal Churn Label
        ↓
Train / Test Split
        ↓
Multiple Model Comparison
        ↓
Threshold Tuning
        ↓
Churn Probability
        ↓
Risk Classification
"""
    )