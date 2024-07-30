import csv

#import pandas as pd
from web3 import Web3

connection = Web3()


def get_private_key(seed):
    connection.eth.account.enable_unaudited_hdwallet_features()
    account = connection.eth.account.from_mnemonic(seed, account_path=f"m/44'/60'/0'/0/0")
    address = account.address
    private_key = account.key.hex()
    return private_key, address


# Функция для чтения файла с разными кодировками
def read_file_with_different_encodings(filename):
    encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'latin1']
    for encoding in encodings:
        try:
            with open(filename, 'rb') as file:
                content = file.read()
                return content.decode(encoding).splitlines()
        except (UnicodeDecodeError, LookupError):
            continue
    raise UnicodeDecodeError("None of the attempted encodings worked.")


# Считываем seed-фразы из файла seeds.txt
try:
    seed_phrases = read_file_with_different_encodings('seeds.txt')
except UnicodeDecodeError:
    print("Ошибка: Файл seeds.txt не может быть прочитан ни в одной из попыток кодировки. Попробуйте другой файл.")
    exit(1)

# Удаляем лишние пробелы и переводы строк
seed_phrases = [seed.strip() for seed in seed_phrases]

# Подготавливаем данные для записи в CSV
data = []
for seed in seed_phrases:
    try:
        private_key, public_address = get_private_key(seed)
        data.append([seed, private_key, public_address])
    except Exception as e:
        print(f"Error processing seed: {seed}, error: {e}")

# Создаем DataFrame
# df = pd.DataFrame(data, columns=["Seed-фраза", "Приватный ключ", "Публичный адрес"])
# df.to_csv('private_keys.csv', index=False, encoding='utf-8')

# Results
with open("private_keys.csv", "w", encoding="utf-8", newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["Seed-фраза", "Приватный ключ", "Публичный адрес"])
    csv_writer.writerows(data)

print("Processing completed. Check the file private_keys.csv for results.")