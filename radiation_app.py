import streamlit as st
import pandas as pd
import plotly.express as px

# --- การตั้งค่าเบื้องต้น ---
st.set_page_config(page_title="Radiation Mini App", layout="centered")

# --- ส่วนหัวของแอป ---
st.title("🛡️ Radiation Exposure Mini App")
st.markdown("""
แอปนี้ช่วยให้คุณเข้าใจปริมาณรังสีที่ได้รับจากการตรวจทางการแพทย์ 
โดยเปรียบเทียบกับกิจกรรมในชีวิตประจำวันเพื่อให้เห็นภาพชัดเจนขึ้น
""")

st.divider()

# --- ส่วนรับข้อมูลจากผู้ใช้ (User Input) ---
st.subheader("📥 ระบุปริมาณรังสีที่ได้รับ")
user_mSv = st.number_input("ใส่ค่ารังสีที่ได้รับ (หน่วย: mSv):", 
                           min_value=0.0, 
                           value=0.1, 
                           format="%.4f",
                           help="คุณสามารถดูค่านี้ได้จากใบรายงานผลการตรวจ หรือสอบถามเจ้าหน้าที่รังสีเทคนิค")

# --- ส่วนการคำนวณ (Calculation Logic) ---
# ค่ามาตรฐานอ้างอิง
BANANA_UNIT = 0.0001  # mSv per banana
FLIGHT_UNIT = 0.05    # mSv per 10-hour flight (approx)
SMOKING_UNIT = 16.0   # mSv per year for 1.5 packs/day
NATURAL_YEAR = 2.4    # mSv average per year

# คำนวณค่าเปรียบเทียบ
bananas = user_mSv / BANANA_UNIT
flights = user_mSv / FLIGHT_UNIT
nature_days = (user_mSv / NATURAL_YEAR) * 365

# --- ส่วนแสดงผลเปรียบเทียบ (Comparison Cards) ---
st.subheader("🔍 เมื่อเทียบกับกิจกรรมอื่น ๆ ค่าที่คุณกรอกเท่ากับ:")

col1, col2 = st.columns(2)
with col1:
    st.info(f"🍌 **กินกล้วย:** \n\n {bananas:,.0f} ลูก")
    st.warning(f"✈️ **นั่งเครื่องบินไป-กลับยุโรป:** \n\n {flights / 2:.2f} รอบ")

with col2:
    st.error(f"🚬 **การสูบบุหรี่ (1.5 ซอง/วัน):** \n\n รับรังสีเท่ากับสูบนาน { (user_mSv/SMOKING_UNIT)*365 :.2f} วัน")
    st.success(f"🌍 **รังสีธรรมชาติ:** \n\n เท่ากับการใช้ชีวิตปกติ {nature_days:.1f} วัน")

st.divider()

# --- ส่วนแสดงกราฟเปรียบเทียบ (Visual Comparison) ---
st.subheader("📊 เปรียบเทียบกับรังสีมาตรฐาน")

chart_data = pd.DataFrame({
    "แหล่งที่มา": ["ค่าของคุณ", "รังสีธรรมชาติ (1 ปี)", "สูบบุหรี่ (1 ปี)"],
    "ปริมาณ (mSv)": [user_mSv, NATURAL_YEAR, SMOKING_UNIT]
})

fig = px.bar(chart_data, x="แหล่งที่มา", y="ปริมาณ (mSv)", 
             color="แหล่งที่มา", text_auto='.2f',
             log_y=True if user_mSv < 0.1 else False, # ใช้ Log Scale ถ้าค่าเล็กมากเพื่อให้เห็นแท่งกราฟ
             title="เปรียบเทียบในเชิงปริมาณ (สเกลอาจมีการปรับเพื่อความสวยงาม)")

st.plotly_chart(fig, use_container_width=True)

# --- คำแนะนำด้านสุขภาพ ---
with st.expander("📝 คำแนะนำเพิ่มเติม"):
    if user_mSv < 1.0:
        st.write("✅ **ระดับต่ำมาก:** ปริมาณรังสีนี้ถือว่าปลอดภัยมาก เทียบเท่ากับการใช้ชีวิตปกติไม่กี่เดือน")
    elif user_mSv <= 10.0:
        st.write("⚠️ **ระดับปานกลาง:** เป็นระดับปกติของการตรวจ CT Scan ร่างกายสามารถซ่อมแซมเซลล์ได้เอง")
    else:
        st.write("❗ **ระดับเฝ้าระวัง:** ควรปรึกษาแพทย์ถึงความจำเป็นในการตรวจซ้ำในระยะเวลาใกล้กัน")