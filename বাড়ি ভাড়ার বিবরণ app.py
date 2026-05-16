#@title 🏠 মারুফ ভাইয়ের বাড়ি ভাড়া জেনারেটর (সিঙ্গেল ও বাল্ক) { run: "auto" }

import pandas as pd
from google.colab import files
import io

# রিসিট টেক্সট জেনারেট করার মেইন ফাংশন
def generate_receipt_text(flat_no, month_year, rent_amount, unit_consumed, per_unit_cost, water_bill, cleaning_bill, arrears, advance):
    try:
        electricity_total = round(float(unit_consumed) * float(per_unit_cost))
        total_bill = int(rent_amount) + electricity_total + int(water_bill) + int(cleaning_bill) + int(arrears)
        net_payable = total_bill - int(advance)
        
        return f"""🌟 ━━☆ বাড়ি ভাড়ার বিবরণ ☆━━ 🌟
🏡 ফ্ল্যাট: {flat_no}
📅 মাস: {month_year}
📋 বিস্তারিত হিসাব:
━━━━━━━━━━━━━━━━━━━
🏠 বাড়ি ভাড়া: {int(rent_amount):,}৳
⚡ বৈদ্যুতিক বিল: {unit_consumed}×{per_unit_cost} = {electricity_total:,}৳
🚿 পানির বিল: {int(water_bill):,}৳
🧹🗑 ক্লিনিং ও আবর্জনা বিল: {int(cleaning_bill):,}৳
📌 বকেয়া: {int(arrears):,}৳
💰 অগ্রিম জমা: -{int(advance):,}৳
━━━━━━━━━━━━━━━━━━━
💵 মোট পরিশোধযোগ্য: ({int(rent_amount):,}+{electricity_total:,}+{int(water_bill):,}+{int(cleaning_bill):,}+{int(arrears):,} - {int(advance):,})
🎯 {net_payable:,} ৳ ✅

🌟 শুভেচ্ছান্তে,
💁‍♂️ মারুফ
"""
    except Exception as e:
        return "ডাটা ইনপুট সঠিক নয়! দয়া করে সংখ্যাগুলো ঠিকঠাক লিখুন।"

#--- ফর্ম এবং ইনপুট সেকশন ---
পদ্ধতি = "\u0Var\u0aef\u0be7\u09b2 \u0987\u09a8\u09aa\u09c1\u099f (Manual Form)" #@param ["ম্যানুয়াল ইনপুট (Manual Form)", "এক্সেল আপলোড (Bulk Excel)"]

if পদ্ধতি == "ম্যানুয়াল ইনপুট (Manual Form)":
    print("👉 ডানপাশের ফর্মে তথ্য লিখুন। ভুল হলে ওখানেই এডিট করুন, মেসেজ অটো আপডেট হবে!\n")
    
    #@markdown ### 📝 এখানে ফ্ল্যাটের তথ্য লিখুন (ভুল হলে এখানেই ঠিক করুন):
    ফ্ল্যাট_নম্বর = "\u09e7\u098f" #@param {type:"string"}
    মাস_ও_বছর = "\u099c\u09be\u09a8\u09c1\u09df\u09be\u09b0\u09c0 \u09eRunning" #@param {type:"string"}
    বাড়ি_ভাড়া = 5000 #@param {type:"number"}
    বিদ্যুৎ_ইউনিট = 9 #@param {type:"number"}
    ইউনিট_রেট = 102.77 #@param {type:"number"}
    পানির_বিল = 100 #@param {type:"number"}
    ক্লিনিং_বিল = 160 #@param {type:"number"}
    বকেয়া = 930 #@param {type:"number"}
    অগ্রিম = 0 #@param {type:"number"}
    
    # আউটপুট দেখানো
    print("="*40)
    print("হোয়াটসঅ্যাপের জন্য নিচের মেসেজটি কপি করুন:")
    print("="*40 + "\n")
    print(generate_receipt_text(ফ্ল্যাট_নম্বর, মাস_ও_বছর, বাড়ি_ভাড়া, বিদ্যুৎ_ইউনিট, ইউনিট_রেট, পানির_বিল, ক্লিনিং_বিল, বকেয়া, অগ্রিম))

else:
    print("\n--- 📂 এক্সেল ফাইল আপলোড করুন ---")
    print("কলামের নামগুলো হবে: [flat_no, month_year, rent_amount, unit_consumed, per_unit_cost, water_bill, cleaning_bill, arrears, advance]\n")
    
    uploaded = files.upload()
    for file_name in uploaded.keys():
        df = pd.read_excel(io.BytesIO(uploaded[file_name]))
        print("\n" + "="*50)
        print(f"--- {file_name} ফাইলের সব রিসিট নিচে তৈরি হলো ---")
        print("="*50 + "\n")
        
        for index, row in df.iterrows():
            receipt = generate_receipt_text(
                row['flat_no'], row['month_year'], row['rent_amount'], 
                row['unit_consumed'], row['per_unit_cost'], row['water_bill'], 
                row['cleaning_bill'], row['arrears'], row['advance']
            )
            print(receipt)
            print("\n" + "-"*40 + "\n")
