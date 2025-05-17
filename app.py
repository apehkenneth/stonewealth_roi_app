import os
import base64
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ------------------ CONFIGURATION ------------------ #
investment_types = {
    "Social Housing": 0.15,
    "Buy-to-Let": 0.12,
    "Property Development": 0.12
}




lang_options = {
    "en": {
        "title": "Stone Wealth ROI Calculator",
        "choose": "Choose Investment Type",
        "amount": "Investment Amount (£)",
        "duration": "Investment Duration (Years)",
        "projected": "ROI Growth for",
        "initial": "Initial Investment",
        "annual": "Annual Return",
        "fixed_return": "Total Fixed Return",
        "fixed_profit": "Total Fixed Profit",
        "roi_3_years": "Total ROI Over Investment Period",
        "monthly_payment": "Monthly Payment",
        "summary": "ROI Summary",
    },
    "ar": {
        "title": "حاسبة العائد على الاستثمار من ستون ويلث",
        "choose": "اختر نوع الاستثمار",
        "amount": "مبلغ الاستثمار (£)",
        "duration": "مدة الاستثمار (بالسنوات)",
        "projected": "نمو العائد لـ",
        "initial": "الاستثمار الأولي",
        "annual": "العائد السنوي",
        "fixed_return": "العائد الثابت الإجمالي",
        "fixed_profit": "الربح الإجمالي",
        "roi_3_years": "إجمالي العائد خلال فترة الاستثمار",
        "monthly_payment": "المبلغ الشهري",
        "summary": "ملخص العائد على الاستثمار",
    }
}

# ------------------ HELPER FUNCTIONS ------------------ #
def display_logo(path="logo.png", width=150):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"""
            <div style='display: flex; justify-content: center;'>
                <img src='data:image/png;base64,{encoded}' width='{width}'>
            </div>
            """,
            unsafe_allow_html=True
        )

def calculate_roi(amount, rate, years):
    return [amount * (1 + rate * year) for year in range(1, years + 1)]

def calculate_investment_details(amount, rate, years):
    total_fixed_return = amount * (1 + rate * years)
    total_fixed_profit = total_fixed_return - amount
    roi_percent = (total_fixed_profit / amount) * 100
    monthly_payment = total_fixed_return / (years * 12)
    return total_fixed_return, total_fixed_profit, roi_percent, monthly_payment

# ------------------ STREAMLIT APP ------------------ #
st.set_page_config(page_title="Stone Wealth ROI Calculator")


# Language selection
import locale
try:
    user_locale = locale.getlocale()[0] or 'en'
except:
    user_locale = 'en'
default_lang = "ar" if user_locale and user_locale.startswith("ar") else "en"
lang = st.sidebar.selectbox("Language / اللغة", ["en", "ar"], index=0 if default_lang == "en" else 1)
txt = lang_options[lang]

if lang == "ar":
    st.markdown("""
        <style>
        body, h1, h2, div { direction: rtl; text-align: right; }
        </style>
    """, unsafe_allow_html=True)

# Logo and Title
display_logo()
st.markdown(f"<h1 style='color:#4B4B4B; text-align:center'>{txt['title']}</h1>", unsafe_allow_html=True)

# Introduction
if lang == "en":
    st.markdown("""
    <p style='text-align: center; color: #444; font-size: 16px;'>
        Welcome to the Stone Wealth ROI Calculator. This tool empowers you to project the potential performance of your investment. 
        By selecting an investment type, amount, and duration, you’ll receive clear estimates of fixed return, total profit, and monthly income. 
        This calculator is designed to support confident, informed decision-making using realistic fixed annual growth models.
    </p>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <p style='text-align: center; color: #444; font-size: 16px;'>
        مرحبًا بك في حاسبة العائد على الاستثمار من ستون ويلث. تساعدك هذه الأداة على تقدير العائد الثابت والأرباح الشهرية
        بناءً على نوع الاستثمار والمبلغ والمدة الزمنية.
    </p>
    """, unsafe_allow_html=True)

# Input widgets
# Benchmark return selector
benchmark_options = {
    "Conservative": 0.05,
    "Market Avg": 0.063,
    "Aggressive": 0.08
}
benchmark_labels = {
    "en": {"Conservative": "Conservative (5%)", "Market Avg": "Market Avg (6.3%)", "Aggressive": "Aggressive (8%)"},
    "ar": {"Conservative": "تحفظي (5٪)", "Market Avg": "متوسط السوق (6.3٪)", "Aggressive": "هجومي (8٪)"}
}
selected_benchmark_label_ui = st.sidebar.selectbox(
    "Benchmark Type" if lang == "en" else "نوع المعيار",
    options=list(benchmark_options.keys()),
    format_func=lambda key: benchmark_labels[lang][key]
)
comparison_rate = benchmark_options[selected_benchmark_label_ui]
selected_benchmark_label = benchmark_labels[lang][selected_benchmark_label_ui]
investment_type_labels = {
    "Social Housing": {"en": "Social Housing", "ar": "الإسكان الاجتماعي"},
    "Buy-to-Let": {"en": "Buy-to-Let", "ar": "شراء للتأجير"},
    "Property Development": {"en": "Property Development", "ar": "تطوير العقارات"}
}
display_options = [investment_type_labels[key][lang] for key in investment_type_labels.keys()]
selected_display = st.sidebar.selectbox(txt["choose"], display_options)
investment_type = next(key for key, label in investment_type_labels.items() if label[lang] == selected_display)

amount = st.sidebar.number_input(txt["amount"], min_value=5000, value=10000, step=1000, format="%d")
years = st.sidebar.slider(txt["duration"], 1, 10, 3, format="%d")

