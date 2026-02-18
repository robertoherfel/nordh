def before_scenario(context, scenario):
    """Setup before each scenario"""
    print(f"\ Running scenario: {scenario.name}")


def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    # Ensure browser is closed in case of error
    if hasattr(context, 'browser') and context.browser:
        try:
            context.browser.close()
        except:
            pass

    if hasattr(context, 'playwright') and context.playwright:
        try:
            context.playwright.stop()
        except:
            pass

    if scenario.status == "failed":
        print(f"❌ Scenario failed: {scenario.name}")
    else:
        print(f"✅ Scenario succeeded: {scenario.name}")


def after_all(context):
    """Final message after all tests are done"""
    print("\n Tests completed!")
