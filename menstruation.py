import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


class CycleTrackerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Исправлен текст подсказки - убран некорректный символ "/"
        self.start_date_input = TextInput(
            hint_text='Введите дату начала (ДД.ММ.ГГГГ или "сегодня")\n'
                      'Enter start date (DD.MM.YYYY or "today")',
            multiline=False
        )
        self.cycle_length_input = TextInput(
            hint_text='Введите длину цикла (по умолчанию 28)\n'
                      'Enter the cycle length (default 28)',
            multiline=False
        )
        self.calculate_button = Button(text='Рассчитать/Calculate', on_press=self.calculate_cycle)

        self.layout.add_widget(self.start_date_input)
        self.layout.add_widget(self.cycle_length_input)
        self.layout.add_widget(self.calculate_button)

        return self.layout

    def calculate_cycle(self, instance):
        start_date_str = self.start_date_input.text.strip().lower()
        cycle_length_str = self.cycle_length_input.text.strip()

        # Исправлена проверка на "сегодня"/"today"
        if start_date_str in ["сегодня", "today"]:
            start_date = datetime.datetime.now()
        else:
            try:
                day, month, year = map(int, start_date_str.split('.'))
                start_date = datetime.datetime(year, month, day)
                if start_date > datetime.datetime.now():
                    self.show_popup(
                        "Ошибка/Error",
                        "Дата не может быть в будущем.\n"
                        "Date cannot be in the future."
                    )
                    return
            except ValueError:
                self.show_popup(
                    "Ошибка/Error",
                    "Некорректная дата. Пожалуйста, попробуйте снова.\n"
                    "Incorrect date. Please try again."
                )
                return

        # Проверка на пустое значение и конвертация в число
        try:
            cycle_length = int(cycle_length_str) if cycle_length_str else 28
            if not (21 <= cycle_length <= 35):
                self.show_popup(
                    "Ошибка/Error",
                    "Длина цикла должна быть между 21 и 35 днями.\n"
                    "Cycle length must be between 21 and 35 days."
                )
                return
        except ValueError:
            self.show_popup(
                "Ошибка/Error",
                "Некорректная длина цикла. Пожалуйста, введите число.\n"
                "Invalid cycle length. Please enter a number."
            )
            return

        # Расчет дат цикла
        cycle_dates = self.calculate_cycle_dates(start_date, cycle_length)
        result_text = self.format_results(cycle_dates)
        self.show_results_popup(result_text)

    def calculate_cycle_dates(self, start_date, cycle_length):
        dates = {
            'Начало цикла/Beginning of the cycle': start_date,
            'Конец цикла/End of the cycle': start_date + datetime.timedelta(days=cycle_length - 1),
            'Овуляция/Ovulation': start_date + datetime.timedelta(days=(cycle_length // 2) - 1)
            # Исправлен расчет овуляции
        }

        # Расчет для следующих циклов
        for i in range(1, 4):
            next_start = start_date + datetime.timedelta(days=i * cycle_length)
            dates[f'Начало цикла {i}/Beginning of the cycle {i}'] = next_start
            dates[f'Конец цикла {i}/End of the cycle {i}'] = next_start + datetime.timedelta(days=cycle_length - 1)
            dates[f'Овуляция {i}/Ovulation {i}'] = next_start + datetime.timedelta(days=(cycle_length // 2) - 1)

        return dates

    def format_results(self, cycle_dates):
        result_text = "Ключевые даты вашего менструального цикла:\n"
        result_text += "Key dates in your menstrual cycle:\n\n"

        for key, date in cycle_dates.items():
            result_text += f"{key}: {date.strftime('%d.%m.%Y')}\n"

        suggestions = self.suggest_conception_dates(cycle_dates)
        result_text += "\nРекомендации по занятиям любовью с целью зачатия:\n"
        result_text += "Recommendations for making love for the purpose of conception:\n\n"

        for ovulation_date, fertile_days in suggestions:
            result_text += (
                f"Наиболее благоприятные дни для зачатия/\n"
                f"The most favorable days for conception:\n"
                f"{', '.join(fertile_days)}\n"
                f"(овуляция/ovulation: {ovulation_date})\n\n"
            )

        return result_text

    def suggest_conception_dates(self, cycle_dates):
        suggestions = []

        for i in range(4):
            ovulation_key = 'Овуляция/Ovulation' if i == 0 else f'Овуляция {i}/Ovulation {i}'
            ovulation_date = cycle_dates.get(ovulation_key)

            if ovulation_date:
                fertile_days = [
                    (ovulation_date - datetime.timedelta(days=2)).strftime('%d.%m.%Y'),
                    (ovulation_date - datetime.timedelta(days=1)).strftime('%d.%m.%Y'),
                    ovulation_date.strftime('%d.%m.%Y'),
                    (ovulation_date + datetime.timedelta(days=1)).strftime('%d.%m.%Y'),
                ]
                suggestions.append((ovulation_date.strftime('%d.%m.%Y'), fertile_days))

        return suggestions

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text=message, halign='center')
        popup_label.bind(size=lambda *_: setattr(popup_label, 'text_size', (popup_label.width, None)))

        close_button = Button(
            text='Закрыть/Close',
            size_hint_y=0.2,
            on_press=lambda x: popup.dismiss()
        )

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup.open()

    def show_results_popup(self, result_text):
        popup_layout = BoxLayout(orientation='vertical', padding=10)

        scroll_view = ScrollView(size_hint=(1, 0.8))
        result_label = Label(
            text=result_text,
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True
        )

        # Правильная настройка размеров и привязок для текста
        result_label.bind(
            width=lambda *x: setattr(result_label, 'text_size', (result_label.width, None)),
            texture_size=lambda *x: setattr(result_label, 'height', result_label.texture_size[1])
        )

        scroll_view.add_widget(result_label)
        close_button = Button(
            text='Закрыть/Close',
            size_hint=(1, 0.2),
            on_press=lambda x: popup.dismiss()
        )

        popup_layout.add_widget(scroll_view)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Результаты расчета/Calculation results",
            content=popup_layout,
            size_hint=(0.8, 0.8)  # Увеличен размер popup для лучшей читаемости
        )
        popup.open()


if __name__ == "__main__":
    CycleTrackerApp().run()