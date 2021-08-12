from datetime import datetime
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton, MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.storage.jsonstore import JsonStore
main_data = JsonStore('main.json')
stored_data = JsonStore('storage.json')
amount_data = JsonStore('amount.json')




def rgba(r, g, b, a):
    return r / 255.0, g / 255.0, b / 255.0, a


# --------------------------------------------------------------------- #


pattern_list = [[], 1]

# pattern_list[0] - это упражнения
# pattern_list[1] - это кол-во подходов (по дефолту 1)


# --------------------------------------------------------------------- #


# --------------------------------------------------------------------- #


main_list = []

# main_list[0] - это одна тренировка
# main_list[0][0] - это время и дата
# main_list[0][1] - это название (тренировка №)
# main_list[0][2] - это инфа про саму тренировку
# main_list[0][2][0] - это список упражнений
# main_list[0][2][1] - это кол-во подходов
# main_list[0][2][2] - это список рез-ов


# --------------------------------------------------------------------- #


if stored_data.exists('pattern'):
    pattern_list = stored_data.get('pattern')['text']


class JournalApp(MDApp):
    def __init__(self):
        super(JournalApp, self).__init__()

        self.main_screen = Screen(name='main')

        self.create_pattern_box = MDBoxLayout(orientation='vertical',
                                              pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                              size_hint=(1, 0.4))

        self.create_res_box = MDBoxLayout(pos_hint={'center_x': 0.5, 'center_y': 0.5}, adaptive_width=True)

        main_toolbar = MDToolbar(title="Дневник тренировок", pos_hint={'top': 1}, md_bg_color=rgba(193, 0, 255, 1))
        main_toolbar.right_action_items = [["dots-vertical", lambda x: self.menu_callback(x)]]

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Новый шаблон",
                "height": 50,
                "on_release": self.new_pattern
            }
        ]
        self.menu = MDDropdownMenu(items=menu_items, width_mult=3)

        self.main_screen.add_widget(main_toolbar)

        # ---------------------------------------------------------- #

        pattern_screen = Screen(name='pattern')

        pattern_toolbar = MDToolbar(title="Шаблон", pos_hint={'top': 1}, md_bg_color=rgba(193, 0, 255, 1))
        pattern_toolbar.left_action_items = [["arrow-left", self.change_sc_to_main]]
        pattern_toolbar.right_action_items = [["check", self.save_pattern]]

        pattern_screen.add_widget(pattern_toolbar)

        scroll_view = ScrollView(do_scroll_x=True, do_scroll_y=True)

        main_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, adaptive_width=True,
                                  padding=20, pos_hint={'center_x': 0.5, 'center_y': 0.5}
                                  )

        self.column_box = MDStackLayout(orientation='rl-tb', size_hint_x=None, width=85, adaptive_height=True)

        self.column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                          md_bg_color=rgba(193, 0, 255, 1))
        self.column_pattern.add_widget(MDLabel(text='Упражнения', theme_text_color='Custom',
                                               text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                               bold=True
                                               ))

        self.column_box.add_widget(self.column_pattern)

        # self.column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85), md_bg_color=rgba(193, 0, 255, 1))
        # self.column_pattern.add_widget(MDLabel(text='', theme_text_color='Custom',
        #                                        text_color=(1, 1, 1, 1), halign='center', font_style='Caption', bold=True
        #                                        ))
        #
        # self.column_box.add_widget(self.column_pattern)

        self.row_box = MDStackLayout(orientation='bt-lr', size_hint_y=None, height=85, adaptive_width=True,
                                     pos_hint={'top': 1})

        self.row_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85), md_bg_color=rgba(193, 0, 255, 1))
        self.row_pattern.clear_widgets()
        self.row_pattern.add_widget(MDLabel(text=f'Подход №{pattern_list[1]}', theme_text_color='Custom',
                                            text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                            bold=True))

        self.row_box.add_widget(self.row_pattern)

        self.res_box = MDGridLayout(rows=1, row_force_default=True, row_default_height=85,
                                    col_force_default=True, col_default_width=85, size_hint=(None, None),
                                    adaptive_size=True
                                    )

        # self.res_box.add_widget(MDBoxLayout(md_bg_color=rgba(228, 228, 228, 1)))

        rows_and_res = MDBoxLayout(orientation='vertical', size_hint=(None, None), adaptive_size=True)

        rows_and_res.add_widget(self.row_box)
        rows_and_res.add_widget(self.res_box)

        main_layout.add_widget(self.column_box)
        main_layout.add_widget(rows_and_res)

        scroll_view.add_widget(main_layout)

        mini_win = MDBoxLayout(size_hint=(0.9, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                               md_bg_color=rgba(233, 233, 233, 1))
        mini_win.add_widget(scroll_view)

        pattern_screen.add_widget(mini_win)

        # screen.add_widget(scroll_view)

        btns_box = MDBoxLayout(pos_hint={'center_x': 0.5, 'y': 0.03}, height=50, size_hint_y=None,
                               adaptive_width=True, spacing=20)

        exercise_btn = MDFillRoundFlatButton(text='Добавить упражнение', pos_hint={'center_y': 0.5},
                                             md_bg_color=rgba(167, 0, 255, 1), on_release=self.add_exercise)

        amount_btn = MDFillRoundFlatButton(text='+1 Подход', pos_hint={'center_y': 0.5},
                                           md_bg_color=rgba(167, 0, 255, 1), on_release=self.add_amount)

        btns_box.add_widget(exercise_btn)
        btns_box.add_widget(amount_btn)

        pattern_screen.add_widget(btns_box)

        # ---------------------------------------------------------- #

        self.res_screen = Screen(name='res')

        res_toolbar = MDToolbar(title="Результат", pos_hint={'top': 1}, md_bg_color=rgba(193, 0, 255, 1))
        res_toolbar.left_action_items = [["arrow-left", self.change_sc_to_main]]
        res_toolbar.right_action_items = [["check", self.save_res]]

        res_scroll_view = ScrollView(do_scroll_x=True, do_scroll_y=True)

        res_main_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, adaptive_width=True,
                                      padding=20, pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.res_column_box = MDStackLayout(orientation='rl-tb', size_hint_x=None, width=85, adaptive_height=True)

        self.res_column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                              md_bg_color=rgba(193, 0, 255, 1))
        self.res_column_pattern.add_widget(MDLabel(text='Упражнения', theme_text_color='Custom',
                                                   text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                                   bold=True
                                                   ))

        self.res_column_box.add_widget(self.res_column_pattern)

        self.res_row_box = MDStackLayout(orientation='bt-lr', size_hint_y=None, height=85, adaptive_width=True,
                                         pos_hint={'top': 1})
        if stored_data.exists('pattern'):
            for i in stored_data.get('pattern')['text'][0]:
                self.res_column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                                      md_bg_color=rgba(193, 0, 255, 1))
                self.res_column_pattern.add_widget(MDLabel(text=f'{i}', theme_text_color='Custom',
                                                           text_color=(1, 1, 1, 1), halign='center',
                                                           font_style='Caption', bold=True
                                                           ))

                self.res_column_box.add_widget(self.res_column_pattern)

            for i in range(stored_data.get('pattern')['text'][1]):
                self.res_row_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                                   md_bg_color=rgba(193, 0, 255, 1))
                self.res_row_pattern.clear_widgets()
                self.res_row_pattern.add_widget(MDLabel(text=f'Подход №{i + 1}', theme_text_color='Custom',
                                                        text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                                        bold=True))

                self.res_row_box.add_widget(self.res_row_pattern)

        self.res_res_box = MDGridLayout(rows=1, row_force_default=True, row_default_height=85,
                                        col_force_default=True, col_default_width=85, size_hint=(None, None),
                                        adaptive_size=True
                                        )

        self.res_res_box_event()

        res_rows_and_res = MDBoxLayout(orientation='vertical', size_hint=(None, None), adaptive_size=True)

        res_rows_and_res.add_widget(self.res_row_box)
        res_rows_and_res.add_widget(self.res_res_box)

        res_main_layout.add_widget(self.res_column_box)
        res_main_layout.add_widget(res_rows_and_res)

        res_scroll_view.add_widget(res_main_layout)

        res_mini_win = MDBoxLayout(size_hint=(0.9, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                   md_bg_color=rgba(233, 233, 233, 1))
        res_mini_win.add_widget(res_scroll_view)

        self.res_screen.add_widget(res_mini_win)
        self.res_screen.add_widget(res_toolbar)

        # ---------------------------------------------------------- #

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(pattern_screen)
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.res_screen)
        self.screen_manager.current = 'main'

    def save_res(self, obj):
        stored_data.store_load()
        isFull = False
        self.res_list = []
        self.res_error_dialog = MDDialog(title='Ошибка', text='Имеется пустой результат!',
                                         buttons=[MDFlatButton(text='Отмена', text_color=rgba(193, 0, 255, 1),
                                                               on_release=lambda
                                                                   x: self.res_error_dialog.dismiss()),
                                                  MDFillRoundFlatButton(text='Понятно',
                                                                        md_bg_color=rgba(193, 0, 255, 1),
                                                                        on_release=lambda
                                                                            x: self.res_error_dialog.dismiss()
                                                                        )]
                                         )
        for i in range(self.res_res_box.cols * self.res_res_box.rows):
            self.res_list.append(self.res_screen.ids[f'{i}'].text.strip())
        for i in range(self.res_res_box.cols * self.res_res_box.rows):
            if self.res_screen.ids[f'{i}'].text == '':
                isFull = False
                break
            elif self.res_screen.ids[f'{i}'].text != '':
                isFull = True

        if isFull:
            self.main_screen.remove_widget(self.create_res_box)
            if not amount_data.exists('amount'):
                amount_data.put('amount', num=1)
            elif amount_data.exists('amount'):
                amount_data.put('amount', num=amount_data.get('amount')['num'] + 1)


            self.main_list = [datetime.now().strftime("Дата: %d-%m-%Y, Время: %H:%M:%S"),
                                   str(amount_data.get('amount')['num']), [stored_data.get('pattern')['text'][0],
                                          stored_data.get('pattern')['text'][1],
                                          self.res_list]]


            main_data.store_load()
            amount_data.store_load()
            if not main_data.exists('list1'):
                main_data.put('list1', item=self.main_list)
            elif main_data.exists('list1'):
                main_data.put(f"list{amount_data.get('amount')['num']}", item=self.main_list)



            #########################################

            try:
                self.main_screen.remove_widget(self.main_res_box)
            except:
                pass

            self.main_res_box = MDBoxLayout(size_hint_y=0.76, pos_hint={'y': 0.105})

            self.main_res_box_scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)

            self.main_res_box_adaptive = (MDBoxLayout(size_hint_y=None, adaptive_height=True,
                                                      pos_hint={'top': 1}, orientation='vertical'
                                                      ))

            for i in range(amount_data.get('amount')['num']):
                self.main_res_box_adaptive_cont = MDBoxLayout(size_hint_y=None, height=400, padding=30,
                                                              orientation='vertical',
                                                              spacing=30,
                                                              md_bg_color=rgba(228, 229, 228, 1))

                self.main_res_box_adaptive_title = MDLabel(text=f"Тренировка №{i + 1}",
                                                           font_style='H5', bold=True, halign='center',
                                                           size_hint_y=0.05
                                                           )
                self.main_res_box_adaptive_date = MDLabel(text=f'{main_data.get(f"list{i + 1}")["item"][0]}',
                                                          font_style='Caption', bold=True,
                                                          theme_text_color='Secondary', halign='center',
                                                          size_hint_y=0.05)

                main_results_scroll_view = ScrollView(do_scroll_x=True, do_scroll_y=True)

                main_results_main_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True,
                                                       adaptive_width=True,
                                                       padding=20, pos_hint={'center_x': 0.5, 'center_y': 0.5}
                                                       )

                self.main_results_column_box = MDStackLayout(orientation='rl-tb', size_hint_x=None, width=85,
                                                             adaptive_height=True)

                self.main_results_column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                                               md_bg_color=rgba(193, 0, 255, 1))
                self.main_results_column_pattern.add_widget(MDLabel(text='Упражнения', theme_text_color='Custom',
                                                                    text_color=(1, 1, 1, 1), halign='center',
                                                                    font_style='Caption',
                                                                    bold=True
                                                                    ))

                self.main_results_column_box.add_widget(self.main_results_column_pattern)

                for j in main_data.get(f"list{i + 1}")["item"][2][0]:
                    self.main_results_column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                                                   md_bg_color=rgba(193, 0, 255, 1))
                    self.main_results_column_pattern.add_widget(MDLabel(text=f'{j}', theme_text_color='Custom',
                                                                        text_color=(1, 1, 1, 1), halign='center',
                                                                        font_style='Caption', bold=True
                                                                        ))

                    self.main_results_column_box.add_widget(self.main_results_column_pattern)

                self.main_results_row_box = MDStackLayout(orientation='bt-lr', size_hint_y=None, height=85,
                                                          adaptive_width=True,
                                                          pos_hint={'top': 1})
                for j in range(main_data.get(f"list{i + 1}")["item"][2][1]):
                    self.main_results_row_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                                                md_bg_color=rgba(193, 0, 255, 1))
                    self.main_results_row_pattern.clear_widgets()
                    self.main_results_row_pattern.add_widget(MDLabel(text=f'Подход №{j + 1}', theme_text_color='Custom',
                                                                     text_color=(1, 1, 1, 1), halign='center',
                                                                     font_style='Caption',
                                                                     bold=True))

                    self.main_results_row_box.add_widget(self.main_results_row_pattern)

                self.main_results_res_box = MDGridLayout(rows=len(main_data.get(f'list{i + 1}')['item'][2][0]),
                                                         cols=main_data.get(f'list{i + 1}')['item'][2][1],
                                                         row_force_default=True, row_default_height=85,
                                                         col_force_default=True, col_default_width=85,
                                                         size_hint=(None, None),
                                                         adaptive_size=True
                                                         )

                for j in main_data.get(f'list{i + 1}')['item'][2][2]:
                    self.main_results_res_pattern = MDBoxLayout(md_bg_color=rgba(193, 0, 255, 1), padding=3)
                    self.main_results_res_pattern.clear_widgets()
                    self.main_results_res_pattern_box = MDBoxLayout(md_bg_color=(1, 1, 1, 1))
                    self.main_results_res_pattern.add_widget(self.main_results_res_pattern_box)
                    self.main_results_res_pattern_box.add_widget(
                        MDLabel(text=f'{j}', font_style='Caption', halign='center'))
                    self.main_results_res_box.add_widget(self.main_results_res_pattern)

                # self.res_box.add_widget(MDBoxLayout(md_bg_color=rgba(228, 228, 228, 1)))

                main_results_rows_and_res = MDBoxLayout(orientation='vertical', size_hint=(None, None),
                                                        adaptive_size=True)

                main_results_rows_and_res.add_widget(self.main_results_row_box)
                main_results_rows_and_res.add_widget(self.main_results_res_box)

                main_results_main_layout.add_widget(self.main_results_column_box)
                main_results_main_layout.add_widget(main_results_rows_and_res)

                main_results_scroll_view.add_widget(main_results_main_layout)

                main_results_mini_win = MDBoxLayout(size_hint=(1, 1), md_bg_color=rgba(245, 245, 245, 1))
                main_results_mini_win.add_widget(main_results_scroll_view)

                self.main_res_box_adaptive_cont.add_widget(self.main_res_box_adaptive_title)
                self.main_res_box_adaptive_cont.add_widget(self.main_res_box_adaptive_date)
                self.main_res_box_adaptive_cont.add_widget(main_results_mini_win)

                self.main_res_box_adaptive.add_widget(self.main_res_box_adaptive_cont)

            self.main_res_box_scroll.add_widget(self.main_res_box_adaptive)

            self.main_res_box.add_widget(self.main_res_box_scroll)

            self.main_screen.add_widget(self.main_res_box)



            #########################################

            for i in range(self.res_res_box.cols * self.res_res_box.rows):
                self.res_screen.ids[f'{i}'].text = ''
            self.change_sc_to_main(None)

        else:
            self.res_error_dialog.open()

    def res_box_event(self):
        self.res_box.rows = len(pattern_list[0])
        self.res_box.cols = pattern_list[1]
        self.res_box.clear_widgets()
        for i in range(len(pattern_list[0]) * pattern_list[1]):
            self.res_pattern = MDBoxLayout(md_bg_color=rgba(193, 0, 255, 1), padding=3)
            self.res_pattern.add_widget(MDBoxLayout(md_bg_color=(1, 1, 1, 1)))
            self.res_box.add_widget(self.res_pattern)

    def res_res_box_event(self):
        if stored_data.exists('pattern'):
            self.res_res_box.clear_widgets()
            self.res_res_box.rows = len(stored_data.get('pattern')['text'][0])
            self.res_res_box.cols = stored_data.get('pattern')['text'][1]
            for i in range(len(stored_data.get('pattern')['text'][0]) * stored_data.get('pattern')['text'][1]):
                self.res_res_pattern = MDBoxLayout(md_bg_color=rgba(193, 0, 255, 1), padding=3)
                self.res_res_pattern_input = TextInput(multiline=False, hint_text='Результат', halign='center',
                                                       padding=[0, 25])
                self.res_screen.ids[f'{i}'] = self.res_res_pattern_input
                self.res_res_pattern.add_widget(self.res_res_pattern_input)

                self.res_res_box.add_widget(self.res_res_pattern)

    def add_exercise(self, obj):
        self.exercise_dialog_content = MDBoxLayout(size_hint_y=None, height=50, padding=15)
        self.exercise_dialog_content_input = MDTextField(hint_text='Название упражнения',
                                                         color_mode='primary',
                                                         required=True,
                                                         helper_text='Пустое поле!', helper_text_mode='on_error'
                                                         )
        self.exercise_dialog_content.add_widget(self.exercise_dialog_content_input)

        self.exercise_dialog = MDDialog(title='Добавить упражнение', type='custom',
                                        content_cls=self.exercise_dialog_content,
                                        buttons=[MDFlatButton(text='Отмена', text_color=rgba(193, 0, 255, 1),
                                                              on_release=lambda
                                                                  x: self.exercise_dialog.dismiss()),
                                                 MDFillRoundFlatButton(text='Готово',
                                                                       md_bg_color=rgba(193, 0, 255, 1),
                                                                       on_release=self.add_exercise_event
                                                                       )])
        self.exercise_dialog.open()

    def add_exercise_event(self, obj):
        if self.exercise_dialog_content_input.text != '':
            self.column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                              md_bg_color=rgba(193, 0, 255, 1))
            self.column_pattern.add_widget(
                MDLabel(text=self.exercise_dialog_content_input.text, theme_text_color='Custom',
                        text_color=(1, 1, 1, 1), halign='center', font_style='Caption', bold=True
                        ))

            pattern_list[0].append(self.exercise_dialog_content_input.text)

            self.column_box.add_widget(self.column_pattern)
            self.res_box_event()
            self.exercise_dialog.dismiss()



    def add_amount(self, obj):
        pattern_list[1] += 1
        self.row_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85), md_bg_color=rgba(193, 0, 255, 1))
        self.row_pattern.clear_widgets()
        self.row_pattern.add_widget(MDLabel(text=f'Подход №{pattern_list[1]}', theme_text_color='Custom',
                                            text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                            bold=True))

        self.row_box.add_widget(self.row_pattern)

        self.res_box_event()



    def menu_callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def change_sc_to_pattern(self, obj):

        self.screen_manager.current = 'pattern'
        self.screen_manager.transition.direction = 'left'

    def change_sc_to_main(self, obj):
        pattern_list[0] = []
        pattern_list[1] = 1

        self.column_box.clear_widgets()

        self.column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                          md_bg_color=rgba(193, 0, 255, 1))
        self.column_pattern.add_widget(MDLabel(text='Упражнения', theme_text_color='Custom',
                                               text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                               bold=True
                                               ))

        self.column_box.add_widget(self.column_pattern)

        self.row_box.clear_widgets()

        self.row_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85), md_bg_color=rgba(193, 0, 255, 1))
        self.row_pattern.add_widget(MDLabel(text=f'Подход №1', theme_text_color='Custom',
                                            text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                            bold=True))

        self.row_box.add_widget(self.row_pattern)

        self.res_box.clear_widgets()

        self.screen_manager.current = 'main'
        self.screen_manager.transition.direction = 'right'

    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        self.theme_cls.primary_hue = '300'
        self.theme_cls.theme_style = 'Light'

        return self.screen_manager

    def save_pattern(self, obj):
        if len(pattern_list[0]) == 0:
            self.pattern_error = MDDialog(title='Ошибка!', text='Пустой шаблон.',
                                          buttons=[MDFlatButton(text='Отмена', text_color=rgba(193, 0, 255, 1),
                                                                on_release=lambda x: self.pattern_error.dismiss()),
                                                   MDFillRoundFlatButton(text='Понятно',
                                                                         md_bg_color=rgba(193, 0, 255, 1),
                                                                         on_release=lambda
                                                                             x: self.pattern_error.dismiss()
                                                                         )])
            self.pattern_error.open()

        elif len(pattern_list[0]) > 0:

            stored_data.put('pattern', text=pattern_list)

            self.res_column_box.clear_widgets()
            self.res_column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                                  md_bg_color=rgba(193, 0, 255, 1))
            self.res_column_pattern.add_widget(MDLabel(text='Упражнения', theme_text_color='Custom',
                                                       text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                                       bold=True
                                                       ))

            self.res_column_box.add_widget(self.res_column_pattern)

            self.res_row_box.clear_widgets()
            for i in stored_data.get('pattern')['text'][0]:
                self.res_column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                                      md_bg_color=rgba(193, 0, 255, 1))
                self.res_column_pattern.add_widget(MDLabel(text=f'{i}', theme_text_color='Custom',
                                                           text_color=(1, 1, 1, 1), halign='center',
                                                           font_style='Caption',
                                                           bold=True
                                                           ))

                self.res_column_box.add_widget(self.res_column_pattern)

            for i in range(stored_data.get('pattern')['text'][1]):
                self.res_row_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                                   md_bg_color=rgba(193, 0, 255, 1))
                self.res_row_pattern.clear_widgets()
                self.res_row_pattern.add_widget(MDLabel(text=f'Подход №{i + 1}', theme_text_color='Custom',
                                                        text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                                        bold=True))

                self.res_row_box.add_widget(self.res_row_pattern)

            self.res_res_box_event()

            self.change_sc_to_main(None)
            try:
                self.main_screen.remove_widget(self.create_pattern_box)
            except:
                pass
            try:
                amount_data.store_load()
                if not amount_data.exists('amount'):
                    self.create_res_box.clear_widgets()
                    self.create_res_box.add_widget(
                        MDLabel(text='Шаблон готов, добавьте свои первые результаты!', theme_text_color='Secondary',
                                width=300, size_hint_x=None, pos_hint={'center_x': 0.5}, halign='center'))
                    self.main_screen.add_widget(self.create_res_box)
                    self.main_screen_btn_box = MDBoxLayout(size_hint=(None, None), adaptive_size=True,
                                                           pos_hint={'right': 1},
                                                           padding=10)

                    self.main_screen_btn_box.add_widget(
                        MDFillRoundFlatIconButton(text='Новый результат', font_style='Button',
                                                  md_bg_color=rgba(193, 0, 255, 1), icon='plus',
                                                  on_release=self.change_sc_to_res))
                    self.main_screen.add_widget(self.main_screen_btn_box)

            except:
                pass

    def new_pattern(self):
        self.menu.dismiss()
        self.change_sc_to_main(None)
        self.change_sc_to_pattern(None)

    def on_start(self):
        stored_data.store_load()
        amount_data.store_load()
        if not stored_data.exists('pattern'):
            create_pattern_box_text = MDLabel(
                text='Для начала создайте шаблон, по которому в дальнейшем будут вноситься результаты.',
                width=300, size_hint_x=None, pos_hint={'center_x': 0.5}, halign='center')

            create_pattern_box_btn = MDRaisedButton(text='СОЗДАТЬ', md_bg_color=rgba(193, 0, 255, 1),
                                                    pos_hint={'center_x': 0.5},
                                                    font_style='Button',
                                                    on_release=self.change_sc_to_pattern
                                                    )

            self.create_pattern_box.add_widget(create_pattern_box_text)
            self.create_pattern_box.add_widget(create_pattern_box_btn)

            self.main_screen.add_widget(self.create_pattern_box)

        elif stored_data.exists('pattern'):
            try:
                self.create_res_box.add_widget(
                    MDLabel(text='Шаблон готов, добавьте свои первые результаты!', theme_text_color='Secondary',
                            width=300, size_hint_x=None, pos_hint={'center_x': 0.5}, halign='center'))
                self.main_screen.add_widget(self.create_res_box)
                self.main_screen_btn_box = MDBoxLayout(size_hint=(None, None), adaptive_size=True,
                                                       pos_hint={'right': 1},
                                                       padding=10)

                self.main_screen_btn_box.add_widget(
                    MDFillRoundFlatIconButton(text='Новый результат', font_style='Button',
                                              md_bg_color=rgba(193, 0, 255, 1), icon='plus',
                                              on_release=self.change_sc_to_res))
                self.main_screen.add_widget(self.main_screen_btn_box)
            except:
                pass

        if amount_data.exists('amount'):
            self.main_screen.remove_widget(self.create_res_box)

            self.main_res_box = MDBoxLayout(size_hint_y=0.76, pos_hint={'y': 0.105})

            self.main_res_box_scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)

            self.main_res_box_adaptive = (MDBoxLayout(size_hint_y=None, adaptive_height=True,
                                                      pos_hint={'top': 1}, orientation='vertical'
                                                      ))



            for i in range(amount_data.get('amount')['num']):
                self.main_res_box_adaptive_cont = MDBoxLayout(size_hint_y=None, height=400, padding=30, orientation='vertical',
                                                              spacing=30,
                                                              md_bg_color=rgba(228, 229, 228, 1))

                self.main_res_box_adaptive_title = MDLabel(text=f"Тренировка №{i + 1}",
                                                           font_style='H5', bold=True, halign='center',
                                                           size_hint_y=0.05
                                                           )
                self.main_res_box_adaptive_date = MDLabel(text=f'{main_data.get(f"list{i + 1}")["item"][0]}',
                                                          font_style='Caption', bold=True,
                                                          theme_text_color='Secondary', halign='center', size_hint_y=0.05)



                main_results_scroll_view = ScrollView(do_scroll_x=True, do_scroll_y=True)

                main_results_main_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, adaptive_width=True,
                                          padding=20, pos_hint={'center_x': 0.5, 'center_y': 0.5}
                                          )

                self.main_results_column_box = MDStackLayout(orientation='rl-tb', size_hint_x=None, width=85, adaptive_height=True)

                self.main_results_column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85),
                                                  md_bg_color=rgba(193, 0, 255, 1))
                self.main_results_column_pattern.add_widget(MDLabel(text='Упражнения', theme_text_color='Custom',
                                                       text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                                       bold=True
                                                       ))

                self.main_results_column_box.add_widget(self.main_results_column_pattern)


                for j in main_data.get(f"list{i + 1}")["item"][2][0]:
                    self.main_results_column_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85), md_bg_color=rgba(193, 0, 255, 1))
                    self.main_results_column_pattern.add_widget(MDLabel(text=f'{j}', theme_text_color='Custom',
                                                           text_color=(1, 1, 1, 1), halign='center', font_style='Caption', bold=True
                                                           ))

                    self.main_results_column_box.add_widget(self.main_results_column_pattern)



                self.main_results_row_box = MDStackLayout(orientation='bt-lr', size_hint_y=None, height=85, adaptive_width=True,
                                             pos_hint={'top': 1})
                for j in range(main_data.get(f"list{i + 1}")["item"][2][1]):
                    self.main_results_row_pattern = MDBoxLayout(size_hint=(None, None), size=(85, 85), md_bg_color=rgba(193, 0, 255, 1))
                    self.main_results_row_pattern.clear_widgets()
                    self.main_results_row_pattern.add_widget(MDLabel(text=f'Подход №{j + 1}', theme_text_color='Custom',
                                                        text_color=(1, 1, 1, 1), halign='center', font_style='Caption',
                                                        bold=True))

                    self.main_results_row_box.add_widget(self.main_results_row_pattern)

                self.main_results_res_box = MDGridLayout(rows=len(main_data.get(f'list{i + 1}')['item'][2][0]),
                                                         cols=main_data.get(f'list{i + 1}')['item'][2][1],
                                                         row_force_default=True, row_default_height=85,
                                                         col_force_default=True, col_default_width=85, size_hint=(None, None),
                                                         adaptive_size=True
                                                         )

                for j in main_data.get(f'list{i + 1}')['item'][2][2]:
                    self.main_results_res_pattern = MDBoxLayout(md_bg_color=rgba(193, 0, 255, 1), padding=3)
                    self.main_results_res_pattern.clear_widgets()
                    self.main_results_res_pattern_box = MDBoxLayout(md_bg_color=(1, 1, 1, 1))
                    self.main_results_res_pattern.add_widget(self.main_results_res_pattern_box)
                    self.main_results_res_pattern_box.add_widget(MDLabel(text=f'{j}', font_style='Caption', halign='center'))
                    self.main_results_res_box.add_widget(self.main_results_res_pattern)




                # self.res_box.add_widget(MDBoxLayout(md_bg_color=rgba(228, 228, 228, 1)))

                main_results_rows_and_res = MDBoxLayout(orientation='vertical', size_hint=(None, None), adaptive_size=True)

                main_results_rows_and_res.add_widget(self.main_results_row_box)
                main_results_rows_and_res.add_widget(self.main_results_res_box)

                main_results_main_layout.add_widget(self.main_results_column_box)
                main_results_main_layout.add_widget(main_results_rows_and_res)

                main_results_scroll_view.add_widget(main_results_main_layout)

                main_results_mini_win = MDBoxLayout(size_hint=(1, 1), md_bg_color=rgba(245, 245, 245, 1))
                main_results_mini_win.add_widget(main_results_scroll_view)




                self.main_res_box_adaptive_cont.add_widget(self.main_res_box_adaptive_title)
                self.main_res_box_adaptive_cont.add_widget(self.main_res_box_adaptive_date)
                self.main_res_box_adaptive_cont.add_widget(main_results_mini_win)


                self.main_res_box_adaptive.add_widget(self.main_res_box_adaptive_cont)

            



            self.main_res_box_scroll.add_widget(self.main_res_box_adaptive)

            self.main_res_box.add_widget(self.main_res_box_scroll)

            self.main_screen.add_widget(self.main_res_box)

    def change_sc_to_res(self, obj):

        self.screen_manager.current = 'res'
        self.screen_manager.transition.direction = 'left'


if __name__ == '__main__':
    JournalApp().run()
