from behave import step
from playwright.sync_api import sync_playwright, expect, TimeoutError
from datetime import datetime
import sys
import time
from pathlib import Path

from utils.page_manager import PageManager
from utils.config_manager import ConfigManager
from utils.steps import perform_transaction, check_home_page_loaded

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


PAGES_MANAGER = PageManager()
CONFIG = ConfigManager().config

@step('I open Chrome browser')
def step_open_chrome(context):
    """
    Opens Chrome browser using Playwright with configuration from YAML
    param context: Behave context
    """
    context.playwright = sync_playwright().start()

    browser_cfg = CONFIG.get('browser', {})

    browser_name = browser_cfg.get('name', 'chromium')
    headless = browser_cfg.get('headless', False)
    slowmo = browser_cfg.get('slowmo', 0)
    devtools = browser_cfg.get('devtools', False)

    if browser_name == 'chrome':
        context.browser = context.playwright.chromium.launch(
            headless=headless,
            channel="chrome",
            slow_mo=slowmo,
            devtools=devtools
        )
    elif browser_name == 'chromium':
        context.browser = context.playwright.chromium.launch(
            headless=headless,
            slow_mo=slowmo,
            devtools=devtools
        )
    elif browser_name == 'firefox':
        context.browser = context.playwright.firefox.launch(
            headless=headless,
            slow_mo=slowmo
        )
    elif browser_name == 'webkit':
        context.browser = context.playwright.webkit.launch(
            headless=headless,
            slow_mo=slowmo
        )
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    context.page = context.browser.new_page()
    context.page.wait_for_load_state("networkidle")

@step('I navigate to XYZ Bank land page')
def step_navigate_google(context):
    """
    Navigates to Google homepage
    param context: Behave context
    """
    google_url = CONFIG.get('urls').get('bank_homepage')
    context.page.goto(google_url, timeout=50000)

    check_home_page_loaded(context)


@step('I login as "{name}" name')
def step_navigate_google(context, name):
    """
    Navigates to Google homepage
    param context: Behave context
    param name: Name of the user
    """
    customer_login_button_locator = PAGES_MANAGER.get_combined_locator('home', 'home_page', 'customer_login')
    customer_login_button = context.page.locator(customer_login_button_locator)
    customer_login_button.click()

    dropdown_selector = PAGES_MANAGER.get_combined_locator('customer_login', 'customer_login_page', 'your_name_selector')
    context.page.locator(dropdown_selector).select_option(name)

    login_button = PAGES_MANAGER.get_combined_locator('customer_login', 'customer_login_page', 'login_button')
    context.page.locator(login_button).click()


@step('I perform logout')
def step_perform_logout(context):
    """
    Performs logout action
    param context: Behave context
    """
    logout_button_locator = PAGES_MANAGER.get_combined_locator('customer_login', 'customer_login_page', 'logout')
    context.page.locator(logout_button_locator).click()


@step('I see the XYZ Bank home page')
def step_verify_home_page(context):
    """
    Verifies that the XYZ Bank home page is loaded
    param context: Behave context
    """
    check_home_page_loaded(context)


@step('I navigate to the transactions page')
def step_navigate_to_transactions(context):
    """
    Navigates to the transactions page
    param context: Behave context
    """
    time.sleep(2) #Explicit wait for the transaction is recorded
    transactions_locator = PAGES_MANAGER.get_combined_locator('customer_login', 'customer_login_page', 'login_transactions')
    context.page.locator(transactions_locator).click()
    time.sleep(1)


@step('the customer main page is loaded')
def step_verify_search_field(context):
    """
    Verifies that customer main page is loaded
    param context: Behave context
    """
    transactions = PAGES_MANAGER.get_combined_locator('customer_login', 'customer_login_page', 'login_transactions')
    transactions_button = context.page.locator(transactions)
    transactions_button.wait_for(state="visible", timeout=5000)
    assert transactions_button.is_enabled(), "Transactions button is not enabled on the page after login"

    deposit = PAGES_MANAGER.get_combined_locator('customer_login', 'customer_login_page', 'login_deposit')
    deposit_button = context.page.locator(deposit)
    deposit_button.wait_for(state="visible", timeout=5000)
    assert deposit_button.is_enabled(), "Deposit button is not enabled on the page after login"

    withdrawl = PAGES_MANAGER.get_combined_locator('customer_login', 'customer_login_page', 'login_withdrawl')
    withdrawl_button = context.page.locator(withdrawl)
    withdrawl_button.wait_for(state="visible", timeout=5000)
    assert withdrawl_button.is_enabled(), "Withdrawal button is not enabled on the page after login"


@step('I deposit "{amount}" Dollars')
def step_deposit_galleons(context, amount):
    """
    Deposits specified Dollars
    param context: Behave context
    param amount: Amount to deposit
    """
    perform_transaction(context, amount, 'deposit')


@step('I withdrawl "{amount}" Dollars')
def step_withdrawl_dollars(context, amount):
    """
    Withdraws specified Dollars
    param context: Behave context
    param amount: Amount to withdraw
    """
    perform_transaction(context, amount, 'withdrawl')


@step('I see the balance updated with "{amount}" Dollars')
def step_verify_balance_updated(context, amount):
    """
    Verifies that the balance is updated with the specified Dollars
    param context: Behave context
    param amount: Expected balance amount
    """
    balance_locator = PAGES_MANAGER.get_combined_locator('customer_login', 'customer_login_page', 'money_ballance')
    balance_element = context.page.locator(balance_locator).first
    assert balance_element.inner_text() == amount, f"Expected balance to be {amount} Dollars, but got {balance_element.inner_text()}"


@step('I see a transaction recorded with "{amount}" Dollars amount')
def step_verify_transaction_recorded(context, amount):
    """
    Verifies that a transaction is recorded with the specified Dollars amount
    param context: Behave context
    param amount: Amount to verify
    """
    transactions_table_locator = PAGES_MANAGER.get_combined_locator('transactions', 'transactions_page', 'transactions_table')
    transactions_table = context.page.locator(transactions_table_locator).all()
    today = datetime.now().strftime("%b %d, %Y")

    found_transaction = False
    for row in transactions_table:
        transaction_date = row.locator('td:nth-child(1)').text_content()
        transaction_amount = row.locator('td:nth-child(2)').text_content()

        if today in transaction_date and transaction_amount.strip() == amount:
            found_transaction = True
            break

    assert found_transaction, f"No transaction recorded with {amount} Dollars amount"
