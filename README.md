# Bot de Transferência USDT (Polygon)

Bot em Python para automação de transferências USDT via contrato ERC20 na Polygon, com integração ao Telegram.

## 🚀 Funcionalidades
- Envio de USDT de múltiplas wallets
- Consulta de saldo
- Proteção por lista de CHAT_IDS autorizados
- RPC via Infura
- Notificações automáticas no Telegram
- Com comandos do tipo "/ro 10" o bot envia o comando para a rede infura que por sua vez solicita o envio na blockchain Polygon o valor de 10 USDt da wallet de origem para a wallet de destino pré configurada no código em Python. O comando /balace exibe o saldo de todas as wallet pre-configuradas. Basta alterar para sua wallet para obter o resultado. Outros comandos podem ser adicionados no código .py

## 📦 Instalação

```bash
git clone https://github.com/SEU_USUARIO/meu-bot-usdt.git  
cd meu-bot-usdt
pip install -r requirements.txt
