# Импорт нужных библиотек.
import requests
import json
from bs4 import BeautifulSoup


# Ссылка на общий сайт(В моём случае с квартирами. А так можно использовать любую страничку с товарами, обязательно на авито!).
main_link = "https://www.avito.ru/kursk/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_wEgAN__YToxOntzOjg6ImZyb21QYWdlIjtzOjQ6Im1haW4iO33DmpuUIAAAAA"


def reponse_site():
    """
    Получение всей страницы, полностью с html тегами и т.д.!
    """

    # Создание всей страницы в виде текста html.
    reponse = requests.get(main_link).text

    return reponse


def new_file_site(reponse: str):
    """
    Создание файла под сайт, чтобы не делать много запросов. \n
    И чтобы эти многочисленные запросы никто не блочил.
    """

    # Создание файла в определённом месте, под запись, с кодировкой "UTF-8"(обязательно указывать для html).
    with open(
        "AvitoSiteInFile.html",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(reponse)


def replace_reponse():
    """
    Замена запроса сайта на файл сайта.
    """

    # Создание файла в определённом месте, под запись, с кодировкой "UTF-8"(обязательно указывать для html).
    with open(
        "AvitoSiteInFile.html",
        "r",
        encoding="utf-8",
    ) as file:
        reponse = file.read()

    return reponse


# Объект библиотеки для поиска на страницы.
main_soup = BeautifulSoup(replace_reponse(), "lxml")


def heading(soup):
    # Получение массива с заголовками и с тегами html.
    heading = soup.find_all("h3")
    heading_list = []  # Создание чистого листа заголовков.

    for i in heading:
        heading_list.append(i.text)

    return heading_list


def price(soup):
    price = soup.find_all("span", class_="price-root-IfnJI")
    price_list = []

    for i in price:
        price_list.append(
            f"{i.find("span").text} // {i.find("p",
                          class_="styles-module-root-s4tZ2 styles-module-size_s-nEvE8 styles-module-size_s-PDQal stylesMarningNormal-module-root-_xKyG stylesMarningNormal-module-paragraph-s-HX94M styles-module-noAccent-XIvJm").text}"
        )

    return price_list


def address(soup):
    address = soup.find_all("div", class_="geo-root-NrkbV")
    address_list = []

    for i in address:
        address_list.append(i.text)

    return address_list


def date(soup):
    date = soup.find_all("div", class_="iva-item-dateInfoStep-qcDJA")
    date_list = []
    return_date_list = []

    for i in date:
        date_list.append(i.text)

    for i in date_list:
        if i == "" or i == " " or i == None:
            return_date_list.append("[ДАННЫЕ УДАЛЕНЫ]")
        else:
            return_date_list.append(i)

    return return_date_list


def link_post(soup):
    link = soup.find_all("div", class_="iva-item-title-CdRXl")
    link_list = []

    for i in link:
        for j in i.find_all("a"):
            link_list.append(j.get("href"))

    return link_list


def new_file_txt(
    name: str,
    heading_list: list,
    price_list: list,
    address_list: list,
    date_list: list,
    link_list: list,
):
    """
    Создание итогового файла со всеми данными.
    """

    # Создание файла в определённом месте, под запись, с кодировкой "UTF-8".
    with open(
        f"{name}.txt",
        "w",
        encoding="utf-8",
    ) as file:
        # Через цикл получаем файл с данными по разным строкам благодаря "\n".
        for i in range(
            len(heading_list)
            and len(price_list)
            and len(address_list)
            and len(date_list)
            and len(link_list)
        ):
            file.writelines(
                f"""
Квартира номер {i + 1}:
    Заголовок: {heading_list[i]}
    Цена: {price_list[i]}.
    Адрес: {address_list[i]}.
    Выложено: {date_list[i] if i < len(date_list) else "[ДАННЫЕ УДАЛЕНЫ]"}.
    Ссылка на пост: https://www.avito.ru{link_list[i]}
"""
            )


def new_file_json(
    name: str,
    heading_list: list,
    price_list: list,
    address_list: list,
    date_list: list,
    link_list: list,
):
    """
    Создание итогового файла со всеми данными, но в формате json.
    """

    # Создание словаря для передачи в файл в формате json.
    py_json = dict()

    # Заполнение словаря данными.
    for i in range(
        len(heading_list)
        and len(price_list)
        and len(address_list)
        and len(date_list)
        and len(link_list)
    ):
        py_json[f"Квартира номер {i + 1}"] = {
            "Заголовок": heading_list[i],
            "Цена": price_list[i],
            "Адрес": address_list[i],
            "Выложено": date_list[i] if i < len(date_list) else "[ДАННЫЕ УДАЛЕНЫ]",
            "Ссылка на пост": f"https://www.avito.ru{link_list[i]}",
        }

    # Создание файла json и внесение данных со словаря в него.
    with open(f"{name}.json", "w", encoding="utf-8") as json_file:
        # ensure_ascii=False - нормально отображает русские символы. indent=4 - отступы в 4 пробела.
        json.dump(py_json, json_file, indent=4, ensure_ascii=False)


def print_all():
    """
    Распечатать всё в консоль. \n
    Отладка.
    """

    # print("Заголовки: \n")
    # print(heading(main_soup))
    # print("Цены: \n")
    # print(price(main_soup))
    # print("Адрес: \n")
    # print(address(main_soup))

    pass


def main():
    # Запустить один раз:
    # reponse_site()  # Запрос сайта на отдачу html файла.

    # Cоздание html файла сайта прямо на пк(чтобы не блокало).
    # new_file_site(reponse_site())

    # Создание файла с паршенными данными.
    new_file_txt(
        "ParserOutput",
        heading(main_soup),
        price(main_soup),
        address(main_soup),
        date(main_soup),
        link_post(main_soup),
    )

    # Создание файла с паршенными данными. Только в формате json.
    new_file_json(
        "ParserOutput",
        heading(main_soup),
        price(main_soup),
        address(main_soup),
        date(main_soup),
        link_post(main_soup),
    )

    # print_all() # режим отладки


if __name__ == "__main__":
    main()
