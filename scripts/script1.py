from Task1.UiBank.uibank import UiBank

with UiBank(teardown=True) as bot:
    bot.landing_page_and_login()
    bot.apply_for_loan()
    bot.already_have_loan()
