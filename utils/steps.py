from utils.page_manager import PageManager
import time

PAGES_MANAGER = PageManager()

def perform_transaction(context, amount, action):
    """
    Performs a deposit or withdrawl transaction
    param context: Behave context
    param amount: Amount to be deposited or withdrawn
    param action: 'deposit' or 'withdrawl'
    """
    main_button_locator = PAGES_MANAGER.get_combined_locator(
        'customer_login',
        'customer_login_page',
        f'login_{action}'
    )
    context.page.locator(main_button_locator).first.click()

    time.sleep(2) # Explicit wait for the transaction being registered

    input_locator = PAGES_MANAGER.get_combined_locator(
        'customer_login',
        'customer_login_page',
        f'money_input'
    )
    context.page.get_by_placeholder(input_locator).fill(amount)

    action_button_locator = PAGES_MANAGER.get_combined_locator(
        'customer_login',
        'customer_login_page',
        f'{action}_action'
    )
    context.page.locator(action_button_locator).click()


def check_home_page_loaded(context):
    """
    Checks that the XYZ Bank home page is loaded
    param context: Behave context
    """
    home_logo_locator = PAGES_MANAGER.get_combined_locator('home', 'home_page', 'logo')
    home_logo = context.page.locator(home_logo_locator)
    home_logo.wait_for(state="visible", timeout=5000)
    assert home_logo.is_visible(), "Home logo is not found or not visible on the page"
