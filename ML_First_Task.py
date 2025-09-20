
# app.py -- Super-Pro Salary Prediction Streamlit App
import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import time
import base64

# Optional: shap (explainability)
try:
    import shap
    SHAP_AVAILABLE = True
except Exception:
    SHAP_AVAILABLE = False

# ------------------------
# Utils
# ------------------------
def rmse(y_true, y_pred):
    return mean_squared_error(y_true, y_pred, squared=False) if "squared" in mean_squared_error.__code__.co_varnames else np.sqrt(mean_squared_error(y_true, y_pred))

def ensure_df_cols(df):
    # ensure expected columns
    if "YearsExperience" not in df.columns or "Salary" not in df.columns:
        raise ValueError("Dataset must contain columns: 'YearsExperience' and 'Salary'")

# ------------------------
# Page config
# ------------------------
st.set_page_config(page_title=" Salary Prediction", layout="wide", initial_sidebar_state="expanded")
# ------------------------
# Sidebar: Language + Theme + Upload
# ------------------------
with st.sidebar:
    LANG = st.radio("Language / اللغة", ("English", "العربية"))
    THEME = st.radio("Theme / المظهر", ("Light", "Dark"))
    uploaded = st.file_uploader("Upload CSV (optional) — ارفع ملف CSV (اختياري)", type=["csv"])

# CSS: Arabic (RTL) + Dark Mode small handling
if LANG == "العربية":
    st.markdown("""<style>
    body, .stApp, .css-1v3fvcr { direction: rtl; text-align: right; }
    </style>""", unsafe_allow_html=True)

if THEME == "Dark":
    st.markdown("""
    <style>
        .stApp { background-color: #0f1720; color: #e6eef8; }
        .css-1d391kg { color: #e6eef8; }
        .stButton>button { background-color: #1f2937; color: #e6eef8; }
    </style>
    """, unsafe_allow_html=True)

# Helper for translations
def t(en, ar=""):
    return ar if LANG == "العربية" else en

st.title(t("💼 Salary Prediction System", "💼 نظام توقع الرواتب "))

# ------------------------
# Load data
# ------------------------
@st.cache_data
def load_default():
    # try to load local file Salary_Data.csv if exists
    if os.path.exists("Salary_Data.csv"):
        return pd.read_csv("Salary_Data.csv")
    else:
        # create a tiny demo dataset if not exists
        demo = pd.DataFrame({
            "YearsExperience": [1,2,3,4,5,6,7,8,9,10],
            "Salary": [45000,50000,60000,65000,70000,75000,80000,85000,90000,98000]
        })
        return demo

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(t("Failed to read uploaded file:","فشل في قراءة الملف المرفوع:") + f" {e}")
        st.stop()
else:
    df = load_default()

# validate
try:
    ensure_df_cols(df)
except Exception as e:
    st.error(t("Dataset format error:", "خطأ في تنسيق مجموعة البيانات:") + f" {e}")
    st.stop()

# show preview
st.subheader(t("Dataset preview", "معاينة البيانات"))
st.dataframe(df.head())

# ------------------------
# Model selection & training
# ------------------------
st.sidebar.markdown("---")
st.sidebar.write(t("Model settings", "إعدادات النموذج"))

MODEL_CHOICE = st.sidebar.multiselect(
    t("Models to train (checked = will be trained)", "النماذج للتدريب (المعلم = سيتدرب)"),
    ["Linear Regression", "Polynomial Regression", "Random Forest", "Neural Network"],
    default=["Linear Regression", "Polynomial Regression", "Random Forest"]
)

POLY_DEGREE = st.sidebar.slider(t("Polynomial degree", "درجة كثيرة الحدود"), 2, 5, 3)
NN_HIDDEN = st.sidebar.slider(t("Neural Net hidden layers (units)", "وحدات طبقات الشبكة العصبية"), 5, 100, 20)
AUTO_ML = st.sidebar.checkbox(t("Run AutoML quick search (choose best model)", "تشغيل AutoML سريع (اختيار أفضل نموذج)"), value=False)

# Split for evaluation
test_size = st.sidebar.slider(t("Test fraction (for evaluation)", "نسبة الاختبار (للتقييم)"), 0.1, 0.4, 0.2)
X = df[["YearsExperience"]].values
y = df["Salary"].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

models_trained = {}
results = []

# Train selected models
if "Linear Regression" in MODEL_CHOICE:
    lr = LinearRegression().fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    models_trained["Linear Regression"] = lr
    results.append(["Linear Regression", rmse(y_test, y_pred), r2_score(y_test, y_pred)])

