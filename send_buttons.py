from telegram import ReplyKeyboardMarkup
# from telegram import InlineKeyboardMarkup, InlineKeyboardButton  # inline keybord ishlatilganda
# from telegram.ext import CallbackQueryHandler                    # inline keybord ishlatilganda



def main_menu():
    keyboard=[
        [("Radar"),("Jarimalarni tekshirish")],
        [("Jarimani to'lash"), ("Admin")]
    ]
    return ReplyKeyboardMarkup (keyboard, resize_keyboard=True, one_time_keyboard=False )

# def main_menu():
#     keyboard=[[
#         InlineKeyboardButton("Radar", callback_data="radar"),
#         InlineKeyboardButton("Jarimalarni tekshirish", callback_data="check_fine")
#     ],
#         [
#             InlineKeyboardButton("Jarimani to'lash", callback_data="pay_fine"),
#             InlineKeyboardButton("Admin", callback_data="admin")
#         ]
#     ]
#     return InlineKeyboardMarkup (keyboard)