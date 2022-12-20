from UiBank.uibank import UiBank

with UiBank(teardown=True) as bot:
    bot.landing_page_and_login()
    # bot.apply_for_new_account()
    # bot.apply_for_loan()
    # bot.already_have_loan()
    # bot.transfer_funds()
    # bot.automate_dispute_center_random_account()
