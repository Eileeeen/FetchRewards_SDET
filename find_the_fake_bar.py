import game_methods


def fill_the_balance_scale(driver, left_bars, right_bars):
    game_methods.fill_bowl(
        driver, game_methods.LEFT_BOWL, left_bars)

    game_methods.fill_bowl(
        driver, game_methods.RIGHT_BOWL, right_bars)

    game_methods.click_weigh_button(driver)

    return game_methods.get_compare_results(driver)


def find_the_fake_bar():
    driver = game_methods.open_game_page()

    fake_bar_number = -1
    compare_results = fill_the_balance_scale(driver,
                                             [(0, 0), (1, 1), (2, 2)], [(0, 3), (1, 4), (2, 5)])
    if compare_results == "<":  # the fake is in 0, 1, 2
        game_methods.click_reset_button(driver)
        compare_results = fill_the_balance_scale(driver, [(0, 0)], [(0, 1)])
        if compare_results == "<":
            fake_bar_number = 0
        elif compare_results == ">":
            fake_bar_number = 1
        else:
            fake_bar_number = 2
    elif compare_results == ">":  # the fake is in 3, 4, 5
        game_methods.click_reset_button(driver)
        compare_results = fill_the_balance_scale(driver, [(0, 3)], [(0, 4)])
        if compare_results == "<":
            fake_bar_number = 3
        elif compare_results == ">":
            fake_bar_number = 4
        else:
            fake_bar_number = 5
    else:  # the fake is in 6, 7, 8
        game_methods.click_reset_button(driver)
        compare_results = fill_the_balance_scale(driver, [(0, 6)], [(0, 7)])
        if compare_results == "<":
            fake_bar_number = 6
        elif compare_results == ">":
            fake_bar_number = 7
        else:
            fake_bar_number = 8

    # Verify that the test has identified a fake bar
    assert fake_bar_number >= 0

    # Click the fake bar and verify the alert
    allert_message = game_methods.click_bottom_gold_bar(
        driver, fake_bar_number
    )

    assert game_methods.verify_alert_message(
        allert_message
    ), f"Alert was {allert_message} expected {game_methods.ALLERT_MESSAGE_RIGHT}"

    list_of_weighings = game_methods.get_weighings(driver)
    # number_of_weighings = int(list_of_weighings.count("[") / 2)
    number_of_weighings = len(list_of_weighings.split('\n'))

    # Print desired output
    print(f"Alert message: {allert_message}")
    print(f"Number of weighings: {number_of_weighings}")
    print(f"List of weighings:\n{list_of_weighings}")