# Investment notices
if lang == "en":
    st.sidebar.markdown("""
    **Note:**
    - The **Social Housing Investment Plan** starts from **£5,000 and above**.
    - The **Buy-to-Let Investment Plan** requires a minimum investment of **£149,000**.
    - The **Property Development Investment Plan** requires a minimum investment of **£450,000**.
    """)
else:
    st.sidebar.markdown("""
    **ملاحظة:**
    - تبدأ خطة الاستثمار في الإسكان الاجتماعي من **5,000 جنيه إسترليني** فما فوق.
    - تتطلب خطة شراء للتأجير حدًا أدنى قدره **149,000 جنيه إسترليني**.
    - تتطلب خطة تطوير العقارات حدًا أدنى قدره **450,000 جنيه إسترليني**.
    """)

rate = investment_types[investment_type]
returns = calculate_roi(amount, rate, years)
# comparison_rate reassigned below using selector; this line is now redundant
comparison_returns = calculate_roi(amount, comparison_rate, years)
df = pd.DataFrame({"Year": list(range(1, years + 1)), "Value": returns, "Comparison": comparison_returns})
total_fixed_return, total_fixed_profit, roi_percent, monthly_payment = calculate_investment_details(amount, rate, years)

st.markdown("---")

benchmark_return_final = comparison_returns[-1]
benchmark_roi_percent = ((benchmark_return_final - amount) / amount) * 100

# Toggle display of UK Avg Benchmark
show_benchmark = st.checkbox("Show UK Average Return Benchmark" if lang == "en" else "إظهار العائد المتوسط في المملكة المتحدة", value=True)
if show_benchmark:
    st.markdown(f"### {selected_benchmark_label}")
    col7, col8 = st.columns(2)
    col7.metric(label=selected_benchmark_label + (" Total Return" if lang == "en" else " - إجمالي العائد"), value=f"£{benchmark_return_final:,.2f}")
    col8.metric(label=selected_benchmark_label + (" ROI" if lang == "en" else " - نسبة العائد"), value=f"{benchmark_roi_percent:.0f}%")

st.write("")
st.markdown("---")

st.markdown(f"### {txt['summary']}")
col1, col2 = st.columns(2)
col1.metric(label=txt["initial"], value=f"£{amount:,}")
col2.metric(label=txt["annual"], value=f"{int(rate * 100)}%")

col3, col4 = st.columns(2)
col3.metric(label=txt["fixed_return"], value=f"£{total_fixed_return:,.2f}")
col4.metric(label=txt["fixed_profit"], value=f"£{total_fixed_profit:,.2f}")

col5, col6 = st.columns(2)
col5.metric(label=txt["roi_3_years"], value=f"{roi_percent:.0f}%")
col6.metric(label=txt["monthly_payment"], value=f"£{monthly_payment:,.2f}")

st.markdown("---")

display_name = investment_type_labels[investment_type][lang]
st.markdown(f"### {txt['projected']} {display_name}")
st.caption("X-axis: Year | Y-axis: Value (£)" if lang == "en" else "المحور الأفقي: السنة | المحور العمودي: القيمة (£)")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Year"], y=df["Value"], mode="lines+markers", name=display_name, line=dict(color="#cc9241", width=3)))
fig.add_trace(go.Scatter(x=df["Year"], y=df["Comparison"], mode="lines+markers", name=selected_benchmark_label, line=dict(color="#00BFA6", width=2, dash="dash")))
fig.update_layout(margin=dict(t=10, b=30), xaxis_title="Year" if lang == "en" else "السنة",
    yaxis_title="Value (£)" if lang == "en" else "القيمة (£)", plot_bgcolor="white")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})


st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# Educational write-up about benchmarks
if lang == "en":
    st.markdown("""
    <p style='font-size: 15px; line-height: 1.6; color: #444;'>
    <strong>About Investment Benchmarks:</strong><br>
    Benchmarks are reference points that help evaluate the performance of your investment. In this app, you can compare your selected plan against three typical scenarios:
    <ul>
        <li><strong>Conservative (5%)</strong> – a low-risk benchmark often used in cautious portfolios.</li>
        <li><strong>Market Avg (6.3%)</strong> – based on the 20-year average return of the UK FTSE 100 index, including dividends.</li>
        <li><strong>Aggressive (8%)</strong> – represents a higher-risk growth-focused investment benchmark.</li>
    </ul>
    These benchmarks help set realistic expectations and guide your financial planning decisions.
    </p>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <p style='font-size: 15px; line-height: 1.8; color: #444; text-align: right;'>
    <strong>حول معايير الاستثمار:</strong><br>
    المعايير هي نقاط مرجعية تساعد في تقييم أداء استثمارك. في هذه الأداة، يمكنك مقارنة خطتك المختارة مع ثلاث سيناريوهات شائعة:
    <ul dir='rtl'>
        <li><strong>تحفظي (5٪)</strong> – معيار منخفض المخاطر يُستخدم عادةً في المحافظ الحذرة.</li>
        <li><strong>متوسط السوق (6.3٪)</strong> – يستند إلى متوسط عائد مؤشر FTSE 100 البريطاني خلال 20 عامًا، بما في ذلك الأرباح الموزعة.</li>
        <li><strong>هجومي (8٪)</strong> – يمثل معيارًا لاستثمار يركز على النمو ويتحمل مخاطر أعلى.</li>
    </ul>
    تساعد هذه المعايير في وضع توقعات واقعية ودعم قراراتك المالية المستقبلية.
    </p>
    """, unsafe_allow_html=True)


# Footer
st.markdown("""
    <hr style="margin-top: 2em;">
    <div style="text-align: center; color: #888; font-size: 14px; padding: 10px 0;">
        © 2025 Stone Wealth. All rights reserved.
    </div>
""", unsafe_allow_html=True)
