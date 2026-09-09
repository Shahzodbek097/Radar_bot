from send_buttons import main_menu
from radar_db import db
from datetime import datetime
user_status={}
AKLAD=412_000



def start_handler(update, contex):
    update.message.reply_text(text="Radar_24 botiga xush kelibsiz!",reply_markup=main_menu())


def massage_handler(update, contex):
    # query = update.callback_query.from_user.id  # inline button uchun ishlatiladi
    user_id=update.message.from_user.id
    text=update.message.text
    if text=="Radar":
        user_status[user_id]={"step":"speed"}
        update.message.reply_text(text="Tezlikni kiriting:")
        return
    elif text=="Jarimalarni tekshirish":
        user_status[user_id]={"step":"check_car"}
        update.message.reply_text(text="Avtomobil raqamini kiriting:")
        return

    elif text=="Jarimani to'lash":
        user_status[user_id]={"step":"pay_id"}
        update.message.reply_text(text="Jarima ID ni kiriting:")
        return
    elif text=="Admin":
        rows=db.get_all_jarima()
        if not rows:
            update.message.reply_text(text="Jarima yo'q")
        else:
            msg="To'lanmagan jarimalar:\n"
            for r in rows:
                msg+=f"\nID:{r[0]} | {r[1]} | {r[3] } so'm"
            update.message.reply_text(msg)
        return

    if user_id not in user_status:
        update.message.reply_text(text="Menyuni tanlang", reply_markup=main_menu())
        return
    state=user_status[user_id]

    if state["step"]=="speed":
        # user_status[user_id]["step"]=="speed"
        if not text.isdigit():
            update.message.reply_text("Faqat son kiriting")
            return
        state["speed"]=int(text)
        state["step"]="car"
        update.message.reply_text("Avtomobil raqamini kiriting")
    elif state["step"]=="car":
        car=text.upper()
        speed=state["speed"]
        jarima=0
        if 65<speed <=85:
            jarima=AKLAD
        elif 85<speed<=100:
            jarima=AKLAD*5
        elif speed>100:
            jarima=10*AKLAD
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if jarima>0:
            db.add_radar(car,speed,jarima,time)
            update.message.reply_text(f"{car} ga mashinaga {jarima} so'm jarima yozildi")
        else:
            update.message.reply_text("Jarima yozilmadi")

        user_status.pop(user_id,None)
        update.message.reply_text(text="Menyuni tanlang", reply_markup=main_menu())

    # 08.07.2026 Zoom Meeting
    elif state["step"]=="check_car":
        rows=db.get_car_number(text.upper())
        if not rows:
            update.message.reply_text("Jarima topilmadi")
        else:
            msg="Jarimalar:\n"
            for r in rows:
                msg+=f"\n ID:{r[0]}\nRaqam{r[1]}\nTezlik:{r[2]}\nSumma:{r[3]}\nVaqt:{r[4]}"
            update.message.reply_text(msg)

        user_status.pop(user_id, None)
        update.message.reply_text(text="Menyuni tanlang", reply_markup=main_menu())

    elif state["step"] == "pay_id":
        if not text.isdigit():
            update.message.reply_text("ID raqamdan iborat bo'lsin")
            return
        jarima_id=int(text)
        rows=db.pay_by_id(jarima_id)
        if not rows or rows[3]==0:
            update.message.reply_text("Jarima mavjud emas yoki to'langan")
            user_status.pop(user_id, None)
            update.message.reply_text(text="Menyuni tanlang", reply_markup=main_menu())
        else:
            state["jarima_id"]=jarima_id
            state["summa"]=rows[3]
            state["step"] = "pay_sum"
            update.message.reply_text(f"Jarima:{rows[3]} so'm to'lov kiriting: ")

    elif state["step"] == "pay_sum":
        if not text.isdigit():
            update.message.reply_text("raqamdan iborat bo'lsin")
            return
        tulov=int(text)
        if tulov==state["summa"]:
            db.set_jarima(state["jarima_id"],0)
            update.message.reply_text("Jarima to'liq to'landi")
        elif tulov>state["summa"] or tulov<0:
            update.message.reply_text(f"Maksimal to'lov {state['summa']} so'm")
        else:
            qoldiq=state["summa"]-tulov
            update.message.reply_text(f"Jarima qisman to'landi. Qoldiq {qoldiq}")
            db.set_jarima(state["jarima_id"], qoldiq)

        user_status.pop(user_id, None)
        update.message.reply_text(text="Menyuni tanlang", reply_markup=main_menu())







































