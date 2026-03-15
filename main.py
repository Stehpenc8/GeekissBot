import asyncio 
import logging 

from aiogram import Dispatcher, Bot, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import LinkPreviewOptions
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config_reader import config


logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_prefer_large_media=True
    )
    )
dp = Dispatcher()


@dp.message(F.text, Command('start')) 
async def cmd_start(message: types.Message):
    await message.answer(
        'This code with HTML parse mode',
        parse_mode=None
        )
    

@dp.message(F.text, Command('test'))
async def cmd_test(message: types.Message):
    await message.answer('This code without <s>HTML parse_mode</s>')


@dp.message(Command('hello'))
async def cmd_hello(message: types.Message):
    await message.answer(
        f'Hello <b>{message.from_user.full_name}</b>',
        parse_mode=ParseMode.HTML 
    )


@dp.message(Command("say_hello"))
async def cmd_say_hello(
    message: types.Message,
    command: CommandObject
):
    await message.answer(command.args)


@dp.message(Command("links"))
async def cmd_links(message: types.Message):
    links_text = (
        "https://music.yandex.ru/album/33611143"
        "\n"
        "https://www.twitch.tv/anarabdullaev"
    )
    # options1 = LinkPreviewOptions(is_disabled=True)
    await message.answer(
        f'Нет превью {links_text}',
        # link_preview_options=options1
        )
    # options2 = LinkPreviewOptions(
    #     url="https://music.yandex.ru/album/33611143",
    #     prefer_small_media=True
    #     # prefer_large_media=True
    #     # show_above_text=True
    # )
    # await message.answer(
    #     f"Маленькое превью:\n",
    #     link_preview_options=options2
    # )


@dp.message(F.new_chat_members)
async def smb_added(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Привет, {user.full_name}")

# keyboards
# default
# first version
@dp.message(F.text.lower() == 'lets go fuck')
async def fuck_or_not(message: types.Message):
    kb = [
        [
        types.KeyboardButton(text='go'),
        types.KeyboardButton(text='if with olya no no no')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Enter what do you wana do: '
        )
    await message.answer('Do you want?))', reply_markup=keyboard)


@dp.message(F.text.lower() == 'go')
async def go(messge: types.Message):
    await messge.reply('Ahhhh', reply_markup=types.ReplyKeyboardRemove)

# second version
@dp.message(Command('iwanastillyourdata'))
async def iwsyd(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(2)
    await message.answer(
        'Choose number:',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


# special buttons 
@dp.message(Command('special_buttons'))
async def special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Send your geolocation', request_location=True),
        types.KeyboardButton(text='Send your contact', request_contact=True)
    )
    builder.row(
        types.KeyboardButton(
            text='Create poll',
            request_poll=types.KeyboardButtonPollType(type='quiz')
        )
    )
    # builder.row(
    #     types.KeyboardButton(
    #         text='Choose premium user',
    #         request_user=types.KeyboardButtonRequestUser(
    #             request_id=1,
    #             user_is_premium=True
    #         )
    #     ),
    #     types.KeyboardButton(
    #         text='Choose supergroup with forum',
    #         request_chat=types.KeyboardButtonRequestChat(
    #         request=2,
    #         chat_is_channel=False,
    #         chat_is_forum=True
    #         )
    #     )
    # )
    await message.answer(
        'Choose action:',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())