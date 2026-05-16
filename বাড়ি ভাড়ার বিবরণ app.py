import streamlit as st
import pandas as pd
import io

# পেজ কনফিগারেশন (ওয়েবসাইটের নাম ও আইকন)
st.set_page_config(page_title="Maruf Rent Generator", page_icon="🏠", layout="centered")

# ইংলিশ সংখ্যা ও অক্ষরকে বাংলায় রূপান্তর করার ফাংশন
def to_bangla(text):
    if text is None:
        return ""
    text = str(text)
    numbers = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'}
    alphabets = {
        'A': 'এ', 'B': 'বি', 'C': 'সি', 'D': 'ডি', 'E': 'ই', 'F': 'এফ',
        'a': 'এ', 'b': 'বি', 'c': 'সি', 'd': 'ডি', 'e': 'ই', 'f': 'এফ'
    }
    for eng, ban in alphabets.items():
        text = text.replace(eng, ban)
    for eng, ban in numbers.items():
        text = text.replace(eng, ban)
    return text

def month_to_bangla(month_text):
    months = {
        'January': 'জানুয়ারী', 'February': 'ফেব্রুয়ারী', 'March': 'মার্চ', 'April': 'এপ্রিল',
        'May': 'মে', 'June': 'জুন', 'July': 'জুলাই', 'August': 'আগস্ট',
        'September': 'সেপ্টেম্বর', 'October': 'অক্টোবর', 'November': 'নভেম্বর', 'December': 'ডিসেম্বর'
    }
    for eng, ban in months.items():
        if eng.lower() in month_text.lower():
            year = "".join([c for c in month_text if c.isdigit()])
            if year:
                return f"{ban} {to_bangla(year)}"
            return ban
    return to_bangla(month_text)

def generate_receipt_text(flat_no, month_year, rent_amount, unit_consumed, per_unit_cost, water_bill, cleaning_bill, arrears, advance):
    try:
        rent = int(rent_amount)
        unit = float(unit_consumed)
        rate = float(per_unit_cost)
        water = int(water_bill)
        cleaning = int(cleaning_bill)
        arr = int(arrears)
        adv = int(advance)
        
        electricity_total = round(unit * rate)
        total_bill = rent + electricity_total + water + cleaning + arr
        net_payable = total_bill - adv
        
        flat_bn = to_bangla(flat_no)
        month_bn = month_to_bangla(month_year)
        rent_bn = to_bangla(f"{rent:,}")
        unit_bn = to_bangla(str(unit_consumed))
        rate_bn = to_bangla(str(per_unit_cost))
        elec_bn = to_bangla(f"{electricity_total:,}")
        water_bn = to_bangla(f"{water:,}")
        cleaning_bn = to_bangla(f"{cleaning:,}")
        arr_bn = to_bangla(f"{arr:,}")
        adv_bn = to_bangla(f"{adv:,}")
        net_bn = to_bangla(f"{net_payable:,}")
        
        return f"""🌟 ━━☆ বাড়ি ভাড়ার বিবরণ ☆━━ 🌟
🏡 ফ্ল্যাট: {flat_bn}
📅 মাস: {month_bn}
📋 বিস্তারিত হিসাব:
━━━━━━━━━━━━━━━━━━━
🏠 বাড়ি ভাড়া: {rent_bn}৳
⚡ বৈদ্যুতিক বিল: {unit_bn}×{rate_bn} = {elec_bn}৳
🚿 পানির বিল: {water_bn}৳
🧹🗑 ক্লিনিং ও আবর্জনা বিল: {cleaning_bn}৳
📌 বকেয়া: {arr_bn}৳
💰 অগ্রিম জমা: -{adv_bn}৳
━━━━━━━━━━━━━━━━━━━
💵 মোট পরিশোধযোগ্য: ({rent_bn}+{elec_bn}+{water_bn}+{cleaning_bn}+{arr_bn} - {adv_bn})
🎯 {net_bn} ৳ ✅

🌟 শুভেচ্ছান্তে,
💁‍♂️ মারুফ
"""
    except:
        return "দয়া করে ইনপুটগুলো সঠিকভাবে দিন।"

# ওয়েবসাইটের ইন্টারফেস ডিজাইন
st.title("🏠 বাড়ি ভাড়া জেনারেটর")
st.write("ইংলিশে ইনপুট দিন, আউটপুট অটোমেটিক বাংলা হয়ে যাবে।")

tab1, tab2 = st.tabs(["সিঙ্গেল ইনপুট (Manual)", "এক্সেল আপলোড (Bulk)"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        flat = st.text_input("ফ্ল্যাট নম্বর", value="1A")
        month = st.text_input("মাস ও বছর", value="January 2026")
        rent = st.number_input("বাড়ি ভাড়া", value=5000, step=100)
        unit = st.number_input("বিদ্যুৎ ইউনিট", value=9.0, step=1.0)
        rate = st.number_input("প্রতি ইউনিট রেট", value=102.77, step=0.1)
        water = st.number_input("পানির বিল", value=100, step=10)
        cleaning = st.number_input("ক্লিনিং বিল", value=160, step=10)
        arrears = st.number_input("বকেয়া", value=930, step=10)
        advance = st.number_input("অগ্রিম জমা", value=0, step=10)
        
    with col2:
        st.subheader("হোয়াটসঅ্যাপ মেসেজ:")
        receipt = generate_receipt_text(flat, month, rent, unit, rate, water, cleaning, arrears, advance)
        st.text_area("কপি করার জন্য নিচে ক্লিক করুন", value=receipt, height=450)

with tab2:
    st.subheader("📂 এক্সেল ফাইল আপলোড করুন")
    st.caption("কলামের নামগুলো হবে: [flat_no, month_year, rent_amount, unit_consumed, per_unit_cost, water_bill, cleaning_bill, arrears, advance]")
    uploaded_file = st.file_uploader("Choose a file", type="xlsx")
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            all_receipts = ""
            for index, row in df.iterrows():
                receipt = generate_receipt_text(
                    row['flat_no'], row['month_year'], row['rent_amount'], 
                    row['unit_consumed'], row['per_unit_cost'], row['water_bill'], 
                    row['cleaning_bill'], row['arrears'], row['advance']
                )
                all_receipts += receipt + "\n" + "="*40 + "\n\n"
            st.text_area("সব ফ্ল্যাটের মেসেজ একসাথে:", value=all_receipts, height=500)
        except Exception as e:
            st.error("ফাইল প্রসেস করতে সমস্যা হয়েছে। কলামের নামগুলো চেক করুন।")
