import os
import csv


class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, folder_path=''):
        loaded_count = 0
        for filename in os.listdir(folder_path):
            if 'price' in filename.lower() and filename.endswith('.csv'):
                file_path = os.path.join(folder_path, filename)
                print(f'Загружаем файл: {file_path}')

                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=',')  # Используем запятую как разделитель
                    headers = next(reader)  # Пропустить заголовки

                    # Получить индексы нужных столбцов
                    product_idx, price_idx, weight_idx = self._search_product_price_weight(headers)

                    for row in reader:
                        product = row[product_idx].strip()  # Убираем лишние пробелы
                        price = row[price_idx].strip()
                        weight = row[weight_idx].strip()

                        # Преобразуем цену и вес в числовой формат и округляем до целого
                        try:
                            price = round(float(price.replace(',', '.')))  # Округляем до целого числа
                            weight = round(float(weight.replace(',', '.')))  # Округляем до целого числа
                        except ValueError:
                            print(f'Ошибка при преобразовании данных: {row}')
                            continue  # Пропустить строки с ошибками

                        # Рассчитываем цену за кг, округляя до 2 знаков после запятой
                        price_per_kg = round(price / weight, 2) if weight > 0 else float('inf')

                        # Добавить в список
                        self.data.append({
                            'product': product,
                            'price': price,
                            'weight': weight,
                            'file': filename,
                            'price_per_kg': price_per_kg
                        })

                        loaded_count += 1

        return loaded_count

    def _search_product_price_weight(self, headers):
        product_idx = -1
        price_idx = -1
        weight_idx = -1

        # Поиск столбцов
        for idx, header in enumerate(headers):
            header = header.lower()
            if any(word in header for word in ['название', 'продукт', 'товар', 'наименование']):
                product_idx = idx
            elif any(word in header for word in ['цена', 'розница']):
                price_idx = idx
            elif any(word in header for word in ['фасовка', 'масса', 'вес']):
                weight_idx = idx

        return product_idx, price_idx, weight_idx

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for idx, item in enumerate(self.data, 1):
            result += f'''
                <tr>
                    <td>{idx}</td>
                    <td>{item['product']}</td>
                    <td>{item['price']}</td>
                    <td>{item['weight']}</td>
                    <td>{item['file']}</td>
                    <td>{item['price_per_kg']}</td>
                </tr>
            '''

        result += '''
            </table>
        </body>
        </html>
        '''
        with open(fname, 'w', encoding='utf-8') as file:
            file.write(result)

    def find_text(self, text):
        # Поиск позиций по фрагменту текста
        return [item for item in self.data if text.lower() in item['product'].lower()]


def main():
    pm = PriceMachine()
    folder_path = r'C:\Users\Administrator\PycharmProjects\pythonProject9\pricelists'  # Укажите путь к папке с файлами
    loaded_count = pm.load_prices(folder_path)
    print(f'Загружено {loaded_count} позиций.')

    # Интерфейс для поиска товара
    while True:
        search_text = input('Введите текст для поиска (или "exit" для завершения): ')
        if search_text.lower() == 'exit':
            print('Работа завершена.')
            break

        found_items = pm.find_text(search_text)
        if not found_items:
            print('Товары не найдены.')
        else:
            # Вывод найденных позиций
            print(f'Найдено {len(found_items)} позиций:')
            print(f'№   Наименование               Цена   Вес   Файл   Цена за кг.')
            for idx, item in enumerate(found_items, 1):
                print(
                    f'{idx}   {item["product"]:<25} {item["price"]:<6} {item["weight"]:<5} {item["file"]:<15} {item["price_per_kg"]}')

    # Экспорт в HTML
    pm.export_to_html()


if __name__ == '__main__':
    main()