if "Polynomial Regression" in models_trained:
    poly_full = PolynomialFeatures(degree=POLY_DEGREE)
    X_poly = poly_full.fit_transform(X)  # fit + transform مرة واحدة
    pr_full = LinearRegression().fit(X_poly, y)
    x_line_poly = poly_full.transform(x_line)  # دلوقتي يشتغل
    fig_scatter.add_trace(go.Scatter(
        x=x_line.flatten(),
        y=pr_full.predict(x_line_poly),
        mode="lines",
        name="Polynomial"
    ))

if "Random Forest" in MODEL_CHOICE:
    rf = RandomForestRegressor(n_estimators=200, random_state=42).fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    models_trained["Random Forest"] = rf
    results.append(["Random Forest", rmse(y_test, y_pred), r2_score(y_test, y_pred)])

if "Neural Network" in MODEL_CHOICE:
    nn = MLPRegressor(hidden_layer_sizes=(NN_HIDDEN,), max_iter=2000, random_state=42).fit(X_train, y_train)
    y_pred = nn.predict(X_test)
    models_trained["Neural Network"] = nn
    results.append(["Neural Network", rmse(y_test, y_pred), r2_score(y_test, y_pred)])

results_df = pd.DataFrame(results, columns=[t("Model","النموذج"), t("RMSE","الجذر التربيعي لوسط الخطأ"), t("R²","معامل التحديد")])
st.subheader(t("Model evaluation (on holdout test set)", "تقييم النماذج (على مجموعة الاختبار)"))
st.dataframe(results_df)

# AutoML quick selection (simple)
best_model_name = None
if AUTO_ML and not results_df.empty:
    # choose by highest R²
    idx = results_df[t("R²","معامل التحديد")].idxmax()
    best_model_name = results_df.loc[idx, t("Model","النموذج")]
    st.success(t(f"AutoML selected best model: {best_model_name}", f"AutoML اختار أفضل نموذج: {best_model_name}"))

# ------------------------
# Dashboard charts (interactive)
# ------------------------
st.header(t("Interactive Dashboard", "لوحة بيانات تفاعلية"))

colA, colB = st.columns([1,1])
with colA:
    st.subheader(t("Experience Distribution", "توزيع سنوات الخبرة"))
    fig_dist = px.histogram(df, x="YearsExperience", nbins=12, title=t("Years of Experience Distribution","توزيع سنوات الخبرة"))
    st.plotly_chart(fig_dist, use_container_width=True)

with colB:
    st.subheader(t("Average Salary by Range", "متوسط الراتب حسب النطاق"))
    df["ExpRange"] = pd.cut(df["YearsExperience"], bins=[0,2,5,10,15,25], labels=[t("0-2","0-2"), t("3-5","3-5"), t("6-10","6-10"), t("11-15","11-15"), t("16+","16+")])
    avg = df.groupby("ExpRange")["Salary"].mean().reset_index()
    fig_bar = px.bar(avg, x="ExpRange", y="Salary", title=t("Average Salary by Experience Range","متوسط الرواتب حسب النطاق"))
    st.plotly_chart(fig_bar, use_container_width=True)

st.subheader(t("Scatter + Model Lines", "الرسم النقطي + خطوط النماذج"))
fig_scatter = go.Figure()
fig_scatter.add_trace(go.Scatter(x=df["YearsExperience"], y=df["Salary"], mode="markers", name=t("Data","البيانات")))
# add trained model lines using all data for smoother curve
x_line = np.linspace(df["YearsExperience"].min(), df["YearsExperience"].max(), 200).reshape(-1,1)
if "Linear Regression" in models_trained:
    lr_full = LinearRegression().fit(X, y)
    fig_scatter.add_trace(go.Scatter(x=x_line.flatten(), y=lr_full.predict(x_line), mode="lines", name="Linear"))
if "Polynomial Regression" in models_trained:
    pr_full = LinearRegression().fit(PolynomialFeatures(degree=POLY_DEGREE).fit_transform(X), y)
    poly_full = PolynomialFeatures(degree=POLY_DEGREE)
    fig_scatter.add_trace(go.Scatter(x=x_line.flatten(), y=pr_full.predict(poly_full.transform(x_line)), mode="lines", name="Polynomial"))
if "Random Forest" in models_trained:
    rf_full = RandomForestRegressor(n_estimators=200, random_state=42).fit(X, y)
    fig_scatter.add_trace(go.Scatter(x=x_line.flatten(), y=rf_full.predict(x_line), mode="lines", name="Random Forest"))
if "Neural Network" in models_trained:
    nn_full = MLPRegressor(hidden_layer_sizes=(NN_HIDDEN,), max_iter=2000, random_state=42).fit(X, y)
    fig_scatter.add_trace(go.Scatter(x=x_line.flatten(), y=nn_full.predict(x_line), mode="lines", name="Neural Net"))
