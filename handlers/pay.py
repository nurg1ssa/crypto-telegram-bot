from aiogram import Bot

from aiogram.types import Message, LabeledPrice

PAYMENTS_TOKEN = '1877036958:TEST:c8820583d0e309a9f7d5e13aab823c00d0600c9c'

PRICE = LabeledPrice(label="Donation", amount=1*100)

async def donate(message: Message, bot: Bot):
    await message.answer("Thank you for deciding to support the bot! 💖")
    await bot.send_invoice(message.chat.id,
                           title="Support to the bot",
                           description=f"Thank you for supporting the bot! Your donation will contribute to the continuous development and deployment.",
                           provider_token=PAYMENTS_TOKEN,
                           currency="usd",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="donation",
                           payload="donation-payload")
    