import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")  # Thay thế bằng token của bạn

async def get_results():
    results_url = os.getenv("RESULT_URL")
    date_url = os.getenv("DATE_URL")

    try:
        results_response = requests.get(results_url)
        date_response = requests.get(date_url)

        if results_response.status_code == 200 and date_response.status_code == 200:
            results = results_response.json()
            date = date_response.text.strip().replace('"','')
            match = " ".join(date.split()[1:])  # Lấy phần sau "XSMB"

            message = "📅 <b>Kết quả xổ số ngày "+match+"</b>\n\n"
            message += "<pre>\n"
            message += "┌──────┬───────────────────────────┐\n"
            message += "│ Giải │ Số trúng                  │\n"
            message += "├──────┼───────────────────────────┤\n"
            
            for prize, numbers in results.items():
                formatted_numbers = ', '.join(numbers)
                message += f"│ {prize:<4} │ {formatted_numbers:<25} │\n"
            
            message += "└──────┴───────────────────────────┘\n"
            message += "</pre>"
            return message

        else:
            return "Không thể lấy dữ liệu, vui lòng thử lại sau."
    except Exception as e:
        return f"Lỗi khi lấy dữ liệu: {e}"

async def results_command(update: Update, context: CallbackContext) -> None:
    waiting_message = await update.message.reply_text("⏳ Đang lấy kết quả...")
    message = await get_results()
    await waiting_message.delete()
    await update.message.reply_text(text=message, parse_mode="HTML")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("results", results_command))

    print("Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
