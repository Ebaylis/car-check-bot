import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7723553290:AAG_N-Fmt34I-wiNWpBpkmdGc8DV5n_Pdus"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a car registration number to check.")

async def check_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reg_plate = update.message.text.strip().replace(' ', '').upper()
    result = fetch_car_details(reg_plate)
    await update.message.reply_text(result, parse_mode="Markdown")

def fetch_car_details(reg_plate):
    try:
        url = f"https://cartaxcheck.co.uk/free-car-check/?vrm={reg_plate}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Scrape the important fields
        car_make = soup.find("span", string="Make").find_next_sibling("span").string
        car_model = soup.find("span", text="Model").find_next_sibling("span").text
        year = soup.find("span", text="Year of manufacture").find_next_sibling("span").text
        tax_status = soup.find("span", text="Tax Status").find_next_sibling("span").text
        mot_status = soup.find("span", text="MOT Status").find_next_sibling("span").text
        insurance = soup.find("span", text="Insurance Status").find_next_sibling("span").text

        result = (
            f"🚗 *Car Details:*\n\n"
            f"*Make:* {car_make}\n"
            f"*Model:* {car_model}\n"
            f"*Year:* {year}\n"
            f"*Tax Status:* {tax_status}\n"
            f"*MOT Status:* {mot_status}\n"
            f"*Insurance Status:* {insurance}"
        )
        return result
    except Exception as e:
        return "❗ Could not fetch car details. Please check the reg number."

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_registration))

app.run_polling()
