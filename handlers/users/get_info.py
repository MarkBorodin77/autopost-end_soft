from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import return_menu_keyboard
from loader import dp


@dp.callback_query_handler(lambda c: c.data == "get_info")
async def get_info(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(f"""<b>🏝 Инфо о проекте</b>\n\n<b>Владелец:</b> @RSHOP_ROBOT\n<b>Кодер:</b> @RSHOP_ROBOT\n\nУдачного использования!""", reply_markup=return_menu_keyboard)
