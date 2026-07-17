import streamlit as st
import pandas as pd
import pickle
from datetime import datetime, timedelta
import time
from database import init_db, register_user, verify_user, increment_usage, get_all_usage, delete_user_account

init_db()

# --- STATE INITIALIZATION ---
if 'machines' not in st.session_state:
    st.session_state.machines = {i: {"status": "Available", "end_time": None, "user_roll": "", "user_name": "", "duration": 0} for i in range(1, 6)}
if 'queue' not in st.session_state:
    st.session_state.queue = []

MAX_LIMIT = 20
st.set_page_config(page_title="TIME WASHINE", layout="wide")

# --- ML LOGIC ---
def get_ml_adjustment():
    try:
        model = pickle.load(open('laundry_model.pkl', 'rb'))
        now = datetime.now()
        pred = model.predict([[now.weekday(), now.hour, len(st.session_state.queue)]])
        return pred[0]
    except: return 0

# --- AUTO-MANAGER ---
def update_system_state():
    current_time = datetime.now()
    for m_id in st.session_state.machines:
        m = st.session_state.machines[m_id]
        if m["status"] == "Busy" and m["end_time"] <= current_time:
            st.session_state.machines[m_id] = {"status": "Available", "end_time": None, "user_roll": "", "user_name": "", "duration": 0}

    for m_id in st.session_state.machines:
        if st.session_state.machines[m_id]["status"] == "Available" and len(st.session_state.queue) > 0:
            next_entry = st.session_state.queue.pop(0)
            increment_usage(next_entry["roll_no"])
            st.session_state.machines[m_id] = {
                "status": "Busy", "end_time": datetime.now() + timedelta(minutes=next_entry["duration"]),
                "user_roll": next_entry["roll_no"], "user_name": next_entry["name"], "duration": next_entry["duration"]
            }
            st.toast(f"🚀 Machine {m_id} assigned to {next_entry['name']}!", icon="🧺")

update_system_state()

# --- UI ---
st.title("🤖 TIME WASHINE!!")

with st.sidebar:
    st.header("🔒 Student Portal")
    tab_login, tab_reg = st.tabs(["Login", "Register"])
    
    with tab_reg:
        reg_roll = st.text_input("Reg Roll No", key="reg_roll")
        reg_name = st.text_input("Name", key="reg_name")
        reg_pass = st.text_input("Pass", type="password", key="reg_pass")
        if st.button("Register Account"):
            if register_user(reg_roll, reg_name, reg_pass): 
                st.toast("✅ Registered Successfully!", icon="🎉")
            else: 
                st.error("Roll No exists or Error.")
            
    with tab_login:
        l_roll = st.text_input("Login Roll No", key="log_roll")
        l_pass = st.text_input("Password", type="password", key="log_pass")
        user_info = verify_user(l_roll, l_pass) if (l_roll and l_pass) else None
        
        if l_roll and l_pass and not user_info:
            st.error("❌ Invalid Credentials")
        elif user_info:
            st.write(f"👋 **Welcome, {user_info[0]}**")
            st.metric("Semester Usage", f"{user_info[1]}/{MAX_LIMIT}")

# SECTION 1: MACHINE STATUS
st.subheader("🏢 Machine Status")
cols = st.columns(len(st.session_state.machines))
rem_times = []
for i, m_id in enumerate(st.session_state.machines):
    m_data = st.session_state.machines[m_id]
    with cols[i]:
        color = "#dc3545" if m_data['status'] == "Busy" else "#28a745"
        st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:10px; text-align:center; color:white;'><b>Machine {m_id}</b><br>{m_data['status']}<br><small>{m_data['user_name']}</small></div>", unsafe_allow_html=True)
        if m_data['status'] == "Busy":
            diff = m_data['end_time'] - datetime.now()
            secs = int(diff.total_seconds())
            if secs > 0:
                rem_times.append(secs/60)
                st.write(f"⏱️ {secs//60:02d}:{secs%60:02d}")
            else: rem_times.append(0)

st.divider()
c1, c2 = st.columns([1, 1.5])
with c1:
    st.subheader("👥 Join Queue")
    if user_info:
        if user_info[1] >= MAX_LIMIT:
            st.error(f"🚫 LIMIT REACHED. Access Blocked.")
        else:
            u_time = st.number_input("Duration (Mins)", 1, 120, 30)
            if st.button("Add to Queue"):
                st.session_state.queue.append({"roll_no": l_roll, "name": user_info[0], "duration": u_time})
                st.toast("Added to queue!", icon="📝")
                st.rerun()
    else: st.info("Login to join the queue.")

with c2:
    st.subheader("🔮 Predicted Waiting Time")
    if not st.session_state.queue: st.info("Queue is empty.")
    else:
        base = min(rem_times) if rem_times else 0
        adj = get_ml_adjustment()
        f_list = []
        cum_wait = base
        for idx, p in enumerate(st.session_state.queue):
            p_wait = cum_wait + (adj / len(st.session_state.machines))
            f_list.append({"Pos": idx+1, "Name": p["name"], "Forecast": f"{round(p_wait, 1)} mins"})
            cum_wait += (p["duration"] / len(st.session_state.machines))
        st.table(pd.DataFrame(f_list))

# SECTION 3: WARDEN PANEL
st.divider()
with st.expander("🔑 Warden Control Panel (Restricted)"):
    st.subheader("Manage Hardware")
    m_count = st.number_input("Total Machines", 1, 20, len(st.session_state.machines))
    if st.button("Update Inventory"):
        if m_count > len(st.session_state.machines):
            for i in range(len(st.session_state.machines)+1, m_count+1):
                st.session_state.machines[i] = {"status": "Available", "end_time": None, "user_roll": "", "user_name": "", "duration": 0}
        st.toast("Inventory Updated!")
        st.rerun()
    
    st.subheader("📊 User Administration")
    logs = get_all_usage()
    if logs:
        st.table(pd.DataFrame(logs, columns=["Roll No", "Name", "Total Uses"]))
        target_roll = st.text_input("Enter Roll No to Delete Account:")
        if st.button("Confirm Delete Student Account"):
            if target_roll:
                delete_user_account(target_roll)
                st.toast(f"Account {target_roll} deleted!", icon="🗑️")
                st.rerun()
    else: st.write("No users registered.")

time.sleep(1)
st.rerun()