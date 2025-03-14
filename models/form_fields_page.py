from playwright.sync_api import Page


class FormFieldsPage:

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://practice-automation.com/form-fields/")
        self.name_locator = self.page.get_by_role("textbox", name="Name")
        self.password_locator = self.page.get_by_role("textbox", name="Password")
        self.drinks = lambda drink: self.page.locator(f'input[type="checkbox"][value="{drink}"]')
        self.drinks_section_locator = self.page.get_by_text("What is your favorite drink?")
        self.colors = lambda color: self.page.locator(f'input[type="radio"][value="{color}"]')
        self.email_locator = self.page.get_by_role("textbox", name="Email")
        self.dropdown_locator = self.page.locator("//select[@id='automation']")
        self.message_locator = self.page.get_by_role("textbox", name="Message")
        self.automation_tools = "(//ul)[2]"
        self.submit_btn = self.page.get_by_role("button", name="Submit")
        self.confirm_dialog = self.page.get_by_text("Message received!")

    def name_input(self, name):
        self.name_locator.fill(name)

    def password_input(self, password):
        self.password_locator.type(password)

    def select_drinks(self, selected_drinks: list):
        """Select drinks after ensuring they are visible."""
        # First, ensure the section is scrolled into view
        self.drinks_section_locator.scroll_into_view_if_needed()

        for drink in selected_drinks:
            checkbox = self.drinks(drink)  # Get the checkbox locator dynamically
            checkbox.wait_for(state="visible")  # Ensure it's visible
            if not checkbox.is_checked():  # Avoid unnecessary clicks
                checkbox.click()  # Select the drink

    def get_selected_drinks(self):
        """Return a list of selected drinks."""
        selected_drinks = []
        # The list of available drink options
        drinks_list = ["Water", "Milk", "Coffee", "Wine", "Ctrl-Alt-Delight"]

        for drink in drinks_list:
            checkbox = self.drinks(drink)  # Get the locator for the drink
            if checkbox.is_checked():
                selected_drinks.append(drink)
        return selected_drinks

    def color_selection(self, color: str):
        """Select the radio button based on the color."""
        self.page.locator(f'input[type="radio"][value="{color}"]').scroll_into_view_if_needed()
        selected_color = self.colors(color)
        selected_color.click()

    def get_selected_color_locator(self):
        """Return the locator for the selected radio button."""
        return self.page.locator('input[type="radio"]:checked')

    def dropdown_menu(self, option: str):

        self.dropdown_locator.scroll_into_view_if_needed()
        """Select an option from the dropdown menu (case-insensitive)."""
        option_lower = option.lower()  # Convert input to lowercase

        # Get all available options from the dropdown
        available_options = self.dropdown_locator.locator("option").all_inner_texts()

        # Find the matching option (case-insensitive)
        matched_option = next((opt for opt in available_options if opt.lower() == option_lower), None)

        if matched_option:
            self.dropdown_locator.select_option(matched_option)  # Select the matched option
        else:
            raise ValueError(f"Option '{option}' not found in dropdown. Available: {available_options}")

    def email_input(self, email):
        self.email_locator.scroll_into_view_if_needed()
        self.email_locator.fill(email)

    def tools_count(self):
        """Count elements in Automation tools and find the longest one."""
        # Get the list of tools
        autom_tools_locator = self.page.locator(self.automation_tools)
        tools = autom_tools_locator.locator("li")
        count = tools.count()

        max_length = 0
        max_tool_text = ""

        # Iterate over tools and find the one with the longest text
        for i in range(count):
            tool_text = tools.nth(i).inner_text().strip()  # Get text of the tool
            tool_length = len(tool_text.replace(" ", ""))  # Ignore spaces in length calculation

            if tool_length > max_length:
                max_length = tool_length
                max_tool_text = tool_text  # Keep the longest tool's text with spaces

        return count, max_tool_text, max_length

    def generate_message(self):
        """Generates a formatted message using the automation tool details."""
        count, longest_text, longest_length = self.tools_count()  # Get values from tools_count

        # Generate the formatted message
        message = (f"✅ Number of automation tools: {count}\n"
                   f"📌 The longest tool: {longest_text}: has {longest_length} symbols.")
        return message

    def message_input(self, message):
        self.email_locator.scroll_into_view_if_needed()
        """Fill the message input field with text."""
        self.message_locator.wait_for(state="visible")  # Wait for the field to be visible
        self.message_locator.fill(message)
        self.page.screenshot(path="formatted_message.png")  # Fill the message in the input field

    def submit_form(self):
        """Take a screenshot of the form and Submit the form."""
        self.page.screenshot(path="submitted.png", full_page=True)
        self.submit_btn.click()

    def accept_confirm_dialog(self):
        """ This function is optional which handles the pop-up window 'Message received!'. """
        """Accept the confirm dialog."""

        # Wait for the confirm dialog to appear
        self.page.on('dialog', lambda dialog: (
            print(f"Dialog opened with message: {dialog.message()}"),
            dialog.accept()
        ))
        # Accept the dialog when it appears
        self.confirm_dialog.click()