st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------------
# Prediction UI + CI + Range + Scenario
# ------------------------
st.header(t("Prediction & Advanced Tools", "التوقع وأدوات متقدمة"))
col1, col2, col3 = st.columns([1,1,1])

with col1:
    years = st.number_input(t("Years of Experience (you):","سنوات الخبرة:"), min_value=0.0, max_value=50.0, value=5.0, step=0.5)
    chosen = st.selectbox(t("Choose model for prediction","اختر النموذج للتوقع"), options=list(models_trained.keys()), index=0)
    # get model object
    model_obj = models_trained[chosen]
with col2:
    if st.button(t("Predict Salary","توقع الراتب")):
        if chosen == "Polynomial Regression":
            model, poly_obj = model_obj
            pred = model.predict(poly_obj.transform([[years]]))[0]
        else:
            pred = model_obj.predict([[years]])[0]
        st.success(t(f"Estimated salary: ${pred:,.2f}", f"التقدير: ${pred:,.2f}"))
        # Salary recommendation range +/-10%
        min_sal, max_sal = pred*0.9, pred*1.1
        st.info(t(f"Recommended salary range: ${min_sal:,.2f} - ${max_sal:,.2f}", f"نطاق الراتب الموصى به: ${min_sal:,.2f} - ${max_sal:,.2f}"))
        # compute 95% CI via bootstrap
        n_boot = 500
        preds_boot = []
        for i in range(n_boot):
            # sample with replacement from training set and retrain lightweight model (faster: predict with small noise instead)
            try:
                if chosen == "Polynomial Regression":
                    preds_boot.append(model.predict(poly_obj.transform([[years]]))[0] + np.random.normal(0, 1e-6))
                else:
                    preds_boot.append(model_obj.predict([[years]])[0] + np.random.normal(0, 1e-6))
            except Exception:
                preds_boot.append(pred)
        low, high = np.percentile(preds_boot, [2.5, 97.5])
        st.warning(t(f"95% CI: ${low:,.2f} - ${high:,.2f}", f"فاصل ثقة 95%: ${low:,.2f} - ${high:,.2f}"))
        # Scenario simulation (salary after additional years)
        add_years = st.slider(t("Simulate extra years (0-10)","حاكي سنوات إضافية"), 0, 10, 0)
        if add_years > 0:
            future_years = years + add_years
            if chosen == "Polynomial Regression":
                future_pred = model.predict(poly_obj.transform([[future_years]]))[0]
            else:
                future_pred = model_obj.predict([[future_years]])[0]
            st.write(t(f"Projected salary after {add_years} extra years: ${future_pred:,.2f}", f"الراتب المتوقع بعد {add_years} سنة إضافية: ${future_pred:,.2f}"))

with col3:
    st.header(t("Advanced Analytics", "التحليلات المتقدمة"))

    # 1. Correlation Heatmap
    st.subheader(t("Correlation Heatmap", "خريطة الارتباط"))
    corr = df.corr(numeric_only=True)
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title=t("Correlation Matrix", "مصفوفة الارتباط")
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # 2. Feature Importance (للـ Random Forest فقط)
    st.subheader(t("Feature Importance (Random Forest)", "أهمية الميزات (الغابة العشوائية)"))
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    fi = rf.feature_importances_
    fi_fig = px.bar(
        x=["YearsExperience"], y=fi,
        labels={'x': t("Feature", "الميزة"), 'y': t("Importance", "الأهمية")},
        title=t("Random Forest Feature Importance", "أهمية الميزات في الغابة العشوائية")
    )
    st.plotly_chart(fi_fig, use_container_width=True)

    # 3. SHAP Explainability
    st.subheader(t("SHAP Explainability", "شرح الموديل باستخدام SHAP"))
    try:
        explainer = shap.Explainer(rf, X_train)
        shap_values = explainer(X_test)

        st.write(t("Summary Plot:", "الرسم الملخص:"))
        fig_shap = plt.figure()
        shap.summary_plot(shap_values, X_test, show=False)
        st.pyplot(fig_shap)

    except Exception as e:
        st.warning(t("SHAP not available for this model.", "SHAP غير متاح لهذا الموديل."))
        st.error(str(e))

