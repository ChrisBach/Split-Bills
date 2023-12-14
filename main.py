from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty



class StartWindow(Screen):
    num_people_input = ObjectProperty(None)

    def next_button(self):
        num_people = int(self.ids.num_people_input.text)
        input_window = self.manager.get_screen("input")
        input_window.create_entries(num_people)
        self.manager.current = "input"


class InputWindow(Screen):
    input_grid = ObjectProperty(None)
    text_inputs = {}

    def create_entries(self, num_people):
        input_grid = self.ids.input_grid  # Get a reference to the input_grid

        input_grid.clear_widgets()  # Clear previous entries

        # Dictionary to store references to TextInput widgets
        self.text_inputs = {}

        for i in range(num_people):
            label_name = f"name_input_{i + 1}"
            text_name = f"Ape {i + 1} name:"
            label_money = f"money_input_{i + 1}"
            text_money = f"Money Ape {i + 1} spent:"

            pos_hint_y = 0.2
            
            # Create and add Label for Name
            input_grid.add_widget(Label(text=text_name, size_hint_x=None, pos_hint={"x": 0.3, "y": pos_hint_y}, font_size=14))
            # Create and add TextInput for Name
            name_input = TextInput(multiline=False, pos_hint={"x": 0.4, "top": pos_hint_y})
            input_grid.add_widget(name_input)
            # Store the reference in the dictionary
            self.text_inputs[label_name] = name_input

            # Create and add Label for Money
            pos_hint_y = 0.35   # Adjust the vertical position
            input_grid.add_widget(Label(text=text_money, size_hint_x=None, pos_hint={"x": 0.3, "top": pos_hint_y}, font_size=14))
            # Create and add TextInput for Money
            money_input = TextInput(multiline=False, pos_hint={"x": 0.4, "top": pos_hint_y})
            input_grid.add_widget(money_input)
            # Store the reference in the dictionary
            self.text_inputs[label_money] = money_input

        # Add the Submit Button
        #pos_hint_y = 0.6
        #input_grid.add_widget(Button())

    def calculate_shares(self, button_instance):
        contributions = []

        for i in range(len(self.text_inputs) // 2):
            name_input = self.text_inputs[f"name_input_{i + 1}"]
            money_input = self.text_inputs[f"money_input_{i + 1}"]

            name = name_input.text
            money = float(money_input.text) if money_input.text else 0.0

            print(f"Name: {name}, Money Spent: {money}")
            contributions.append({"name": name, "money": money})

        total_contribution = sum(c["money"] for c in contributions)
        num_people = len(contributions)

        # Calculate the share for each person
        if num_people > 0:
            share_per_person = total_contribution / num_people

            # Create a popup to enter the assigned person
            popup_content = BoxLayout(orientation="vertical")
            input_text = TextInput(multiline=False, hint_text="Enter Ape name (Assigning ape to get money transfered to): ")
            assign_button = Button(text="Assign", on_press=lambda instance: self.process_assigned_person(contributions, share_per_person, input_text.text))
            
            popup_content.add_widget(input_text)
            popup_content.add_widget(assign_button)
            
            popup = Popup(title='Enter Assigned Person', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()

    def process_assigned_person(self, contributions, share_per_person, assigned_person_text):
        try:
            # Find the index of the assigned person based on their name
            ##assigned_person = next((i for i, contribution in enumerate(contributions) if contribution[0] == assigned_person_text), None)
            print(type(contributions))
            assigned_person = next((i for i, contribution in enumerate(contributions) if contribution.get("name") == assigned_person_text), None)

            if assigned_person is not None:
                # Calculate and print the amount others have to transfer to the assigned person and vice versa
                share_result = f"Eventually Each Share: {share_per_person:.2f}zl\n"
                assigned_person_result = f"{contributions[assigned_person]['name']} will receive money.\n"

                for i, contribution in enumerate(contributions):
                    if i != assigned_person:
                        amount_to_transfer = share_per_person - contribution['money']
                        if amount_to_transfer > 0:
                            share_result += f"{contribution['name']} has to transfer {amount_to_transfer:.2f}zl to {contributions[assigned_person]['name']}\n"
                        else:
                            share_result += f"{contributions[assigned_person]['name']} has to transfer {abs(amount_to_transfer):.2f}zl to {contribution['name']}\n"

                result_window = self.manager.get_screen("result")
                result_window.display_result(share_result + assigned_person_result)
                self.manager.current = "result"
            else:
                print("Invalid assigned person. Please enter a valid person name.")
        except StopIteration:
            print("Invalid assigned person. Please enter a valid person name.")


class ResultWindow(Screen):
    result_label = ObjectProperty(None)

    def display_result(self, result):
        self.result_label.text = result

    def on_enter(self):
        # Add an "OK" button to return to the StartWindow
        ok_button = Button(text="OK", size_hint=(None, None), size=(100, 50), pos_hint={"center_x": 0.5, "center_y": 0.2})
        ok_button.bind(on_press=self.return_to_start)
        self.add_widget(ok_button)

    def return_to_start(self, instance):
        self.manager.current = "start"

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [StartWindow(name="start"), InputWindow(name="input"),ResultWindow(name="result")]
for screen in screens:
    sm.add_widget(screen)

class MyApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyApp().run()