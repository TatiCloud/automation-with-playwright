import pytest
from models.form_fields_page import FormFieldsPage
from playwright.sync_api import sync_playwright, Page, expect


@pytest.fixture(scope="function")
def form_fields_page(page: Page):
    return FormFieldsPage(page)


def test_name_input(form_fields_page):
    name = "Test User"
    form_fields_page.name_input(name)
    expect(form_fields_page.name_locator).to_have_value(name)


def test_password_input(form_fields_page):
    password = "123456789"
    form_fields_page.password_input(password)
    expect(form_fields_page.password_locator).to_have_value(password)


def test_drink_selection(form_fields_page):
    # List of selected drinks
    selected_drinks = ["Milk", "Coffee"]
    # Available drinks: ["Water", "Milk", "Coffee", "Wine", "Ctrl-Alt-Delight"]

    # Select the drinks
    form_fields_page.select_drinks(selected_drinks)

    assert form_fields_page.get_selected_drinks() == selected_drinks, \
        f"Expected {selected_drinks}, but got {form_fields_page.get_selected_drinks()}"


def test_color_selection(form_fields_page):
    color = "Yellow"
    form_fields_page.color_selection(color)

    selected_color_locator = form_fields_page.get_selected_color_locator()

    # Validate that the selected color is the same as the one passed
    expect(selected_color_locator).to_have_value(color)


def test_dropdown_menu(form_fields_page):
    option = "YES"  # Uppercase input (should still work)

    form_fields_page.dropdown_menu(option)

    # Ensure the dropdown has the correct selected value (convert expected to lowercase)
    expect(form_fields_page.dropdown_locator).to_have_value(option.lower())


def test_email_input(form_fields_page):
    email = "name@example.com"
    form_fields_page.email_input(email)
    expect(form_fields_page.email_locator).to_have_value(email)


def test_message_input(form_fields_page):
    # Get the formatted message
    message = form_fields_page.generate_message()

    # Fill the message in the input field
    form_fields_page.message_input(message)

    # Verify that the input field contains the correct message
    expect(form_fields_page.message_locator).to_have_value(message)


def test_form_submission(form_fields_page):
    # Fill out all form fields
    form_fields_page.name_input("Test User")
    form_fields_page.password_input("123456789")
    form_fields_page.select_drinks(["Milk", "Coffee"])
    form_fields_page.color_selection("Yellow")
    form_fields_page.dropdown_menu("YES")
    form_fields_page.email_input("name@example.com")

    # Generate and input message
    message = form_fields_page.generate_message()
    form_fields_page.message_input(message)

    # Submit the form with all necessary information
    form_fields_page.submit_form()

    # Wait for confirmation dialog
    # form_fields_page.confirm_dialog.wait_for(state="visible", timeout=5000)

    # Verify success message appears
    # expect(form_fields_page.page.locator("text=Message received!")).to_be_visible()

    # Accept the confirmation dialog
    # form_fields_page.accept_confirm_dialog()
