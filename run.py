from UiBank.uibank import UiBank
import os
import runpy
import time

# with UiBank(teardown=True) as bot:
#     bot.landing_page_and_login()
#     # bot.apply_for_new_account(account_type='checking')
#     # bot.apply_for_new_account(account_type='savings')
#     # bot.navigate_to(where_to='Profile')
#     # bot.select_product("Mobile Banking")
#     # bot.get_help()
#     # bot.apply_for_loan()
#     # bot.apply_for_loan()
#     # bot.already_have_loan()
#     # bot.get_loans()
#     # bot.transfer_funds()
#     # bot.get_accounts()
#     # bot.download_transactions()
#     # bot.select_account_by_name("Vlad's Account")
#     # bot.download_all_transactions()
#     # bot.automate_dispute_center_random_account()
#     # bot.automate_dispute_center_by_account_name("Vlad's Account")
#     bot.download_transactions_random_account()
#
#     time.sleep(2)


dir_path = os.getcwd() + '/scripts'
nr_of_scripts = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])

for i in range(1, nr_of_scripts + 1):
    print(f'Running script{i}...')
    runpy.run_path(path_name=dir_path + f'/script{i}.py')
    time.sleep(3)