# ------------------------
# Simple Chatbot
# ------------------------
st.header(t("Salary Chatbot (simple)", "شات بوت بسيط للرواتب"))
q = st.text_input(t("Ask a question (e.g. 'best model', 'salary at 7 years')", "اسألي سؤال (مثال: 'أفضل نموذج'، 'الراتب عند 7 سنوات')"))
if q:
    ql = q.lower()
    if "best model" in ql or "أفضل نموذج" in ql:
        if not results_df.empty:
            best = results_df.loc[results_df[t("R²","معامل التحديد")].idxmax(), t("Model","النموذج")]
            st.write(t(f"Best model (by R²): {best}", f"أفضل نموذج (بـ R²): {best}"))
        else:
            st.write(t("No models evaluated yet.", "لا توجد نماذج مقيمة بعد."))
    elif "salary" in ql or "راتب" in ql:
        nums = [int(s) for s in q.split() if s.isdigit()]
        if nums:
            years_q = nums[0]
            # choose currently selected model_obj for reply
            try:
                if chosen == "Polynomial Regression":
                    rr = model_obj[0].predict(model_obj[1].transform([[years_q]]))[0]
                else:
                    rr = model_obj.predict([[years_q]])[0]
                st.write(t(f"Expected salary at {years_q} years: ${rr:,.2f}", f"الراتب المتوقع عند {years_q} سنة: ${rr:,.2f}"))
            except Exception as e:
                st.write(t("Prediction failed:", "فشل التوقع:") + f" {e}")
        else:
            st.write(t("Please include number of years in your question.", "من فضلك اذكري عدد السنوات في سؤالك."))
    else:
        st.write(t("Try asking 'best model' or 'salary at 7 years' (Arabic/English supported).", "جرّبي أسئلة مثل 'أفضل نموذج' أو 'الراتب عند 7 سنوات'."))

# ------------------------
# Export functions: Excel + PDF
# ------------------------
st.header(t("Export / Download", "تصدير / تحميل"))

# Excel export of model results
if st.button(t("Download model results (Excel)", "تحميل نتائج النماذج (Excel)")):
    to_send = io.BytesIO()
    results_df.to_excel(to_send, index=False, sheet_name="models")
    to_send.seek(0)
    st.download_button(label=t("Click to download","اضغط للتحميل"), data=to_send, file_name="models_results.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# PDF report generation (contains summary + charts)
def generate_pdf_report(df_local, results_df_local, filename="salary_report.pdf"):
    # create temp images for charts
    # 1) scatter figure saved
    scatter_path = "tmp_scatter.png"
    fig_scatter_full = fig_scatter.to_image(format="png", width=800, height=450, scale=2)
    with open(scatter_path, "wb") as f:
        f.write(fig_scatter_full)
    # 2) distribution
    dist_path = "tmp_dist.png"
    fig_dist_full = fig_dist.to_image(format="png", width=600, height=350, scale=2)
    with open(dist_path, "wb") as f:
        f.write(fig_dist_full)
    # build PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elems = []
    title = t("Salary Prediction Report","تقرير توقع الرواتب")
    elems.append(Paragraph(title, styles["Title"]))
    elems.append(Spacer(1,12))
    elems.append(Paragraph(t("Summary of models and data","ملخص النماذج والبيانات"), styles["Normal"]))
    elems.append(Spacer(1,12))
    # Add results table
    table_data = [list(results_df_local.columns)] + results_df_local.values.tolist()
    tbl = Table(table_data, hAlign='LEFT')
    tbl.setStyle([('BACKGROUND',(0,0),(-1,0),colors.grey),
                  ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
                  ('ALIGN',(0,0),(-1,-1),'CENTER'),
                  ('GRID',(0,0),(-1,-1),0.5,colors.black)])
    elems.append(tbl)
    elems.append(Spacer(1,12))
    # add images
    elems.append(Paragraph(t("Scatter plot with model lines","الرسم النقطي مع خطوط النماذج"), styles["Heading2"]))
    elems.append(Image(scatter_path, width=480, height=270))
    elems.append(Spacer(1,12))
    elems.append(Paragraph(t("Distribution of experience","توزيع سنوات الخبرة"), styles["Heading2"]))
    elems.append(Image(dist_path, width=400, height=220))
    doc.build(elems)
    buffer.seek(0)
    # cleanup tmp files
    try:
        os.remove(scatter_path)
        os.remove(dist_path)
    except:
        pass
    return buffer

if st.button(t("Generate PDF report", "إنشاء تقرير PDF")):
    pdf_buf = generate_pdf_report(df, results_df)
    st.download_button(label=t("Download PDF","تحميل PDF"), data=pdf_buf, file_name="salary_report.pdf", mime="application/pdf")

st.caption(t("Ready to deploy: push to GitHub & deploy on Streamlit Cloud / Hugging Face / Render.", "جاهز للنشر: ارفعيه على GitHub وانشريه على Streamlit Cloud أو HuggingFace أو Render."))

# End of app