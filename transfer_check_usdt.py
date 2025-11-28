import requests
from web3 import Web3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ================================
# CONFIGURAÇÕES
# ================================

TELEGRAM_TOKEN = "8445853763:AAFvENSmBsxwJgsUclQMA8UXLtyjbZNvGDU"
CHAT_IDS = ["375132125", "5416461659"]

#Troque pelo seu INFURA
INFURA_URL = "https://polygon-mainnet.infura.io/v3/000"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Wallets e chaves privadas
PRIVATE_KEY = "000"
wallet_origem = w3.to_checksum_address("0x...")

PRIVATE_KEY_SA = 'a6c4b38c3c7f612b0e6bf6a393ecf9bc6ad9e7072ddb30c2a7b3f7dc2773d01c'
wallet_origem_sa = w3.to_checksum_address("0x...")

PRIVATE_KEY_INVEST = "000"
wallet_origem_invest = w3.to_checksum_address("0x...")

PRIVATE_KEY_CUSTOS = "000"
wallet_origem_custos = w3.to_checksum_address("0x...")

wallet_destino = w3.to_checksum_address("0x...")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

USDT_CONTRACT = w3.to_checksum_address("0xc2132D05D31c914a87C6611C10748AEb04B58e8F")

ABI_ERC20 = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
]

usdt_contract = w3.eth.contract(address=USDT_CONTRACT, abi=ABI_ERC20)

# ================================
# FUNÇÕES AUXILIARES
# ================================

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        try:
            requests.post(
                f"{TELEGRAM_API_URL}sendMessage",
                data={"chat_id": chat_id, "text": message},
            )
        except:
            pass


def conectar_w3():
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    if not w3.is_connected():
        raise Exception("❌ Não conectou ao RPC Infura.")
    return w3


def transfer_usdt(valor, origem, private_key):
    try:
        w3 = conectar_w3()
        contract = w3.eth.contract(address=USDT_CONTRACT, abi=ABI_ERC20)

        amount_wei = int(valor * 10**6)
        nonce = w3.eth.get_transaction_count(origem, "pending")

        gas_estimate = contract.functions.transfer(wallet_destino, amount_wei).estimate_gas(
            {"from": origem}
        )
        gas_limit = int(gas_estimate * 1.2)

        tx = contract.functions.transfer(wallet_destino, amount_wei).build_transaction(
            {
                "chainId": 137,
                "gas": gas_limit,
                "gasPrice": w3.eth.gas_price,
                "nonce": nonce,
            }
        )

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        return f"✅ USDT enviado!\n🔗 HASH: {w3.to_hex(tx_hash)}"

    except Exception as e:
        return f"❌ ERRO transferência: {e}"


def get_balances():
    w3 = conectar_w3()
    contract = w3.eth.contract(address=USDT_CONTRACT, abi=ABI_ERC20)

    wallets = {
        "origem": wallet_origem,
        "sa": wallet_origem_sa,
        "invest": wallet_origem_invest,
        "custos": wallet_origem_custos,
    }

    saldos = {}
    for nome, w in wallets.items():
        bal_raw = contract.functions.balanceOf(w).call()
        saldos[nome] = bal_raw / 10**6

    return saldos


# ================================
# COMANDOS
# ================================

async def cmd_ro(update: Update, context):
    chat = str(update.effective_chat.id)
    if chat not in CHAT_IDS:
        return await update.message.reply_text("❌ Sem permissão.")

    try:
        valor = float(update.message.text.split()[1])
        saldos = get_balances()

        if saldos["origem"] < valor:
            return await update.message.reply_text(
                f"❌ Saldo insuficiente. Saldo: {saldos['origem']} USDT"
            )

        await update.message.reply_text("⏳ Enviando...")
        resp = transfer_usdt(valor, wallet_origem, PRIVATE_KEY)
        await update.message.reply_text(resp)

    except Exception as e:
        await update.message.reply_text(f"❌ ERRO: {e}")


async def cmd_sa(update: Update, context):
    chat = str(update.effective_chat.id)
    if chat not in CHAT_IDS:
        return await update.message.reply_text("❌ Sem permissão.")

    try:
        valor = float(update.message.text.split()[1])
        saldos = get_balances()

        if saldos["sa"] < valor:
            return await update.message.reply_text(
                f"❌ Saldo insuficiente. Saldo: {saldos['sa']} USDT"
            )

        await update.message.reply_text("⏳ Enviando...")
        resp = transfer_usdt(valor, wallet_origem_sa, PRIVATE_KEY_SA)
        await update.message.reply_text(resp)

    except Exception as e:
        await update.message.reply_text(f"❌ ERRO: {e}")


async def cmd_invest(update: Update, context):
    chat = str(update.effective_chat.id)
    if chat not in CHAT_IDS:
        return await update.message.reply_text("❌ Sem permissão.")

    try:
        valor = float(update.message.text.split()[1])
        saldos = get_balances()

        if saldos["invest"] < valor:
            return await update.message.reply_text(
                f"❌ Saldo insuficiente. Saldo: {saldos['invest']} USDT"
            )

        await update.message.reply_text("⏳ Enviando...")
        resp = transfer_usdt(valor, wallet_origem_invest, PRIVATE_KEY_INVEST)
        await update.message.reply_text(resp)

    except Exception as e:
        await update.message.reply_text(f"❌ ERRO: {e}")


async def cmd_custos(update: Update, context):
    chat = str(update.effective_chat.id)
    if chat not in CHAT_IDS:
        return await update.message.reply_text("❌ Sem permissão.")

    try:
        valor = float(update.message.text.split()[1])
        saldos = get_balances()

        if saldos["custos"] < valor:
            return await update.message.reply_text(
                f"❌ Saldo insuficiente. Saldo: {saldos['custos']} USDT"
            )

        await update.message.reply_text("⏳ Enviando...")
        resp = transfer_usdt(valor, wallet_origem_custos, PRIVATE_KEY_CUSTOS)
        await update.message.reply_text(resp)

    except Exception as e:
        await update.message.reply_text(f"❌ ERRO: {e}")


async def cmd_balance(update: Update, context):
    saldos = get_balances()

    msg = (
        "💰 *Saldos atuais:*\n"
        f"• Ro: {saldos['origem']:.2f}\n"
        f"• Sa: {saldos['sa']:.2f}\n"
        f"• Invest: {saldos['invest']:.2f}\n"
        f"• Custos: {saldos['custos']:.2f}"
    )

    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_help(update: Update, context):
    await update.message.reply_text(
        "📌 Comandos:\n"
        "/ro <valor>\n"
        "/sa <valor>\n"
        "/invest <valor>\n"
        "/custos <valor>\n"
        "/balance\n"
        "/help"
    )


# ================================
# MAIN
# ================================

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("ro", cmd_ro))
    app.add_handler(CommandHandler("sa", cmd_sa))
    app.add_handler(CommandHandler("invest", cmd_invest))
    app.add_handler(CommandHandler("custos", cmd_custos))
    app.add_handler(CommandHandler("balance", cmd_balance))
    app.add_handler(CommandHandler("help", cmd_help))

    print("🚀 Bot ativo...")
    app.run_polling()


if __name__ == "__main__":
    main()
